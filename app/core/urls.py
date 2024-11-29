from django.urls import path
from .views import MergeFilesView

urlpatterns = [
    path('merge-files/', MergeFilesView.as_view(), name='merge-files'),
]