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

### Compile CSS
```sass front_end/static/base.scss front_end/static/base.css```

### Git hooks
```ln -s -f ../../hooks/pre-commit .git/hooks/pre-commit```

## To do
### High priority
1. Fix field errors pushing out input fields

### Medium priority
1. Change sqlite database to postgres

### Low priority
1. Dockerise deployment
1. Send emails when resetting passwords
1. Make it mobile friendly
1. Dockerise deployments