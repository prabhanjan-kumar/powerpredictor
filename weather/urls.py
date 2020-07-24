from . import views
from django.urls import path,include
app_name='weather'

urlpatterns = [
    path('',views.index)
]