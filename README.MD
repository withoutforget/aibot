# aibot ✨

Бот для интеграции искусственного интеллекта в ваши беседы в телеграм. 

[![Статус сборки](https://img.shields.io/badge/build-passing-brightgreen)]()
[![Качество кода](https://img.shields.io/badge/code%20quality-checked-blue)]()


## 🚀 Начало работы

## Зависимости
*   ⚙️ uv
*   🐍 Python
*   🔨 Make

### Установка

1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/withoutforget/aibot.git
    cd aibot
    ```

2.  **Установите зависимости:**
    ```bash
    make depends
    ```
    Далее вам потребуется настроить секретные ключи. Этот шаг описан далее.
### 🔑 Настройка Секретов 

Для использования API ключей (например, для Telegram бота и AI сервисов), необходимо создать файл конфигурации с секретами.

1.  Создайте директорию `config`, если она еще не существует:
    ```bash
    mkdir -p config
    ```
2.  Создайте файл `./config/.secrets.toml` со следующим содержимым:

    ```toml
    # ./config/.secrets.toml

    dynaconf_merge = true

    [bot]
    # Ключ для Telegram API (основной)
    general_api_key = 'ВАШ_ОСНОВНОЙ_TELEGRAM_API_КЛЮЧ'
    # Ключ для Telegram API (для отладки, если используется)
    debug_api_key = 'ВАШ_DEBUG_TELEGRAM_API_КЛЮЧ_ЕСЛИ_НУЖЕН'

    [ai]
      [ai.gemini]
      # Ключ для Google Gemini API
      api_key = 'ВАШ_GOOGLE_GEMINI_API_КЛЮЧ'
    ```

3.  **Получение ключей:**
    * **Для секции `[bot]`:** Получите ваши API ключи для Telegram бота через [BotFather](https://t.me/BotFather). Вставьте полученный токен(ы) в `general_api_key` (и `debug_api_key`, если необходимо).
    * **Для секции `[ai.gemini]`:** Получите API ключ для Gemini API в [Google AI Studio](https://aistudio.google.com/app/apikey). Вставьте его в поле `api_key`.

**Важно:** Добавьте `config/.secrets.toml` в ваш файл `.gitignore`, чтобы случайно не загрузить секретные ключи в репозиторий!

### ⚙️ Использование
**Запуск приложения**
```bash
make run
```

### 🛠️ Разработка
**Форматирование**
```bash
make format
```
**Линтиг**
```bash 
make check
```
**Обновление зависимостей**
```bash
make depends
```
**Очистка кэша**
```bash
make clean
```
**Инициализация нужных директорий**
```bash
make init_dirs
```
