# stdlib
from datetime import datetime

# discord.py
import discord
from discord.ext import tasks

# Red-DiscordBot
from redbot.core import commands, Config, checks

# Current Plugin
import pytz
from pytz import all_timezones

__author__ = 'CryptoLover'
__version__ = '1.0.3'

channel_defaults = {
    "timezone": None,
    "time_format": "%A, %I:%M %p (%Z)"
}

class TimeZone(commands.Converter):

    async def convert(self, ctx, argument):
        if argument.title() not in all_timezones:
            raise commands.BadArgument("Couldn't find that timezone. Look for it in "
                                       "https://en.wikipedia.org/wiki/List_of_tz_database_time_zones")
        return argument

class Clock(commands.Cog):
    """Display time for timezones as voice channels"""

    def __init__(self, bot):
        self.bot = bot
        self.db = Config.get_conf(self, 675875687587, force_registration=True)
        self.db.register_channel(**channel_defaults)
        self.update_channels.start()

    async def cog_unload(self):
        self.update_channels.cancel()

    @tasks.loop(minutes=5)
    async def update_channels(self):
        channels = await self.db.all_channels()
        for channel_id in channels:
            channel = self.bot.get_channel(channel_id)
            if channel is None:
                continue

            time = channels[channel_id]["timezone"]
            time = datetime.now(pytz.timezone(time))
            fmt = channels[channel_id]["time_format"]
            try:
                time = time.strftime(fmt)
                await channel.edit(name=time)
            except Exception as e:
                print(f"Error updating channel: {e}")

    @update_channels.before_loop
    async def before_update_channels(self):
        await self.bot.wait_until_ready()

    @commands.guild_only()
    @commands.group(autohelp=True)
    async def clock(self, ctx):
        """
        Commands for creating new clocks
        """
        pass

    @clock.command()
    @checks.admin_or_permissions(manage_guild=True)
    async def create(self, ctx, timezone: TimeZone, *, format=None):
        """
        Create timezones for VoiceChannels. Wrap tz in quotes if it has spaces inside of it.
        For timezone, check out: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
        For format, check out: https://strftime.org. Default is "%A, %I:%M %p (%Z)"
        """
        # Get the guild
        guild = ctx.guild

        # Check if the category "Staff TimeZones" exists, and create it if it doesn't
        category = discord.utils.get(guild.categories, name='Staff TimeZones')
        if category is None:
            category = await guild.create_category('Staff TimeZones', reason='Initial Category Creation')

        time = datetime.now(pytz.timezone(timezone))
        try:
            time = time.strftime(format)
        except ValueError:
            return await ctx.send("That is an invalid format! "
                                "Please only use variables from https://strftime.org")
        try:
            channel = await guild.create_voice_channel(name=time, category=category)
        except Exception as e:
            await ctx.send(e)
            return
        await self.db.channel(channel).timezone.set(timezone)
        if format:
            await self.db.channel(channel).time_format.set(format)
        await ctx.send(f"Successfully created a channel with **{timezone}** timezone in the 'Staff TimeZones' category."
                    " It should be resolved on the next cycle (5 minutes)")

    @clock.command(hidden=True)
    @commands.is_owner()
    async def clear_all(self, ctx):
        await self.db.clear_all()

