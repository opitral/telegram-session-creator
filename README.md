# Telegram session creator: первая настройка и руководство по использованию

## Первая настройка

### Подготовка

У вас должен быть установлен **Python** версии **3.10** или выше. Также убедитесь, что **pip** (Python Installs Packages) добавлен в **PATH** (переменные окружения).

Путь к рабочей директории проекта должен состоять только из **латинских** символов.

### Виртуальное окружение

#### Linux/MacOS
1. Открываем консоль и переходим в корневую папку директории с проектом (если исходники скачаны с GitHub, то этой директорией будет **telegram-session-creator-main**).
2. Создаем виртуальное окружение командой `python3 -m venv venv`.
3. Активируем виртуальное окружение командой `source venv/bin/activate`.
4. Устанавливаем зависимости проекта командой `pip install -r requirements.txt`.

#### Windows
1. Открываем консоль и переходим в корневую папку директории с проектом (если исходники скачаны с GitHub, то этой директорией будет **telegram-session-creator-main**).
2. Создаем виртуальное окружение командой `python -m venv venv`.
3. Активируем виртуальное окружение командой `venv\Scripts\activate`.
4. Устанавливаем зависимости проекта командой `pip install -r requirements.txt`.

### Конфигурационный файл
Создаем в корне файл `config.ini`. В рабочей директории есть пример `config.ini.example`.

Для получения **api_id** и **api_hash** переходим на [my.telegram.org/auth](https://my.telegram.org/auth) и регистрируем новое приложение.

Для получения **api_key** переходим на https://asocks.com/api-help.

В **country_code** пишем код станы, прикси которой хотим регистрировать.

## Руководство по использованию
Открываем консоль, переходим в рабочую директорию и активируем виртуальное окружение в зависимости от вашей ОС.

### Запуск скрипта
Запуск парсера выполняется одной простой командой.
#### Linux/MacOS
`python3 telegram_session_creator_cli_client.py example.txt`.
#### Windows
`python telegram_session_creator_cli_client.py example.txt`.

1. Введите название вашей сессии, оно должно быть уникальным.
2. Введите название базы лидов (без расширения `.db`).
3. Введите ссылку на целевой чат (публичный - только ник, приватный - полная ссылка).

#### Выходной файл
После того, как скрипт отработает, в консоли будет сообщение об успешном создании сессии и конфига. Все выходные файлы находятся в директории `results/your_session_name`.
#### Примечание
Прокси подлючать не нужно, скрипт делает все за вас.

Если после создания прокси видите ошибку `Unable to connect due to network issues: Error connecting to SOCKS5 proxy host:port` - не продолжайте создавать сессию, а завершайте выполнение и пробуйте: поменять интернет сеть/изменить код страны/подождать.

Если вы ввели что-то неправильно - откройте файл `results/your_session_name/your_session_name.json` и измените данные вручную.
#### Возможные проблемы
Если у вас возникла ошибка, откройте файл `creator.log` и найдите логи по дате. В сообщении будут указаны детали ошибки.