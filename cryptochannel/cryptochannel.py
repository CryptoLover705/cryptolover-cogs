import discord
from redbot.core import commands
import aiohttp

class CryptoChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.coinpaprika_api_url = "https://api.coinpaprika.com/v1/tickers"

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

    async def create_crypto_channels(self, guild, coins_to_include):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.coinpaprika_api_url) as response:
                if response.status == 200:
                    data = await response.json()
                    category = None

                    for coin_data in data:
                        coin_id = coin_data["id"]
                        coin_name = coin_data["name"]
                        coin_symbol = coin_data["symbol"]

                        # Check if the coin should be included
                        if coin_id in coins_to_include or coin_symbol in coins_to_include:
                            price_usd = coin_data["quotes"]["USD"]["price"]
                            price_change_24h = coin_data["quotes"]["USD"]["percent_change_24h"]
                            is_price_up = price_change_24h > 0

                            # Create and configure the voice channel
                            overwrites = {
                                guild.default_role: discord.PermissionOverwrite(connect=False),
                                guild.me: discord.PermissionOverwrite(manage_channels=True, connect=True),
                            }

                            if category is None:
                                category = await guild.create_category("Price Watch", overwrites=overwrites)
                                print("Created category")  # Add this line to check if the category is created.

                            # Define channel_emoji here
                            channel_emoji = "🟢⬈" if is_price_up else "🔴⬊"

                            # Create channel name with the emoji
                            channel_name = f"🪙 {channel_emoji} {coin_symbol} Price: ${price_usd:.2f}"

                            channel = await category.create_voice_channel(channel_name, reason="Crypto Info")
                            await channel.set_permissions(
                                guild.default_role,
                                connect=False,
                                speak=False
                            )
                            await channel.edit(user_limit=0)  # No user limit
                            print(f"Created voice channel: {channel_name}")  # Add this line to check if the voice channel is created.
                else:
                    await guild.text_channels[0].send("Failed to fetch cryptocurrency data from Coinpaprika API.")

    async def delete_crypto_channels(self, guild):
        category = discord.utils.get(guild.categories, name="Price Watch")
        if category:
            for channel in category.channels:
                await channel.delete()
            await category.delete()

def setup(bot):
    bot.add_cog(CryptoChannel(bot))
