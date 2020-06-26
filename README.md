# Funds

## Installation instructions
### Install conda
Download the latest conda release from [here](https://www.anaconda.com/distribution/).

### Configure environment
Create a new environment and install install relevant packages by running:
```conda env create -f build-mac.yml```

### Install sass
For MacOS users, run
```brew install sass/sass/sass```.
Alternatively, you can find [instructions](https://sass-lang.com/install) on how to install it for other platforms.


### Compile CSS
```sass front_end/static/base.scss front_end/static/base.css```

### Git hooks
```ln -s -f ../../hooks/pre-commit .git/hooks/pre-commit```

## To do
### High priority
1. Write tests
1. Fix "My user with this Email already exists." error when creating existing user. Is it getting "My user" from class name?
1. Opening password reset link multiple times. Give a warning saying that the link has expired and redirect to the login page?

### Medium priority
1. Send emails when resetting passwords

### Low priority
1. Make it mobile friendly