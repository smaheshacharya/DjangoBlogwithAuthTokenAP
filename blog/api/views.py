from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth.models import User
from blog.models import Post
from blog.api.serializer import BlogSerializer


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def api_detail_blog_view(request, pk):
    try:
        blog_post = Post.objects.get(pk=pk)
    except Post.PostDoesNotExit:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method =='GET':
        serializer = BlogSerializer(blog_post)
        return Response(serializer.data)


@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def api_update_blog_view(request, pk):
    try:
        blog_post = Post.objects.get(pk=pk)
    except Post.PostDoesNotExit:
        return Response(status=status.HTTP_404_NOT_FOUND )

    user = request.user
    if blog_post.author != user:
        return Response({"response":"You don't have permission to edit the post"})

    if request.method == 'PUT':
        serializer = BlogSerializer(blog_post, data = request.data)
        data = {

        }
        if serializer.is_valid():
            serializer.save()
            data["success"] = "update successfully"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def api_delete_blog_view(request, pk):
    try:
        blog_post = Post.objects.get(pk=pk)
    except Post.PostDoesNotExit:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if blog_post.author != user:
        return Response({"response": "You don't have permission to delete    the post"})

    if request.method == 'DELETE':
        operation = blog_post.delete()
        data = {}
        if operation:
            data['success'] = 'Delete Success'
        else:
            data['failure'] = 'Delete Fail'
        return Response(data=data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_create_blog_view(request):
    user = User.objects.get(pk=4)
    post = Post(author=user)
    if request.method == 'POST':
        serializer = BlogSerializer(post, data = request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# function based views to return all the list
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def api_list_blog_view(request):
    try:
        blog_post = Post.objects.all()
    except Post.PostDoesNotExit:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BlogSerializer(blog_post, many=True)
        return Response(serializer.data)


class ApiBlogListViews(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = BlogSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_classes = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('title', 'content','author__username')