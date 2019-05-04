from .models import Tags, Post, PostTags
from .serializers import TagSerializer, PostSerializer
from django.contrib.staticfiles import views
from .retrieval import getPosts
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import permissions
from rest_framework import generics


class TagsList(generics.ListCreateAPIView):
    serializer_class =  TagSerializer

    def get_queryset(self):
        queryset = Tags.objects.all()
        tag_name = self.request.query_params.get('tag', None)
        if tag_name is not None:
            queryset = queryset.filter(tags__icontains=tag_name)
        return queryset


# returns a specific favourite home of a specific user if exists
class PostList(generics.ListAPIView):
    serializer_class = TagSerializer
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset( self ):
        tags = self.kwargs['tag'].split(',')
        tag_ids = Tags.objects.filter(tags__in=tags).values('id')
        post_ids = PostTags.objects.filter(tags_id__in=tag_ids).values('post_id')
        return Post.objects.filter(id__in=post_ids)
