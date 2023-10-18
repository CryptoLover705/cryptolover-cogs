import discord
from redbot.core import commands
from discord.ext import tasks
import requests
import json
import os
import sys

class CryptoChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_channels.start()

        # Get the path to the directory where this script is located
        self.cog_directory = os.path.dirname(os.path.abspath(__file__))

    def cog_unload(self):
        self.update_channels.cancel()

    @tasks.loop(minutes=5)
    async def update_channels(self):
        guild = self.bot.guilds[0]
        category = discord.utils.get(guild.categories, name='Cryptocurrency Prices')
        if category:
            for channel in category.voice_channels:
                await channel.delete()

        cryptocurrencies = self.get_cryptocurrencies()

        category = discord.utils.get(guild.categories, name='Cryptocurrency Prices')
        if category is None:
            category = await guild.create_category('Cryptocurrency Prices', reason='Initial Category Creation')

        for crypto in cryptocurrencies:
            symbol = crypto["symbol"]
            api_endpoint = crypto["api_endpoint"]
            url = f'https://api.coinpaprika.com/v1/tickers/{api_endpoint}'

            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise an error if the response is not successful

                data = response.json()
                price_usd = data['quotes']['USD']['price']
                percent_change_24h = data['quotes']['USD']['percent_change_24h']

                price_usd_formatted = '{:.2f}'.format(price_usd)
                emoji = "🟢⭎" if percent_change_24h > 0 else "🔴⭏"
                percent_change_formatted = '{:.4f}%'.format(percent_change_24h)
                channel_name = f'{symbol}: {emoji} ${price_usd_formatted} ({percent_change_formatted})'
            except requests.RequestException as e:
                # Handle API request errors
                channel_name = f'{symbol}: Data Unavailable (Error: {e})'
            except json.JSONDecodeError as e:
                # Handle JSON decoding errors
                channel_name = f'{symbol}: Data Unavailable (Error: {e})'

            new_channel = await category.create_voice_channel(name=channel_name, reason='Initial Creation')
            print(f'Created voice channel: {symbol}: {channel_name}')

    @update_channels.before_loop
    async def before_update_channels(self):
        await self.bot.wait_until_ready()

    def get_cryptocurrencies(self):
        # Use os.path.join to construct the full path to cryptocurrencies.json
        json_path = os.path.join(self.cog_directory, 'cryptocurrencies.json')
        try:
            with open(json_path, 'r') as file:
                cryptocurrencies = json.load(file)
        except FileNotFoundError:
            # Handle the case where cryptocurrencies.json doesn't exist
            cryptocurrencies = []

        return cryptocurrencies

    @commands.command()
    async def enable(self, ctx, input_string: str):
        try:
            symbol, endpoint = input_string.split('-')
            symbol = symbol.upper()
            api_endpoint = f'{symbol.lower()}-{endpoint.lower()}'

            cryptocurrencies = self.get_cryptocurrencies()
            json_path = os.path.join(self.cog_directory, 'cryptocurrencies.json')

            response = requests.get(f'https://api.coinpaprika.com/v1/tickers/{api_endpoint}')
            response.raise_for_status()  # Raise an error if the response is not successful

            data = response.json()
            price_usd = data['quotes']['USD']['price']
            percent_change_24h = data['quotes']['USD']['percent_change_24h']

            price_usd_formatted = '{:.2f}'.format(price_usd)
            emoji = "🟢⭎" if percent_change_24h > 0 else "🔴⭏"
            percent_change_formatted = '{:.4f}%'.format(percent_change_24h)
            channel_name = f'{symbol}: {emoji} ${price_usd_formatted} ({percent_change_formatted})'

            new_crypto = {"symbol": symbol, "api_endpoint": api_endpoint}
            cryptocurrencies.append(new_crypto)

            with open(json_path, 'w') as file:
                json.dump(cryptocurrencies, file, indent=4)

            await ctx.send(f'Enabled {symbol}-{api_endpoint} for tracking')
        except (ValueError, requests.RequestException, json.JSONDecodeError) as e:
            # Handle and log any exceptions that occur
            print(f"An error occurred while enabling: {e}")
            await ctx.send('An error occurred while enabling the cryptocurrency.')

    @commands.command()
    async def disable(self, ctx, input_string: str):
        try:
            symbol, endpoint = input_string.split('-')
            symbol = symbol.upper()
            api_endpoint = f'{symbol.lower()}-{endpoint.lower()}'

            cryptocurrencies = self.get_cryptocurrencies()
            json_path = os.path.join(self.cog_directory, 'cryptocurrencies.json')

            updated_cryptocurrencies = [crypto for crypto in cryptocurrencies if not (crypto["symbol"] == symbol and crypto["api_endpoint"] == api_endpoint)]

            with open(json_path, 'w') as file:
                json.dump(updated_cryptocurrencies, file, indent=4)

            await ctx.send(f'Disabled {symbol}-{api_endpoint} from tracking')
        except ValueError:
            # Handle the case where the input format is invalid
            await ctx.send('Invalid input format. Please use symbol-endpoint format.')

    @commands.command()
    async def cryptoreload(self, ctx, extension):
        try:
            if extension not in self.bot.extensions:
                self.bot.load_extension(extension)
            else:
                self.bot.reload_extension(extension)
            await ctx.send(f"Reloaded extension: {extension}")
        except commands.ExtensionError as error:
            await ctx.send(f"Failed to reload extension {extension}: {error}")
