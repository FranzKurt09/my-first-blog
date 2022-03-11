from blog.models import Post, Comment

from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = "id", "author", "title", "text"

class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = "id", "post", "author", "text"