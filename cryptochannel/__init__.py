from .cryptochannel import CryptoChannel


async def setup(bot):
    await bot.add_cog(CryptoChannel(bot))