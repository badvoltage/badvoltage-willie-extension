# Badvoltage extensions

This is a [Bad Voltage](http://badvoltage.org) extension for [Willie bot](http://willie.dftba.net/).

## Setup

### Dependencies

You'll need `feedparser`

### Installation

Several options:

* Put the ``badvoltage.py`` file in your ``modules`` directory, or some location where your Willie bot can load it.
* Simply checkout this repository and add its full path to your ``extra`` configuration variable.

### Configure

The bot needs to be configured. If necessary, configure it using:

    willie --configure-modules

or simply edit the default.cfg file (if you feel like it). There are only a few variables to set. For example:

    [badvoltage]
    rss_url = http://www.badvoltage.org/feed/mp3/
    utc_start = 20:00
    utc_end = 21:00

Restart your bot, or try to use the `.reload` command.

## Usage

Three commands are available:

* ``.out``: to check a new release. it basically answers the question: "Is it out yet?"
* ``.check``: it forces the check of a new release, except if we already know if the episode has already been released today.
* ``.party``: two options. Either you're the bot admin, then you may want to set the UTC start and end times. Or you're a regular badvolter, and it simply tells you when will the party happen, if it's *today*.

### Setting the UTC start/end

If you send a **private message** to the bot **and** if you are in the admin list, then you can set the UTC start and end. Like this:

    /msg voltbot .party 20:00 21:00

If you don't provide the start and the end UTC times, the command will fail.

----

## License

    badvoltage.py - Willie Badvoltage Module
    Copyright 2014, Bruno Bord
    Licensed under the terms of the WTFPL.

    DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
    Version 2, December 2004

    Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

    Everyone is permitted to copy and distribute verbatim or modified copies of this license document, and changing it is allowed as long as the name is changed.

    DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
    TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

    0. You just DO WHAT THE FUCK YOU WANT TO.
