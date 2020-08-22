## HTTPHops: Test Your Infrastructure with Simple N-tier Application

### About

Sometimes you need to test your container infrastructure (such as Kubernetes+Contrail cluster) to make sure it 
works properly. In this case you may deploy a simple application, such as 2- or 3-tier application.
You also want to see how tiers (or microservices) talk to each other and what path is taken.
This project provides a simple but rather universal Docker image for such tests.   


### Use case

E.g. we have

```
Gateway router -> Frontend (Tier1) -> AppLogic (Tier2) -> Backend (Tier3)
```

Here, each tier may be represented by a deployment with several containers (pods) and a k8s service performing 
load-balancing. You want to see how exactly the request propagates from Internet/Gateway all the way to backend.  

With HTTPHops, you can gain this visibility in your test setup using a single container image for all tiers. 


### Configuration

Just pass proper environment variables to tell HTTPHops where to connect to.

These variables are: 
- ADDR_LISTEN (default is 0.0.0.0, i.e. all available addresses) - IP address to listen to incoming HTTP requests;  
- PORT_LISTEN (default is 8000) - HTTP port to listen to;
- ADDR_REQUEST (default is None, i.e. do not request anything) - IP address or DNS name (such as k8s service name) to send HTTP request to;
- PORT_REQUEST (default is 80) - port to send the request.


### Example run using plain Docker 

In this example we chain 2 httphops + Apache Web server:
```shell script
sudo docker run --name httphops1 -d -p 8000:8000 -e ADDR_REQUEST=192.168.56.101 -e PORT_REQUEST=80 pklimai/httphops:latest
sudo docker run --name httphops2 -d -p 9000:9000 -e ADDR_REQUEST=172.17.0.2 -e PORT_REQUEST=8000 -e PORT_LISTEN=9000 pklimai/httphops:latest
```

Example response (from http://192.168.56.101:9000/):
```
HTTPHops server: Hostname=73fa29edab56, Server IP=172.17.0.3, Client IP=192.168.56.1
Response from the next tier:
HTTPHops server: Hostname=ecc90061ed1d, Server IP=172.17.0.2, Client IP=172.17.0.3
Response from the next tier:
I am Apache!
```

### Example using Kubernetes cluster

Two-tier application - backend deployment and service:
```
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
spec:
  selector:
    matchLabels:
      tier: backend
  replicas: 2
  template:
    metadata:
      labels:
        tier: backend
    spec:
      containers:
      - name: backend
        image: httphops:1.0
        ports:
        - containerPort: 8000
EOF

cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: backend
spec:
  ports:
  - port: 8000
    protocol: TCP
  selector:
    tier: backend
  type: ClusterIP
EOF
```

Frontend:
```
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
spec:
  selector:
    matchLabels:
      tier: frontend
  replicas: 2
  template:
    metadata:
      labels:
        tier: frontend
    spec:
      containers:
      - name: frontend
        image: httphops:1.0
        ports:
        - containerPort: 8000
        env:
        - name: ADDR_REQUEST
          value: backend
        - name: PORT_REQUEST
          value: "8000"
EOF

cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: frontend
  annotations:
    "opencontrail.org/fip-pool": "{'domain': 'default-domain', 'project': 'k8s-default', 'network': 'PUBLIC', 'name': 'PUBLIC-FIP-POOL'}"
spec:
  ports:
  - port: 8000
    protocol: TCP
  selector:
    tier: frontend
  type: LoadBalancer
EOF
```

Example response from HTTP request to public External VIP:
```
HTTPHops server: Hostname=frontend-6d4c4c9bdd-ddgc2, Server IP=10.47.255.250, Client IP=172.16.0.100 <br>
Response from the next tier: <br>
HTTPHops server: Hostname=backend-7b5595bd79-957zq, Server IP=10.47.255.247, Client IP=10.47.255.250 <br>
<br>
```


### Building and running container

To build container (from project dir):
```shell script
sudo docker build -t httphops:1.0 .
```

To save image to file / load from file:
```shell script
sudo docker save -o httphops.tar httphops:1.0
sudo docker load -i httphops.tar 
```


##### Other useful Docker commands
```shell script
sudo docker ps -a
sudo docker stop <CONTAINER>
sudo docker rm <CONTAINER>
sudo docker images
sudo docker rmi <IMAGE>
sudo docker run -it alpine:3.10 /bin/sh

```
