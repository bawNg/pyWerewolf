#!/usr/bin/env python

class Role:
    villager    = 0
    wolf        = 1
    seer        = 2
    guardian    = 3
    angel       = 4
    traitor     = 5
    noone       = 6
    num         = 7

class Player:
    def __init__(self, name):
        self.role       = None  #Player's role
        self.appears_as = None  #Player appears as this to a seer
        self.wins_with  = None  #Player wins with this role
        self.alive      = True  #Is the player alive
        self.nick       = name  #Player's actual nick preserving case
        self.vote       = None  #Who player votes to lynch
        self.kill       = None  #Who player votes to kill
        self.see        = None  #Who player chooses to see
        self.guard      = None  #Who player chooses to guard
        self.notvoted   = 0     #How many times in a row player has not voted
    
    def reset(self):
        self.vote   = None
        self.kill   = None
        self.see    = None
        self.guard  = None

    def set_role(self, role):
        self.role = role
    
        self.appears_as = role
        #if player is a traitor he appears as wolf
        if role == Role.traitor:
            self.appears_as = Role.wolf
    
        #set who to win with
        if role == Role.wolf:
            self.wins_with = Role.wolf
        else:
            self.wins_with = Role.villager
