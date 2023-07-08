from actions.utils import create_action
from bookmarks.common.decorators import ajax_required
from bookmarks.common.utils import is_ajax
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger,
)
from django.http import JsonResponse
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
    HttpResponseRedirect,
    HttpResponse,
)
from django.views.decorators.http import require_POST

from .forms import ImageCreateForm
from .models import Image


@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, per_page=8)
    page = request.GET.get('page')
    ajax = is_ajax(request)
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(number=1)
    except EmptyPage:
        if ajax:
            return HttpResponse('')
        images = paginator.page(number=paginator.num_pages)
    if ajax:
        return render(request, 'images/image/list_ajax.html',
                      {'section': 'images', 'images': images})
    return render(request, 'images/image/list.html',
                  {'section': 'images', 'images': images})


@login_required
@require_POST
@ajax_required
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, 'liked', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except ObjectDoesNotExist:
            messages.error(request, 'An error occurred in adding like process')
            return HttpResponseRedirect('/account/dashboard/')

    return JsonResponse({'status': 'ok'})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, 'images/image/detail.html',
                  {'section': 'images', 'image': image})


@login_required
def image_create(request):
    if request.method == 'POST':
        image_form = ImageCreateForm(data=request.POST)
        if image_form.is_valid():
            new_image = image_form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            create_action(request.user, 'added ', new_image)
            messages.success(request, 'Image has been added.')
            return redirect(new_image.get_absolute_url())
        else:
            messages.error(request, 'An error occurred while image was adding')
    else:
        image_form = ImageCreateForm(data=request.GET)
    return render(request, 'images/image/create.html',
                  {'section': 'gallery', 'image_form': image_form})
