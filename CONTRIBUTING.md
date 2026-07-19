# Как создать локальную инсталляцию бота

На проекте используется [uv](https://docs.astral.sh/uv/).

Для удобства разработки с IDE создайте виртуальное окружение

```sh
uv sync --frozen
```

Установите pre-commit хуки

```
uvx pre-commit install
```

Полезные команды `justfile` (только Windows):

- `lint` - проверить код с помощью ruff, mypy и editorconfig-checker.
- `test` - запустить тесты.
- `alembic-rev` - создать новую миграцию БД.
- `alembic-up` - применить миграции к БД.
- `alembic-down` - откатить указанное число последних миграций.

TODO: Доработать `Makefile`.

Запуск бота:

```sh
docker compose build
docker compose up
```
