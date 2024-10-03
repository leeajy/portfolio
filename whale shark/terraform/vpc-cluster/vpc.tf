resource "aws_vpc" "do-vpc-1" {
  cidr_block = "178.0.0.0/16"

  tags = {
    Name = "do-vpc-1"
  }
}


resource "aws_subnet" "do-public-subnet-1" {
  vpc_id                  = aws_vpc.do-vpc-1.id
  cidr_block              = "178.0.10.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "us-east-2a"

  tags = {
    Name = "do-public-subnet-1"
  }
}


resource "aws_subnet" "do-public-subnet-2" {
  vpc_id                  = aws_vpc.do-vpc-1.id
  cidr_block              = "178.0.20.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "us-east-2a"

  tags = {
    Name = "do-public-subnet-2"
  }
}


resource "aws_subnet" "do-public-subnet-3" {
  vpc_id                  = aws_vpc.do-vpc-1.id
  cidr_block              = "178.0.30.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "us-east-2b"

  tags = {
    Name = "do-public-subnet-3"
  }
}



resource "aws_internet_gateway" "do-igw-1" {
  vpc_id = aws_vpc.do-vpc-1.id

  tags = {
    Name = "do-igw-1"
  }
}


resource "aws_route_table" "do-public-rt-1" {
  vpc_id = aws_vpc.do-vpc-1.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.do-igw-1.id
  }

  tags = {
    Name = "do-public-rt-1"
  }
}

resource "aws_route_table_association" "do-public-rt-asso" {
  subnet_id      = aws_subnet.do-public-subnet-1.id
  route_table_id = aws_route_table.do-public-rt-1.id
}

resource "aws_route_table_association" "do-public-rt-asso-2" {
  subnet_id      = aws_subnet.do-public-subnet-2.id
  route_table_id = aws_route_table.do-public-rt-1.id
}


output "do-public-subnet-1-id" {
  value = aws_subnet.do-public-subnet-1.id
}

output "do-public-subnet-2-id" {
  value = aws_subnet.do-public-subnet-2.id
}

output "do-public-subnet-3-id" {
  value = aws_subnet.do-public-subnet-3.id
}

