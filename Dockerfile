FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DEBIAN_FRONTEND=noninteractive \
    PORT=8080

# Enable non-free components for unrar
RUN echo "deb http://deb.debian.org/debian trixie main contrib non-free non-free-firmware" > /etc/apt/sources.list.d/debian.sources && \
    echo "deb http://deb.debian.org/debian trixie-updates main contrib non-free non-free-firmware" >> /etc/apt/sources.list.d/debian.sources && \
    echo "deb http://security.debian.org/debian-security trixie-security main contrib non-free non-free-firmware" >> /etc/apt/sources.list.d/debian.sources

RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    git \
    ffmpeg \
    unzip \
    unrar \
    p7zip-full \
    procps \
    net-tools \
    ca-certificates \
    aria2 \
    && rm -rf /var/lib/apt/lists/*

RUN curl -O https://downloads.rclone.org/rclone-current-linux-amd64.zip \
    && unzip rclone-current-linux-amd64.zip \
    && cd rclone-*-linux-amd64 \
    && cp rclone /usr/local/bin/ \
    && chmod 755 /usr/local/bin/rclone \
    && cd .. && rm -rf rclone-*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p downloads encode thumbnails config sessions data/logs \
    && chmod -R 755 /app

COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

EXPOSE 8080

CMD ["/bin/bash", "/app/start.sh"]
