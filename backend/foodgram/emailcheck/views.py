import random
from django.shortcuts import render
from emailcheck.constants import (EMAIL_SUBJECT, EMAIL_BODY,
                                   CONFIRMATION_CODE_LENGTH,
                                   SEND_EMAIL, MINUTE_FOR_VERIFICATION_EMAIL,
                                   SEND_EMAIL_ERROR, SEND_EMAIL_ERROR_JSON,
                                   BAD_CONFIRMATION_CODE,
                                   URL_FOR_EMAIL_VERIFICATION,
                                   MAX_COUNT_VERIFICATION_EMAIL,
                                   VERIFICATION_PREFIX)
from smtplib import SMTPResponseException
from string import digits, ascii_letters
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response

from emailcheck.models import Code
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from hashlib import sha1
from users.models import User
import datetime as dt


def validate_email(**validated_data):
    """
    Проверка, что email принадлежит пользователю.
    Проверку, что в модели User пользователь существует и он активирован
    делать не нужно, так как после активации будет создан объект в модели User.
    Сериализатор не разрешит повторное использование username и email.
    """
    if Code.objects.filter(email=validated_data['email']).exists():
        # Проверка, что ссылка верификации не устарела
        verification_user = Code.objects.get(email=validated_data['email'])
        # В datetime добавляется информация о временной зоне из другого объекта
        if dt.datetime.now(verification_user.date_joined.tzinfo) < (
            verification_user.date_joined + dt.timedelta(
                minutes=MINUTE_FOR_VERIFICATION_EMAIL)
        ):
            return SEND_EMAIL.format(email=validated_data['email'])
        # Ссылка устарела, значит нужно генерировать все заново
        verification_user.delete()
    # Верификация проходит впервые или отправленная ранее ссылка устарела
    confirmation_code = (
        ''.join(random.choices(
            ascii_letters + digits, k=CONFIRMATION_CODE_LENGTH)
        )
    )
    # Email содержит символ Unicode, поэтому сначала необходимо
    # выполнить преобразование encode
    email_hash = sha1(validated_data['email'].encode('utf-8')).hexdigest()
    link = (
        f'{URL_FOR_EMAIL_VERIFICATION}/{VERIFICATION_PREFIX}/'
        f'{email_hash}/{confirmation_code}/'
    )
    try:
        send_mail(
            EMAIL_SUBJECT,
            EMAIL_BODY.format(link=link),
            settings.EMAIL_HOST_USER,
            [validated_data['email'], ],
            fail_silently=False,
        )
        # Через метод create_user, чтобы пароль был хеширован
        temp_user = User.objects.create_user(**validated_data)
        validated_data['password'] = temp_user.password
        temp_user.delete()
        Code.objects.create(
            **validated_data, email_hash=email_hash,
            confirmation_code=confirmation_code, is_active=False)
        return SEND_EMAIL.format(email=validated_data['email'])

    except SMTPResponseException as error:
        return SEND_EMAIL_ERROR.format(
            email=validated_data['email'],
            code=error.smtp_code, error=error.smtp_error)


@api_view(('GET',))
def verification_request(request, email_hash, confirmation_code):
    """Обрабатывать запросы для верификации email."""
    pass
        #    return Response(serializer.data, status=status.HTTP_201_CREATED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
