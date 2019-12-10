
## HTTPHops: Test Your Infrastructure with Simple N-tier Application

Sometimes you need to test your container infrastructure (such as Kubernetes+Contrail cluster) to make sure it 
works properly. In this case you may deploy a simple application, such as 2- or 3-tier application.
You also want to see how tiers (or call them microservices) talk to each other and what path is taken.
This project provides a simple but rather universal Docker image for such tests.   

To build container (from project dir):  \
```shell script
sudo docker build -t pklimai/httphops:latest .
sudo docker run --name httphops1 -d -p 8000:8000 pklimai/httphops:latest
```

Other useful Docker commands
```shell script
sudo docker ps -a
sudo docker stop <CONTAINER>
sudo docker rm <CONTAINER>
sudo docker images
sudo docker rmi <IMAGE>
sudo docker run -it alpine:3.10 /bin/sh

```
