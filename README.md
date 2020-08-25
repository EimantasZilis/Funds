# Spending Tree

## Installation instructions
Download the latest conda release from [here](https://www.anaconda.com/distribution/).
Populate settings in `.env` file and run the following 
```
source .env
bash install.sh
```

## To do
### High priority
#### Docker deployment
1. Create `docker_deployment/helpers/docker_build.sh` script.
This will run all relevant commands to generate any deployment dependencies and build the image itself.
This script should replace `docker build` command.

Dependencies:
 - Generate `docker_deployment/webapp/requirements.txt` file. This will contain all python modules based on `environment.yml` file. It should be deleted at the end of the `docker_build.sh` script.
 - Source code for the app. 
 - Make sure `docker_deployment/webapp/Dockerfile` generates and deletes relevant directories
 - `.env` file. Generate it from a template. Also have an option to pre-populate it for dev.

1. Copy relevant files/folders into `docker_deployment/webapp` 
1. Run `docker build`



### Medium priority

### Low priority
1. Add proper description in README for Spending Tree
1. Dockerise deployment
1. Send emails when resetting passwords
1. Make it mobile friendly