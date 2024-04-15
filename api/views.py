from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Post
from .serializers import PostSerializer, StoryListSerializer,FullPostSerializer,PostWithoutChildrenSerializer
from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().prefetch_related('children')
    serializer_class = PostSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = PostSerializer(instance, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def replies(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = FullPostSerializer(instance, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def fetch_multiple(self, request, *args, **kwargs):
        ids = request.data.get('ids')
        if not ids:
            return Response({'detail': 'No IDs provided'}, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.filter_queryset(self.get_queryset().filter(id__in=ids))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PostWithoutChildrenSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = PostWithoutChildrenSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    pagination_class = StandardResultsSetPagination

    @action(detail=True, methods=['post'], url_path='update-score')
    def update_score(self, request, pk=None):
        post = self.get_object()
        operation_type = request.data.get('type')

        if operation_type == 'increment':
            post.score += 1
        elif operation_type == 'decrement':
            post.score -= 1
        else:
            return Response({"error": "Invalid operation type specified. Use 'increment' or 'decrement'."},
                            status=status.HTTP_400_BAD_REQUEST)

        post.save()
        serializer = self.get_serializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StoryListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.filter(type='story').order_by('-time')
    serializer_class = StoryListSerializer
    pagination_class = StandardResultsSetPagination
