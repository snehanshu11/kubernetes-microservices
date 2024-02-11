# kubernetes Architecture 
- used https://excalidraw.com/ to draw.
- Diagram:
![kubernees](https://github.com/snehanshu11/kubernetes-microservices/assets/8538859/c6865abb-4877-42ed-94e4-c048e8ae530e)
- k8s Architecture Concepts:
  - Worker Nodes
  - Pods
  - containers
  - images
  - Master/Control plane
  - ReplicaSet
  - Deployment
  - Services
    - NodePort
    - ClusterIP
    - Loadbalancer
    
# Application Code
- Write two microservices in FASTAPI.
  - ([server.py](https://github.com/snehanshu11/kubernetes-microservices/blob/main/server/server.py)
    - A simple get request that returns item+100 value
    - Since the server is processing the request , client field is set to false and server field is set to true
    - server endpoint is exposed only to thw client
  - [client.py](https://github.com/snehanshu11/kubernetes-microservices/blob/main/client/client.py))
    - client endpoint is exposed to the public
    - client will call server endpoint to get the value
    - Since client is calling server, both client and server is set to true in teh response. 
- Run the microservices on a local machine to test that it works.
  - Add how to run using uvicorn and screenshots later
- Use of  environment variables in the code to keep it microservices decoupled
  - As we use environment varibles and don't hard code values, similarly configMaps and secrets will be used  

# Creating and uploading Docker images to ECR
- pip3 freeze -> requirements.txt
- Write a docker file for each microservices .
  - [server-dockerfile](https://github.com/snehanshu11/kubernetes-microservices/blob/main/server/Dockerfile)
  - [client-dockerfile](https://github.com/snehanshu11/kubernetes-microservices/blob/main/client/Dockerfile)
- Build docker file for each microservices and test individually
   - local bulid docker image - server.py
     ```
      sudo docker build -t server:v1 .
      sudo docker run -p 8000:8000 server:v1 &
     ```
   - local bulid docker image - client.py
     ```
      sudo docker build -t client:v1 .
      sudo docker run -p 8001:8001 client:v1 &
     ```
   - Mention steps to test
- Upload the images to ECR repository
  ``` 
    aws ecr get-login-password --region us-west-2
    sudo docker login -u AWS -p $(aws ecr get-login-password --region us-west-2) 748735308412.dkr.ecr.us-west-2.amazonaws.com
    sudo docker tag server:v1 748735308412.dkr.ecr.us-west-2.amazonaws.com/server:latest
    sudo docker push 748735308412.dkr.ecr.us-west-2.amazonaws.com/server:latest
  ```
  
# create EKS cluster
- Create a kubernetes cluster using eksctl command with two nodes 
  ```
   eksctl get cluster
   eksctl utils write-kubeconfig --cluster=<name>
   kubectl config current-context 
   eksctl create cluster --name kube-cluster --nodegroup-name ng-default --version 1.28 --node-type t2.micro --nodes 6 --region us-west-2 -clea-zones=us-west-2a,us-west-2b
  ```
-  AWS managed, 2 nodes

# create deployment/service/configmaps  file for server and cleint microservice
- Create configmap file to store the environment variable
- Create deployment and service file for server and client
- Deploy
  ```
  kubectl apply -f configMap.yaml
  kubectl apply -f server.yaml
  kubectl apply -f client.yaml
  ```
- Make sure you are able to see the environment variables on the pods
  ```
  snehanshu.suman@LT7818 kubernetes % kubectl exec -it client-deployment-64dc9f87c-9ddfj -- /bin/bash
  root@client-deployment-64dc9f87c-9ddfj:/app# env  | grep SERVER_HOST
  SERVER_HOST=server-service
  root@client-deployment-64dc9f87c-9ddfj:/app# env  | grep SERVER_PORT
  SERVER_PORT=8000
  root@client-deployment-64dc9f87c-9ddfj:/app# 

  ```
- Make sure that the communication between client and server  is happening inside the cluster so it needs to be of ClusterIP type. However the client should be exposed to outside world, so use LoadBalancer type




# Deletion/ cleanup
```
kubectl delete deployment --all
kubectl delete configmap --all 
kubectl delete service --all
eksctl delete cluster --name=kube-cluster --region=us-west-2
```

# Miscellaneous
```
kubectl config current-context 
MegaAdmin@kube-cluster.us-west-2.eksctl.io
kubectl get pods
kubectl exec -it server-deployment-5d8d8869ff-2vkcz -- /bin/bash
```

# Installing Ingress Controller - AWS Load Balancer Controller
```
$ curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.5.4/docs/install/iam_policy.json 
$ aws iam create-policy --policy-name AWSLoadBalancerControllerIAMPolicy --policy-document file://iam_policy.json
$ eksctl utils associate-iam-oidc-provider --region=us-west-2 --cluster=kube-cluster --approve
$ eksctl create iamserviceaccount \
  --cluster=kube-cluster \
  --namespace=kube-system \
  --name=aws-load-balancer-controller \
  --role-name AmazonEKSLoadBalancerControllerRole \
  --attach-policy-arn=arn:aws:iam::748735308412:policy/AWSLoadBalancerControllerIAMPolicy \
  --approve
$ kubectl apply \
    --validate=false \
    -f https://github.com/jetstack/cert-manager/releases/download/v1.13.3/cert-manager.yaml
$ curl -Lo v2_5_4_full.yaml https://github.com/kubernetes-sigs/aws-load-balancer-controller/releases/download/v2.5.4/v2_5_4_full.yaml
$ sed -i.bak -e '596,604d' ./v2_5_4_full.yaml
$ sed -i.bak -e 's|your-cluster-name|kube-cluster|' ./v2_5_4_full.yaml
$ kubectl apply -f v2_5_4_full.yaml
$ curl -Lo v2_5_4_ingclass.yaml https://github.com/kubernetes-sigs/aws-load-balancer-controller/releases/download/v2.5.4/v2_5_4_ingclass.yaml
$ kubectl apply -f v2_5_4_ingclass.yaml
$ kubectl get deployment -n kube-system aws-load-balancer-controller
``` 
