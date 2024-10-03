import os
import hikari
import boto3
import awswrangler as wr
import pandas as pd
from datetime import date, datetime, timezone

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
bot = hikari.GatewayBot(token=f"{DISCORD_TOKEN}")

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")

session = boto3.Session(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, 
    region_name=AWS_REGION)
s3_client = session.client('s3', region_name=AWS_REGION)
#lambda_client = session.client('lambda', region_name=AWS_REGION)

#global variables
blacklist_channel_id = [821787611420426280] # real-talk channel
  
def get_blacklist(blacklist_name):
    BL_FILENAME = f"/opt/whale-shark/discord-bot/blacklist/{blacklist_name}"
    with open(BL_FILENAME, "r") as f:
        blacklist = f.read()
        return blacklist.split(',')

def set_blacklist(blacklist_name, data):
    BL_FILENAME = f"/opt/whale-shark/discord-bot/blacklist/{blacklist_name}"
    try:
        with open(BL_FILENAME, "w") as f:
            f.write(data)
    except Exception as e:
        error_message = "Processing another command. Try running the command again in a little bit."
        return error_message

@bot.listen(hikari.StartedEvent)
async def bot_started(event):
    print("Bot has started!")
        
@bot.listen(hikari.GuildMessageCreateEvent)
async def opt_in_out(event: hikari.GuildMessageCreateEvent) -> None:
    if event.is_bot or not event.content:
        return
    blacklist_author_id = get_blacklist("author_id")
    if event.content == "ws.opt-out":
        if str(event.author.id) in blacklist_author_id:
            await event.message.respond("You are already opted out.")
        else:
            blacklist_author_id.append(str(event.author.id))
            new_blacklist_author_id = ','.join(blacklist_author_id)
            error_message = set_blacklist("author_id", new_blacklist_author_id)
            if error_message:
                await event.message.respond(error_message)
            await event.message.respond("You have opted out.")
    if event.content == "ws.opt-in":
        if str(event.author.id) in blacklist_author_id:
            blacklist_author_id.remove(str(event.author.id))
            new_blacklist_author_id = ','.join(blacklist_author_id)
            error_message = set_blacklist("author_id", new_blacklist_author_id)
            if error_message:
                await event.message.respond(error_message)
            await event.message.respond("You have opted in.")
        else:
            await event.message.respond("You are already opted in.")


@bot.listen(hikari.GuildMessageCreateEvent)
async def ws_history(event):
    if event.content.startswith("ws.history") and event.guild_id == 973222164276867112:
        try:
            before_dt = event.content.split('.')[2]
            before_dt = datetime.strptime(before_dt, "%y/%m/%d")
            before_dt = before_dt.replace(tzinfo=timezone.utc)
            channels = await bot.rest.fetch_guild_channels(821755302780862514)
            for channel in channels:
                if isinstance(channel, hikari.channels.GuildTextChannel) and channel.id not in blacklist_channel_id:
                    await event.message.respond(f"loading for {str(channel)}, {str((channel.id))}")
                    iterator = channel.fetch_history(before=before_dt)
                    rows = []
                    async for message in iterator:
                        row = [message.channel_id, message.author.id, message.content, message.timestamp]
                        if (message.timestamp - before_dt).days < -1:
                            break
                        rows.append(row)
                    if rows:
                        df = pd.DataFrame(rows, columns = ['channel_id', 'author', 'content', 'timestamp'])
                        path1 = f"s3://whale-shark/events-v2/{before_dt}"
                        wr.s3.to_csv(df, path1, index=False, mode="append", dataset=True)
                    await event.message.respond(f"loaded {(len(rows) if rows else 0)} messages")
        except IndexError: 
            await event.message.respond("Provide one arguments before_dt - ex. ws.history.21/12/25")
        except ValueError: 
            await event.message.respond("Argument must be in the format '%y/%m/%d - ex. ws.history.21/12/25")

bot.run()
