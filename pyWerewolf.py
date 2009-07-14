#!/usr/bin/env python

import sys
import traceback
import string
from ircbot import SingleServerIRCBot
from irclib import nm_to_n, nm_to_h, irc_lower, ip_numstr_to_quad, ip_quad_to_numstr

from command_handler import *
from timers import *
from game import *
from theme import Theme, ThemeMessageType as MessageType
from theme_handler import ThemeHandler
import config

class WerewolfBot(SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel
        self.command_handler = Command_Handler(self, self.theme)
        self.connection.add_global_handler("all_events", self.on_all_events, -100)
        self.timers = Timers()
        self.theme = WerewolfTheme()
        self.theme_handler = ThemeHandler(self.theme)

        #game
        self.game = None
        self.command_handler.reg_callback("start", self.start_game)

    def set_theme(self, theme):
        self.theme = theme
        self.command_handler.set_theme(self.theme)
        self.theme_handler.set_theme(self.theme)

    ### IRC Events ###
    def on_all_events(self, c, e):
        if e.eventtype() != "all_raw_messages":
            print e.source(), e.eventtype().upper(), e.target(), e.arguments()

    def on_welcome(self, c, e):
        c.mode(c.get_nickname(), "+B")

    def on_nicknameinuse(self, c, e):
        for n in config.irc.nickname:
            if n != c.get_nickname():
                c.nick(n)
                break
        if c.get_nickname() != config.irc.nickname[0]:
            c.nick(config.irc.nickname[0])
        c.nick(c.get_nickname() + "_")

    def on_privmsg(self, c, e):
        msg = e.arguments()[0]
        if (msg[:1] == "!") and ((msg.find("!",1,4) & msg.find("?",1,4)) == -1):
            msg = msg[1:]
        self.command_handler.process_command(e, msg)

    def on_pubmsg(self, c, e):
        msg = e.arguments()[0]
        a = msg.split(":", 1)
        if len(a) > 1 and irc_lower(a[0]) == irc_lower(c.get_nickname()):
            self.command_handler.process_command(e, a[1].strip())
        elif msg[:1] == "!" and ((msg.find("!",1,4) & msg.find("?",1,4)) == -1):
            self.command_handler.process_command(e, msg[1:])

    def on_privnotice(self, c, e):
        nick = nm_to_n(e.source())
        msg  = e.arguments()[0]
        if (nick == "NickServ") and \
        (msg.startswith("This nickname is registered and protected.")):
            c.privmsg(nick, "identify %s" % config.irc.password)
            c.join(self.channel)

    def on_kick(self, c, e):
        self.on_quit(c, e)

    def on_join(self, c, e):
        nick = nm_to_n(e.source())
        self.send_message("%s has joined the channel" % nick)
        if self.game is not None: self.game.on_channel_join(nick)

    def on_part(self, c, e):
        nick = nm_to_n(e.source())
        self.send_message("%s has left the channel" % nick)
        if self.game is not None: self.game.on_player_channel_leave(nick)

    def on_nick(self, c, e):
        target  = e.target()
        nick    = nm_to_n(e.source())
        self.send_message("%s has changed their nick to %s" % (nick, target))
        if self.game is not None: self.game.on_player_nick_change(nick, target)

    def on_quit(self, c, e):
        self.on_part(c, e)

    def on_mode(self, c, e):
        nick = nm_to_n(e.source())
        if (nick == "ChanServ") and (e.arguments()[1] == c.get_nickname()):
            if e.arguments()[0].startswith("+") and "o" in e.arguments()[0]:
                self.reset_modes()

    ### Wrapper Methods ###
    def send_message(self, *args):
        if len(args) == 1:
            self.connection.privmsg(self.channel, args[0])
        elif len(args) == 2:
            self.connection.privmsg(args[0], args[1])

    def send_notice(self, target, msg):
        self.connection.notice(target, msg)

    def reset_modes(self):
        voiced_nicks = self.channels[self.channel].voiced()
        self.devoice_users(voiced_nicks, True)

    def devoice_everyone(self):
        self.devoice_users(self.channels[self.channel].voiced())

    def set_modes(self, modes):
        self.connection.mode(self.channel, modes)

    def set_moderated(self, moderated=True):
        self.set_modes("%sm" % ('+' if moderated else '-'))

    def voice_users(self, targets):
        for start in xrange(0, len(targets), 12):
            end = start+12
            if len(targets) < end: end = len(targets)
            nicks = ""
            for t in targets[start:end]: nicks += "%s " % t
            modes = "+%s %s" % ('v'*(end-start), nicks)
            self.set_modes(modes)

    def devoice_users(self, targets, unmoderate=False):
        for start in xrange(0, len(targets), 12):
            end = start+12
            if len(targets) < end: end = len(targets)
            nicks = ""
            for t in targets[start:end]: nicks += "%s " % t
            modes = "-%s %s" % ('v'*(end-start), nicks)
            if unmoderate: modes = "-m%s" % modes[1:]
            self.set_modes(modes)

    ### Game Events ###
    def game_on_game_start(self, g, nick):
        pass #announce that nick has started a game

    def game_on_game_restart(self, g):
        pass #announce that nick has restarted a game

    def game_on_game_end(self, g):
        self.remove_game()

    def game_on_join_end(self, g, game_started):
        #join_end_message
        if game_started:
            self.set_moderated()
            #join_success_message (g.player_count)
        else:
            #join_fail_message
            self.remove_game()

    def game_on_role_notify(g, type, nick, role=None, other_players=None):
        if type == MessageType.Role.announce:
            pass #role_message[role]
        elif type == MessageType.Role.other:
            if len(other_wolves) == 1:
                pass #role_other_message[] (other_players)
            else:
                pass #role_others_message[] (other_players)

    def game_on_roles_assigned(self, g, wolf_count, seer_count, \
                               guard_count, angel_count):
        if wolf_count > 1:
            pass #role_num_message[Role.wolf]
        if seer_count > 1:
            pass #role_num_message[Role.seer]
        if guard_count > 1:
            pass #role_num_message[Role.guard]
        if angel_count > 1:
            pass #role_num_message[Role.angel]

    def game_on_night_start(self, g):
        for role in [Role.wolf, Role.seer, Role.guardian]:
            if g._is_alive(role):
                if g._num(role) == 1:
                    pass #night_player_message[role]
                else:
                    pass #night_players_message[role]

    def game_on_see_result(self, g, nick, target, role):
        pass #see_message[role]

    def game_on_night_end(self, g):
        pass

    def game_on_day_start(self, g):
        self.voice_users(g.player_nicks)
        #day_start_message

    def game_on_day_end(self, g):
        pass #NOTE: event has no place to be raised

    def game_on_vote_start(self, g):
        pass #vote_start_message

    def game_on_vote_end(self, g):
        self.devoice_everyone()
        #vote_end_message

    def game_on_vote_result(self, g, type):
        if type == MessageType.Vote.tie:
            pass #vote_tie_message

    def game_on_player_vote(self, g, nick, target):
        if nick.lower() not in g.players:
            pass #not_player_message
        if g.mode != g.Mode.day_vote:
            pass #vote_not_vote_time_message
        if target.lower() not in g.players:
            pass #vote_invalid_target_message
        #TODO: move the above command error checking to command_handler
        pass #vote_target_message

    def game_on_player_kill(self, g, nick, target):
        #check command arguments
        if nick.lower() not in g.players:
            # nick is not taking part in the game
            pass #not_player_message
        elif g.mode != g.Mode.night:
            # its not night time
            pass #kill_not_night_time_message
        elif target.lower() not in g.players:
            # target is not taking part in the game
            pass #kill_invalid_target_message
        elif player.role.role != Role.wolf:
            # player is not a wolf
            pass #kill_not_wolf_message
        elif target.role == Role.wolf:
            # target is a wolf
            pass #kill_invalid_wolf_message

        if g.get_role_count(Role.wolf) == 1:
            pass #kill_wolf_message
        else:
            pass #kill_wolves_message

    def game_on_player_guard(self, g, nick, target):
        #check command arguments
        if nick.lower() not in g.players:
            # nick is not taking part in the game
            pass #not_player_message
        elif g.mode != g.Mode.night:
            # its not night time
            pass #guard_not_night_time_message
        elif target.lower() not in g.players:
            # target is not taking part in the game
            pass #guard_invalid_target_message
        elif player.role != Role.guardian:
            # player is not a guardian
            pass #guard_not_guard_message

        pass #guard_target_message

    def game_on_player_see(self, g, nick, target):
        #check command arguments
        if nick.lower() not in g.players:
            # nick is not taking part in the game
            pass #not_player_message
        elif g.mode != g.Mode.night:
            # its not night time
            pass #see_not_night_time_message
        elif target.lower() not in g.players:
            # target is not taking part in the game
            pass #seer_invalid_target_message
        elif player.role != Role.guardian:
            # player is not a seer
            pass #seer_not_seer_message

        pass #see_target_message

    def game_on_player_death(self, g, type, nick, role):
        if type == MessageType.Die.kill:
            pass #kill_die_message[role]
        elif type == MessageType.Die.vote:
            pass #vote_die_message[role]
        elif type == MessageType.Die.not_voting:
            pass #good_defy_message[role]

    ### Game Management Methods ###
    def start_game(self, who, args):
        if self.game is None:
            self.game = Game(self, who)
            game_events = self.game.events
            game_events.on_game_start       += game_on_game_start
            game_events.on_game_restart     += game_on_game_restart
            game_events.on_game_end         += game_on_game_end
            game_events.on_role_notify      += game_on_role_notify
            game_events.on_roles_assigned   += game_on_roles_assigned
            game_events.on_join_end         += game_on_join_end
            game_events.on_night_start      += game_on_night_start
            game_events.on_night_end        += game_on_night_end
            game_events.on_see_result       += game_on_see_result
            game_events.on_day_start        += game_on_day_start
            game_events.on_day_end          += game_on_day_end
            game_events.on_vote_start       += game_on_vote_start
            game_events.on_vote_end         += game_on_vote_end
            game_events.on_vote_result      += game_on_vote_result
            game_events.on_player_vote      += game_on_player_vote
            game_events.on_player_kill      += game_on_player_kill
            game_events.on_player_guard     += game_on_player_guard
            game_events.on_player_see       += game_on_player_see
            game_events.on_player_death     += game_on_player_death
        else:
            self.game.restart(who, args)

    def end_game(self):
        if self.game is not None:
            self.game.end()

    def remove_game(self):
        self.game = None

    ### Miscellaneous ###
    def is_admin(self, nick):
        if nick.lower() in config.irc.admins: return True
        return False

    def process_forever(self):
        self._connect()
        while 1:
            self.ircobj.process_once(0.2)
            self.timers.process_timeout()

def main():
    if len(sys.argv) is 5:
        bot = WerewolfBot(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]))
    elif len(sys.argv) is not 1:
        print "Usage:\n\tpyWerewolf.py [<#channel> <nickname> <server> <port>]"
        sys.exit(1)
    else:
        bot = WerewolfBot(config.irc.channel, config.irc.nickname[0], \
                                    config.irc.server, config.irc.port)
    try:
        bot.process_forever()
    except KeyboardInterrupt:
        print "^C - Exiting gracefully..."
        bot.disconnect(msg="Terminated at terminal")
        sys.exit(0)
    except Exception as exc:
        bot.disconnect(msg="Unexpected Error. Sorry Folks.")
        print "traceback:"
        print traceback.print_exc()
        sys.exit(0)

if __name__ == "__main__":
    main()
