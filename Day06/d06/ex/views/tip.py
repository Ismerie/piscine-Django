from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from ..forms import Signup
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from ..models import Tip, Vot
from ..forms import For_tip

def delete(request):
    if not request.user.is_authenticated:
        return redirect('/')
    id = request.GET.get('id')
    tips = Tip.objects.get(id=id)
    if tips.auteur == request.user or request.user.has_perm('ex.delete_tip'):
        tips.delete()
    return redirect('/')

def like_tip(request):
    if not request.user.is_authenticated:
        return redirect('/')
    id = request.GET.get('id')
    nam = request.user.id
    try:
        u = User.objects.get(id=nam)
    except:
        return redirect('/')
    tips = Tip.objects.get(id=id)
    try:
        v = Vot.objects.get(user=u, tip=tips)
        if (v.downvote == 1) and (v.upvote == 0) :
            tips.downvote -= 1
            v.downvote = 0
        elif (v.upvote == 0) and (v.downvote == 0):
            tips.upvote += 1
            v.upvote = 1
        elif (v.upvote == 1) and (v.downvote == 0):
            tips.upvote -= 1
            v.upvote = 0
        tips.save()
        v.save()
        return redirect('/')
    except:
        uder = Vot.objects.create(user=u, tip=tips, upvote=1, downvote=0)
        tips.upvote += 1
        tips.save()
        uder.save()
        return redirect('/')
    return redirect('/')

def dislike_tip(request):
    if not request.user.is_authenticated:
        return redirect('/')

    id = request.GET.get('id')
    nam = request.user.id
    try:
        u = User.objects.get(id=nam)
    except:
        return redirect('/')
    tips = Tip.objects.get(id=id)
    if tips.auteur != request.user and not request.user.has_perm('ex.can_downvote'):
        return redirect('/')
    try:
        v = Vot.objects.get(user=u, tip=tips)
        if (v.upvote == 1) and (v.downvote == 0):
            tips.upvote -= 1
            v.upvote = 0
        elif (v.downvote == 1) and (v.upvote == 0):
            tips.downvote -= 1
            v.downvote = 0
        elif (v.downvote == 0) and (v.upvote == 0):
            tips.downvote += 1
            v.downvote = 1
        tips.save()
        v.save()
        return redirect('/')
    except:
        uder = Vot.objects.create(user=u, tip=tips, upvote=0, downvote=1)
        tips.downvote += 1
        tips.save()
        uder.save()
        return redirect('/')
    return redirect('/')

# CREATE DOWNVOTE PERMISSION
# from django.contrib.auth.models import Group, Permission
# from django.contrib.contenttypes.models import ContentType

# # Create your own permission
# content_type = ContentType.objects.get_for_model(User)
# permission = Permission.objects.create(
#     codename='can_downvote',
#     name='Can Downvote Tips',
#     content_type=content_type,
# )

# # Add the permission to a specific group or user
# group = Group.objects.get(name='downvoters')
# group.permissions.add(permission)