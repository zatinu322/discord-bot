lint: ## Проверяет линтерами код в репозитории
	uvx ruff check ./src
	uvx --with pydantic --python 3.12 mypy .
	uvx --from editorconfig-checker ec ./src

format: ## Запуск автоформатера
	uvx ruff check --fix ./src

test: ## Запускает автотесты
	docker compose --profile test run --rm discord-bot-test

help: ## Отображает список доступных команд и их описания
	@echo "Cписок доступных команд:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
