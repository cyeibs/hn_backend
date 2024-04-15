from rest_framework import serializers
from .models import Post

class ShallowChildSerializer(serializers.ModelSerializer):
    replies_count = serializers.IntegerField(source='children.count', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'by', 'text', 'time', 'type', 'replies_count']

class PostSerializer(serializers.ModelSerializer):
    children = ShallowChildSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'by', 'descendants', 'score', 'text', 'time', 'title', 'type', 'children']

class DeepChildSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'by', 'text', 'time', 'type', 'children']

    def get_children(self, obj):
        serializer = DeepChildSerializer(obj.children.all(), many=True, context=self.context)
        return serializer.data

class FullPostSerializer(serializers.ModelSerializer):
    children = DeepChildSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'by', 'descendants', 'score', 'text', 'time', 'title', 'type', 'children']
               
class StoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'by', 'score', 'time', 'title', 'type'] 

class PostWithoutChildrenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'by', 'descendants', 'score', 'text', 'time', 'title', 'type']