import discord
from redbot.core import commands
from popcat_wrapper import popcat_wrapper as pop

intents = discord.Intents.default()
intents.typing = False

bot = commands.Bot(command_prefix='!', intents=intents)

class Steam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def get_steam_info(name):
        try:
            s = await pop.steam(name)
            return s
        except Exception as e:
            return None

@commands.command()
async def steam(ctx, name: str):
    steam_info = await Steam.get_steam_info(name)

    if steam_info is None:
        return await ctx.send("Application not found!")

    embed = discord.Embed(title=f"🎮・{steam_info.name}", thumbnail=steam_info.thumbnail)
    embed.add_field(name="💬┇Name", value=steam_info.name, inline=True)
    embed.add_field(name="📃┇Capital", value=steam_info.description, inline=False)
    embed.add_field(name="💻┇Developers", value=", ".join(steam_info.developers), inline=True)
    embed.add_field(name="☁┇Publishers", value=", ".join(steam_info.publishers), inline=True)
    embed.add_field(name="🪙┇Price", value=steam_info.price, inline=True)

    await ctx.send(embed=embed)