docker run --privileged -u root -d -i -t -v "/sys/fs/cgroup:/sys/fs/cgroup:ro" centos7-salt-master:latest /usr/sbin/init
