## HTTPHops: Test Your Infrastructure with Simple N-tier Application

### About

Sometimes you need to test your container infrastructure (such as Kubernetes+Contrail cluster) to make sure it 
works properly. In this case you may deploy a simple application, such as 2- or 3-tier application.
You also want to see how tiers (or call them microservices) talk to each other and what path is taken.
This project provides a simple but rather universal Docker image for such tests.   


### Usage example

E.g. we have

```
Gateway router -> Frontend (Tier1) -> AppLogic (Tier2) -> Backend (Tier3)
```

each tier may be represented by several containers (pods) and typically 1 k8s service with load-balancing. You
want to see how exactly the request propagates from Internet/Gateway all the way to backend.  

With HTTPHops, you can use a single container image for all tiers. Just pass proper environment variables
to tell each tier where to connect to.

TODO - show configs.


### Building and running container

To build container (from project dir):  \
```shell script
sudo docker build -t pklimai/httphops:latest .
```

Example run:
```shell script
sudo docker run --name httphops1 -d -p 8000:8000 -e ADDR_REQUEST=http://192.168.56.101 pklimai/httphops:latest
```

Example response (TODO update with better example with 3-tiers)
```
HTTPHops server: Hostname=fe83c3e72567, Server IP=172.17.0.3, Client IP=192.168.56.1
Response from the next tier:
I am Apache!
```

#### Other useful Docker commands
```shell script
sudo docker ps -a
sudo docker stop <CONTAINER>
sudo docker rm <CONTAINER>
sudo docker images
sudo docker rmi <IMAGE>
sudo docker run -it alpine:3.10 /bin/sh

```
