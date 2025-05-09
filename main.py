import os
import discord
from discord.ext import tasks, commands
from datetime import datetime
import pytz

TOKEN = os.environ['DISCORD_BOT_TOKEN']
CHANNEL_ID = int(os.environ['DISCORD_CHANNEL_ID'])

TIMEZONES = {
    'New York': 'America/New_York',
    'London': 'Europe/London',
    'Tokyo': 'Asia/Tokyo',
    'Sydney': 'Australia/Sydney',
}

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

message_id = None

def get_time_message():
    lines = ["🕒 **Current Time in Selected Locations:**"]
    for city, tz in TIMEZONES.items():
        now = datetime.now(pytz.timezone(tz)).strftime('%H:%M:%S')
        lines.append(f"**{city}**: {now}")
    return "\n".join(lines)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    update_time.start()

@tasks.loop(minutes=1)
async def update_time():
    global message_id
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        return

    content = get_time_message()
    if message_id is None:
        msg = await channel.send(content)
        message_id = msg.id
    else:
        try:
            msg = await channel.fetch_message(message_id)
            await msg.edit(content=content)
        except discord.NotFound:
            msg = await channel.send(content)
            message_id = msg.id

bot.run(TOKEN)
