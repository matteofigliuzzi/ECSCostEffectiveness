Following:
https://towardsdatascience.com/how-to-use-docker-to-deploy-a-dashboard-app-on-aws-8df5fb322708


# create requirements

conda list --export > requirements.txt

# create folder structure

# write dockerfile

# create docker image

docker build -t ecs_dashboard .

# check if dashboard runs locally

docker run -p 8080:8053 ecs_dashboard

visit 0.0.0.0:8080

