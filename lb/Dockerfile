FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

# Install ca-certificates first (using HTTP, which works with network: host during build)
RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Switch to HTTPS repos for runtime (containers will be able to use apt-get at runtime)
RUN sed -i 's|http://archive.ubuntu.com|https://archive.ubuntu.com|g' /etc/apt/sources.list.d/ubuntu.sources && \
    sed -i 's|http://security.ubuntu.com|https://security.ubuntu.com|g' /etc/apt/sources.list.d/ubuntu.sources

# Install remaining packages
RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends \
        openssh-server sudo iputils-ping \
        nano curl wget net-tools vim-tiny && \
    mkdir /run/sshd && \
    if ! id -u ubuntu >/dev/null 2>&1; then \
        useradd --create-home --uid 1000 --shell /bin/bash ubuntu; \
    fi && \
    echo 'ubuntu:pass123' | chpasswd && \
    usermod -aG sudo ubuntu && \
    sed -ri 's/#?PermitRootLogin.*/PermitRootLogin no/'  /etc/ssh/sshd_config && \
    sed -ri 's/#?PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN ssh-keygen -A
CMD ["/usr/sbin/sshd","-D"]
