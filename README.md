# Spending Tree

## Installation instructions
### Install conda
Download the latest conda release from [here](https://www.anaconda.com/distribution/).

### Configure environment
Create a new environment and install install relevant packages by running:
```conda env create -f build-mac.yml```

### Install brew packages (MacOS)
```
brew install sass/sass/sass
```

### Install and configure postgres
```
brew install postgresql
brew postgresql-upgrade-database
brew services start postgres
psql
CREATE USER spuser WITH PASSWORD '1234';
CREATE DATABASE spdb WITH OWNER 'postgres' TEMPLATE template0 ENCODING 'UTF8';   
GRANT ALL PRIVILEGES ON DATABASE spdb to spuser;
ALTER ROLE spuser SET timezone TO 'UTC';
ALTER USER spuser CREATEDB;
```

### Compile CSS
```sass front_end/static/base.scss front_end/static/base.css```

### Git hooks
```ln -s -f ../../hooks/pre-commit .git/hooks/pre-commit```

## To do
### High priority

### Medium priority

### Low priority
1. Add proper description in README for Spending Tree
1. Dockerise deployment
1. Send emails when resetting passwords
1. Make it mobile friendly