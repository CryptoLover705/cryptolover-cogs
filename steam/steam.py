import discord
from redbot.core import commands
from popcat_wrapper import popcat_wrapper as pop
from datetime import datetime

intents = discord.Intents.default()
intents.typing = False

bot = commands.Bot(command_prefix='!', intents=intents)

class Steam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def steam(self, ctx, name: str):
        try:
            steam_info = await pop.steam(name)
        except Exception as e:
            return await ctx.send("Package not found!")

        if "name" in steam_info:  # Check if 'name' key exists in the package_info dictionary
            last_published_str = steam_info.get('last_published', 'N/A')
            try:
                last_published_timestamp = datetime.strptime(last_published_str, '%a %b %d %Y')
                last_published_formatted = f"<t:{int(last_published_timestamp.timestamp())}>"
            except ValueError:
                last_published_formatted = "N/A"

            embed = discord.Embed(title=f"🎮・{steam_info.name}", thumbnail=steam_info.thumbnail)
            embed.add_field(name="💬┇Name", value=steam_info.name, inline=True)
            embed.add_field(name="📃┇Capital", value=steam_info.description, inline=False)
            embed.add_field(name="💻┇Developers", value=", ".join(steam_info.developers), inline=True)
            embed.add_field(name="☁┇Publishers", value=", ".join(steam_info.publishers), inline=True)
            embed.add_field(name="🪙┇Price", value=steam_info.price, inline=True)
            embed.add_field(name="⏰┇Published", value=last_published_formatted, inline=True)
        else:
            return await ctx.send("Package information format is not recognized.")

        await ctx.send(embed=embed)