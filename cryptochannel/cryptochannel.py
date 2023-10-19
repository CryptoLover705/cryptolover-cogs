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
servers_json_file = os.path.join(current_directory, 'servers.json')

class CryptoChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_channels.start()
        self.enabled_cryptos = {}  # Dictionary to store enabled cryptocurrencies per server
        self.guild_ids = load_server_ids()  # Load server IDs from servers.json

    def cog_unload(self):
        self.update_channels.cancel()

    @tasks.loop(minutes=5)
    async def update_channels(self):
        for guild_id, enabled_cryptos in self.enabled_cryptos.items():
            guild = self.bot.get_guild(guild_id)

            if guild is None:
                continue

            category = discord.utils.get(guild.categories, name='Cryptocurrency Prices')
            if category is None:
                category = await guild.create_category('Cryptocurrency Prices', reason='Initial Category Creation')

            with open(json_file_path, 'r') as file:
                cryptocurrencies = json.load(file)

            for crypto in cryptocurrencies:
                if crypto["symbol"] in enabled_cryptos:
                    symbol = crypto["symbol"]
                    api_endpoint = crypto["api_endpoint"]
                    url = f'https://api.coinpaprika.com/v1/tickers/{api_endpoint}'
                    response = requests.get(url)
                    data = response.json() if response.status_code == 200 else None
                    if data:
                        price_usd = data['quotes']['USD']['price']
                        percent_change_24h = data['quotes']['USD']['percent_change_24h']
                        price_usd_formatted = '{:.2f}'.format(price_usd)
                        emoji = "🟢⭎" if percent_change_24h > 0 else "🔴⭏"
                        channel_name = f'{symbol}: {emoji} ${price_usd_formatted}'
                        if len(channel_name) > 100:
                            channel_name = channel_name[:97] + "..."
                    else:
                        channel_name = f'{symbol}: Data Unavailable'

                    # Check if the channel already exists
                    existing_channel = discord.utils.get(category.voice_channels, name=channel_name)
                    if existing_channel:
                        await existing_channel.edit(name=channel_name, reason='Update Channel')
                        print(f'Updated voice channel: {symbol}: {channel_name}')
                    else:
                        new_channel = await category.create_voice_channel(name=channel_name, reason='Initial Creation')
                        print(f'Created voice channel: {symbol}: {channel_name}')

    @update_channels.before_loop
    async def before_update_channels(self):
        await self.bot.wait_until_ready()

    @commands.command()
    async def assign_server(self, ctx):
    # Store the Guild ID for this server
        guild_id = ctx.guild.id
        self.guild_ids.append({"guild_id": str(guild_id)})
        await ctx.send(f'Assigned this server to Guild ID: {ctx.guild.id}')

        # Save the server IDs to servers.json
        save_server_ids(self.guild_ids)

    @commands.command()
    async def enable(self, ctx, input_string: str):
        if "-" in input_string:
            symbol, endpoint = input_string.split('-', 1)  # Use 'split' with maxsplit parameter to avoid splitting on additional hyphens
            symbol = symbol.upper()
            api_endpoint = f'{symbol.lower()}-{endpoint.lower()}'

            # Get the guild ID
            guild_id = ctx.guild.id

            # Load the server data from servers.json
            server_data = load_server_ids()

            # Check if the guild is already in the server data
            if guild_id not in server_data:
                server_data[guild_id] = {
                    "enabled_currencies": []
                }

            # Check if the symbol is not already enabled for this guild
            if symbol not in server_data[guild_id]["enabled_currencies"]:
                server_data[guild_id]["enabled_currencies"].append(symbol)

                # Save the updated server data back to servers.json
                save_server_ids(server_data)

                with open(json_file_path, 'r') as file:
                    cryptocurrencies = json.load(file)

                new_crypto = {"symbol": symbol, "api_endpoint": api_endpoint}
                cryptocurrencies.append(new_crypto)

                with open(json_file_path, 'w') as file:
                    json.dump(cryptocurrencies, file, indent=4)

                await ctx.send(f'Enabled {symbol}-{api_endpoint} for tracking.')
            else:
                await ctx.send(f'{symbol}-{api_endpoint} is already enabled.')
        else:
            await ctx.send("Invalid input format. Use 'enable symbol-endpoint.'")

    @commands.command()
    async def disable(self, ctx, input_string: str):
        if "-" in input_string:
            symbol, endpoint = input_string.split('-', 1)
            symbol = symbol.upper()
            api_endpoint = f'{symbol.lower()}-{endpoint.lower()}'

            # Get the guild ID
            guild_id = ctx.guild.id

            # Load the server data from servers.json
            server_data = load_server_ids()

            if guild_id in server_data and symbol in server_data[guild_id]["enabled_currencies"]:
                server_data[guild_id]["enabled_currencies"].remove(symbol)

                # Save the updated server data back to servers.json
                save_server_ids(server_data)

                with open(json_file_path, 'r') as file:
                    cryptocurrencies = json.load(file)

                updated_cryptocurrencies = [crypto for crypto in cryptocurrencies if not (crypto["symbol"] == symbol and crypto["api_endpoint"] == api_endpoint)]

                with open(json_file_path, 'w') as file:
                    json.dump(updated_cryptocurrencies, file, indent=4)

                await ctx.send(f'Disabled {symbol}-{api_endpoint} from tracking.')
            else:
                await ctx.send(f'{symbol}-{api_endpoint} is not enabled for this server.')
        else:
            await ctx.send("Invalid input format. Use 'disable symbol-endpoint.'")

# Add these two functions for saving and loading server IDs

def save_server_ids(guild_ids):
    with open(servers_json_file, 'w') as file:
        json.dump(guild_ids, file, indent=4)

def load_server_ids():
    if os.path.exists(servers_json_file):
        with open(servers_json_file, 'r') as file:
            server_data = json.load(file)
            return server_data
    return []

bot.add_cog(CryptoChannel(bot))
