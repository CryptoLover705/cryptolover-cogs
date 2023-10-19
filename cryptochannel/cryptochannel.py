import discord
from redbot.core import commands
from discord.ext import tasks
import requests
import json
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

current_directory = os.getcwd()
json_file_path = os.path.join(current_directory, 'cryptocurrencies.json')

class CryptoChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_channels.start()
        self.enabled_cryptos = {}  # Dictionary to store enabled cryptocurrencies per server

    def cog_unload(self):
        self.update_channels.cancel()

    @tasks.loop(minutes=5)
    async def update_channels(self):
        for guild_id, enabled_cryptos in self.enabled_cryptos.items():
            guild = self.bot.get_guild(guild_id)

            if guild is None:
                continue

            category = discord.utils.get(guild.categories, name='Cryptocurrency Prices')
            if category:
                for channel in category.voice_channels:
                    await channel.delete()

            with open(json_file_path, 'r') as file:
                cryptocurrencies = json.load(file)

            category = discord.utils.get(guild.categories, name='Cryptocurrency Prices')
            if category is None:
                category = await guild.create_category('Cryptocurrency Prices', reason='Initial Category Creation')

            for crypto in cryptocurrencies:
                if crypto["symbol"] in enabled_cryptos:
                    symbol = crypto["symbol"]
                    api_endpoint = crypto["api_endpoint"]
                    url = f'https://api.coinpaprika.com/v1/tickers/{api_endpoint}'
                    response = requests.get(url)
                    data = response.json() if response.status_code == 200 else None
                    price_usd = data['quotes']['USD']['price'] if data else None
                    percent_change_24h = data['quotes']['USD']['percent_change_24h'] if data else None
                    if price_usd is not None and percent_change_24h is not None:
                        price_usd_formatted = '{:.2f}'.format(price_usd)
                        emoji = "🟢⭎" if percent_change_24h > 0 else "🔴⭏"
                        percent_change_formatted = '{:.4f}%'.format(percent_change_24h)
                        channel_name = f'{symbol}: {emoji} ${price_usd_formatted} ({percent_change_formatted})'
                        if len(channel_name) > 100:
                            channel_name = channel_name[:97] + "..."
                    else:
                        channel_name = f'{symbol}: Data Unavailable'
                    new_channel = await category.create_voice_channel(name=channel_name, reason='Initial Creation')
                    print(f'Created voice channel: {symbol}: {channel_name}')

    @update_channels.before_loop
    async def before_update_channels(self):
        await self.bot.wait_until_ready()

    @commands.command()
    async def enable(self, ctx, input_string: str):
        symbol, endpoint = input_string.split('-')
        symbol = symbol.upper()
        api_endpoint = f'{symbol.lower()}-{endpoint.lower()}'

        guild_id = ctx.guild.id
        if guild_id not in self.enabled_cryptos:
            self.enabled_cryptos[guild_id] = [1161408772888080414]

        if symbol not in self.enabled_cryptos[guild_id]:
            self.enabled_cryptos[guild_id].append(symbol)

            with open(json_file_path, 'r') as file:
                cryptocurrencies = json.load(file)

            new_crypto = {"symbol": symbol, "api_endpoint": api_endpoint}
            cryptocurrencies.append(new_crypto)

            with open(json_file_path, 'w') as file:
                json.dump(cryptocurrencies, file, indent=4)

            await ctx.send(f'Enabled {symbol}-{api_endpoint} for tracking.')
        else:
            await ctx.send(f'{symbol}-{api_endpoint} is already enabled.')

    @commands.command()
    async def disable(self, ctx, input_string: str):
        symbol, endpoint = input_string.split('-')
        symbol = symbol.upper()
        api_endpoint = f'{symbol.lower()}-{endpoint.lower()}'

        guild_id = ctx.guild.id
        if guild_id not in self.enabled_cryptos:
            self.enabled_cryptos[guild_id] = []

        if symbol in self.enabled_cryptos[guild_id]:
            self.enabled_cryptos[guild_id].remove(symbol)

            with open(json_file_path, 'r') as file:
                cryptocurrencies = json.load(file)

            updated_cryptocurrencies = [crypto for crypto in cryptocurrencies if not (crypto["symbol"] == symbol and crypto["api_endpoint"] == api_endpoint)]

            with open(json_file_path, 'w') as file:
                json.dump(updated_cryptocurrencies, file, indent=4)

            await ctx.send(f'Disabled {symbol}-{api_endpoint} from tracking.')
        else:
            await ctx.send(f'{symbol}-{api_endpoint} is not enabled.')