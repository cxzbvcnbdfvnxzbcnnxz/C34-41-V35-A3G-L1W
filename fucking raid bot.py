import discord
from discord.ext import commands
from discord import app_commands
import asyncio

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
INVITE_LINK = "https://discord.gg/govsec"
GIF_URL = "https://files.catbox.moe/2p9lgx.gif"
EMBED_COLOR = 0x000000
RAID_COUNT = 5
RAID_DELAY = 0.5

RAID_MESSAGE = """# YOUR TITLE HERE
https://discord.gg/your-invite

EMBED_TITLE = "[Your Title Here](https://discord.gg/your-invite)"
EMBED_DESCRIPTION = "Your description here"
EMBED_FOOTER = "Your footer here"

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents, status=discord.Status.invisible)

context = app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
install = app_commands.allowed_installs(guilds=True, users=True)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

@bot.tree.command(name="raid", description="Send raid messages")
@context
@install
async def raid_cmd(interaction: discord.Interaction):
    embed = discord.Embed(
        title=EMBED_TITLE,
        description=EMBED_DESCRIPTION,
        color=EMBED_COLOR
    )
    
    if GIF_URL:
        embed.set_image(url=GIF_URL)
    
    if EMBED_FOOTER:
        embed.set_footer(text=EMBED_FOOTER)
    
    await interaction.response.send_message(f"### Join: {INVITE_LINK}", ephemeral=True)
    
    for _ in range(RAID_COUNT):
        await interaction.followup.send(content=RAID_MESSAGE, embed=embed)
        await asyncio.sleep(RAID_DELAY)

@bot.tree.command(name="say", description="Make the bot say something")
@context
@install
@app_commands.describe(message="The message to send")
async def say_cmd(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(f"### Join: {INVITE_LINK}", ephemeral=True)
    await interaction.followup.send(content=message)

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if interaction.response.is_done():
        return
    
    if isinstance(error, discord.Forbidden):
        await interaction.response.send_message("Bot lacks permission.", ephemeral=True)
    elif isinstance(error, discord.HTTPException):
        await interaction.response.send_message("Rate limited.", ephemeral=True)
    else:
        await interaction.response.send_message(f"Error: {error}", ephemeral=True)

if __name__ == "__main__":
    bot.run(BOT_TOKEN)
