from django.contrib.auth import user_logged_in
from django.dispatch import receiver
from social_django.models import UserSocialAuth


@receiver(user_logged_in)
def update_custom_user(sender, user, request, **kwargs):
    try:
        soc_user = UserSocialAuth.objects.get(user=user)
        user.is_custom_user = True
        user.save()
    except UserSocialAuth.DoesNotExist:
        pass