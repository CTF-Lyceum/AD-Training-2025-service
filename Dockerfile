FROM alpine:latest

# Commands executed by root user
RUN apk add --no-cache python3 py3-pip
RUN addgroup -S service && adduser -S service -G service

USER service
WORKDIR /app

COPY --chown=service:service . .
RUN python3 -m venv .venv && \
    .venv/bin/pip install --no-cache-dir -r requirements.txt

RUN chmod +x entrypoint.sh
ENTRYPOINT [ "/app/entrypoint.sh" ]
VOLUME [ "/app" ]

EXPOSE 80