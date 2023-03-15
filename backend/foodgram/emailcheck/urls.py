from django.urls import path
from emailcheck.views import verification_request


urlpatterns = [
    path('<str:username>/<str:code>/', verification_request),
]
