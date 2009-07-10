#!/usr/bin/env python
from random import randint

class Mode:
    join        = 0
    night       = 1
    day_talk    = 2
    day_vote    = 3
    processing  = 4 #temporary mode

class Theme:
    def __init__(self):
        self.user   = ""
        self.target = ""
        self.votes  = ""
        self.wolves = ""
        self.alive  = ""
        self.tokens = ["user", "target", "votes", "wolves", "alive"]
        self.token_delim = '$'

    def get_string(self, string_list):
        if len(string_list) == 0:
            raise ValueError("string_list is of size 0")
        i = randint(0, len(string_list)-1)
        result = string_list[i]
        for token in self.tokens:
            result = result.replace(self.token_delim+token,
                                    getattr(self, token))
        return result
        

    ### Game Text Messages ###
    #$user gets replaced by the current user
    #$target gets replaced by who is targeted by current user
    #$votes gets replaced by current vote tallies
    #$wolves gets the names of the wolves
    #$alive gets the alive villagers

    #message when game starts
    game_start_message = ["$user started a new game!"]

    #message when someone new joins hunt
    join_new_message = ["$user joined the hunt!"]
    
    #message when someone tries to rejoin the hunt
    join_old_message = ["You have already joined the hunt."]

