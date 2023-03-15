"""Сообщения в контроллере."""

EMAIL_SUBJECT = 'Сервис Foodgram ждет подтверждания email'
EMAIL_BODY = (
    'Для подтверждения email воспользуйтесь ссылкой из письма:\n'
    '\n'
    '{link}'
)
SEND_EMAIL = 'Код подтверждения отправлен на почту {email}.'
SEND_EMAIL_ERROR = (
    'Не удалось отправь электронное письмо на {email}. '
    'Код ошибки: {code}. Ошибка: {error}.'
)
SEND_EMAIL_ERROR_JSON = (
    'Не удалось отправить электронное письмо на {email}! '
    'Пользователь {username} не создан!'
)
BAD_CONFIRMATION_CODE = 'Не корректный confirmation code: {code}!'
