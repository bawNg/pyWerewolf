#!/usr/bin/env python

class MessageType:
    chan        = 0 #Message that will be sent to the channel
    notice_p    = 1 #Notice that will be sent to the player
    notice_c    = 2 #Notice that will be sent to the channel

class OutputHandler:
    def __init__(self, bot):
        self.irc = bot

    

