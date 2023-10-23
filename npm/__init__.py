# Correct the import statement to point to the right location
from popcat_wrapper import npm



async def setup(bot):
    await bot.add_cog(npm(bot))