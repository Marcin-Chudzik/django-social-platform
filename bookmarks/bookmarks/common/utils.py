"""
Util functionalities.
"""
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from account.models import Profile
from images.models import Image
from actions.models import Action


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def create_user(password: str = 'sample123', superuser: bool = False,
                **extra_fields) -> User:
    """Create and return a User."""
    last_user = get_user_model().objects.last()
    new_user_id = 1 if not last_user else last_user.id + 1
    email = f'test{new_user_id}@example.com'

    new_user = get_user_model().objects.create(
        email=extra_fields.pop('email', email),
        username=extra_fields.pop('username', email),
        password=password,
        **extra_fields
    )
    if superuser:
        new_user.is_staff = True
        new_user.is_superuser = True
        new_user.save()

    return new_user


def create_profile(user: User = create_user(),
                   date_of_birth: str = '2001-01-01',
                   photo: str = 'user.png',
                   **extra_fields) -> Profile:
    """Create and return a Profile."""
    new_profile = Profile.objects.create(
        user=user,
        date_of_birth=date_of_birth,
        photo=photo,
        **extra_fields
    )
    return new_profile


def create_image(user: User = create_user(), title: str = 'TestTitle',
                 image: str = 'user.png', description: str = 'TestDesc',
                 **extra_fields) -> Image:
    """Create and return an Image."""
    new_image = Image.objects.create(
        user=user,
        title=title,
        image=image,
        description=description,
        **extra_fields
    )
    new_image.url = new_image.get_absolute_url()
    return new_image


def create_action(user: User = create_user(), verb: str = 'added',
                  target_obj: object = None) -> Action:
    if not target_obj:
        target_obj = create_image(user=user)

    target_ct = ContentType.objects.get_for_model(target_obj)
    action = Action(user=user, verb=verb, target=target_ct)
    action.save()
    return action
