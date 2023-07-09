"""
Tests for Django models.
"""
from bookmarks.common.utils import (
    create_user,
    create_profile,
    create_contact,
    create_image,
    create_action,
)
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.utils.text import slugify


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a User with an email is successful."""
        email = 'test@example.com'
        password = 'sample123'
        user = create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new Users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = create_user(email=email)
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a User without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            create_user(email='')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = create_user(superuser=True)

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_profile_with_existing_user_successful(self):
        """Test creating a Profile for existing user is successful."""
        payload = {
            'user': create_user(),
            'date_of_birth': '2000-01-01',
            'photo': 'user.png'
        }

        profile = create_profile(**payload)

        self.assertEqual(profile.user, payload['user'])
        self.assertEqual(
            str(profile), f"User profile {payload['user'].username}")
        for key, value in payload.items():
            self.assertEqual(getattr(profile, key), value)

    def test_update_existing_profile_data(self):
        """Test updating a data of existing Profile."""
        date = '2001-01-01'
        photo = 'user.png'

        user = create_user()
        profile = create_profile(
            user=user,
            date_of_birth=date,
            photo=photo
        )
        new_date = '1999-09-09'
        new_photo = 'new_photo.png'

        profile.date_of_birth = new_date
        profile.photo = new_photo

        self.assertNotEqual(profile.date_of_birth, date)
        self.assertNotEqual(profile.photo, photo)
        self.assertEqual(profile.date_of_birth, new_date)
        self.assertEqual(profile.photo, new_photo)

    def test_create_contact_for_users_is_successful(self):
        """Test creating a Contact for users is successful."""
        user_from = create_user(email='user1@example.com')
        user_to = create_user(email='user2@example.com')

        contact = create_contact(user_from, user_to)

        self.assertEqual(str(contact), f"{user_from} follows {user_to}.")
        self.assertEqual(contact.user_from, user_from)
        self.assertEqual(contact.user_to, user_to)

    def test_create_action_for_existing_user_successful(self):
        """Test creating an Action for existing user is successful."""
        user = create_user()
        image = create_image(user=user)
        payload = {
            'user': user,
            'verb': 'added',
            'target': image
        }

        action = create_action(**payload)
        payload['target'] = ContentType.objects.get_for_model(image)

        for k, v in payload.items():
            self.assertEqual(getattr(action, k), v)
        self.assertEqual(action.target_id, payload['target'].id)

    def test_create_image_with_existing_user_successful(self):
        """Test creating an Image with existing user is successful."""
        payload = {
            'user': create_user(),
            'title': 'TestTitle',
            'image': 'user.png',
            'description': 'TestDesc',
        }

        image = create_image(**payload)
        url = image.get_absolute_url()
        image.url = url

        for k, v in payload.items():
            self.assertEqual(getattr(image, k), v)
        self.assertEqual(image.slug, slugify(image.title))
        self.assertEqual(image.url, url)
        self.assertEqual(str(image), payload['title'])
        self.assertEqual(0, image.total_likes)

    def test_add_and_remove_like_for_image(self):
        """Test adding and removing an Image likes."""
        user = create_user()
        image = create_image(user=user)

        image.users_like.add(user)

        self.assertEqual(1, image.total_likes)
        self.assertIn(user, image.users_like.all())
        image.users_like.remove(user)
        self.assertEqual(0, image.total_likes)
        self.assertNotIn(user, image.users_like.all())
