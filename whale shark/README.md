# whale-shark

This folder contains all the code required for the Whale Shark bot. The docker-compose / Dockerfile in the base folder can be built and ran locally or on an EC2 instance. 

## folder contents

atlantis: contains a container for Atlantis, a github based Terraform manager.
lambda-functions: contains the lambda functions to calculate word counts and respond to users. 
mnt: contains the bot code which will be a volume to the container that runs on EC2. bot.py includes functions to save data, opt-in, and opt-out. 
terraform: contains terraform which transforms all infrastructure to code, including lambda, EC2, S3, and VPC cluster. 


