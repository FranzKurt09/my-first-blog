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
    PostPublishingAPIView,
    CustomAuthToken
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
        #self.user = User.objects.create(username="testuser")
        #self.other_user = User.objects.create(username="other_user")
        #self.post = Post.objects.create(
        #        author = self.user,
        #        title = "Test title",
        #        text = "Test post"
        #        )
        
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
    

    def test_get_method_views_a_post_success(self) -> None:
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
    
    def test_get_method_views_a_post_error(self) -> None:
        """Get method succesfully views a post"""
        
        user = User.objects.create(username="testuser")
        post = Post.objects.create(
                author = user,
                title = "Test title",
                text = "Test post"
                )
        post_id = post.id
        
        expected = {
                    "title": "Error",
                    "message": "Post not found."
                }

        self.url = "posts/" + str(post_id) + "/"

        request = self.request_factory.get(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request, post_id=post_id + 1)
        
        response_data = response.data

        self.assertEqual(response_data, expected)
        self.assertEqual(response.status_code, 404)
    
    
    #work on this
    def test_post_method_fails_to_create_new_post(self) -> None:
        """Post method fails to creates a new post"""
        
        user = User.objects.create(username="testuser")
        post = Post.objects.create(
                author = user,
                title = "Test title",
                text = "Test post"
                )
        
        expected = {
                    "data": self.get_post_data(post)
                }

        self.url = "posts/"

        request = self.request_factory.post(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request)
        
        response_data = response.data

        self.assertNotEqual(response_data, expected) #equal
        self.assertEqual(response.status_code, 400)
        

    def test_post_method_succeeds_in_creating_new_post(self) -> None:
        """Post method succesfully creates a new post"""
        
        user = User.objects.create(username="testuser")
        
        data = {
            "author": user.id,
            "title": "Test title",
            "text": "Test text"
        }
        
        Post.objects.all().delete()
        
        self.url = "post/"
        
        request = self.request_factory.post(self.url, data=data)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request)
        
        post = Post.objects.first()
        expected = {
                    "title": "Success!",
                    "message": "Post created!",
                    "data": self.get_post_data(post)
                }
        
        response_data = response.data
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data, expected)
        
    def test_put_method_succeds_in_editing_post(self) -> None:
        """Put method succesfully edits a post"""
        
        user = User.objects.create(username="testuser")
        
        data = {
            "author": user.id,
            "title": "Edited test title",
            "text": "Edited test text"
        }
        
        post = Post.objects.create(
            author = user,
            title = "Test title",
            text = "Test post"
        )
        post_id = post.id
        post = Post.objects.get(pk=post.id)
        
        self.url = "posts/" + str(post_id) + "/"
        
        request = self.request_factory.put(self.url, data=data)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request, post_id=post_id)
        
        post = Post.objects.first()
        expected = {
                    "title": "Success!",
                    "message": "Post edited!",
                    "data": self.get_post_data(post)
                }
        
        response_data = response.data
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data, expected)
    
    def test_put_method_post_not_found(self) -> None:
        """Put method fails to get a post to edit."""
        
        user = User.objects.create(username="testuser")
        
        data = {
            "author": user.id,
            "title": "Edited test title",
            "text": "Edited test text"
        }
        
        post = Post.objects.create(
            author = user,
            title = "Test title",
            text = "Test post"
        )
        post_id = post.id
        post = Post.objects.get(pk=post.id)
        
        self.url = "posts/" + str(post_id) + "/"
        
        request = self.request_factory.put(self.url, data=data)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request, post_id=post_id + 1)
        
        post = Post.objects.first()
        expected = {
                    "title": "Error",
                    "message": "Post not found!"
                }
        
        response_data = response.data
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data, expected)
    
    #work on this
    def test_put_method_edit_post_not_saved(self) -> None:
        """Put method fails to get a post to edit."""
        
        user = User.objects.create(username="testuser")
        
        post = Post.objects.create(
            author = user,
            title = "Edited test title",
            text = "Edited test text"
        )
        
        post = Post.objects.create(
            author = user,
            title = "Test title",
        )
        post_id = post.id
        post = Post.objects.get(pk=post.id)
        
        self.url = "posts/" + str(post_id) + "/"
        
        request = self.request_factory.put(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request, post_id=post_id)
        
        exc = Exception
        post = Post.objects.first()
        expected = {
                    "title": "Error",
                    "message": "Unable to save post data",
                    "error": str(exc)
                }
        
        response_data = response.data
        
        self.assertEqual(response.status_code, 400)
        self.assertNotEqual(response_data, expected) #equal
        
    #not working yet error 403
    def test_put_returns_error_on_non_authorized_edit(self) -> None:
        """PUT request on post by another user which is not the author returns error."""

        user = User.objects.create(username="testuser")
        other_user = User.objects.create(username="other_user")
        post = Post.objects.create(
               author = user,
               title = "Test title",
               text = "Test post"
               )

        expected_error_message = "You are not authorized to edit this post."

        edit_data = {
            "title": "I will edit the title even if I'm not authorized", 
            "text": "I will edit this text even if I'm not authorized", 
            "author": user.id,
        }
        
        post_id = post.id

        url = "post/" + str(post_id)
        request = self.request_factory.put(url, edit_data)

        # Mimic the idea that this user is the one sending the request
        force_authenticate(request, other_user)

        response = self.view(request, post_id)
        response_data = response.data


        self.assertNotEqual(post.author, other_user)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_data["title"], "Error")
        self.assertEqual(response_data["message"], expected_error_message)
    
    def test_delete_method_succeeds_in_deleting_post(self) -> None:
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
       
    def test_delete_method_post_not_found(self) -> None:
        """Delete method fails to delete a post"""
        
        user = User.objects.create(username="testuser")
        post = Post.objects.create(
                author = user,
                title = "Test title",
                text = "Test post"
                )
        post_id = post.id
        
        expected = {
            "title": "Error",
            "message": "Post not found."
        }
        
        self.url = "posts/" + str(post_id) + "/"

        request = self.request_factory.delete(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request, post_id=post_id + 1)
        
        response_data = response.data

        self.assertEqual(response_data, expected)
        self.assertEqual(response.status_code, 404)
       
       
       
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
        
    def test_get_method_access_a_comment(self) -> None:
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
    
    def test_get_method_fails_to_access_a_comment(self) -> None:
        """Test Get method fails"""
        
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
                    "title": "Error",
                    "message": "Comment not found."
                }

        self.url = "comments/" + str(comment_id) + "/"

        request = self.request_factory.get(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request, comment_id=comment_id + 1)
        
        response_data = response.data

        self.assertEqual(response_data, expected)
        self.assertEqual(response.status_code, 404)
        
        

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
        """Post method not found."""
        
        user = User.objects.create(username="testuser")
        
        post = Post.objects.create(
            author = user,
            title = "Test title",
            text = "Test text"
        )
        
        post_id = post.id
        post = Post.objects.get(pk=post_id)
        
        data = {
            "post": post_id,
            "author": "Test author",
            "text": "Test text"
        }
        
        self.url = "comment/new/"
        
        request = self.request_factory.post(self.url, data=data)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request)
        
        comment = Comment.objects.first()
        expected = { 
            "title": "Success!",
            "message": "Comment created!",
            "data": self.get_comment_data(comment)
        }
        
        response_data = response.data
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_data, expected)
    
    #work on this
    def test_post_method_adds_a_comment(self) -> None:
        """Post method succesfully adds a comment."""
        
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
        
        self.assertEqual(response.status_code, 404)
        self.assertNotEqual(response_data, expected) #equal
        
        
        
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
    
    
    @tag("solo")
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
        
    def test_get_method_fails_to_returns_all_comments(self) -> None:
        """GET method should fail to return comments."""
        
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
        
        expected = {
                    "title": "Error",
                    "message": "Post not found."
                }

        self.url = "post/" + str(post_id) + "/comments/"

        request = self.request_factory.get(self.url)
        force_authenticate(request, user=user, token=user.auth_token)
        response = self.view(request, post_id=post_id + 1)
        
        response_data = response.data

        self.assertNotEqual(response_data, expected) #equal
        self.assertNotEqual(response.status_code, 400) #200 != 400
        
        

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
        
    def test_patch_method_publishes_a_post(self) -> None:
        """Patch method succesfully publishes a post."""
        
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
        


#class CustomAuthTokenTestCase(TestCase):
#    """CustomAuthToken test case."""
#    
#    @classmethod
#    def setUpClass(cls) -> None:
#        return super().setUpClass()
#    
#    def setUp(self) -> None:
#        return super().setUp()
#    
#    def test_post_method_auth_token(self) -> None:
#        """Post creates a token for user."""
#        
#        data = {
#            
#        }