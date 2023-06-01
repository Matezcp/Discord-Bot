import nextcord
from nextcord.ext import commands
import wavelink
from wavelink.ext import spotify
import os
from dotenv import load_dotenv

load_dotenv()
intents = nextcord.Intents.all()

bot = commands.Bot(command_prefix = os.environ['bot_prefix'], intents=intents)

@bot.event
async def on_ready():
    print("Bot Ready to Use")
    print("-----------------")
    bot.loop.create_task(node_connect())

async def node_connect():
    await bot.wait_until_ready()
    await wavelink.NodePool.create_node(
        bot = bot, 
        host = os.environ['lavalink_host'], 
        port = os.environ['lavalink_port'], 
        password = os.environ['lavalink_password'],
        spotify_client = spotify.SpotifyClient(client_id=os.environ['spotify_client_id'],client_secret=os.environ['spotify_client_secret'])
    )

@bot.event
async def on_wavelink_node_ready(node: wavelink.Node):
    print(f"Node {node.identifier} is ready")

initial_extensions = []

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

if __name__ == "__main__":
    for extension in initial_extensions:
        bot.load_extension(extension)

bot.run(os.environ['bot_token'])