from django.urls import path
from . import views
from .views import (
    PostBlogView,
    PostDetainView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    PostUserBlogView
)

urlpatterns = [
    path('', PostBlogView.as_view() , name = "homepage"),
    path('post/<int:pk>/',PostDetainView.as_view(),name='detailpage'),
    path('post/create/', PostCreateView.as_view(), name='Createpage'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='Updatepage'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='Deletepage'),
    path('about/',views.about, name = "aboutpage"),
    path('user/<str:username>/', PostUserBlogView.as_view(), name='Userposts'),

]
