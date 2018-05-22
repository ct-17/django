from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import DeleteView, ListView
from django.urls import reverse
from .forms import CommentForm, PostForm
from .models import Comment, Post
from django.utils import timezone


class IotListView(ListView):
    ct = Post
    paginate_by= 10     # số lượng bài biết hiện thị
    template_name = "iot/iot.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def get_queryset(self):
        return Post.objects.all()

class IotDetailView(DeleteView):
    ct = Post
    success_url= "iot/detail.html"
    #form_class = CommentForm
    template_name = "iot/detail.html"
       
    def get_queryset(self):
        return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def comments(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, author=request.user)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = form.author
            comment.save()
            return redirect('iot:detail', pk=post.pk)
    else:
        form = CommentForm()
        return render(request, 'iot/comments.html', {"form":form})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.author
            #post.upload_time = timezone.now()
            post.save()
            return redirect('iot:detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'iot/post.html', {"form":form})



