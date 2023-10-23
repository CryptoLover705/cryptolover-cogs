import discord
from redbot.core import commands

class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def verify(self, ctx, enable: bool, channel: discord.TextChannel, role: discord.Role):
        if not ctx.author.guild_permissions.manage_messages:
            return

        if enable:
            await ctx.send("Verify panel has been successfully created", embed=self.create_embed(ctx.guild.name, channel, role))
            await self.create_verification_button(ctx, channel)

    def create_embed(self, guild_name, channel, role):
        embed = discord.Embed(
            title=f"{guild_name}・verify",
            description="Click on the button to verify yourself",
        )
        embed.add_field(name="📘┆Channel", value=f"{channel} ({channel.name})", inline=True)
        embed.add_field(name="📛┆Role", value=f"{role} ({role.name})", inline=True)
        return embed

    async def create_verification_button(self, ctx, channel):
        verify_button = discord.Button(style=discord.ButtonStyle.success, label="Verify")
        verify_action_row = discord.ActionRow(verify_button)
        await channel.send("Click the button to verify yourself.", components=[verify_action_row])
