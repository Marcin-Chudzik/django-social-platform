import datetime

from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from .models import Action


def create_action(user, verb: str, target=None) -> bool:
    # Checking if any similar actions weren't processing in a last minute.
    last_minute = timezone.now() - datetime.timedelta(seconds=60)
    # Saving all "actions" from last minute since now which contains similar verb and same user.
    similar_actions = Action.objects.filter(user_id=user.id, verb=verb, created__gte=last_minute)

    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_ct=target_ct, target_id=target.id)

    if not similar_actions:
        # Any similar actions found.
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False
