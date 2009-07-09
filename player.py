#!/usr/bin/env python

class Role:
	villager = 0
	wolf		= 1
	seer		= 2
	guardian = 3

class Abilities:
	vote	= 0
	kill	= 1
	see	= 2
	guard	= 3

class Base_Role:
	def __init__(self):
		#role in the game
		self.role = None
		#what the seer sees
		self.appears_as = None
		#role abilities eg. vote, see, etc.
		self.abilities = []
		#which party does this role win with
		self.wins_with = None

class Villager(Base_Role):
	def __init__(self):
		base_role.__init__(self)
		self.role = Role.villager
		self.appears_as = 'Villager'
		self.abilities.append(Abilities.vote)
		self.wins_with = Role.villager

class Wolf(Villager):
	def __init__(self):
		Villager.__init__(self)
		self.role = Role.wolf
		self.appears_as = "Wolf"
		self.abilities.append(Abilities.kill)
		self.wins_with = Role.wolf

class Seer(Villager):
	def __init__(self):
		Villager.__init__(self)
		self.role = Role.seer
		self.appears_as = "Seer"
		self.abilities.append(Abilities.see)
		self.wins_with = Role.villager

class Traitor(Villager):
	def __init__(self):
		Villager.__init__(self)
		self.appears_as = "Wolf"

class Guardian(Villager):
	def __init__(self):
		Villager.__init__(self)
		self.role = Role.guardian
		self.appears_as = "Guardian"
		self.abilities.append(Abilities.guard)
		self.wins_with = Role.villager
