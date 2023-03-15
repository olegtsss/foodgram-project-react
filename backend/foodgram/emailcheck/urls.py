from emailcheck.views import verification_request
from django.conf.urls import url


# 64 = CONFIRMATION_CODE_LENGTH from emailcheck.constants
urlpatterns = [
    url(
        r'^(?P<email_hash>\w{40})/(?P<confirmation_code>\w{64})/$',
        verification_request
    ),
]
