"""Copyright (c) <2016> <Lance Zukel>
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


import os
import boto3

# AWS_ACCESS_KEY_ID AND AWS_SECRET_ACCESS_KEY ARE BOTH STORED AS ENVIRONMENT VARIABLES
# THIS ALLOWS US TO CALL THESE VALUES WITHOUT GIVING OUT VITAL DATA
os.environ["AWS_ACCESS_KEY_ID"]
os.environ["AWS_SECRET_ACCESS_KEY"]
os.environ["AWS_DEFAULT_REGION"] = "us-west-2"


#Bash commands for installing elk stack
userdata = """#!/bin/bash
sudo su
cd ~
wget --no-cookies --no-check-certificate --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie" "http://download.oracle.com/otn-pub/java/jdk/8u73-b02/jdk-8u73-linux-x64.rpm"
yum -y localinstall jdk-8u73-linux-x64.rpm
rpm --import http://packages.elastic.co/GPG-KEY-elasticsearch
#create new repo for elasticsearch
wget -O /etc/yum.repos.d 'https://github.com/lanerjo/aws_ELK_stack_launcher/blob/master/elasticsearch.repo' #edit me with the github repo file 

#install elastic search
yum -y install elasticsearch
#edit elasticsearch config
sed -i '$network.host: localhost' /etc/elasticsearch/elasticsearch.yml 

service start elasticsearch
service enable elasticsearch
#kibana
#add kibana repo
wget -O /etc/yum.repos.d 'https://github.com/lanerjo/aws_ELK_stack_launcher/blob/master/kibana.repo' #edit me with the github repo file 
#install kibana
yum -y install kibana
#edit kibana config
sed -i '$server.host: "localhost"' /opt/kibana/config/

#start kibana
service start kibana
#install logstash

#add logstash repo
wget -O /etc/yum.repos.d 'https://github.com/lanerjo/aws_ELK_stack_launcher/blob/master/logstash.repo' #edit me with the github repo file 
#install logstash
yum -y install logstash
service start logstash
"""

#creating the ec2 instance on AWS using a predefined security group, t2 micro size, and amazon linux machine image
ec2 = boto3.resource('ec2')
instances = ec2.create_instances(
    ImageId='ami-7172b611',
    InstanceType='t2.micro',
    KeyName='AWS_Testing',
    MinCount=1,
    MaxCount=1,
    SecurityGroupIds=['Jenkins'],
    UserData=userdata
)

#start the instance and print to command instance id, state, public dns, public ip
for instance in instances:
    print("Waiting until running...")
    instance.wait_until_running()
    instance.reload()
    print((instance.id, instance.state, instance.public_dns_name,
instance.public_ip_address))