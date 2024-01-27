from django.urls import path
from upvotes import views

urlpatterns = [
    path('upvotes/', views.UpvoteListView.as_view()),
    path('upvotes/<int:pk>/', views.UpvoteDetail.as_view()),
]