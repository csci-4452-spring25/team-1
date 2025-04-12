terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "discord_bot" {
  ami           = "ami-0c614dee691cbbf37"  # Amazon Linux 2 (Free tier)
  instance_type = "t2.micro"
  key_name      = "my-aws-key" # Replace with your key
  subnet_id     = "subnet-02ee129fd02cdd5f2 " # Replace with your subnet
  vpc_security_group_ids = [aws_security_group.allow_ssh.id]

  user_data = <<-EOF
    #!/bin/bash
    yum update -y
    yum install -y python3 git
    cd /home/ec2-user
    git clone https://github.com/csci-4452-spring25/team-1.git
    pip3 install -r YOUR_BOT_REPO/requirements.txt
    nohup python3 YOUR_BOT_REPO/discord_bot.py > bot.log 2>&1 &
  EOF

  tags = {
    Name = "DiscordBot"
  }
}

resource "aws_security_group" "allow_ssh" {
  name        = "discord-trafficbot-sg"
  description = "Allow SSH and HTTPS"
  vpc_id      = "vpc-0e70353d11f544d95"  # Replace with your VPC ID

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

output "public_ip" {
  value = aws_instance.discord_bot.public_ip
}
