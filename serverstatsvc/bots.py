import discord
from redbot.core import commands
from redbot.core import Config

class Bots(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier, force_registration=True)

    @commands.command()
    @commands.guild_only()
    async def create_bots_count_channel(self, ctx, *args):
        members = await ctx.guild.fetch_members()

        channelName = await self.config.guild(ctx.guild).get_template()
        channelName = channelName.replace('{emoji}', '🤖')
        bot_count = sum(1 for member in members if member.bot)
        channelName = channelName.replace('{name}', f'Bots: {bot_count or "0"}')

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(connect=False)
        }

        channel = await ctx.guild.create_voice_channel(
            name=channelName,
            overwrites=overwrites
        )

        await ctx.send('Bots count created!', embed=None)
