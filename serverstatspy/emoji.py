import discord
from redbot.core import commands
from redbot.core import Config

class Emoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier, force_registration=True)

    @commands.command()
    @commands.guild_only()
    async def create_emojis_count_channel(self, ctx, *args):
        channelName = await self.config.guild(ctx.guild).get_template()
        channelName = channelName.replace('{emoji}', '😛')
        emoji_count = len(ctx.guild.emojis)
        channelName = channelName.replace('{name}', f'Emojis: {emoji_count or "0"}')

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(connect=False)
        }

        channel = await ctx.guild.create_voice_channel(
            name=channelName,
            overwrites=overwrites
        )

        await ctx.send("Emoji's count created!", embed=None)
