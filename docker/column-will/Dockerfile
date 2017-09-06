#Pull CENTOS
FROM centos

# Maintainer
# ----------
MAINTAINER mlove@columnit.com 

# Environment variables required for this build (do NOT change)
# WillHome: /opt/will
# HipchatServer: 
# Password: 
# Email: 
# V2 Token: 
# V1 Token:
# HttpServer: 8181
# LogLevel: DEBUG
# Redis: redis://localhost:6379/
# */*\*/*\*/*\*/*\*/*\*
# PLUGIN ENV Vars
# ** Jira **
# JiraServer: 
# JiraUserName:
# JiraPassword:
# ** Confluence **
# ConfluenceServer
# ConfluenceUserName:
# ConfluencePassword:

ARG WILL_BUNDLE
ENV _WILL_HOME=/opt/will

RUN mkdir -p $_WILL_HOME
RUN yum install epel-release -y && \
    yum install python python-devel python-pip python-wheel python-setuptools openssl-devel \
    git gcc -y && \
    yum clean all

ADD $WILL_BUNDLE $_WILL_HOME

WORKDIR $_WILL_HOME
RUN pip install -r requirements.dev.txt 

CMD $_WILL_HOME/start_dev_will.py
