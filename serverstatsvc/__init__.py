from .animatedemojis import AnimatedEmojis
from .boosts import Boosts
from .bots import Bots
from .channels import Channels
from .emoji import Emoji
from .members import Members
from .newschannels import NewsChannels
from .roles import Roles
from .stagechannels import StageChannels
from .staticemoji import StaticEmoji
from .textchannels import TextChannels
from .tier import Tier
from .time import Time
from .voicechannels import VoiceChannels
from redbot.core.bot import Red


async def setup(bot: Red) -> None:
    await bot.add_cog(AnimatedEmojis(bot))
    await bot.add_cog(Boosts(bot))
    await bot.add_cog(Bots(bot))
    await bot.add_cog(Channels(bot))
    await bot.add_cog(Emoji(bot))
    await bot.add_cog(Members(bot))
    await bot.add_cog(NewsChannels(bot))
    await bot.add_cog(Roles(bot))
    await bot.add_cog(StageChannels(bot))
    await bot.add_cog(StaticEmoji(bot))
    await bot.add_cog(TextChannels(bot))
    await bot.add_cog(Tier(bot))
    await bot.add_cog(Time(bot))
    await bot.add_cog(VoiceChannels(bot))


