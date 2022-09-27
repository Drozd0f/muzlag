import logging

from nextcord.ext.commands import Bot

from bot.events import users


def register_all_events(bot: Bot):
    events = []
    events.extend(users.register_events(bot))

    for event in events:
        logging.info(f"event --> {event}")
