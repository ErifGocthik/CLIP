import os
import random

from PIL import Image as IMAGE
from transformers import CLIPProcessor, CLIPModel
import numpy as np

# import re
#
# import requests
# import uvicorn
# from django.views.decorators.csrf import csrf_exempt
# from fastapi import FastAPI
# from fuzzywuzzy import fuzz
#

from django.contrib.auth import logout
# from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView

from cloudapp.forms import ArchiveCreateForm
# from cloudapp.image_predict import image_predict
from cloudapp.models import Image, CustomUser, Archive, Design

model = CLIPModel.from_pretrained('openai/clip-vit-base-patch32')
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")


def predict(image, text):
    image = IMAGE.open(image.image.path)

    inputs = processor(text=[text, "other"], images=image, return_tensors="pt", padding=True)

    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image  # this is the image-text similarity score
    probs = logits_per_image.softmax(dim=1)
    predict_result = probs.tolist()
    result = predict_result[0][0]
    result = result >= 0.75
    return result


    # def root_view(request):
    #     # request.session['design'] = Design.objects.get(pk=1).file.path
    #     # file = request.session['design']
    #     user = CustomUser
    #     image_ = Image.objects.get(pk=1).name
    #     # file_content = (open(file, 'r').read()).split('\n')
    #     return render(request, 'root.html', {'user': user, 'test': image_})


def logout_view(request):
    user = CustomUser
    if user.is_authenticated or request.user:
        logout(request)
    return redirect(reverse_lazy('main:main'))

# @csrf_exempt
# def get_neuro_images(request):
#     uvicorn.run(app, host='127.0.0.1', port=8001)
#     requests.get()
#     return JsonResponse({'message': 'FastAIP running', 'user': request.POST.get('user')})

class MainListView(ListView):
    model = Image
    template_name = 'main.html'
    context_object_name = 'images'

    def get_size(self, size):
        size = size
        name = 'б'
        result = 0
        if (size > 1024):
            result = size / 1024
            name = 'Кб'
            if (result > 1024):
                result = result / 1024
                name = 'Мб'
                if (result > 1024):
                    result = result / 1024
                    name = 'Гб'
        return f'{round(result, 2)} {name}'

    def get_context_data(self, **kwargs):
        self.request.session['Bs'] = False
        self.request.session['Sb'] = False
        self.request.session['nero'] = False
        user = self.request.user.pk
        images = Image.objects.filter(user_id=user)
        search_text = self.request.GET.get('search')
        image_list = []
        global_size = 0

        if self.request.GET.get('search'):
            if self.request.GET.get('nero') == 'нейро':
                for image in Image.objects.filter(user_id=user):
                    if predict(image, self.request.GET.get('search')) == True:
                        image_list.append(str(image.pk))

                images = Image.objects.filter(id__in=image_list)
            if self.request.GET.get('nero') != 'нейро':
                if self.request.GET.get('filt') == 'Bs' or self.request.session['Bs']:
                    if self.request.session['Sb'] == False:
                        self.request.session['Bs'] = True
                    images = Image.objects.filter(user_id=user, name__icontains=self.request.GET.get('search')).order_by('-file_size')
                elif self.request.GET.get('filt') == 'Sb':
                    if not self.request.session['Bs']:
                        self.request.session['Sb'] = True
                    images = Image.objects.filter(user_id=user, name__icontains=self.request.GET.get('search')).order_by('file_size')
                else:
                    images = Image.objects.filter(user_id=user, name__icontains=self.request.GET.get('search'))
        else:
            if self.request.GET.get('filt') == 'Bs':
                if self.request.session['Sb'] == False:
                    self.request.session['Bs'] = True
                images = Image.objects.filter(user_id=user).order_by('-file_size')
            elif self.request.GET.get('filt') == 'Sb':
                if self.request.session['Bs'] == False:
                    self.request.session['Sb'] = True
                images = Image.objects.filter(user_id=user).order_by('file_size')
            else:
                images = Image.objects.filter(user_id=self.request.user.pk)[:8]
        archives = Archive.objects.filter(user_id=self.request.user.pk)
        img_list = Image.objects.filter(user_id=user)
        for image in img_list:
            global_size += int(image.file_size)
        natural_size = (global_size / 21474836480) * 100
        natural_size = str(natural_size).replace(',', '.')
        context = {'images': images,
                   'archives': archives,
                   'global_size': self.get_size(global_size),
                   'natural_size': natural_size,
                   'fBs': self.request.session['Bs'],
                   'fSb': self.request.session['Sb'],
                   'nero': self.request.GET.get('nero'),
                   'search_text': search_text,
                   }
        return context

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect(reverse_lazy('authorization:login'))
        return render(self.request, self.template_name, self.get_context_data())

    # def post(self, request):


class InfinityArchiveListView(View):

    def get(self, request):
        page = self.request.GET.get('page')
        result = self.get_result(int(page))
        result = list(result.values())
        return JsonResponse({'results': result})

    def get_result(self, page):
        archive = get_object_or_404(Archive, pk=self.request.GET.get('pk'))
        all_obj = archive.images.all()
        per_page = 8
        result = all_obj[(page - 1) * per_page: page * per_page]
        return result


class InfinityListView(View):
    def get(self, request):
        page = self.request.GET.get('page')
        result = self.get_result(int(page))
        result = list(result.values())
        return JsonResponse({'results': result})

    def get_result(self, page):
        all_obj = Image.objects.all()
        per_page = 8
        result = all_obj[(page - 1) * per_page: page * per_page]
        return result


class UploadingFilesView(View):

    def get(self, request):
        return redirect(reverse_lazy('main:main'))

    def post(self, request):
        # if not self.request.user.is_authenticated:
        #     return redirect(reverse_lazy('authorization:login'))
        file = request.FILES.get('file')
        images_info = request.POST.get('keys')
        images_info = images_info.split(',')
        images_info = list(map(int, images_info))
        image = Image.objects.create(name=file.name,
                                     image=file,
                                     file_size=images_info[2],
                                     width=images_info[0],
                                     height=images_info[1],
                                     user_id=self.request.user)
        image.save()
        return JsonResponse({'success': True})


class ArchivesListView(CreateView):
    model = Archive
    context_object_name = 'archives'
    template_name = 'archives.html'
    form_class = ArchiveCreateForm

    def get_context_data(self, *, object_list=None, **kwargs):
        archives = Archive.objects.filter(user_id=self.request.user.pk)
        # images = Image.objects.filter(archive_id=archives.)
        form = self.form_class
        return {'archives': archives, 'form': form}

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect(reverse_lazy('authorization:login'))
        return render(self.request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        archive = form.save(commit=False)
        color = ['#' + ''.join([random.choice('ABCDEF0123456789') for i in range(6)])][0]
        archive.color = color
        archive.user_id = self.request.user
        archive.save()
        return redirect(reverse_lazy('main:archives'))


class GetImageId(View):
    def get(self, request):
        image_id = self.request.GET.get('image_id')
        image = Image.objects.get(pk=image_id)
        return JsonResponse({'image_url': image.image.url,
                             'image_w': image.width,
                             'image_h': image.height,
                             'image_size': image.get_size(),
                             'image_name': image.name,
                             'add_date': image.added_at})


class ArchiveDetailView(DetailView):
    model = Archive
    template_name = 'archive.html'
    context_object_name = 'archive'

    def get_context_data(self, pk, **kwargs):
        archive = get_object_or_404(Archive, pk=pk)
        images = archive.images.all()[:8]
        return {'archive': archive, 'images': images}

    def get(self, request, pk, *args, **kwargs):
        return render(self.request, self.template_name, self.get_context_data(pk))


class AddInArchive(View):
    def get(self, request):
        image_id = self.request.GET.get('img_id')
        archive_id = self.request.GET.get('a_id')
        archive = Archive.objects.get(pk=archive_id)
        image = Image.objects.get(pk=image_id)
        if not (archive.images.filter(id=image.pk).exists()):
            try:
                archive.images.add(image)
            except KeyError as e:
                return JsonResponse({'succeed': False, 'has': False})
            return JsonResponse({'succeed': True, 'has': False})
        else:
            return JsonResponse({'succeed': False, 'has': True})


class RemoveFromArchive(View):
    def get(self, request):
        image_id = self.request.GET.get('img_id')
        archive_id = self.request.GET.get('a_id')
        archive = Archive.objects.get(pk=archive_id)
        image = Image.objects.get(pk=image_id)
        if archive.images.filter(id=image.pk).exists():
            try:
                archive.images.remove(image)
            except KeyError as e:
                return JsonResponse({'succeed': False, 'has': True})
            return JsonResponse({'succeed': True, 'has': True})
        else:
            return JsonResponse({'succeed': False, 'has': False})


class CheckImageInArchive(View):
    def get(self, request):
        image_id = self.request.GET.get('img_id')
        archive_id = self.request.GET.get('a_id')
        archive = Archive.objects.get(pk=archive_id)
        image = Image.objects.get(pk=image_id)
        if archive.images.filter(id=image.pk).exists():
            return JsonResponse({'image_exists': True})
        else:
            return JsonResponse({'image_exists': False})


def download_image(request, pk):
    image = get_object_or_404(Image, pk=pk)
    file_path = image.image.path
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='image/*')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
    return response


def info_view(requset):
    return render(requset, 'info.html')

def get_link(request, pk):
    image = Image.objects.get(pk=pk)
    return JsonResponse({'link': image.image.url})