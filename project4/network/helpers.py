from .models import *

def compare_user(user1, user2):
    if user1 == user2:
        return True
    return False

def create_profile(user):
    try:
        profile = Profile.objects.get(user=user)
    except:
        profile = Profile()
        profile.user = user
        profile.save()
    return profile
