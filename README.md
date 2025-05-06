# pyMail

Simple app that receives email on port 25 via SMTP and sends the email out to a Discord channel via Webhook.

Dockerfile provided and pre-built in Dockerhub

Can be run with the below command:
```
docker run --name pymail -p 25:25 -e WEBHOOK_URI=https://examplewebhook boximus/pymail:latest