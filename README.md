# тестовое

привет) это мое тестовое, ниже лежит все самое нужное

v1.0.1 завязал тесты на вызове функции из main

структура:

```text
main.py           функция
test_main.py      тесты
requirements.txt  пакетики
pytest.ini        тут настройки тестов; не обязательно но прикольно)
.gitignore        не тянем окружение и логи
```

⬇️ тык

```bash
pip install -r requirements.txt
pytest
```

⬇️ тык

```bash
pytest -m positive
```

⬇️ тык

```bash
pytest -m negative
```
