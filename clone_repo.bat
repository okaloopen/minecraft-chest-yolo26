@echo off
REM Batch-скрипт для клонирования репозитория с детектором сундуков.

set REPO_URL=https://github.com/okaloopen/minecraft-chest-yolo26.git
echo Клонирование репозитория %REPO_URL%
git clone %REPO_URL%
