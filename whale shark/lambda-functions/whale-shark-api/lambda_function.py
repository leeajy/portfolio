import json
import requests
import os

def lambda_handler(event, context):
    ws_application_id=os.getenv('ws_application_id')
    ws_bot_token=os.getenv('ws_bot_token')
    
    crud_operation = event.get("crud_operation", "").lower()
    url = event.get("url", None)
    
    # authorization
    headers = {
        "Authorization": f"Bot {ws_bot_token}"
    }
    if url == "globalappcmd":
        command_id = event.get("command_id", )
        url = f"https://discord.com/api/v10/applications/{ws_application_id}/commands/{command_id}"
    elif url == "globalappcmds":
        url = f"https://discord.com/api/v10/applications/{ws_application_id}/commands"
    elif url == "guildcommand":
        url = f"https://discord.com/api/v10/applications/{ws_application_id}/guilds/{guild_id}/commands"
    else:
        url = None
    if crud_operation == "delete":
        r = requests.delete(url, headers=headers)
    elif crud_operation == "get":
        r = requests.get(url, headers=headers)
    elif crud_operation == "post":
        json = event.get("json", {})
        r = requests.post(url, headers=headers, json=json)
    
    print(r)
    print(r.status_code)
    print(r.text)
