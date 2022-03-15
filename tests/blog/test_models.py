from django.tests import TestCase


class PostModelTestCase(TestCase):
    """Post model test case."""

    @classmethod
    def setUpClass(cls) -> None:
        """Run one time class set up."""
        super().setUpClass()

    def setUp(self) -> None:
        """Run this set up before each test."""
        pass