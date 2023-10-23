import discord
from redbot.core import commands
from popcat_wrapper import popcat_wrapper as pop
from datetime import datetime

intents = discord.Intents.default()
intents.typing = False

bot = commands.Bot(command_prefix='!', intents=intents)

@commands.command()
async def steam(ctx, *, name: str):
    try:
        steam_info = await get_steam_info(name)
    except Exception as e:
        return await ctx.send("Game not found!")

    if "name" in steam_info:
        last_published_str = steam_info.get('last_published', 'N/A')
        try:
            last_published_timestamp = datetime.strptime(last_published_str, '%a %b %d %Y')
            last_published_formatted = f"<t:{int(last_published_timestamp.timestamp())}>"
        except ValueError:
            last_published_formatted = "N/A"

        embed = discord.Embed(title=f"🎮・{steam_info['name']}", thumbnail=steam_info['thumbnail'])
        embed.add_field(name="💬┇Name", value=steam_info['name'], inline=True)
        embed.add_field(name="📃┇Description", value=steam_info['description'], inline=False)
        embed.add_field(name="💻┇Developers", value=", ".join(steam_info['developers']), inline=True)
        embed.add_field(name="☁┇Publishers", value=", ".join(steam_info['publishers']), inline=True)
        embed.add_field(name="🪙┇Price", value=steam_info['price'], inline=True)
        embed.add_field(name="⏰┇Published", value=last_published_formatted, inline=True)
    else:
        return await ctx.send("Game information format is not recognized.")

    await ctx.send(embed=embed)

async def get_steam_info(name):
    try:
        s = await pop.steam(name)
        return s
    except Exception as e:
        return None