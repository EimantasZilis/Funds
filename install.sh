#!/usr/bin/env bash

echo "Installing dependencies..."
conda env create -f environment.yml
brew update
brew install sass/sass/sass
brew install postgresql

psql -U "$USER" -d postgres -c "CREATE USER ${POSTGRES_USER} WITH PASSWORD '${POSTGRES_PASSWORD}';"
psql -U "$USER" -d postgres -c "CREATE DATABASE ${POSTGRES_DB} WITH OWNER "$USER" TEMPLATE template0 ENCODING 'UTF8';"
psql -U "$USER" -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} to spuser;"
psql -U "$USER" -d postgres -c "ALTER ROLE ${POSTGRES_USER} SET timezone TO 'UTC';"
psql -U "$USER" -d postgres -c "ALTER USER ${POSTGRES_USER} CREATEDB;"

echo "Compiling CSS..."
sass front_end/static/base.scss front_end/static/base.css

echo "Applying Django migrations..."
python front_end/manage.py migrate
python front_end/manage.py makemigrations

echo "Applying git hooks..."
ln -s -f ../../hooks/pre-commit .git/hooks/pre-commit
