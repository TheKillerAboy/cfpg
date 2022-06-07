poetry run coverage erase
poetry run pytest --cov=cfpg "$@"
poetry run coverage xml
