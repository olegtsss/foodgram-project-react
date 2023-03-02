"""Сообщения в сериализаторе и контроллере."""

# api/serializers.py
BAD_USERNAME_ERROR = {'error': 'Нельзя использовать me в качестве username!'}
VALIDATION_ERROR = {'error': 'Не хватаает обязательного поля!'}
INGREDIENT_COUNT_MIN_ERROR = {'error': 'Количество ингредиента слишком малое!'}
INGREDIENT_COUNT_MAX_ERROR = {
    'error': 'Количество ингредиента должно слишком большое!'}
INGREDIENT_NAME_ERROR = {'error': 'Ингридиенты должны быть уникальными!'}
INGREDIENT_ID_ERROR = {'error': 'Не корректно задан ингридиент!'}
INGREDIENT_AMOUNT_ERROR = {
    'error': 'Количество ингридиента должно быть числом!'}
TAG_ID_ERROR = {'error': 'Не корректно задан тег!'}
TAG_NAME_ERROR = {'error': 'Теги должны быть уникальными!'}
CREATE_SHOPPING_CART_ERROR = {'error': 'Ошибка добавления в список покупок!'}
CREATE_SHOPPING_CART_EXIST_ERROR = {
    'error': 'Рецепт уже добавлен в список покупок!'}
LIMIT_NAME_ERROR = {
    'error': 'Параметр запроса recipes_limit должен быть целым числом!'}
FOLLOW_EXIST_ERROR = {'error': 'Подписка на автора уже существует!'}
FOLLOW_YOURSELF_ERROR = {'error': 'Нельзя подписаться на себя самого!'}

# api/views.py
ERROR_MESSAGE_FOR_USERNAME = (
    'Невозможно войти с предоставленными учетными данными.')
RECIPES_ID_ERROR = {'error': 'Не верно указан номер рецепта!'}
DELETE_SHOPPING_CART_RECIPES_ERROR = {'error': 'Рецепта не существует!'}
DELETE_SHOPPING_CART_ERROR = {
    'error': 'В списке покупок рецепта не существует!'}
FILE_NAME = 'shopping_list'
ADD_RECIPE_IN_FAVORITE_ERROR = {'error': 'Указанный рецепт не существует!'}
RECIPE_IN_FAVORITE_EXIST_ERROR = {
    'error': 'Указанный рецепт уже есть в избранном!'}
RECIPE_IN_FAVORITE_NOT_EXIST_ERROR = {
    'error': 'Указанный рецепт отсутствует в избранном!'}
FOLLOW_NOT_EXIST_ERROR = {'error': 'Подписка на автора не существует!'}
