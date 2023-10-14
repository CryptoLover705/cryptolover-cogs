import discord
from redbot.core import commands
from redbot.core import Config

class VoiceChannels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier, force_registration=True)

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
