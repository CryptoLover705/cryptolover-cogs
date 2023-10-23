import discord
from redbot.core import commands
from popcat_wrapper import popcat_wrapper as pop
from datetime import datetime
import aiohttp
import requests

intents = discord.Intents.default()
intents.typing = False

bot = commands.Bot(command_prefix='!', intents=intents)

class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def npm(self, ctx, name: str):
        try:
            package_info = await pop.npm(name)
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

    # @commands.command()
    # async def steam(self, ctx, name: str):
    #     await ctx.defer()
        
    #     try:
    #         s = await pop.steam(name)
    #     except Exception as e:
    #         return await ctx.send("Application not found!", reference=ctx.message)
        
    #     embed = discord.Embed(title=f"🎮・{s.name}")
    #     embed.set_thumbnail(url=s.thumbnail)
    #     embed.add_field(name="💬┇Name", value=s.name, inline=True)
    #     embed.add_field(name="📃┇Capital", value=s.description, inline=False)
    #     embed.add_field(name="💻┇Developers", value=", ".join(s.developers), inline=True)
    #     embed.add_field(name="☁┇Publishers", value=", ".join(s.publishers), inline=True)
    #     embed.add_field(name="🪙┇Price", value=s.price, inline=True)

    #     await ctx.send(embed=embed)

    @commands.command()
    async def google(self, ctx, name: str):
        name = name.replace(" ", "+")
        link = f'https://www.google.com/search?q={name}'

        embed = discord.Embed(description=f"I have found the following for: `{name}`")
        embed.add_field(name="🔗┇Link", value=f'[Click here to see the link]({link})', inline=True)

        await ctx.send(embed=embed)

    @commands.command()
    async def duckduckgo(self, ctx, name: str):
        name = name.replace(" ", "+")
        link = f'https://duckduckgo.com/?q={name}'

        embed = discord.Embed(description=f"I have found the following for: `{name}`")
        embed.add_field(name="🔗┇Link", value=f'[Click here to see the link]({link})', inline=True)

        await ctx.send(embed=embed)

    @commands.command()
    async def bing(self, ctx, name: str):
        name = name.replace(" ", "+")
        link = f'https://www.bing.com/search?q={name}'

        embed = discord.Embed(description=f"I have found the following for: `{name}`")
        embed.add_field(name="🔗┇Link", value=f'[Click here to see the link]({link})', inline=True)

        await ctx.send(embed=embed)

    @commands.command()
    async def github(self, ctx, name: str):
        try:
            r = await pop.github(name)
        except Exception as e:
            return await ctx.send(f"No account found with the username: {name}", reference=ctx.message)

        embed = discord.Embed(title=f"🏷️・{r['name']}")
        embed.set_thumbnail(url=r['avatar'])
        embed.url = r['url']
        embed.add_field(name="💬┇Name", value=r['name'], inline=True)
        embed.add_field(name="🧑‍💼┇Company", value=r['company'], inline=True)
        embed.add_field(name="💬┇Bio", value=r['bio'], inline=True)
        embed.add_field(name="📁┇Public Repositories", value=r['public_repos'], inline=True)

        created_at = datetime.fromisoformat(r['created_at'][:-1])  # Convert created_at string to datetime
        embed.add_field(
            name="⏰┇Created At",
            value=f"<t:{int(created_at.timestamp())}>",
            inline=True,
        )

        await ctx.send(embed=embed)

    # @commands.command()
    # async def itunes(self, ctx, song: str):
    #     try:
    #         song_info = await pop.itunes(song)
    #     except Exception as e:
    #         return await ctx.send("Song not found!")

    #     song_data = await song_info
    #     if "name" in song_data:  # Check if 'name' key exists in the song_info dictionary
    #         song_name = song_data['name']
    #         artist = song_data['artist']
    #         album = song_data['album']
    #         length = song_data['length']
    #         genre = song_data['genre']
    #         price = song_data['price']
            
    #         release_date_str = song_data['release_date']
    #         try:
    #             release_date = datetime.strptime(release_date_str, '%a %b %d %Y')
    #             release_date_formatted = f"<t:{int(release_date.timestamp())}>"
    #         except ValueError:
    #             release_date_formatted = "N/A"

    #         embed = discord.Embed(title=f"🎶・{song_name}")
    #         embed.set_thumbnail(url=song_data['thumbnail'])
    #         embed.url = song_data['url']
    #         embed.add_field(name="💬┇Name", value=song_name, inline=True)
    #         embed.add_field(name="🎤┇Artist", value=artist, inline=True)
    #         embed.add_field(name="📁┇Album", value=album, inline=True)
    #         embed.add_field(name="🎼┇Length", value=length, inline=True)
    #         embed.add_field(name="🏷️┇Genre", value=genre, inline=True)
    #         embed.add_field(name="💵┇Price", value=price, inline=True)
    #         embed.add_field(name="⏰┇Release Date", value=release_date_formatted, inline=True)
    #     else:
    #         return await ctx.send("Song information format is not recognized.")

    #     await ctx.send(embed=embed)

    @commands.command()
    async def gecko(self, ctx, coin: str, currency: str):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f'https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies={currency}') as response:
                    data = await response.json()
                
                if coin not in data or currency not in data[coin]:
                    return await ctx.send("Please check your inputs!", reference=ctx.message)

                price = data[coin][currency]
                embed = discord.Embed(title="💹・Crypto stats", description=f"The current price of 1 {coin} = {price} {currency}")
                await ctx.send(embed=embed)
            except Exception as e:
                return await ctx.send("An error occurred. Please try again later.", reference=ctx.message) 