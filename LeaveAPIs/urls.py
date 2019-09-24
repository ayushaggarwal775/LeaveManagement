from django.urls import  path
from . import views
urlpatterns = [
    path('applyLeave', views.ApplyForLeave.as_view())
]