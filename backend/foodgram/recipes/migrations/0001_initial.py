# Generated by Django 2.2.19 on 2023-03-01 18:10

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите наименование ингридиента', max_length=128, verbose_name='Наименование ингридиента')),
                ('measurement_unit', models.CharField(help_text='Введите наименование единицы измерения', max_length=24, verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name': 'ингридиент',
                'verbose_name_plural': '2. Ингридиенты',
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')),
                ('image', models.ImageField(help_text='Выберете картинку для рецепта', upload_to='static/', verbose_name='Картинка')),
                ('name', models.CharField(help_text='Введите наименование рецепта', max_length=200, verbose_name='Наименование рецепта')),
                ('text', models.TextField(help_text='Введите описание рецепта', verbose_name='Описание')),
                ('cooking_time', models.IntegerField(help_text='Введите время приготовления (в минутах)', validators=[django.core.validators.MinValueValidator(1, 'Указано не корректное время приготовления.'), django.core.validators.MaxValueValidator(10080, 'Указано не корректное время приготовления.')], verbose_name='Время приготовления')),
                ('author', models.ForeignKey(help_text='Укажите автора рецепта', on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'рецепт',
                'verbose_name_plural': '3. Рецепты',
                'ordering': ('pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите наименование тега', max_length=10, verbose_name='Наименование тега')),
                ('color', models.CharField(help_text='Введите цветовой HEX-код (например, #49B64E)', max_length=10, verbose_name='Цвет тега')),
                ('slug', models.SlugField(help_text='Введите уникальный идентификатор', max_length=10, unique=True, verbose_name='Уникальный slug')),
            ],
            options={
                'verbose_name': 'тег',
                'verbose_name_plural': '1. Теги',
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_in_cart', to='recipes.Recipe', verbose_name='Рецепт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopper', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'рецепт',
                'verbose_name_plural': '6. Список покупок',
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='RecipeTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(help_text='Введите ID рецепта', on_delete=django.db.models.deletion.CASCADE, to='recipes.Recipe', verbose_name='Рецепт')),
                ('tag', models.ForeignKey(help_text='Введите ID тега', on_delete=django.db.models.deletion.CASCADE, to='recipes.Tag', verbose_name='Тег')),
            ],
            options={
                'verbose_name': 'у рецепта нужные теги',
                'verbose_name_plural': '5. Рецепты и теги',
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(help_text='Введите сколько необходимо ингридиента', validators=[django.core.validators.MinValueValidator(0, 'Указано не корректное количество.'), django.core.validators.MaxValueValidator(999999999, 'Указано не корректное количество.')], verbose_name='Количество ингридиента')),
                ('ingredient', models.ForeignKey(help_text='Введите ID ингридиента', on_delete=django.db.models.deletion.CASCADE, to='recipes.Ingredient', verbose_name='Ингридиент')),
                ('recipe', models.ForeignKey(help_text='Введите ID рецепта', on_delete=django.db.models.deletion.CASCADE, to='recipes.Recipe', verbose_name='Рецепт')),
            ],
            options={
                'verbose_name': 'у рецепта нужные ингридиенты',
                'verbose_name_plural': '4. Рецепты и ингридиенты',
                'ordering': ('pk',),
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(help_text='Введите используемые ингридиенты', related_name='recipes', through='recipes.RecipeIngredient', to='recipes.Ingredient', verbose_name='Ингридиенты'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(help_text='Введите теги для рецепта', related_name='recipes', through='recipes.RecipeTag', to='recipes.Tag', verbose_name='Теги'),
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_in_favorite', to='recipes.Recipe', verbose_name='Рецепт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favoriter', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'рецепт',
                'verbose_name_plural': '7. Список избранного',
                'ordering': ('pk',),
            },
        ),
        migrations.AddConstraint(
            model_name='shoppingcart',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_shopping_cart'),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_favorite'),
        ),
    ]
