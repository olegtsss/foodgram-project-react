"""
Приложение предназначено для верификации email при регистрации.
(пользователь создается посредством API - набор ModelMixin).

Логика работы:
1) API получает запрос на создание нового пользователя.
2) Новый пользователь не создается, вместо это создается объект в новой
модели. Она не унаследована от User, однако имеет точно такие же поля.
3) Пользователь получает email с ссылкой валидации, после перехода по
ней создается первоначальный объект в модели User.
4) Учтены самые разные ситуации, попытки подбора ссылки и многое другое.

Примеры запросов:
### Создание пользователя ###
POST http://127.0.0.1:8000/api/users/
Content-Type: application/json

{
    "email": "admin2@admin.ru",
    "username": "vasya.pupkin2",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "password": "Qwerty123"
}
### Верификация email ###
GET http://127.0.0.1:8000/verification/5eb51149...f099df0/MOmr25X...V1ObMu5/

Интеграция в проект:
1) Добавляем приложение в settings.py
INSTALLED_APPS = [
    ...
    'emailcheck.apps.EmailcheckConfig',
    ...
]

2) Переопределяем CreateModelMixin:

class UserViewSet(
    CustomCreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet
):
    ...
class CustomCreateModelMixin(CreateModelMixin):
    throttle_scope = 'low_request'
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Добавленный код
        return Response(
            {'message': validate_email(**serializer.validated_data)},
            status=status.HTTP_200_OK)

3) Подключаем нужный роут в главном urls.py:
urlpatterns = [
    ...
    path(f'{VERIFICATION_PREFIX}/', include('emailcheck.urls')),
]

4) Ограничиваем интенсивность запросов для защиты своего почтового сервера:
REST_FRAMEWORK = {
    ...
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'low_request': '1/minute',
    }
}

5) Настраиваем SMTP backend:
if os.getenv('SMTP_BACKEND_EMULATION'):
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')

6) Добавляем переменные окружения:
EMAIL_HOST =
EMAIL_PORT =
EMAIL_HOST_USER =
EMAIL_HOST_PASSWORD =
EMAIL_USE_TLS =
SMTP_BACKEND_EMULATION =

7) В emailcheck.urls проверяем длину <confirmation_code> внутри регулярного
выражения (по умолчанию равна 64, однако не извлекается из переменной
CONFIRMATION_CODE_LENGTH)
"""

"""Настройки приложения."""
CONFIRMATION_CODE_LENGTH = 64
MINUTE_FOR_VERIFICATION_EMAIL = 20
MAX_COUNT_VERIFICATION_EMAIL = 10
URL_FOR_EMAIL_VERIFICATION = 'http://127.0.0.1:8000'
VERIFICATION_PREFIX = 'verification'


"""Сообщения в контроллере."""
EMAIL_SUBJECT = 'Сервис Foodgram ждет подтверждания email'
EMAIL_BODY = (
    'Для подтверждения email воспользуйтесь ссылкой из письма:\n'
    '\n'
    '{link}'
)
EMAIL_SUBJECT_SUCCESS = 'Ваш email на сервисе Foodgram подтвержден!'
EMAIL_BODY_SUCCESS = (
    'Cайт Foodgram, «Продуктовый помощник» - это онлайн-сервис, на котором '
    'пользователи могут публиковать рецепты, подписываться на публикации '
    'других пользователей, добавлять понравившиеся рецепты в список '
    '«Избранное», а перед походом в магазин скачивать сводный список '
    'продуктов, необходимых для приготовления одного или нескольких '
    'выбранных блюд.'
)
SEND_EMAIL = 'Код подтверждения отправлен на почту {email}.'
SEND_EMAIL_ERROR = (
    'Не удалось отправь электронное письмо на {email}. '
    'Код ошибки: {code}. Ошибка: {error}.'
)
VERIFICATION_ERROR = 'Не корректный запрос!'
VERIFICATION_OUTDATED = 'Ссылка устарела, получите новое подтверждение!'
VERIFICATION_ALREADY_DONE = 'Ваш email уже подтвержден!'
