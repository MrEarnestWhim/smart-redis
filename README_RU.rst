============
SMART REDIS
============

Данная библиотека позволяет бессрочно кешировать в Redis не изменяемую инфрмацию
отдаваемой Django с помощью только лишь декоратора. То есть вам не нужно
сбрасывать кэш каждые N часов.

**Кэш очищается в случаях:**

- Перезагрузки проекта (можно выключить)
- Вы явно вызвали **out_cache()** (в сигнале или просто в коде)

Быстрый старт
-------------
0. Установка пакета::

    pip install django-smart-redis

1. Добавте "django_smart_redis" в ваш INSTALLED_APPS в настройках Django::

    INSTALLED_APPS = [
        ...
        'django_smart_redis',
        ...
    ]

2. Настройки (указаны дефолт значения)::

    SMART_REDIS_HOST='127.0.0.1'
    SMART_REDIS_PORT=6379
    SMART_REDIS_DB=0
    SMART_REDIS_PASSWORD="pswd"
    SMART_REDIS_NAMESPACE="cache"
    SMART_REDIS_RESTART_AND_CLEAR_CACHE=True

- **SMART_REDIS_PASSWORD**
    Пароль. Если у вас его нет(на локале работаете), можно настройку не указывать.

- **SMART_REDIS_NAMESPACE**
    Ваше пространство имён, чтобы небыло коллизий с другими данными в Redis.

- **SMART_REDIS_RESTART_AND_CLEAR_CACHE**
    Включение/выключение очистки кэша при рестарте сервиса.

3. Провести миграции::

    python manage.py migrate

Это нуужно чтобы в админке вывести текущий кэш.

4. Примеры использования:

**view.py** (Кешируем выдаваемую информацию)::

    from django.views import View
    from django.http import JsonResponse
    from django_smart_redis.core.decorators import out_cache

    class ExampleView(View):
        @smart_cache("Название_вашего_ключа")
        def get(self, request, *args, **kwargs):
            category = ExampleModel.objects.filter(...)
            return JsonResponse({"data": category.to_json()})


**models.py** (Для очистки кэша при изменении данных в БД)::

    from django.db import models
    from django.db.models.signals import post_save, post_delete
    from django.dispatch import receiver
    from django_smart_redis.core.core import clear_cache

    class ExampleModel(models.Model):
        title = models.TextField(max_length=255)

    # Вешаем сигнал
    @receiver((post_save, post_delete), sender=ExampleModel)
    def my_handler(sender, **kwargs):
        clear_cache("Название_вашего_ключа")

Немного позже завезу еще оптимизации.