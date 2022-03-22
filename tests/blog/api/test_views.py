from django.utils import timezone
from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIRequestFactory

from blog.api.views import PublishedPostsAPIView
from blog.models import Post
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

        user = User.objects.create(username="testuser")
        published_post = Post.objects.create(
            author = user,
            title="Test unpublished post",
            text="Test",
            published_date=timezone.now()
        )

        unpublished_post = Post.objects.create(
            author = user,
            title="Test unpublished post",
            text="Test",
            published_date=None
        )

        posts_data = self.get_posts_data(posts)
        expected = {
            "data": posts_data,
            "count": len(posts_data)
        }
<<<<<<< Updated upstream
=======
        
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
        self.user = User.objects.create(username="testuser")
        self.other_user = User.objects.create(username="other_user")
        self.post = Post.objects.create(
                author = self.user,
                title = "Test title",
                text = "Test post"
                )

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
        
        post_id = self.post.id
        
        expected = {
                    "data": self.get_post_data(self.post)
                }

        self.url = "posts/" + str(post_id) + "/"

        request = self.request_factory.get(self.url)
        force_authenticate(request, user=self.user, token=self.user.auth_token)
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
        
    def test_put_returns_error_on_non_authorized_edit(self) -> None:
        """PUT request on post by another user which is not the author returns error."""

        author = self.user
        post = self.post
        other_user = self.other_user

        expected_error_message = "You are not authorized to edit this post."

        edit_data = {
            "title": "I will edit the title even if I'm not authorized", 
            "text": "I will edit this text even if I'm not authorized", 
            "author": author.id,
        }
        
        url = "post/" + str(post.id)
        request = self.request_factory.put(url, edit_data)

        # Mimic the idea that this user is the one sending the request
        force_authenticate(request, other_user)

        response = self.view(request)
        response_data = response.data


        self.assertNotEqual(post.author, other_user)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response_data["title"], "Error")
        self.assertEqual(response_data["message"], expected_error_message)



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
>>>>>>> Stashed changes

        published_posts_count = Post.objects.exclude(published_date=None).count()
        

        request = self.request_factory.get(self.url)
        response = self.view(request)

        response_data = response.data
        
        self.assertEqual(response_data, expected)
        self.assertEqual(published_posts_count, response_data["count"])


        
        