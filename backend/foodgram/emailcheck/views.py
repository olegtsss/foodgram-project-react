import datetime as dt
import random
from hashlib import sha1
from smtplib import SMTPResponseException
from string import ascii_letters, digits

from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, JsonResponse
from emailcheck.constants import (CONFIRMATION_CODE_LENGTH, EMAIL_BODY,
                                  EMAIL_BODY_SUCCESS, EMAIL_SUBJECT,
                                  EMAIL_SUBJECT_SUCCESS,
                                  MAX_COUNT_VERIFICATION_EMAIL,
                                  MINUTE_FOR_VERIFICATION_EMAIL, SEND_EMAIL,
                                  SEND_EMAIL_ERROR, VERIFICATION_ALREADY_DONE,
                                  VERIFICATION_ERROR, VERIFICATION_OUTDATED,
                                  VERIFICATION_PREFIX)
from emailcheck.models import Code
from rest_framework.decorators import api_view
# from rest_framework.response import Response
from users.models import User


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
        f'{settings.URL_FOR_EMAIL_VERIFICATION}/{VERIFICATION_PREFIX}/'
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
    """Обрабатывает запросы для верификации email."""
    # 1. Такого пользователя не было
    if not Code.objects.filter(email_hash=email_hash).exists():
        return JsonResponse(VERIFICATION_ERROR)
    verification_user = Code.objects.get(email_hash=email_hash)
    # Ссылка протухла
    if dt.datetime.now(verification_user.date_joined.tzinfo) > (
            verification_user.date_joined + dt.timedelta(
                minutes=MINUTE_FOR_VERIFICATION_EMAIL)
    ):
        # 2. Код не верный
        if verification_user.confirmation_code != confirmation_code:
            return JsonResponse(VERIFICATION_ERROR)
        # 3. Верный код
        return JsonResponse(VERIFICATION_OUTDATED)
    # Далее условия, если ссылка не протухла
    # 4. Много попыток
    if verification_user.count > MAX_COUNT_VERIFICATION_EMAIL:
        return JsonResponse(VERIFICATION_ERROR)
    # 5. Код не верный
    if verification_user.confirmation_code != confirmation_code:
        verification_user.count += 1
        verification_user.save()
        return JsonResponse(VERIFICATION_ERROR)
    # 7. Код верный, но пользователь уже активирован
    if verification_user.is_active:
        return JsonResponse(VERIFICATION_ALREADY_DONE)
    # 8. Код верный, все хорошо
    verification_user.is_active = True
    verification_user.save()
    User.objects.create(
        date_joined=verification_user.date_joined,
        username=verification_user.username,
        email=verification_user.email,
        first_name=verification_user.first_name,
        last_name=verification_user.last_name,
        password=verification_user.password,
        is_active=True
    )
    try:
        send_mail(
            EMAIL_SUBJECT_SUCCESS,
            EMAIL_BODY_SUCCESS,
            settings.EMAIL_HOST_USER,
            [verification_user.email, ],
            fail_silently=False,
        )
    except SMTPResponseException as error:
        return SEND_EMAIL_ERROR.format(
            email=verification_user.email,
            code=error.smtp_code, error=error.smtp_error)
    return HttpResponseRedirect(
        redirect_to=settings.URL_FOR_EMAIL_VERIFICATION)
