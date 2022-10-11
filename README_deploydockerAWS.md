# Deploy conteinerized dashboard on AWS

Following:
- https://towardsdatascience.com/how-to-use-docker-to-deploy-a-dashboard-app-on-aws-8df5fb322708
- https://docs.aws.amazon.com/AmazonECR/latest/userguide/getting-started-cli.html

For pricing:
- https://aws.amazon.com/it/fargate/pricing/

# 1 Dockerize dashboard

### 1a create requirements

```
conda list --export > requirements.txt
```

### 1b write Dockerfile

```

```

### 1c create docker image

```
docker build -t ecs_dashboard .
```

### 1d check if dashboard runs locally

```
docker run -p 8080:8053 ecs_dashboard
```

and then visit 0.0.0.0:8080

# 2 Deploy on AWS ECS

### 2a login to AWS ECR  in region (eg: eu-south-1)

```
aws ecr get-login-password --region <region> | sudo docker login --username AWS --password-stdin <AWS_ID>.dkr.ecr.<region>.amazonaws.com
```

### 2b create ECR repo in region (eg: eu-south-1)

```
aws ecr create-repository \
    --repository-name aws_dashboard \
    --image-scanning-configuration scanOnPush=true \
    --region <region>
```

### 2c push the image to ECR

```
docker push <AWS_ID>.dkr.ecr.<region>.amazonaws.com/aws_dashboard
```

### 2d follow instructions to deploy on ECS
