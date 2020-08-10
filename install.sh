#!/usr/bin/env bash

echo "Installing dependencies..."
conda env create -f build-mac.yml
brew install sass/sass/sass
brew install postgresql
brew postgresql-upgrade-database

echo "Starting Postgres..."
brew services start postgres

echo "Setting up Postgres for the first time..."
psql -U postgres -d spdb -c "SELECT * from registration_user"

psql -U postgres -c "CREATE USER spuser WITH PASSWORD '1234';"
psql -U postgres -c "CREATE DATABASE spdb WITH OWNER 'postgres' TEMPLATE template0 ENCODING 'UTF8';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE spdb to spuser;"
psql -U postgres -c "ALTER ROLE spuser SET timezone TO 'UTC';"
psql -U postgres -c "ALTER USER spuser CREATEDB;"

echo "Compiling CSS..."
sass front_end/static/base.scss front_end/static/base.css