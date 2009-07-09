#!/usr/bin/env python

#werewolf game logic
from player import *
import config

class Game(object):
	def __init__(self, bot):
		self.irc = bot
		self.c 	= bot.connection
		self.execute_delayed = bot.connection.execute_delayed
		self.players = {}

	def signup(self): #hold game signups
		pass

	def assign_roles(self,): #assign player roles
		pass

	def night_cycle(self,):
		pass

	def day_cycle(self,):
		pass

	def vote_tally(self,):
		pass

