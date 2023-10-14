import discord
from redbot.core import commands
from redbot.core import Config

class StaticEmoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier, force_registration=True)

    @commands.command()
    @commands.guild_only()
    async def create_static_emojis_count_channel(self, ctx, *args):
        emoji_count = 0
        animated = 0
        overall_emojis = 0

        for emoji in ctx.guild.emojis:
            overall_emojis += 1
            if emoji.animated:
                animated += 1
            else:
                emoji_count += 1

        channelName = await self.config.guild(ctx.guild).get_template()
        channelName = channelName.replace('{emoji}', '😀')
        channelName = channelName.replace('{name}', f'Static Emojis: {emoji_count or "0"}')

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(connect=False)
        }

        channel = await ctx.guild.create_voice_channel(
            name=channelName,
            overwrites=overwrites
        )

        await ctx.send('Static emoji count created!', embed=None)
