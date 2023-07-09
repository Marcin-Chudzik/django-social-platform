"""
Util functionalities.
"""
from account.models import (
    Profile,
    Contact,
)
from actions.models import Action
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    User,
    BaseUserManager,
)
from django.contrib.contenttypes.models import ContentType
from images.models import Image


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def create_user(password: str = 'sample123', superuser: bool = False,
                **extra_fields) -> User:
    """Create and return a User."""
    last_user = get_user_model().objects.last()
    new_user_id = 1 if not last_user else last_user.id + 1
    email = extra_fields.pop('email', f'test{new_user_id}@example.com')
    email = BaseUserManager.normalize_email(email)

    if not email:
        raise ValueError('User must have an email address.')

    new_user = get_user_model().objects.create(
        email=email,
        username=extra_fields.pop('username', email),
        **extra_fields
    )
    new_user.set_password(password)

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


def create_contact(user_from: User = create_user(),
                   user_to: User = create_user()) -> Contact:
    new_contact = Contact.objects.create(
        user_from=user_from,
        user_to=user_to,
    )
    return new_contact


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
                  target: object = None) -> Action:
    if not target:
        target = create_image(user=user)

    target_ct = ContentType.objects.get_for_model(target)
    action = Action(user=user, verb=verb, target=target_ct)
    action.save()

    return action
