## Secrets
Чтобы использовать апи ключи создайте файл ```./config/.secrets.toml```, который будет со следующим содержимым:
```toml
dynaconf_merge = true
[bot]
debug_api_key = ''
general_api_key = ''
[ai]
api_key = ''
```
Для секции bot нужно взять ключи [отсюда](https://t.me/BotFather), а для ai надо взять [отсюда](https://aistudio.google.com/app/apikey).
