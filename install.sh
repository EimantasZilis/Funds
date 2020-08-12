#!/usr/bin/env bash

echo "Installing dependencies..."
conda env create -f build-mac.yml
brew update
brew install sass/sass/sass
brew install postgresql

echo "Starting Postgres..."
brew services start postgres

psql -U "$USER" -d postgres -c "CREATE USER spuser WITH PASSWORD '1234';"
psql -U "$USER" -d postgres -c "CREATE DATABASE spdb WITH OWNER "$USER" TEMPLATE template0 ENCODING 'UTF8';"
psql -U "$USER" -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE spdb to spuser;"
psql -U "$USER" -d postgres -c "ALTER ROLE spuser SET timezone TO 'UTC';"
psql -U "$USER" -d postgres -c "ALTER USER spuser CREATEDB;"

echo "Compiling CSS..."
sass front_end/static/base.scss front_end/static/base.css

echo "Applying Django migrations..."
python front_end/manage.py migrate
python front_end/manage.py makemigrations

echo "Applying git hooks..."
ln -s -f ../../hooks/pre-commit .git/hooks/pre-commit
