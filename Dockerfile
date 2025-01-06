FROM debian:slim

RUN groupadd -r service && useradd -r -g service service
USER service:service
WORKDIR /app

COPY . .
RUN chown -R service:service /app

RUN apt-get update && \
    apt-get install -y python3-full curl openssh-server && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m venv ./.venv && \
    ./.venv/bin/pip install -r requirements.txt

EXPOSE 80
EXPOSE 22
VOLUME [ "/app" ]

CMD ["/bin/bash", "-c", "echo service:$PASSWORD | chpasswd; sshd; ./.venv/bin/watchmedo auto-restart -d=. -p=*.py -R ./.venv/bin/python run.py"]