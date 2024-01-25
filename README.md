# beauty_shop_bot

## Установка
* Скопировать к себе репозиторий

* Создать и активировать виртуальное окружение

```
python3 -m venv env

source env/bin/activate
```

* Удостовериться, что у тебя установлена последняя версия pip — программы, которую мы используем для установки Django.

```
python -m pip install --upgrade pip
```

* Установить зависимости

```
pip install -r requirements.txt
```

* Создать в корне файл ``.env``

* Разместить в нем: 

```
DJANGO_SECRET_KEY='DJANGO_KEY'  
DJANGO_DEBUG=True
TIME_ZONE='Europe/Moscow'
```




