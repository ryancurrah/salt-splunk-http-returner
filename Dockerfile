FROM centos7-salt-minion:latest

MAINTAINER Ryan Currah

ENV container docker

RUN yum -y update; yum clean all

RUN yum -y install salt-master

RUN systemctl enable salt-master

RUN systemctl enable salt-minion

RUN mkdir -p /srv/salt/modules/returners

RUN mkdir -p /srv/salt/pillar

RUN mkdir -p /srv/salt/states

COPY master /etc/salt

COPY minion /etc/salt

RUN git clone https://github.com/ryancurrah/salt-apache-formula.git /srv/salt/states

RUN cp /srv/salt/states/tests/integration/defaults/states/top.sls /srv/salt/states

COPY splunk_http_returner.py /srv/salt/modules/returners