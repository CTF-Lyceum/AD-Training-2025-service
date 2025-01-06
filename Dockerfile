FROM alpine:latest

RUN apk add --no-cache python3 py3-pip openssh
RUN addgroup -S service && adduser -S service -G service
USER service
WORKDIR /app

COPY --chown=service:service . .
RUN python3 -m venv .venv && \
    .venv/bin/pip install --no-cache-dir -r requirements.txt

EXPOSE 80
EXPOSE 22
VOLUME [ "/app" ]
ENTRYPOINT [ "entrypoint.sh" ]