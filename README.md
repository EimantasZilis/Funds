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
`sass front_end/static/base.scss front_end/static/base.css`

## To do
1. Write git hooks
1. Change generic error message colour
1. Simplify CSS
1. Write tests
1. Make it mobile friendly