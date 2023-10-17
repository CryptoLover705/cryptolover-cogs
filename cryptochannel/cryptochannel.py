import discord
from redbot.core import commands
import aiohttp
import asyncio
import requests

class CryptoChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.coinpaprika_api_url = "https://api.coinpaprika.com/v1/tickers/{coin_id}"
        self.voice_channels = {}  

    @commands.Cog.listener()
    async def on_ready(self):
        while True:
            await self.update_channel_names()
            await asyncio.sleep(900)  

    async def update_channel_names(self):
        original_coin_id = "cds-crypto-development-services"
        url = f"https://api.coinpaprika.com/v1/tickers/{original_coin_id}"

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            symbol = data['symbol']
            price_change_24h = data["quotes"]["USD"]["percent_change_24h"]
            name = await self.get_channel_name_with_emoji(symbol, price_change_24h)
            await self.rename_crypto_channel(symbol, name)
        else:
            print("Failed to fetch data from CoinPaprika API.")

    async def get_channel_name_with_emoji(self, coin_id, price_change_24h):
        emoji = "🟢" if price_change_24h > 0 else "🔴"
        return f"{emoji} {coin_id} Price: N/A"

    async def rename_crypto_channel(self, coin_id, name):
        if coin_id in self.voice_channels:
            channel = self.voice_channels[coin_id]
            await channel.edit(name=name, reason="Crypto Info Update")

    @commands.command()
    async def cryptochannel(self, ctx, action: str, *coins_to_include: str):
        if action == "enable":
            if not coins_to_include:
                await ctx.send("You need to specify at least one cryptocurrency symbol or ID to include.")
                return
            await self.create_crypto_channels(ctx.guild, coins_to_include)
            await ctx.send("Crypto info voice channels have been enabled for the specified coins.")
        elif action == "disable":
            await self.delete_crypto_channels(ctx.guild)
            await ctx.send("Crypto info voice channels have been disabled.")
        else:
            await ctx.send("Invalid action. Use 'enable' or 'disable'.")

    @commands.command(name="cryptolist")
    async def _cryptochannel_list(self, ctx):
        enabled_channels = list(self.voice_channels.keys())
        if enabled_channels:
            enabled_channels_list = "\n".join(enabled_channels)
            await ctx.send(f"Enabled cryptocurrency info voice channels:\n{enabled_channels_list}")
        else:
            await ctx.send("No cryptocurrency info voice channels are currently enabled.")

    @commands.command(name="togglechannel")
    async def _cryptochannel_togglechannel(self, ctx, coin: str, enabled: Optional[bool] = None):
        coin = coin.lower()
        if enabled is None:
            enabled = not self.voice_channels.get(coin)
        
        if enabled:
            if coin not in self.voice_channels:
                await self.create_crypto_channels(ctx.guild, [coin])
            await ctx.send(f"Crypto info voice channel for {coin} has been enabled.")
        else:
            if coin in self.voice_channels:
                await self.delete_crypto_channel(ctx.guild, coin)
                await ctx.send(f"Crypto info voice channel for {coin} has been disabled.")
            else:
                await ctx.send(f"Crypto info voice channel for {coin} is not currently enabled.")

    @commands.command(name="name")
    async def _cryptochannel_name(self, ctx, coin: str, *, name=None):
        coin = coin.lower()
        
        if name is None:
            if coin in self.voice_channels:
                default_name = await self.get_default_channel_name(coin)
                await self.rename_crypto_channel(ctx.guild, coin, default_name)
                await ctx.send(f"Name of the {coin} info voice channel has been reset to the default.")
            else:
                await ctx.send(f"The {coin} info voice channel is not currently enabled.")
        else:
            await self.rename_crypto_channel(ctx.guild, coin, name)
            await ctx.send(f"Name of the {coin} info voice channel has been updated.")

    async def create_crypto_channels(self, guild, coins_to_include):
        category = discord.utils.get(guild.categories, name="Crypto Channels")
        if not category:
            category = await guild.create_category("Crypto Channels")  

        for coin_symbol in coins_to_include:
            if coin_symbol in self.voice_channels:
                await self.delete_crypto_channel(guild, coin_symbol)
            channel = await guild.create_voice_channel(coin_symbol, category=category, user_limit=0)
            self.voice_channels[coin_symbol] = channel

    async def delete_crypto_channels(self, guild):
        for coin_symbol in self.voice_channels:
            await self.delete_crypto_channel(guild, coin_symbol)

    async def delete_crypto_channel(self, guild, coin):
        if coin in self.voice_channels:
            channel = self.voice_channels.pop(coin)
            await channel.delete()
    
    async def get_default_channel_name(self, coin):
        return f"🪙 {coin} Price: N/A"

def setup(bot):
    bot.add_cog(CryptoChannel(bot))
