#!/bin/bash

set -Eeuo pipefail

cd /opt/discord-bot/

sudo systemctl stop discord-bot
echo "discord bot stopped"

git pull --rebase

docker compose down
docker compose build

docker compose run --rm discord-bot bash -c "uv run alembic upgrade head"

sudo systemctl start discord-bot
echo "discord bot started"
sudo systemctl status discord-bot
