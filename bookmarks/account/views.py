from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile, Contact
from bookmarks.common.decorators import ajax_required
from actions.utils import create_action
from actions.models import Action


@login_required  # Checking if User is authenticated.
def dashboard(request):
    # Default displaying all actions.
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)

    if following_ids:
        # If user is following others, then will get an information only about their actions.
        actions = Action.objects.filter(user_id__in=following_ids)
    actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:10]
    # pass actions list to render in a template.
    return render(request, 'account/dashboard.html', {'section': 'dashboard', 'actions': actions})


@ajax_required  # Check if request is AJAX type.
@require_POST  # Allowing only HTTP POST method.
@login_required  # Checking if User is authenticated.
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'ok'})


@login_required  # Checking if User is authenticated.
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'account/user/list.html', {'section': 'people', 'users': users})


@login_required  # Checking if User is authenticated.
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'account/user/detail.html', {'section': 'people', 'user': user})

@login_required  # Checking if User is authenticated.
def edit(request):
    message = None
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            if 'default' in request.POST:
                profile = Profile.objects.get(user=request.user)
                profile.photo = 'user.png'
                profile.save()
                print('success')
            messages.success(request, 'Your profile information has been updated.')
            return HttpResponseRedirect('/account/edit/')

        else:
            messages.error(request, 'An error occurred while profile update.')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form,
                                                 'message': message})


def login_and_register(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        registration_form = UserRegistrationForm(request.POST)

        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd['l_username'], password=cd['l_password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/account/dashboard/')
                else:
                    return HttpResponseRedirect('/account/blocked/')
            else:
                login_form.add_error('l_username', 'Invalid username or password')
                messages.error(request, 'Login process goes wrong. Please try again.')
                return render(request, 'registration/login.html',
                              {'login_form': login_form, 'registration_form': registration_form})

        if registration_form.is_valid():
            new_user = registration_form.save(commit=False)
            new_user.username = registration_form.cleaned_data['r_username']
            new_user.set_password(registration_form.cleaned_data['r_password'])
            # Creating new User.
            new_user.save()
            # Creating new Profile based on new user.
            Profile.objects.create(user=new_user)
            create_action(new_user, 'create an account.')
            messages.success(request, 'Your new account has been successfully created.')
            return render(request, 'account/register_done.html', {'new_user': new_user})

        else:
            messages.error(request, 'An error occurred while creating the account.')
    else:
        login_form = LoginForm()
        registration_form = UserRegistrationForm()
    return render(request, 'registration/login.html',
                  {'login_form': login_form, 'registration_form': registration_form})
