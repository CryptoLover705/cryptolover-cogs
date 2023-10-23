import discord
from redbot.core import commands
from popcat_wrapper import popcat_wrapper as pop


intents = discord.Intents.default()
intents.typing = False

bot = commands.Bot(command_prefix='!', intents=intents)

class Steam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def steam(self, ctx, name: str):
        try:
            game_info = await pop.steam(name)
        except Exception as e:
            return await ctx.send("game not found!")

        if "name" in game_info:  # Check if 'name' key exists in the game_info dictionary
            last_published_str = game_info.get('last_published', 'N/A')
            try:
                last_published_timestamp = datetime.strptime(last_published_str, '%a %b %d %Y')
                last_published_formatted = f"<t:{int(last_published_timestamp.timestamp())}>"
            except ValueError:
                last_published_formatted = "N/A"

            embed = discord.Embed(title=f"📁・{game_info['name']}")
            embed.add_field(name="💬┇Name", value=game_info['name'], inline=True)
            embed.add_field(name="🏷️┇Version", value=game_info.get('version', 'N/A'), inline=True)
            embed.add_field(name="📃┇Description", value=game_info.get('description', 'N/A'), inline=True)
            embed.add_field(name="🏷️┇Price", value=game_info.get('price', 'N/A'), inline=True)
            embed.add_field(name="💻┇Developer", value=game_info.get('developer', 'N/A'), inline=True)
            embed.add_field(name="💻┇Publisher", value=game_info.get('publisher', 'N/A'), inline=True)
            embed.add_field(name="📁┇Downloads", value=game_info.get('downloads_this_year', 'N/A'), inline=True)
            embed.add_field(name="⏰┇Last publish", value=last_published_formatted, inline=True)
        else:
            return await ctx.send("Game is not recognized.")

        await ctx.send(embed=embed)