import discord
from redbot.core import commands
from redbot.core import Config

moment = datetime.now
momentTimezone = moment.timezone

class Tier(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier, force_registration=True)

    @commands.command()
    @commands.guild_only()
    async def create_tier_count_channel(self, ctx, *args):
        tier = {
            "TIER_1": "1",
            "TIER_2": "2",
            "TIER_3": "3",
            "NONE": "0",
        }

        channelName = await self.config.guild(ctx.guild).get_template()
        channelName = channelName.replace('{emoji}', '🥇')
        premium_tier = tier.get(ctx.guild.premium_tier, "0")
        channelName = channelName.replace('{name}', f'Tier: {premium_tier}')

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(connect=False)
        }

        channel = await ctx.guild.create_voice_channel(
            name=channelName,
            overwrites=overwrites
        )

        await ctx.send('Tier count created!', embed=None)

    @commands.command()
    @commands.guild_only()
    async def create_voice_channel_count_channel(self, ctx, *args):
        channelName = await self.config.guild(ctx.guild).get_template()
        channelName = channelName.replace('{emoji}', '🔊')
        voice_channel_count = sum(1 for channel in ctx.guild.voice_channels)
        channelName = channelName.replace('{name}', f'Voice Channels: {voice_channel_count or "0"}')

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(connect=False)
        }

        channel = await ctx.guild.create_voice_channel(
            name=channelName,
            overwrites=overwrites
        )

        await ctx.send('Voice channel count created!', embed=None)

    @commands.command()
    @commands.guild_only()
    async def create_time_zone_channel(self, ctx, timezone):
        if not momentTimezone.tz.zone(timezone):
            await ctx.send('Timezone is not valid', embed=None)
            return

        time_now = moment.now().tz(timezone).strftime("HH:mm (z)")

        channelName = await self.config.guild(ctx.guild).get_template()
        channelName = channelName.replace('{emoji}', '⏰')
        channelName = channelName.replace('{name}', time_now)

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(connect=False)
        }

        channel = await ctx.guild.create_voice_channel(
            name=channelName,
            overwrites=overwrites
        )

        await ctx.send('Time zone channel created!', embed=None)
