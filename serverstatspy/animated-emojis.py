import discord
from redbot.core import commands
from redbot.core import Config

class AnimatedEmojis(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier, force_registration=True)

    @commands.command()
    @commands.guild_only()
    async def create_emoji_channel(self, ctx, *args):
        EmojiCount = 0
        Animated = 0
        OverallEmojis = 0

        for emoji in ctx.guild.emojis:
            OverallEmojis += 1
            if emoji.animated:
                Animated += 1
            else:
                EmojiCount += 1

        channelName = await self.config.guild(ctx.guild).get_template()
        channelName = channelName.replace('{emoji}', '🤡')
        channelName = channelName.replace('{name}', f'Animated Emojis: {Animated or "0"}')

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(connect=False)
        }

        channel = await ctx.guild.create_voice_channel(
            name=channelName,
            overwrites=overwrites
        )

        await ctx.send("Animated emoji's count created!", embed=None)
