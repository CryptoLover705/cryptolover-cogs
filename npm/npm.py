import discord
from redbot.core import commands
from popcat_wrapper import popcat_wrapper as pop

intents = discord.Intents.default()
intents.typing = False

bot = commands.Bot(command_prefix='!', intents=intents)

class Npm:
    @staticmethod
    async def get_package_info(name):
        try:
            r = await pop.npm(name)
            return r
        except Exception as e:
            return None

@bot.command()
async def package_info(ctx, name: str):
    package_info = await Npm.get_package_info(name)

    if package_info is None:
        return await ctx.send("Package not found!")

    embed = discord.Embed(title=f"📁・{package_info.name}")
    embed.add_field(name="💬┇Name", value=package_info.name, inline=True)
    embed.add_field(name="🏷️┇Version", value=package_info.version, inline=True)
    embed.add_field(name="📃┇Description", value=package_info.description, inline=True)
    embed.add_field(name="⌨️┇Keywords", value=package_info.keywords, inline=True)
    embed.add_field(name="💻┇Author", value=package_info.author, inline=True)
    embed.add_field(name="📁┇Downloads", value=package_info.downloads_this_year, inline=True)
    embed.add_field(name="⏰┇Last publish", value=f"<t:{int(package_info.last_published.timestamp())}>", inline=True)

    await ctx.send(embed=embed)