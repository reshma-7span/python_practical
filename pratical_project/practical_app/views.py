from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import User, Post, Like
from .serializers import UserSerializer, PostSerializer, LikeSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken


def get_tokens_for_user(user):
    refresh = ""
    try:
        user_data = User.objects.get(email=user).id
    except User.DoesNotExist:
        return Response({"status": False, "message": "User Doesn't Exist"}, status=status.HTTP_404_NOT_FOUND)

    refresh = OutstandingToken.objects.filter(user_id=user_data)
    if refresh != []:
        refresh.delete()

    refresh = RefreshToken.for_user(user)

    refresh_token = refresh
    access_token = refresh.access_token

    return {
        'refresh': str(refresh_token),
        'access': str(access_token),
    }


# Generate Manual Token Code End #

# Check Token Code Start #
def check_token(user):
    refresh = ""
    try:
        user_data = User.objects.get(email=user).id
    except User.DoesNotExist:
        return Response({"status": False, "message": "User Doesn't Exist."}, status=status.HTTP_404_NOT_FOUND)

    try:
        refresh = OutstandingToken.objects.get(user_id=user_data).id
    except OutstandingToken.DoesNotExist:
        return Response({"status": False, "message": "User Haven't Any Token."}, status=status.HTTP_404_NOT_FOUND)

    try:
        refresh = BlacklistedToken.objects.get(token_id=refresh)
        if refresh:
            refresh = "Token is Blacklisted."
    except BlacklistedToken.DoesNotExist:
        refresh = ""

    return refresh


################ Create API #################
@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = get_tokens_for_user(user)
        user_data={
            'id':user.id,
            'name':user.name,
            'email':user.email,
            'access_token': token.get('access'),
            'refresh_token': token.get('refresh'),

        }
    return Response({"data": user_data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_post(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        post = serializer.save()
        user_data = {
            'title':post.title,
            'description':post.description,
            'content':post.content,
            'created_at':post.created_at,
        }
        return Response({"data":user_data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_like(request):
    serializer = LikeSerializer(data=request.data)
    if serializer.is_valid():
        like = serializer.save()
        user_data = {
            'post':like.post,
            'user':like.user,
        }
        return Response({"data":user_data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


############# Get API #############

@api_view(['GET'])
def get_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_like(request, like_id):
    try:
        like = Like.objects.get(pk=like_id)
        serializer = LikeSerializer(like)
        return Response(serializer.data)
    except Like.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


################ Update API #################

@api_view(['PUT'])

def update_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def update_post(request, post_id):


    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PostSerializer(post, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_like(request, like_id):
    try:
        like = Like.objects.get(pk=like_id)
    except Like.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = LikeSerializer(like, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



############# Delete API ##############

@api_view(['DELETE'])
def delete_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Check if the post is public or the owner is accessing it
    if post.is_public or post.author == request.user:
        serializer = PostSerializer(post)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)



from django.db.models import Count

@api_view(['GET'])
def get_all_posts(request):
    posts = Post.objects.select_related('author').annotate(like_count=Count('like')).prefetch_related('like_set')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)




