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
from .models import Post, Status


class PostListView(ListView):
    template_name = "posts/list.html"
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        published = Status.objects.get(name="published")
        context["post_list"] = (
            Post.objects
            .filter(status=published)
            .order_by("created_on").reverse()
        )
        return context
    
class DrafPostListView(LoginRequiredMixin, ListView):
    template_name = "posts/list.html"
    model = Post
    
    def get_context_data(self, **kwargs):
        # Retrive the context object (a kind of dictionary)
        context = super().get_context_data(**kwargs)
        # Retrieve the instance of Status that represents "draf" mode
        draft_status = Status.objects.get(name="draft")
        # Filter posts based on draft status and author (and order by created_on)
        context["post_list"] = (
            Post.objects
            .filter(status=draft_status)
            .filter(author=self.request.user)
            .order_by("created_on").reverse()
        )
        return context

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
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "posts/edit.html"
    model = Post
    fields = ["title", "subtitle", "body", "status"]
    
    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = "posts/delete.html"
    model = Post
    success_url = reverse_lazy("list") # this should be the name of a url pattern!
    
    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user