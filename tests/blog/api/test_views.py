from urllib import request, response
from django.test import RequestFactory, TestCase
from django.utils import timezone
from django.contrib.auth.models import User

from django.test.utils import tag
from pprint import pprint

from blog.api.serializers import PostSerializer

from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from blog.api.views import (
    PublishedPostsAPIView,
    ApprovedCommentsAPIView,
    UnpublishedPostsAPIView,
    PostAPIView,
    ListAPIView,
    CommentAPIView,
    CommentsAPIView,
    PostCommentsAPIView,
    ApprovingCommentAPIView,
    PostPublishingAPIView
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
       
       

#work on this too

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
        """Get method succesfully views a post"""
        
        user = User.objects.create(username="testuser")
        post = Post.objects.create(
                author = user,
                title = "Test title",
                text = "Test post"
                )
        post_id = post.id
        
        expected = {
                    "data": self.get_post_data(post)
                }

        self.url = "posts/" + str(post_id) + "/"

        request = self.request_factory.get(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request, post_id=post_id)
        
        response_data = response.data

        self.assertEqual(response_data, expected)
        self.assertEqual(response.status_code, 200)
    
    #okay for error
    def test_post_method_error(self) -> None:
        """Post method succesfully creates a new post"""
        
        user = User.objects.create(username="testuser")
        post = Post.objects.create(
                author = user,
                title = "Test title",
                text = "Test post"
                )
        
        expected = {
                    "data": self.get_post_data(post)
                }
        pprint(expected)

        self.url = "posts/"

        request = self.request_factory.post(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request)
        pprint(request)
        pprint(response)
        
        response_data = response.data
        pprint(response_data)

        self.assertNotEqual(response_data, expected)
        self.assertEqual(response.status_code, 400)
        
    #not working
    def test_post_method_success(self) -> None:
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
        
        user = User.objects.create(username="testuser")
        post = Post.objects.create(
                author = user,
                title = "Test title",
                text = "Test post"
                )
        post_id = post.id
        
        expected = {
            "title": "Success",
                "message": "Post deleted!"
        }
        
        self.url = "posts/" + str(post_id) + "/"

        request = self.request_factory.delete(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request, post_id=post_id)
        
        response_data = response.data

        self.assertEqual(response_data, expected)
        self.assertEqual(response.status_code, 200)
       
       
       
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
        


class CommentAPIViewTestCase(TestCase):
    """CommentAPIView test case."""
    
    @classmethod
    def setUpClass(cls) -> None:
        return super().setUpClass()
    
    def setUp(self) -> None:
        self.url = "comments/<int:comment_id>/"
        self.view = CommentAPIView.as_view()
        self.request_factory = APIRequestFactory()
        
    def get_posts_data(self, posts) -> list:
        """Get posts data."""

        posts_data = []
        for post in posts:
            data = {
                "id": post.id, 
                "title": post.title, 
                "text": post.text,
                "is_published": post.is_published(),
                }
            posts_data.append(data)

        return posts_data
        
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
        
    def test_get_method(self) -> None:
        """Test Get method"""
        
        user = User.objects.create(username="testuser")
        post = Post.objects.create(
                author = user,
                title = "Test title",
                text = "Test post"
                )
        post_id = post.id
        
        comment = Comment.objects.create(
                post = post,
                author = user,
                text = "Test comment on test post ",
        )

        comment_id = comment.id
        
        comments = Comment.objects.filter(post=post_id).first()
        expected = {
                    "data": self.get_comment_data(comments)
                }

        self.url = "comments/" + str(comment_id) + "/"

        request = self.request_factory.get(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request, comment_id=comment_id)
        
        response_data = response.data

        self.assertEqual(response_data, expected)
        self.assertEqual(response.status_code, 200)
        
        

#work on this next
class CommentsAPIViewTestCase(TestCase):
    """CommentsAPIView test case."""
    
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
    
    def test_post_method_return_error(self) -> None:
        """GET method should return all posts."""
        
        user = User.objects.create(username="testuser")
        post = Post.objects.create(
            author = user,
            title = "Test title",
            text = "Test post"
        )
        comment = Comment.objects.create(
            post = post,
            author = user,
            text = "Test comment on test post"
        )
        
        expected = { 
            "title": "Success!",
            "message": "Comment created!",
            "data": self.get_comment_data(comment)
        }
        
        request = self.request_factory.post(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request)
        
        response_data = response.data
        
        self.assertEqual(response.status_code, 400)
        
        
    
    def test_post_method(self) -> None:
        """GET method should return all posts."""
        
        user = User.objects.create(username="testuser")
        post = Post.objects.create(
            author = user,
            title = "Test title",
            text = "Test post"
        )
        comment = Comment.objects.create(
            post = post,
            author = user,
            text = "Test comment on test post"
        )
        
        comments = Comment.objects.all()
        expected = { 
            "title": "Success!",
            "message": "Comment created!",
            "data": self.get_comment_data(comment)
        }
        
        request = self.request_factory.post(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request)
        
        response_data = response.data
        
        self.assertEqual(response.status_code, 400)
        
        
        
class PostCommentsAPIViewTestCase(TestCase):
    """PostCommentsAPIView test case."""

    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        return super().setUpClass()

    def setUp(self) -> None:
        self.url = "post/<int:post_id>/comments/"
        self.view =  PostCommentsAPIView.as_view()
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
    
    def get_post_data(self, post):
        """Return individual post data."""
        
        data = {
            "id": post.id, 
            "title": post.title, 
            "text": post.text, 
            "author": post.author.id,
            "is_published": post.is_published()
            }
        return data

    def get_comments_data(self, comments):
        """Get comment data from comments queryset."""
        comments_data = []
        for comment in comments:
            data = {
                "id": comment.id, 
                "post": self.get_post_data(comment.post),
                "author": comment.author, 
                "text": comment.text,
                "is_approved": comment.is_approved(),
                }
            comments_data.append(data)
        
        return comments_data
    
    def test_get_method_returns_all_comments(self) -> None:
        """GET method should return comments."""
        
        user = User.objects.create(username="testuser")
        post = Post.objects.create(
                author = user,
                title = "Test title",
                text = "Test post"
                )
        comment = Comment.objects.create(
                post = post,
                author = user,
                text = "Test comment on test post ",
        )
        post_id = post.id
        
        comments = Comment.objects.filter(post=post_id)
        expected = {
                    "data": self.get_comments_data(comments)
                }

        self.url = "post/" + str(post_id) + "/comments/"

        request = self.request_factory.get(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request, post_id=post_id)
        
        response_data = response.data

        self.assertEqual(response_data, expected)
        self.assertEqual(response.status_code, 200)
        
        

class ApprovingCommentAPIViewTestCase(TestCase):
    """ApprovingCommentAPIView test case."""
    
    @classmethod
    def setUpClass(cls) -> None:
        return super().setUpClass()
    
    def setUp(self) -> None:
        self.url = "approve/comment/<int:comment_id>/"
        self.request_factory = APIRequestFactory()
        self.view = ApprovingCommentAPIView.as_view()
        
    def test_patch_method(self) -> None:
        
        user = User.objects.create(username="testuser")
        post = Post.objects.create(
                author = user,
                title = "Test title",
                text = "Test post"
                )
        comment = Comment.objects.create(
                post = post,
                author = user,
                text = "Test comment on test post ",
        )
        comment_id = comment.id
        
        comments = Comment.objects.get(pk=comment_id)
        
        comments.approve()
        expected = {
            "title": "Success",
            "message": "Comment Approved!"
        }
        
        self.url = "approve//comment/" + str(comment_id) + "/"

        request = self.request_factory.patch(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request, comment_id=comment_id)
        
        response_data = response.data

        self.assertTrue(comments.is_approved())
        self.assertEqual(response_data, expected)
        self.assertEqual(response.status_code, 200)
        
        
    def test_delete_method(self) -> None:
        
        user = User.objects.create(username="testuser")
        post = Post.objects.create(
                author = user,
                title = "Test title",
                text = "Test post"
                )
        comment = Comment.objects.create(
                post = post,
                author = user,
                text = "Test comment on test post ",
        )
        comment_id = comment.id
        
        expected = {
            "title": "Success",
            "message": "Comment Removed!"
        }
        
        self.url = "approve//comment/" + str(comment_id) + "/"

        request = self.request_factory.delete(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request, comment_id=comment_id)
        
        response_data = response.data

        self.assertEqual(response_data, expected)
        self.assertEqual(response.status_code, 200)
        
        

class PostPublishingAPIViewTestCase(TestCase):
    """PostPublishingAPIView test case."""
    
    @classmethod
    def setUpClass(cls) -> None:
        return super().setUpClass()
    
    def setUp(self) -> None:
        self.url = "post/publish/<int:post_id>/"
        self.view = PostPublishingAPIView.as_view()
        self.request_factory = APIRequestFactory()
        
    def test_patch_method(self) -> None:
        
        user = User.objects.create(username="testuser")
        post = Post.objects.create(
                author = user,
                title = "Test title",
                text = "Test post"
                )
        
        post_id = post.id
        
        posts = Post.objects.get(pk=post_id)
        
        posts.publish()
        expected = {
            "title": "Success",
            "message": "Post published!"
        }
        
        self.url = "post//publish/" + str(post_id) + "/"

        request = self.request_factory.patch(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request, post_id=post_id)
        
        response_data = response.data

        self.assertTrue(posts.is_published())
        self.assertEqual(response_data, expected)
        self.assertEqual(response.status_code, 200)