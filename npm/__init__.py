from .npm import npm


async def setup(bot):
    await bot.add_cog(npm(bot))