import discord
from redbot.core import commands
from popcat_wrapper import popcat_wrapper as pop
from datetime import datetime

intents = discord.Intents.default()
intents.typing = False

bot = commands.Bot(command_prefix='!', intents=intents)

class Pypi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pypi(self, ctx, name: str):
        try:
            package_info = await pop.pypi(name)
        except Exception as e:
            return await ctx.send("Package not found!")

        if "name" in package_info:  # Check if 'name' key exists in the package_info dictionary
            last_published_str = package_info.get('last_published', 'N/A')
            try:
                last_published_timestamp = datetime.strptime(last_published_str, '%a %b %d %Y')
                last_published_formatted = f"<t:{int(last_published_timestamp.timestamp())}>"
            except ValueError:
                last_published_formatted = "N/A"

            embed = discord.Embed(title=f"📁・{package_info['name']}")
            embed.add_field(name="💬┇Name", value=package_info['name'], inline=True)
            embed.add_field(name="🏷️┇Version", value=package_info.get('version', 'N/A'), inline=True)
            embed.add_field(name="📃┇Description", value=package_info.get('description', 'N/A'), inline=True)
            embed.add_field(name="⌨️┇Keywords", value=package_info.get('keywords', 'N/A'), inline=True)
            embed.add_field(name="💻┇Author", value=package_info.get('author', 'N/A'), inline=True)
            embed.add_field(name="📁┇Downloads", value=package_info.get('downloads_this_year', 'N/A'), inline=True)
            embed.add_field(name="⏰┇Last publish", value=last_published_formatted, inline=True)
        else:
            return await ctx.send("Package information format is not recognized.")

        await ctx.send(embed=embed)