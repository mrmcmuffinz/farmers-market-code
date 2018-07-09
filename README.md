# farmers-market-code

# Pre Requisites?

1. docker

2. minikube

# How to build dockerfile?

1. Run docker build command.

command: `docker build . -f Dockerfile -t farmers-market:1.1.5`

# How to deploy code?

1. `cd scripts`

2. `./deploy.sh`

# How to add items to farmers inventory?

1. Get the pods in the farmers namespace

command: kubectl -n farmers-market-123 get pods

2. Exec into the farmers pod.

command: `kubectl -n farmers-market-123 exec -it farmers-app-646ccd6cbf-6n4vm bash`

3. Run the farmers cli inventory add command.

##### Examples:

```
farmers add --code="AP1" --name="Apples" --price=6.00
farmers add --code="CF1" --name="Coffee" --price=11.23
farmers add --code="CH1" --name="Chai" --price=3.11
farmers add --code="MK1" --name="Milk" --price=4.75
farmers add --code="MK1" --name="Oatmeal" --price=3.69
```
