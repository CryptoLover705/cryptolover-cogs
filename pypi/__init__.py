from .pypi import Pypi


async def setup(bot):
    await bot.add_cog(Pypi(bot))