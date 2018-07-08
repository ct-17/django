import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostModelForm
from .models import Comment, PostModel


#@login_required
def post_model_create_view(request):
    form = PostModelForm(request.POST, request.FILES)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.author = request.user
        obj.save()
        #messages.success(request, "Đã tạo một bài đăng blog mới!")
        context = {
            "form": PostModelForm()
        }
        return HttpResponseRedirect("/blog/{num}".format(num=obj.id))
    
    template = "blog/post.html"
    return render(request, template, context)

#@login_required
def post_model_update_view(request, id=None):
    obj = get_object_or_404(PostModel, id=id)
    form = PostModelForm(request.POST or None, instance=obj)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, "Đã cập nhật bài đăng!")
        return HttpResponseRedirect("/blog/{num}".format(num=obj.id))
    
    template = "blog/update.html"
    return render(request, template, context)


def post_model_detail_view(request, id=None):
    post = get_object_or_404(PostModel, id=id)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST, author=request.user, post=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path)

    context = {
        "object": post,
        "form": form,
    }
    template = "blog/detail.html"
    return render(request, template, context)



def post_model_delete_view(request, id=None):
    obj = get_object_or_404(PostModel, id=id)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Đã xóa bài đăng")
        return HttpResponseRedirect("/blog/")
    context = {
        "object": obj,
    }
    template = "blog/delete.html"
    return render(request, template, context)


def post_model_list_view(request):
    query = request.GET.get("q", None)
    qs = PostModel.objects.all().order_by('-publish_date')
    paginator = Paginator(qs, 12)
    page = request.GET.get('page')

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    index = items.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginator.page_range[start_index:end_index]

    if query is not None:
        qs = qs.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(slug__icontains=query)
                )
    context = {
        "object_list": qs,
        "items": items,
        "page_range": page_range,
    }
    template = "blog/home.html"
    return render(request, template, context)



@login_required(login_url='/login/')
def login_required_view(request):
    print(request.user)
    qs = PostModel.objects.all()
    context = {
        "object_list": qs,
    }

    if request.user.is_authenticated():
        template = "blog/home.html"
    else:
        template = "blog/list-view-public.html"
        #raise Http404
        return HttpResponseRedirect("/login")
    
    return render(request, template, context)




def post_model_robust_view(request, id=None):
    obj = None
    context =  {}
    success_message = 'Một bài đăng mới đã được tạo'
    
    if id is None:
        "obj có thể được tạo ra"
        template = "blog/post.html"
    else:
        "obj prob exists"
        obj = get_object_or_404(PostModel, id=id)
        #success_message = 'Một bài đăng mới đã được tạo'
        context["object"] = obj
        template = "blog/detail.html"
        if "edit" in request.get_full_path():
            template = "blog/update.html"
        if "delete" in request.get_full_path():
            template = "blog/delete.html"
            if request.method == "POST":
                obj.delete()
                messages.success(request, "Đã xóa bài đăng")
                return HttpResponseRedirect("/blog/")

    #if "edit" in request.get_full_path() or "create" in request.get_full_path():
    form = PostModelForm(request.POST or None, instance=obj)
    context["form"] = form
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, success_message)
        if obj is not None:
            return HttpResponseRedirect("/blog/{num}".format(obj.id))
        context["form"] - PostModelForm()
    return render(request, template, context)

def comments(request, id):
    post = get_object_or_404(PostModel, id=id)
    if request.method == 'POST':
        form = CommentForm(request.POST, author=request.user)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = form.author
            comment.save()
            return redirect('blog:detail', id=post.id)
    else:
        form = CommentForm()
        return render(request, 'blog/comments.html', {"form":form})

def home(request):
    query = request.GET.get("q", None)
    qs = PostModel.objects.all().order_by('-publish_date')
    paginator = Paginator(qs, 12)
    page = request.GET.get('page')

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    index = items.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginator.page_range[start_index:end_index]

    if query is not None:
        qs = qs.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(slug__icontains=query)
                )
    context = {
        "object_list": qs,
        "items": items,
        "page_range": page_range,
    }
    template = "blog/home.html"
    return render(request, template, context)

def computer(request):
    query = request.GET.get("q", None)
    qs = PostModel.objects.all().order_by('-publish_date').filter(kind="computer")
    paginator = Paginator(qs, 12)
    page = request.GET.get('page')

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    index = items.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginator.page_range[start_index:end_index]

    if query is not None:
        qs = qs.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(slug__icontains=query)
                )
    context = {
        "object_list": qs,
        "items": items,
        "page_range": page_range,
    }
    template = "blog/computer.html"
    return render(request, template, context)

def mobile(request):
    query = request.GET.get("q", None)
    qs = PostModel.objects.all().order_by('-publish_date').filter(kind="mobile")
    paginator = Paginator(qs, 12)
    page = request.GET.get('page')

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    index = items.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginator.page_range[start_index:end_index]

    if query is not None:
        qs = qs.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(slug__icontains=query)
                )
    context = {
        "object_list": qs,
        "items": items,
        "page_range": page_range,
    }
    template = "blog/mobile.html"
    return render(request, template, context)

def technology(request):
    query = request.GET.get("q", None)
    qs = PostModel.objects.all().order_by('-publish_date').filter(kind="technology")
    paginator = Paginator(qs, 12)
    page = request.GET.get('page')

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    index = items.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginator.page_range[start_index:end_index]

    if query is not None:
        qs = qs.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(slug__icontains=query)
                )
    context = {
        "object_list": qs,
        "items": items,
        "page_range": page_range,
    }
    template = "blog/technology.html"
    return render(request, template, context)

def games(request):
    query = request.GET.get("q", None)
    qs = PostModel.objects.all().order_by('-publish_date').filter(kind="games")
    paginator = Paginator(qs, 12)
    page = request.GET.get('page')

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    index = items.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginator.page_range[start_index:end_index]

    if query is not None:
        qs = qs.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(slug__icontains=query)
                )
    context = {
        "object_list": qs,
        "items": items,
        "page_range": page_range,
    }
    template = "blog/games.html"
    return render(request, template, context)
