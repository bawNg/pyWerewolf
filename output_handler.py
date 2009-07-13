#!/usr/bin/env python

from theme_handler import ThemeHandler
from theme import WerewolfTheme

class MessageType:
    chan        = 0 #Message that will be sent to the channel
    notice_p    = 1 #Notice that will be sent to the player
    notice_c    = 2 #Notice that will be sent to the channel

class OutputStream:
    def output_message(self):
        pass

class OutputHandler:
    def __init__(self, bot):
        self.irc = bot
        self.theme_handler = ThemeHandler()
        self.theme_handler.set_theme(WerewolfTheme())

    

