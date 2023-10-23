import discord
from redbot.core import commands
from popcat_wrapper import popcat_wrapper as pop

intents = discord.Intents.default()
intents.typing = False

bot = commands.Bot(command_prefix='!', intents=intents)

class Npm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def npm(self, ctx, name: str):
        try:
            package_info = await pop.npm(name)
        except Exception as e:
            return await ctx.send("Package not found!")

        if "name" in package_info:  # Check if 'name' key exists in the package_info dictionary
            embed = discord.Embed(title=f"📁・{package_info['name']}")
            embed.add_field(name="💬┇Name", value=package_info['name'], inline=True)
            embed.add_field(name="🏷️┇Version", value=package_info.get('version', 'N/A'), inline=True)
            embed.add_field(name="📃┇Description", value=package_info.get('description', 'N/A'), inline=True)
            embed.add_field(name="⌨️┇Keywords", value=package_info.get('keywords', 'N/A'), inline=True)
            embed.add_field(name="💻┇Author", value=package_info.get('author', 'N/A'), inline=True)
            embed.add_field(name="📁┇Downloads", value=package_info.get('downloads_this_year', 'N/A'), inline=True)
            embed.add_field(name="⏰┇Last publish", value=f"<t:{int(package_info['last_published'].timestamp())}>", inline=True)
        else:
            return await ctx.send("Package information format is not recognized.")

        await ctx.send(embed=embed)