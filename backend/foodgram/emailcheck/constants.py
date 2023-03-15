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
SEND_EMAIL = 'Код подтверждения отправлен на почту {email}.'
SEND_EMAIL_ERROR = (
    'Не удалось отправь электронное письмо на {email}. '
    'Код ошибки: {code}. Ошибка: {error}.'
)
VERIFICATION_ERROR = 'Не корректный запрос!'
VERIFICATION_OUTDATED = 'Ссылка устарела, получите новое подтверждение!'
VERIFICATION_OK = 'Верификация пройдена!'
