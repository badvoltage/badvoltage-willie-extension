# coding: utf8
"""
badvoltage.py - Willie Badvoltage Module
Copyright 2014, Bruno Bord
Licensed under the WTFPL.

"""
from __future__ import unicode_literals
from datetime import datetime, date
import time

import feedparser

from willie.module import commands


def setup(bot):
    bot.memory['badvoltage'] = {'latest': None}


def configure(config):
    """
    | [badvoltage] | example | purpose |
    | ------------ | ------- | ------- |
    | rss_url      | http://example.com/rss/ | Set the RSS Feed URL |
    """
    config.interactive_add('badvoltage', 'rss_url',
                           "Set the Badvoltage RSS Feed URL",
                           default='http://www.badvoltage.org/feed/mp3/')
    config.interactive_add('badvoltage', 'utc_start', "UTC party start")
    config.interactive_add('badvoltage', 'utc_end', "UTC party end")


@commands('out')
def out(bot, trigger):
    """Is it out yet?"""
    if date.today() == bot.memory['badvoltage'].get('latest', None):
        bot.say('New episode released today!')
    elif bot.memory['badvoltage'].get('latest', None) is None:
        bot.reply("I don't know when the last one was...")
        bot.reply('Lemme check...')
        check(bot, trigger)
    else:
        bot.reply("Last time it was released was: %s"
                  % bot.memory['badvoltage'].get('latest'))


@commands('check')
def check(bot, trigger):
    """Check it out"""
    if date.today() == bot.memory['badvoltage'].get('latest', None):
        bot.say('New episode released today!')

    feed_url = bot.config.badvoltage.rss_url
    try:
        fp = feedparser.parse(feed_url)
    except IOError as e:
        bot.debug(__file__, "Can't parse feed: {0}".format(
            feed_url, str(e)), 'warning')

    status = getattr(fp, 'status', None)

    bot.debug(
        __file__,
        "{0}: status = {1}, version = '{2}', items = {3}".format(
            feed_url, status, fp.version, len(fp.entries)), 'verbose')

    # check for malformed XML
    if fp.bozo:
        bot.debug(
            __file__,
            "Got malformed feed on {0}, disabling ({1})".format(
                feed_url, fp.bozo_exception.getMessage()), 'warning')

    entry = fp.entries[0]
    # parse published and updated times into datetime objects (or None)
    entry_dt = (datetime.fromtimestamp(time.mktime(entry.published_parsed))
                if hasattr(entry, 'published_parsed') else None)
    bot.memory['badvoltage']['latest'] = entry_dt.date()
    out(bot, trigger)


def get_start_end(bot):
    utc_start = bot.config.badvoltage.utc_start
    utc_end = bot.config.badvoltage.utc_end
    return utc_start, utc_end


def public_party(bot, trigger):
    "A regular badvolter wants to know when it happens"
    if date.today() == bot.memory['badvoltage'].get('latest', None):
        utc_start, utc_end = get_start_end(bot)
        bot.reply("Today, from %s to %s UTC" % (utc_start, utc_end))
    else:
        bot.reply('Too early or too late... :(')


def private_party(bot, trigger):
    "An admin wants to set the party"
    utc_start, utc_end = get_start_end(bot)
    bot.reply("At the moment, it's set from %s to %s UTC" % (
        utc_start, utc_end))
    if trigger.group(2) is None:
        bot.reply('Incorrect. Please set start and end times')
    times = trigger.group(2).split()
    if len(times) != 2:
        bot.reply('Error! you need to provide 2 arguments.')
        bot.reply('Example: .party 4:00 6:00')
        return
    utc_start, utc_end = trigger.group(2).split()
    bot.config.badvoltage.utc_start = utc_start
    bot.config.badvoltage.utc_end = utc_end
    utc_start, utc_end = get_start_end(bot)
    bot.reply("Now, it's set from %s to %s UTC" % (utc_start, utc_end))


@commands('party')
def party(bot, trigger):
    if trigger.owner and trigger.is_privmsg:
        private_party(bot, trigger)
    else:
        public_party(bot, trigger)
