import discord
from redbot.core import commands
from redbot.core import Config
import moment
import moment.timezone as momentTimezone

class Time(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier, force_registration=True)

    @commands.command()
    @commands.guild_only()
    async def create_time_zone_channel(self, ctx, timezone):
        if not momentTimezone.tz.zone(timezone):
            await ctx.send('Timezone is not valid', embed=None)
            return

        time_now = moment.now().tz(timezone).format("HH:mm (z)")

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
