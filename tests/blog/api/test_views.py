from urllib import request, response
from django.test import RequestFactory, TestCase
from django.utils import timezone
from django.contrib.auth.models import User

from blog.api.serializers import PostSerializer

from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from blog.api.views import (
    PublishedPostsAPIView,
    ApprovedCommentsAPIView,
    UnpublishedPostsAPIView,
    PostAPIView,
    ListAPIView,
    CommentsAPIView
)
from blog.models import Post, Comment


class PublishedPostsAPIViewTestCase(APITestCase):
    """PublishedPostsAPIView test case."""

    @classmethod
    def setUpClass(cls) -> None:
        """Run one time class setup initialization."""
        return super().setUpClass()

    def setUp(self) -> None:
        """Run this setup before each test."""
        self.url = "post/published/"
        self.view = PublishedPostsAPIView.as_view()
        self.request_factory = APIRequestFactory()

    def get_posts_data(self, posts) -> list:
        """Get posts data."""

        posts_data = []
        for post in posts:
            if post.is_published():
                data = {
                    "id": post.id, 
                    "title": post.title, 
                    "text": post.text,
                    "is_published": post.is_published(),
                    }
                posts_data.append(data)

        return posts_data

    def test_get_method_returns_all_published_post(self) -> None:
        """GET method should return all published post."""

        posts = Post.objects.all()

        posts_data = self.get_posts_data(posts)
        expected = {
            "data": posts_data,
            "count": len(posts_data)
        }

        published_posts_count = Post.objects.exclude(published_date=None).count()

        request = self.request_factory.get(self.url)
        response = self.view(request)

        response_data = response.data
        
        self.assertEqual(response_data, expected)
        self.assertEqual(published_posts_count, response_data["count"])


        
class ApprovedCommentsAPIViewTestCase(TestCase):
    """ApprovedCommentsAPIView test case."""
    
    @classmethod
    def setUpClass(cls) -> None:
        """Run one time class setup initialization."""
        return super().setUpClass()
    
    def setUp(self) -> None:
        """Run this setup before each test."""
        self.url = "comments/approved/"
        self.view = ApprovedCommentsAPIView.as_view()
        self.request_factory = APIRequestFactory()
    
    def get_post_data(self, post) -> list:
        """Return individual post data."""
        
        data = {
            "id": post.id, 
            "title": post.title, 
            "text": post.text, 
            "author": post.author.id,
            "is_published": post.is_published()
            }
        return data
    
            
    def get_comments_data(self, comments) -> list:
        """Get comments data."""
        
        comments_data = []
        for comment in comments:
            if comment.is_approved():    
                data = {
                    "id": comment.id,
                    "post": self.get_post_data(comment.post),
                    "author": comment.author, 
                    "text": comment.text,
                    "is_approved": comment.is_approved()
                    }
                comments_data.append(data)
        
        return comments_data
    
    def test_get_method_returns_all_approved_post(self) -> None:
        """GET method should return all approved comments."""
        
        comments = Comment.objects.all()
        
        user = User.objects.create(username="testuser")
        
        comments_data = self.get_comments_data(comments)
        expected = {
            "data": comments_data,
            "count": len(comments_data)
        }
        
        approved_comments_count = Comment.objects.exclude(approved_comment = False).count()
        
        request = self.request_factory.get(self.url)
        response = self.view(request)
        
        response_data = response.data
        
        self.assertEqual(response_data, expected)
        self.assertEqual(approved_comments_count, response_data["count"])
        

class UnpublishedPostsAPIViewTestCase(TestCase):
    """UnpublishedPostsAPIView test case."""
    
    @classmethod
    def setUpClass(cls) -> None:
        """Run one time class setup initialization."""
        return super().setUpClass()
    
    def setUp(self) -> None:
        """Run one time class setup initialization."""
        self.url = "post/unpublished/"
        self.view = UnpublishedPostsAPIView.as_view()
        self.request_factory = APIRequestFactory()
        
    def get_posts_data(self, posts) -> list:
        """Get posts data."""

        posts_data = []
        for post in posts:
            if post.is_published():
                data = {
                    "id": post.id, 
                    "title": post.title, 
                    "text": post.text,
                    "is_published": post.is_published(),
                    }
                posts_data.append(data)

        return posts_data
    
    def test_get_method_returns_all_unpublished_post(self) -> None:
        """Get method should return all unpublished post."""
        
        posts = Post.objects.all()
        
        user = User.objects.create(username="testuser")
        
        posts_data = self.get_posts_data(posts)
        expected = {
            "data": posts_data,
            "count": len(posts_data)
        }
        
        unpublished_posts_count = Post.objects.filter(published_date = None).count()
        
        request = self.request_factory.get(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request)
        
        response_data = response.data
        
        self.assertEqual(response_data, expected)
        self.assertEqual(unpublished_posts_count, response_data["count"])
        
class PostAPIViewTestCase(TestCase):
    """PostAPIView test case."""
    
    @classmethod
    def setUpClass(cls) -> None:
        """Run one time class setup initialization."""
        return super().setUpClass()
    
    def setUp(self) -> None:
        """Run one time class setup initialization."""
        self.url = "post/", "posts/<int:post_id>/"
        self.view = PostAPIView.as_view()
        self.request_factory = APIRequestFactory()

    def get_posts_data(self, posts) -> list:
        """Get posts data."""

        posts_data = []
        for post in posts:
            if post.is_published():
                data = {
                    "id": post.id, 
                    "title": post.title, 
                    "text": post.text,
                    "is_published": post.is_published(),
                    }
                posts_data.append(data)

        return posts_data
    
    def get_post_data(self, post) -> list:
        """Return individual post data."""
        
        data = {
            "id": post.id, 
            "title": post.title, 
            "text": post.text, 
            "author": post.author.id,
            "is_published": post.is_published()
            }
        return data
    
    def test_get_method(self) -> None:
        """Get method succesfully edits a post"""
        pass
    
    def test_post_method(self) -> None:
        """Post method succesfully creates a new post"""
        
        user = User.objects.create(username="testuser")
        
        data = {
            "title": "Test title", 
            "text": "Test text", 
            "author": "Test author",
        }
        
        request = self.request_factory.post(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request)
        
        posts = Post.objects.all()
        
        response_data = response.data
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data["title"], "Error")
        self.assertEqual(response_data["message"], "Unable to save post data")
        
        
    def test_put_method(self) -> None:
        """Put method succesfully edits a post"""
        pass
        
    def test_delete_method(self) -> None:
        """Delete method succesfully deletes a post"""
        pass
       
class ListAPIViewTestCase(TestCase):
    """ListAPIView test case."""
    
    @classmethod
    def setUpClass(cls) -> None:
        return super().setUpClass()
    
    def setUp(self) -> None:
        self.url = "post/list/"
        self.view = ListAPIView.as_view()
        self.request_factory = APIRequestFactory()
        
    def test_get_method_return_all_post(self) -> None:
        """GET method should return all posts."""
        
        user = User.objects.create(username="testuser")
        Post.objects.all()
        
        request = self.request_factory.get(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request)
        
        self.assertEqual(response.status_code, 200)
        
class CommentsAPIViewTestCase(TestCase):
    """CommentsAPIView test case"""
    
    @classmethod
    def setUpClass(cls) -> None:
        return super().setUpClass()
    
    def setUp(self) -> None:
        self.url = "comment/new/"
        self.view = CommentsAPIView.as_view()
        self.request_factory = APIRequestFactory()
        
    def get_posts_data(self, posts) -> list:
        """Get posts data."""

        posts_data = []
        for post in posts:
            if post.is_published():
                data = {
                    "id": post.id, 
                    "title": post.title, 
                    "text": post.text,
                    "is_published": post.is_published(),
                    }
                posts_data.append(data)

        return posts_data
    
    def get_post_data(self, post) -> list:
        """Return individual post data."""
        
        data = {
            "id": post.id, 
            "title": post.title, 
            "text": post.text, 
            "author": post.author.id,
            "is_published": post.is_published()
            }
        return data
    
            
    def get_comments_data(self, comments) -> list:
        """Get comments data."""
        
        comments_data = []
        for comment in comments:
            if comment.is_approved():    
                data = {
                    "id": comment.id,
                    "post": self.get_post_data(comment.post),
                    "author": comment.author, 
                    "text": comment.text,
                    "is_approved": comment.is_approved()
                    }
                comments_data.append(data)
        
        return comments_data
    
    def get_comment_data(self, comment) -> list:
        """Return individual comment data."""
        
        data = {
            "id": comment.id, 
            "post": comment.post.id,
            "author": comment.author,
            "text": comment.text,
            "is_approved": comment.is_approved()
            }
        return data
    
    def test_post_method(self) -> None:
        """GET method should return all posts."""
        
        user = User.objects.create(username="testuser")
        
        data = {
            "post": "Test post",
            "author": "Test author",
            "text": "Test text"
        }
        
        Comment.objects.all()
        
        request = self.request_factory.post(self.url, data=data)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request)
        
        response_data = response.data
        
        self.assertEqual(response.status_code, 400)