import discord
from redbot.core import commands
from redbot.core import Config

class TextChannels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier, force_registration=True)

    @commands.command()
    @commands.guild_only()
    async def create_text_channel_count_channel(self, ctx, *args):
        channelName = await self.config.guild(ctx.guild).get_template()
        channelName = channelName.replace('{emoji}', '💬')
        text_channel_count = sum(1 for channel in ctx.guild.channels if isinstance(channel, discord.TextChannel))
        channelName = channelName.replace('{name}', f'Text Channels: {text_channel_count or "0"}')

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(connect=False)
        }

        channel = await ctx.guild.create_voice_channel(
            name=channelName,
            overwrites=overwrites
        )

        await ctx.send('Text channel count created!', embed=None)
