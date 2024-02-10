Architecture.
Write two microservices in FASTAPI. (server.py, client.py)
Run the microservices on a local machine to test that it works.
Use of  environment variables in the code to keep it microservices decoupled
Write a docker file for each microservices . 
Test images individually
Build docker file for each microservices
Upload the images to ECR repository
Create a kubernetes cluster using eksctl command with two nodes (aws managed)
Create configmap file to store the environment variable 
Create deployment and service file for server and client 
Make sure you are able to see the environment variables on the pods
Make sure that the communication between client and server  is happening inside the cluster so it needs to be of ClusterIP type. However the client should be exposed to outside world, so use LoadBalancer type
Test the application again.





- create server.py
- create client.py
- test on local - working
- pip3 freeze -> requirements.txt
- create dockefile - server.py
- local bulid docker image - server.py
    sudo docker build -t server:v1 .
    sudo docker run -p 8000:8000 myserver:v1 &
- push on ECR - server.py
    aws ecr get-login-password --region us-east-1
    sudo docker login -u AWS -p $(aws ecr get-login-password --region us-east-1) 748735308412.dkr.ecr.us-east-1.amazonaws.com
- create dockefile - client.py
- local bulid docker image - client.py
    sudo docker build -t myclient:v1 .
    sudo docker run -p 8001:8001 myclient:v1 &
- push on ECR - client.py
    aws ecr get-login-password --region us-east-1
    sudo docker login -u AWS -p $(aws ecr get-login-password --region us-west-2) 748735308412.dkr.ecr.us-west-2.amazonaws.com
    sudo docker tag client:v1 748735308412.dkr.ecr.us-west-2.amazonaws.com/client:latest
    sudo docker push 748735308412.dkr.ecr.us-west-2.amazonaws.com/client:latest

# create EKS Cluster
eksctl create cluster --name kube-cluster --nodegroup-name ng-default --version 1.28 --node-type t2.micro --nodes 2 --region us-west-2

# deploy images on nodes 
kubectl apply -f configMap.yaml
kubectl apply -f server.yaml
kubectl apply -f client.yaml
# Log inside a pod
kubectl get pods
kubectl exec -it server-deployment-5d8d8869ff-2vkcz -- /bin/bash

# Deletion

kubectl delete deployment --all
kubectl delete configmap --all 
kubectl delete service --all

kubectl config current-context 
MegaAdmin@kube-cluster.us-west-2.eksctl.io


snehanshu.suman@LT7818 kubernetes % kubectl exec -it client-deployment-64dc9f87c-9ddfj -- /bin/bash
 
root@client-deployment-64dc9f87c-9ddfj:/app# env  | grep SERVER_HOST
SERVER_HOST=server-service
root@client-deployment-64dc9f87c-9ddfj:/app# env  | grep SERVER_PORT
SERVER_PORT=8000
root@client-deployment-64dc9f87c-9ddfj:/app# 
