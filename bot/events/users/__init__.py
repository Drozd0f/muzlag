from nextcord.ext.commands import Bot

from bot.events.users.play import play


def register_events(bot: Bot):
    events = []
    events.append(bot.event(play(bot)).__name__)
    return events
