#!/usr/bin/env python

from theme import Theme
from player import Role
import copy

class Tokens:
    #the tokens that get replaced by data
    replace_char = '$' #character tokens are prepended with
    replace = ["bot", "num", "user", "target", "votes", "roles", "alive"]

class ThemeHandler:
    def __init__(self):
        self.theme = Theme()

    def set_theme(self, theme):
        self.theme = theme

    def get_message(self, type, subtype, role=Role.noone, **args):
        #get the message
        message = copy.deepcopy(self.theme.get_message(type, subtype, role))

        #replace tokens
        for i in xrange(len(message)):
            text = message[i][1]
            for token in Tokens.replace:
                if text.find(Tokens.replace_char+token) != -1:
                    #check and see if token has input if not don't replace
                    if token in args:
                        text = text.replace(Tokens.replace_char+token, args[token])
            message[i] = (message[i][0], text)
            
        return message

