from .npm import NPM


async def setup(bot):
    await bot.add_cog(NPM(bot))