from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from .models import Post


class PostListView(ListView):
    template_name = "posts/list.html"
    model = Post
    
class PostDetailView(DetailView):
    template_name = "posts/detail.html"
    model = Post
    
class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = "posts/new.html"
    model = Post
    fields = ["title", "subtitle", "body", "status"]
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "posts/edit.html"
    model = Post
    fields = ["title", "subtitle", "body", "status"]
    
class PostDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "posts/delete.html"
    model = Post
    success_url = reverse_lazy("list") # this should be the name of a url pattern!