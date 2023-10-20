from .clock import Clock


async def setup(bot):
    await bot.add_cog(Clock(bot))