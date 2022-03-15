from django.utils import timezone

from django.test import TestCase
from django.contrib.auth.models import User

from blog.models import Post

class PostModelTestCase(TestCase):
    """Post model test case."""

    @classmethod
    def setUpClass(cls) -> None:
        """Run one time class set up."""
        super().setUpClass()

    def setUp(self) -> None:
        """Run this set up before each test."""
        self.user = User.objects.create(username="testuser")
        self.unpublished_post = Post.objects.create(
            author = self.user,
            title="Test unpublished post",
            text="Test",
            published_date=None
        )
        self.published_post = Post.objects.create(
            author = self.user,
            title="Test unpublished post",
            text="Test",
            published_date=timezone.now()
        )

    def test_is_published_on_unpublished_post(self) -> None:
        """Test is_published method on unpublished post."""
        self.assertFalse(self.unpublished_post.is_published())

    def test_is_published_on_published_post(self) -> None:
        """Test is_published on published post."""
        self.assertTrue(self.published_post.is_published())

    def test_publish_method(self) -> None:
        """Test publish method."""
        pass

    def test_str_method(self) -> None:
        """Test __str__ method."""
        post = self.published_post
        expected = post.title

        self.assertEqual(post.__str__(), expected)
        self.assertEqual(str(post), expected)