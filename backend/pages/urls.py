from django.urls import path
from pages.views import server_status

urlpatterns = [
    path('', server_status, name='server_status'),
]
