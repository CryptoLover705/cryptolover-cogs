from .cryptochannel import CryptoChannel


async def setup(bot):
    cog = CryptoChannel(bot)
    r = bot.add_cog(cog)
    if r is not None:
        await r
        await cog.initialize()