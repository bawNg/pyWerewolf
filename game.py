#!/usr/bin/env python

import random
from events import Events
from timers import *
from player import *
from game_data import *
import config

class Game_Events(Events):
    __events__ = ('on_game_start', 'on_game_restart', 'on_game_end',
                  'on_role_assigned','on_roles_assigned','on_role_notify_other',
                  'on_join_end', 'on_night_start', 'on_night_end',
                  'on_day_start','on_day_end', 'on_wolf_kill', 'on_seer_see',
                  'on_vote_start','on_vote_end','on_vote_result','on_vote_tie',
                  'on_good_defy', 'on_night_after_message',
                  'on_player_vote',
                  'on_player_kill', 'on_player_guard', 'on_player_see')

class Game(object):
    def __init__(self, bot, who):
        self.events = Game_Events()
        self.timers = Timers()
        self.players = {}
        self.roles = [[] for i in xrange(Role.num)]
        self.mode = Mode.join
        self._start(who)

    def process_timeout(self):
        """Process timeouts, call this method atleast once every 0.5 seconds."""
        self.timers.process_timeout()

    def _add_player(self, nick):
        self.players[nick.lower()] = Player(nick)

    def _rem_player(self, nick):
        if nick.lower() in self.players:
            self.irc.devoice_users([nick])
            del self.players[nick.lower()]

    def _check_win(self):
        num_wolves = 0
        num_villagers = 0
        for player in self.players:
            tplayer = self.players[player]
            if tplayer.role.wins_with == Role.villager:
                num_villagers += 1
            else:
                num_wolves += 1

        if num_wolves == 0:
            self.events.on_game_win(self, Role.villager)
            self.end()
        elif num_wolves == num_villagers:
            self.events.on_game_win(self, Role.wolf)
            self.end()
        else:
            return False
        return True

    def _assign_roles(self):
        num_players     = len(self.players)
        num_wolves      = num_players//5
        num_angels      = 1
        num_traitors    = 1
        num_guardians   = num_players//9
        num_seers       = num_players//6

        if num_wolves < 1:
            num_wolves = 1
        if num_seers < 1:
            num_seers = 1

        num_villagers   = num_players-num_wolves-num_angels-num_traitors- \
                            num_guardians-num_seers

        if num_villagers <= 0:
            num_villagers += num_angels
            num_angels = 0
        if num_villagers <= 0:
            num_villagers += num_traitors
            num_traitors = 0

        roles = []
        for i in xrange(num_wolves):
            roles.append(Wolf())
        for i in xrange(num_angels):
            roles.append(Angel())
        for i in xrange(num_traitors):
            roles.append(Traitor())
        for i in xrange(num_guardians):
            roles.append(Guardian())
        for i in xrange(num_seers):
            roles.append(Seer())
        for i in xrange(num_villagers):
            roles.append(Villager())

        random.shuffle(roles)

        for i, player in enumerate(self.players.keys()):
            self.players[player].role = roles[i]
            if roles[i].role == Role.wolf: self.roles[Role.wolf].append(who)
            nick = self.players[player].nick
            self.events.on_role_assigned(self, nick, roles[i].role)


        if num_wolves >= 2:
            for i in xrange(len(self.roles[Role.wolf])):
                other_wolves = []
                for j in xrange(i):
                    other_wolves.append(self.roles[Role.wolf][j])
                for j in xrange(i+1, len(self.roles[Role.wolf])):
                    other_wolves.append(self.roles[Role.wolf][j])

                nick = self.roles[Role.wolf][i]
                self.events.on_role_notify_other(self, nick, other_wolves)

        self.events.on_roles_assigned(self, num_wolves, num_seers, \
                                      num_guardians, num_angels)

    def _is_alive(self, role):
        for player in self.players:
            if role == self.players[player].role.role:
                return True
        return False

    def _num(self, role):
        ans = 0
        for player in self.players:
            if role == self.players[player].role.role:
                ans += 1
        return ans
    def _role(self, role):
        #returns all players of that role
        ans = []
        for player in self.players:
            if role == self.players[player].role.role:
                ans.append(self.players[player])
        return ans

    def _reset_players(self):
        for player in self.players:
            self.players[player].reset()

    def _get_vote_tally(self):
        votes = {}
        for pn in self.players:
            player = self.players[pn]
            if player.vote is not None:
                vote = player.vote.lower()
                if vote not in votes:
                    votes[vote] = 0
                votes[vote] += 1
        return votes

    def _start(self, nick):
        #setup game info
        self.mode = Mode.join
        self._add_player(nick)
        self.timers.add_timer(Consts.join_time, self.join_end)
        self.events.on_game_start(self, nick)

    def restart(self, who, args):
        self.events.on_game_restart(self, nick)

    def end(self):
        self.timers.remove_all()
        self.events.on_game_end(self)

    def join_end(self):
        if len(self.players) >= Consts.min_players:
            self.events.on_join_end(self, True)
            self._assign_roles()
            self.night_start()
        else:
            self.events.on_join_end(self, False)

    def night_start(self):
        time = Consts.night_wolf_time
        if self._num(Role.wolf) > 1: time = Consts.night_wolves_time
        self._reset_players()
        self.mode = Mode.night
        self.events.on_night_start(self)
        self.timers.add_timer(time, self.night_end)

    def night_end(self):
        #find wolf target
        wolf_targets = {}
        max_votes = 0
        for player in self._role(Role.wolf):
            if player.kill:
                kill = player.kill.lower()
                if kill not in wolf_targets:
                    wolf_targets[kill] = 0
                wolf_targets[kill] += 1
                max_votes = max(max_votes, wolf_targets[kill])
        temp_wolf_targets = []
        for t in wolf_targets:
            if wolf_targets[t] == max_votes:
                temp_wolf_targets.append(t)
        wolf_target = None
        if len(temp_wolf_targets) > 0:
            ran_target = random.randint(0, len(temp_wolf_targets)-1)
            wolf_target = temp_wolf_targets[ran_target]

        #guardians protection
        wolf_guardians = []
        for player in self._role(Role.guardian):
            guard = player.guard.lower()
            if self.players[guard].role.role == Role.wolf:
                wolf_guardians.append(player.nick.lower())

        if wolf_guardians:
            wolf_target = wolf_guardians[random.randint(0, len(wolf_guardians)-1)]
        else:
            for player in self._role(Role.guardian):
                guard = player.guard.lower()
                if guard == wolf_target:
                    wolf_target = None
                    break

        #seer results
        for player in self._role(Role.seer):
            if not player.see: continue
            if player.see.lower() in self.players:
                role = self.players[player.see.lower()].role.appears_as
                self.events.on_seer_see(self, player.nick, player.see, role)

        #check if wolf target is alive
        if wolf_target is not None:
            if wolf_target not in self.players:
                wolf_target = None

        #check if wolf target is angel
        if wolf_target is not None:
            target = self.players[wolf_target]
            if target.role.role == Role.angel:
                wolf_target = None

        #kill wolf target
        if wolf_target is not None:
            role = self.players[wolf_target].role.role
            nick = self.players[wolf_target].nick
            self.events.on_wolf_kill(self, nick, role)
            self._rem_player(wolf_target)
        else:
            self.events.on_wolf_kill(self, None, Role.noone)

        #if the game hasn't been won start the next day
        if not self._check_win():
            self.day_start()

    def day_start(self):
        self.mode = Mode.day_talk
        self.events.on_day_start(self)
        self.timers.add_timer(Consts.talk_time, self.vote_start)

    def vote_start(self):
        self._reset_players()
        self.mode = Mode.day_vote
        for player in self.players:
            tplayer = self.players[player]
            tplayer.notvoted += 1
        self.events.on_vote_start(self)
        self.timers.add_timer(Consts.vote_time, self.vote_end)

    def vote_end(self):
        #end voting
        self.events.on_vote_end(self)

        #tally votes
        votes = self._get_vote_tally()
        max_vote = 0
        lynch_targets = []
        for vote, num in votes.items():
            if num > max_vote:
                lynch_targets = [vote]
                max_vote = num
            elif num == max_vote:
                lynch_targets.append(vote)

        lynch_target = None
        if len(lynch_targets) > 1:
            self.events.on_vote_tie(self)
            ran = random.randint(0, len(lynch_targets)-1)
            lynch_target = lynch_targets[ran]
        elif len(lynch_targets) == 1:
            lynch_target = lynch_targets[0]

        if lynch_target is None:
            self.events.on_vote_result(self, None, None)
        else:
            target = self.players[lynch_target]
            role = target.role.role
            self.events.on_vote_result(self, target, role)
            self._rem_player(target.nick.lower())

        #kills for defying the good
        for pn, player in self.players.items():
            if player.notvoted >= Consts.good_kill_times:
                self.events.on_good_defy(self, player.nick, player.role.role)
                self._rem_player(player.nick.lower())

        if not self._check_win():
            self.events.on_night_after_message(self) # event name needs revamping
            self.night_start()

    def join(self, who, args):
        pass #TODO: remove this method and make _add_player() method public

    def leave(self, who, args=None):
        pass #TODO: remove this method and make _rem_player() public

    def vote(self, nick, target):
        player = self.players[nick.lower()]
        target = self.players[target.lower()]
        player.vote = target.nick
        player.notvoted = 0
        votes = self._get_vote_tally()
        self.events.on_player_vote(self, player.nick, target.nick)

    def kill(self, nick, target):
        player = self.players[nick.lower()]
        target = self.players[target.lower()]
        player.kill = target.nick
        self.events.on_player_kill(self, player.nick, target.nick)

    def guard(self, nick, target):
        player = self.players[nick.lower()]
        target = self.players[target.lower()]
        player.guard = target.nick
        self.events.on_player_guard(self, player.nick, target.nick)

    def see(self, nick, target):
        player = self.players[nick.lower()]
        target = self.players[target.lower()]
        player.see = target.nick
        self.events.on_player_see(self, player.nick, target.nick)

    def randplayer(self):
        player_nicks = []
        for player in self.players: player_nicks.append(player.nick)
        return player_nicks[random.randint(0, len(player_nicks)-1)]

    #TODO: add public method(s) for extending timer, etc
