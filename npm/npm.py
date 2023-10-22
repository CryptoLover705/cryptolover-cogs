import discord
from redbot.core import commands
import popcat_wrapper

intents = discord.Intents.default()  # Create a default set of intents
intents.typing = False  # You can adjust the intents as needed

bot = commands.Bot(command_prefix='!')


@bot.command()
async def package_info(ctx, name: str):
    try:
        r = await popcat_wrapper.npm(name)
    except Exception as e:
        return await ctx.send("Package not found!")

    embed = discord.Embed(title=f"📁・{r.name}")
    embed.add_field(name="💬┇Name", value=r.name, inline=True)
    embed.add_field(name="🏷️┇Version", value=r.version, inline=True)
    embed.add_field(name="📃┇Description", value=r.description, inline=True)
    embed.add_field(name="⌨️┇Keywords", value=r.keywords, inline=True)
    embed.add_field(name="💻┇Author", value=r.author, inline=True)
    embed.add_field(name="📁┇Downloads", value=r.downloads_this_year, inline=True)
    embed.add_field(name="⏰┇Last publish", value=f"<t:{int(r.last_published.timestamp())}>", inline=True)

    await ctx.send(embed=embed)


