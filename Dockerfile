FROM alpine:latest

RUN addgroup -S service && adduser -S service -G service
USER service
WORKDIR /app

COPY --chown=service:service . .
RUN apk add --no-cache python3 py3-pip openssh
RUN python3 -m venv .venv && \
    .venv/bin/pip install --no-cache-dir -r requirements.txt

EXPOSE 80
EXPOSE 22
VOLUME [ "/app" ]

CMD ["/bin/sh", "-c", "echo service:$PASSWORD | chpasswd; sshd; ./.venv/bin/watchmedo auto-restart -d=. -p=*.py -R ./.venv/bin/python run.py"]