#!/usr/bin/env python

class Role:
    villager    = 0
    wolf        = 1
    seer        = 2
    guardian    = 3
    angel       = 4

class Abilities:
    vote    = 0
    kill    = 1
    see     = 2
    guard   = 3
    angel   = 4

class BaseRole:
    def __init__(self):
        #role in the game
        self.role = None
        #what the seer sees
        self.appears_as = None
        #role abilities eg. vote, see, etc.
        self.abilities = []
        #which party does this role win with
        self.wins_with = None

class Villager(BaseRole):
    def __init__(self):
        BaseRole.__init__(self)
        self.role = Role.villager
        self.appears_as = Role.villager
        self.abilities.append(Abilities.vote)
        self.wins_with = Role.villager

class Wolf(Villager):
    def __init__(self):
        Villager.__init__(self)
        self.role = Role.wolf
        self.appears_as = Role.wolf
        self.abilities.append(Abilities.kill)
        self.wins_with = Role.wolf

class Seer(Villager):
    def __init__(self):
        Villager.__init__(self)
        self.role = Role.seer
        self.appears_as = Role.seer
        self.abilities.append(Abilities.see)
        self.wins_with = Role.villager

class Traitor(Villager):
    def __init__(self):
        Villager.__init__(self)
        self.appears_as = Role.wolf

class Guardian(Villager):
    def __init__(self):
        Villager.__init__(self)
        self.role = Role.guardian
        self.appears_as = Role.guardian
        self.abilities.append(Abilities.guard)
        self.wins_with = Role.villager

class Angel(Villager):
    def __init__(self):
        Villager.__init__(self)
        self.role = Role.angel
        self.appears_as = Role.angel
        self.abilities.append(Abilities.angel)

class Player:
    def __init__(self, name):
        self.role       = None  #Player's role
        self.name       = name  #Player's actual nick preserving case
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
