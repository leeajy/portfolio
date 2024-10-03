terraform {
  backend "s3" {
    bucket = "do-terraform-2"
    key    = "backends/ec2-instances/backend.tfstate"
    region = "us-east-2"
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.30"
    }
  }
}

data "terraform_remote_state" "do-vpc-cluster-1" {
  backend = "s3"

  config = {
    bucket = "do-terraform-2"
    key    = "backends/vpc-clusters/do-vpc-cluster-1/backend.tfstate"
    region = "us-east-2"
  }
}


resource "aws_instance" "do-webserver-1" {
  instance_type     = "t2.micro"
  ami               = "ami-051dfed8f67f095f5"
  availability_zone = "us-east-2a"
  subnet_id         = data.terraform_remote_state.do-vpc-cluster-1.outputs.do-public-subnet-1-id
  iam_instance_profile = "whale-shark-ec2"
  vpc_security_group_ids   = [data.terraform_remote_state.do-vpc-cluster-1.outputs.do-sg-1-id]
  user_data         = <<-EOF
  #!/bin/bash
  sudo yum update -y
  sudo amazon-linux-extras install docker
  sudo service docker start
  sudo usermod -a -G docker ec2-user
  sudo aws ecr get-login-password --region us-east-2 | sudo docker login --username AWS --password-stdin 913902556403.dkr.ecr.us-east-2.amazonaws.com
  sudo docker pull 913902556403.dkr.ecr.us-east-2.amazonaws.com/data-ocean:jupyter-notebook
  sudo docker run -dp 8888:8888 913902556403.dkr.ecr.us-east-2.amazonaws.com/data-ocean:jupyter-notebook
  sudo docker pull 913902556403.dkr.ecr.us-east-2.amazonaws.com/data-ocean:mina-the-penguin
  sudo docker run -d 913902556403.dkr.ecr.us-east-2.amazonaws.com/data-ocean:mina-the-penguin
  sudo docker pull 913902556403.dkr.ecr.us-east-2.amazonaws.com/data-ocean:whale-shark
  sudo docker run -d 913902556403.dkr.ecr.us-east-2.amazonaws.com/data-ocean:whale-shark
  sudo docker pull 913902556403.dkr.ecr.us-east-2.amazonaws.com/data-ocean:atlantis
  sudo docker run -dp 4041:4041 913902556403.dkr.ecr.us-east-2.amazonaws.com/data-ocean:atlantis
  EOF
  tags = {
    Name    = "do-webserver-1",
    project = "data-ocean"
  }
  key_name = "whale-shark"
}


resource "aws_instance" "do-airflow-1" {
  instance_type        = "t2.micro"
  ami                  = "ami-051dfed8f67f095f5"
  availability_zone    = "us-east-2a"
  subnet_id            = data.terraform_remote_state.do-vpc-cluster-1.outputs.do-public-subnet-2-id
  iam_instance_profile = "do-airflow-1"
  vpc_security_group_ids      = [data.terraform_remote_state.do-vpc-cluster-1.outputs.do-sg-2-id]
  user_data            = <<-EOF
  #!/bin/bash
  sudo yum update -y
  sudo amazon-linux-extras install docker
  sudo service docker start
  sudo usermod -a -G docker ec2-user
  
  # docker-compose
  sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose

  # use existing key, or create new one and replace public key in github
  # ssh-keygen -t rsa -C "leeantonio18@gmail.com"
  # ssh-add ~/.ssh/id_rsa
  # eval $(ssh-agent -s)
  
  sudo yum install git -y
  mkdir ~/airflow-v2-postgres
  cd ~/airflow-v2-postgres/
  git clone git@github.com:leeajy/data-ocean.git . 
  cd applications/airflow-v2-postgres/
  # load secrets 
  # export AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY/AWS_REGION
  
  docker-compose build
  docker-compose up -d
  EOF
  tags = {
    Name    = "do-airflow-1",
    project = "data-ocean"
  }
  key_name = "whale-shark"
}

output "do-webserver-1-ip" {
  value = aws_instance.do-webserver-1.public_ip
}

output "do-airflow-1-ip" {
  value = aws_instance.do-airflow-1.public_ip
}

