#!/usr/bin/env python

class base_role:
	def __init__(self):
		#role in the game
		self.role = ''
		#what the seer sees
		self.appears_as = ''
		#role abilities eg. vote, see, etc.
		self.abilities = []
		#which party does this role win with
		self.wins_with = ''

class villager(base_role):
	def __init__(self):
		base_role.__init__(self)
		self.role = 'villager'
		self.appears_as = 'villager'
		self.abilities.append('vote')
		self.wins_with = 'villagers'

class wolf(villager):
	def __init__(self):
		villager.__init__(self)
		self.role = 'wolf'
		self.appears_as = 'wolf'
		self.abilities.append('kill')
		self.wins_with = 'wolves'

class seer(villager):
	def __init__(self):
		villager.__init__(self)
		self.role = 'seer'
		self.appears_as = 'seer'
		self.abilities.append('see')
		self.wins_with = 'villager'

class traitor(villager):
	def __init__(self):
		villager.__init__(self)
		self.appears_as = 'wolf'

class guardian(villager):
	def __init__(self):
		villager.__init__(self)
		self.role = 'guardian'
		self.appears_as = 'guardian'
		self.abilities.append('guard')
		self.wins_with = 'villager'