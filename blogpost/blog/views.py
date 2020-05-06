from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.models import User
# Create your views here.


def home(request):
    context = {
        'posts':Post.objects.all(),
    }
    return  render(request,'blog/home.html',context)

#using this class based view instead of the above home function
class PostBlogView(ListView):
    model = Post
    template_name = 'blog/home.html'
    # by default class based views looks for template with a certain
    # naming converntion and that is :-
    # <app>/<model>_<viewtype>.html
    # now in our case since it is a list view it will look for a template_name
    # which is :-
    # blog/Post_list.html
    # but we can change the tmeplate it looks for with this above line
    context_object_name = 'posts'
    # by default django looks for a context variable with name object_list
    # but we can override this using this attribute
    ordering = ['-date_posted']
    paginate_by = 4


class PostUserBlogView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User,username = self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetainView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    #for this view we only need t   o provide the fields of the form for the
    # which we want to create
    fields = ['title','content']
    #this veiw by default expects a template which is named as
    #app_form.html rather than the one mentioned above
    #it provides the form we just have to render it in the template
    #the name of this form is form by default

    #now once we click the post button in this view this view should
    #know the author of the post also and for this we have to override the
    #form_valid() method to the the author the the current logged in user

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    #Once we press the post button this view tria to redirect us to the
    #detain page of the post , but it don't know how to get their as it
    #also needs a pk of this post , for this we have to define a
    #get_absolute_url method in our model to tell it that
    #if we wanna simple redirect it to the home page then we can defin
    #the success_url paramenter = 'homepage" and it will redirect their

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    #User passes test mixin is to check if the person who is updating
    #the post is the person who wrote the post or not
    #for this mixin we need to write a function test_User() which checks
    #this condition

    model = Post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'
    #to redirect to home page after deletion
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    #this form expects a template that if we will submit it will then
    #delete the post
    #that template by default is called post_confirm_delete.html
    #the form only required template and a submit button that will
    #conform the deleteion , no form with name form or anything is
    #need to be rendered




def about(request):
    return render(request,'blog/about.html',{'title':'About'})