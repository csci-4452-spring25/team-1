import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
from TrafficUpdate import fetch_traffic

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
HOME = os.getenv("MY_HOME")
SCHOOL = os.getenv("SCHOOL")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} is now running!')
    traffic_update_loop.start()

@bot.command()
async def traffic(ctx, *, args: str = None):
    print("🚨 traffic command triggered")

    if args is None or " to " not in args.lower():
        await ctx.send("❗ Please use the format: `!traffic [origin] to [destination]`")
        return

    origin, destination = map(str.strip, args.split(" to ", 1))

    if origin.lower() == "home":
        origin = os.getenv("MY_HOME")
    if destination.lower() == "home":
        destination = os.getenv("MY_HOME")
    if origin.lower() == "school":
        origin = os.getenv("SCHOOL")
    if destination.lower() == "school":
        destination = os.getenv("SCHOOL")

    if not origin or not destination:
        await ctx.send("❗ One of the addresses couldn't be resolved. Check your .env values.")
        return

    data = fetch_traffic(origin, destination)
    await ctx.send(f'🚗 Traffic from {origin} to {destination}: {data}')

@tasks.loop(hours=5)
async def traffic_update_loop():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        home = os.getenv("MY_HOME")
        school = os.getenv("SCHOOL")
        data = fetch_traffic(home, school)
        await channel.send(f'🔁 Auto Traffic Update from home to school: {data}')

@bot.event
async def on_message(message):
    print(f"Received message: {message.content.encode('ascii', errors='ignore').decode()}")
    await bot.process_commands(message)

bot.run(DISCORD_TOKEN)
