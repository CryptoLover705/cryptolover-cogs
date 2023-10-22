from .npm import Npm


async def setup(bot):
    await bot.add_cog(Npm(bot))