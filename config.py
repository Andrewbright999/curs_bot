import os, json
from dotenv import load_dotenv 

load_dotenv() 

TG_TOKEN = os.getenv("TG_TOKEN")


with open("config.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    ADMIN_LIST = data["admins"]
    CHANNEL_ID = data["channels"]
    LESDS_FIELDS = data["leads_fields"]
