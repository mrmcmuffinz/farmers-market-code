# Pre Requisites?

1. docker

2. minikube

# How to build dockerfile?

1. Run docker build command.

Note: Since we are running this on minikube and we are using local docker, we will need to run `eval $(minikube docker-env)` prior to building the image in order for minikube to know where to get the docker image from. 

command: `docker build . -f Dockerfile -t farmers-market:1.1.7`

# How to deploy code?

1. `cd scripts`

2. `./deploy.sh`

# How to cleanup resources in minikube?

1. `cd scripts`

2. `./cleanup.sh`

# How to interact with farmers app inside docker container deployed to minikube?

1. `export CLI_POD=$(kubectl -n farmers-market-123 get pod -l 'run==farmers-app' -o jsonpath='{.items[*].metadata.name}')`

2. `kubectl -n farmers-market-123 exec -it "$CLI_POD" bash`