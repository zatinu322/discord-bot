set shell := ["powershell.exe", "-c"]

lint:
    uvx --from editorconfig-checker ec ./src
    uvx ruff check ./src
    uvx --with pydantic --python 3.12 mypy .

format:
    uvx ruff check --fix ./src

test:
    docker compose --profile test run --rm discord-bot-test

alembic-rev msg:
    docker compose run --rm discord-bot bash -c "uv run alembic revision --autogenerate -m '{{msg}}'"

alembic-up:
    docker compose run --rm discord-bot bash -c "uv run alembic upgrade head"

alembic-down rev_count='1':
    docker compose run --rm discord-bot bash -c "uv run alembic downgrade -{{rev_count}}"
