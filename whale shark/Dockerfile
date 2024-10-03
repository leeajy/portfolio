FROM python:3.8

ARG DISCORD_TOKEN
ENV DISCORD_TOKEN=${DISCORD_TOKEN}

ARG AWS_ACCESS_KEY_ID
ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}

ARG AWS_SECRET_ACCESS_KEY
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}

ARG AWS_REGION
ENV AWS_REGION=${AWS_REGION}

COPY mnt/whale-shark/requirements.txt /setup/requirements.txt
RUN pip install -r /setup/requirements.txt


COPY mnt/whale-shark/discord-bot /opt/whale-shark/discord-bot
ENTRYPOINT ["python", "opt/whale-shark/discord-bot/bot.py"]
