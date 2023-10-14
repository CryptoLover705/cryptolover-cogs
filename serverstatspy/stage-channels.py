import discord
from redbot.core import commands
from redbot.core import Config

class StageChannels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier, force_registration=True)

    @commands.command()
    @commands.guild_only()
    async def create_stage_channels_count_channel(self, ctx, *args):
        channelName = await self.config.guild(ctx.guild).get_template()
        channelName = channelName.replace('{emoji}', '🎤')
        stage_channels_count = sum(1 for channel in ctx.guild.voice_channels if isinstance(channel, discord.StageChannel))
        channelName = channelName.replace('{name}', f'Stage Channels: {stage_channels_count or "0"}')

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(connect=False)
        }

        channel = await ctx.guild.create_voice_channel(
            name=channelName,
            overwrites=overwrites
        )

        await ctx.send('Stage channel count created!', embed=None)
