#!/usr/bin/env python

from random import randint
from player import *

class Consts:
    join_time           = 60    #time people have to join game
    join_extend_time    = 10    #time extension when someone joins
    night_wolf_time     = 45    #time of night with one wolf
    night_wolves_time   = 75    #time of night with multiple wolves
    talk_time           = 60    #talk time before voting
    vote_time           = 60    #voting time
    good_kill_times     = 2     #number of times you can not vote before killed
    min_players         = 3     #number of players needed before a game can start

class Commands:
    game = ["join", "vote", "kill", "guard", "see", "randplayer", "leave"]

class Mode:
    join        = 0
    night       = 1
    day_talk    = 2
    day_vote    = 3

class Theme:
    def __init__(self, bot):
        self.irc = bot
        self.tokens = ["bot", "num", "user", "target", 
                       "votes", "roles", "alive"]
        for token in self.tokens:
            setattr(self, token, "")
        self.token_delim = '$'

    def get_string(self, string_list):
        if len(string_list) == 0:
            raise ValueError("string_list is of size 0")
        i = randint(0, len(string_list)-1)
        result = string_list[i]
        for token in self.tokens:
            setattr(self, token, str(getattr(self, token))) 
        for token in self.tokens:
            result = result.replace(self.token_delim+token,
                                    getattr(self, token))
        return result

    def reset(self):
        for token in self.tokens:
            setattr(self, token, "")
        self.bot = self.irc.connection.get_nickname()
        
    ### Role Names ###
    role_names = ["Villager", "Werewolf", "Seer", "Guardian", "Angel"]

    ### Game Text Messages ###

    #Message format: <group or command>_<action of group or command>_message
    #TODO: add tokens for chan messages, pvt notices, chan notices and formatting
    #$bot is the name of the bot
    #$num is the number of times an action has been executed like join
    #$user gets replaced by the current user
    #$target gets replaced by who is targeted by current user
    #$votes gets replaced by current vote tallies
    #$roles gets the names of the roles
    #$alive gets the alive villagers

    #message when game starts
    game_start_message = ["$user started a new game! You have $num seconds to join!"]
    game_started_message = ["Game already running."]

    ### JOIN MESSAGES ###

    #message when someone new joins hunt
    join_new_message = ["$num. $user joined the hunt!"]
    
    #message when someone tries to rejoin the hunt
    join_old_message = ["You have already joined the hunt."]

    #message when someone leaves the game during join
    join_leave_message = ["$target has left the hunt."]
    join_leave_nick_message = ["$target has left the hunt."]
    
    #message when the joining has ended
    join_ended_message = ["Sorry the joining has ended."]

    #message when the joining ends
    join_end_message = ["Joining ends."]

    #message when your role gets known
    role_message            = [None for i in xrange(Role.num)]
    role_message[Role.wolf] = ["You are a wolf. rAwr!!!"]
    role_message[Role.seer]      = ["You are a seer."]
    role_message[Role.guardian]  = ["You are a guardian."]
    role_message[Role.angel]     = ["You are an Angel."]
    role_message[Role.villager]  = ["You are a villager."]

    #message sent to wolf when there are more than one wolf
    role_other_message              = [None for i in xrange(Role.num)]
    role_other_message[Role.wolf]   = ["Your brethren is $wolves."]
    role_others_message             = [None for i in xrange(Role.num)]
    role_others_message[Role.wolf]  = ["Your brethren are: $wolves"]

    #message sent when there are more than one of special roles
    role_num_message                = [None for i in xrange(Role.num)]
    role_num_message[Role.wolf]     = ["There are $num wolves."]
    role_num_message[Role.seer]     = ["There are $num seers."]
    role_num_message[Role.guardian] = ["There are $num guardians."]
    role_num_message[Role.angel]    = ["There are $num angels."]

    #message when joining succeeds
    join_success_message = ["Congratulations you have $num players in the hunt!"]

    #message when joining fails
    join_fail_message = ["Sorry not enough players have joined."]
    
    ### NIGHT MESSAGES ###
    
    #message before night after joining ends
    night_first_message = ["Night descends over the unsuspecting village."]
    
    #message after voting and before night
    night_after_message = ["Villagers goes to an uneasy sleep."]

    #message for abilities at night
    night_player_message = [None for i in xrange(Role.num)]
    night_players_message = [None for i in xrange(Role.num)]
    night_player_message[Role.seer] = ["Seer type: /msg $bot see " + 
                                       "<target> to see. You have $num seconds."]
    night_players_message[Role.seer] = ["Seers type: /msg $bot see "+
                                        "<target> to see. You have $num seconds."]

    #message for wolves at night
    night_player_message[Role.wolf] = ["Wolf type: /msg $bot kill "+
                                       "<target> to kill. You have $num seconds."]
    night_players_message[Role.wolf] = ["Wolves type: /msg $bot kill "+
                                        "<target> to kill. You have $num seconds."]

    #message for guardians at night
    night_player_message[Role.guardian] = ["Guardian type: /msg $bot "+
                                           "guard <target> to guard. You have $num "+
                                           "seconds."]
    night_players_message[Role.guardian] = ["Guardians type: /msg $bot "+
                                            "guard <target> to guard. You have $num "+
                                            "seconds."]

    ### DAY START MESSAGES ###
    
    #message at start of day
    day_start_message = ["Make your accusations."]

    ### VOTE MESSAGES ###

    #message when voting starts
    vote_start_message = ["Voting has started. Type: !vote <target> to vote."]

    #message when validly voted
    vote_target_message = ["$user voted for $target. ($votes)"]

    #message when not valid vote
    vote_not_vote_time_message = ["Sorry you can only vote during voting time."]
    vote_invalid_message = ["Your vote message was invalid."]
    vote_invalid_target_message = ["$target is not a player in the game."]
    
    #message when voting ends
    vote_end_message = ["Voting has ended."]

    #message when voting ends in tie
    vote_tie_message = ["There was a tie, randomly choosing target."]

    ### LYNCH MESSAGES ###
    
    vote_die_message = [None for i in xrange(Role.num)]
    #message when seer is killed by a lynch vote
    vote_die_message[Role.seer] = ["$target runs before the mob is organised, "+
                                   "dashing away from the village. Tackled to "+
                                   "the ground near the lake, $target is tied "+
                                   "to a log, screaming, thrown into the water. "+
                                   "With no means of escape, $target the Seer "+
                                   "drowns, but as the villagers watch, cards "+
                                   "float to the surface and their mistake "+
                                   "is all too apparent..."]
    
    #message when gaurdian is killed by a lynch vote
    vote_die_message[Role.guardian] = ["$target runs before the mob is "+ 
                                       "organised, running for the safety "+
                                       "of home. Just before reaching home, "+
                                       "$target is hit with a large stone, "+
                                       "then another. With no means of escape, "+
                                       "$target is stoned to death, his body "+
                                       "crushed. One curious villager enters "+
                                       "the house to find proof that $target "+
                                       "was a Guardian after all..."]
    
    #message when wolf is killed by a lynch vote
    vote_die_message[Role.wolf] = ["After coming to a decision, $target is "+
                                   "quickly dragged from the crowd and "+
                                   "dragged to the hanging tree. $target is "+
                                   "strung up, and the block kicked from "+
                                   "beneath their feet. There is a yelp of "+
                                   "pain, but $target's neck doesn't snap, "+
                                   "and fur begins to sprout from his/her "+
                                   "body. A gunshot rings out, as a "+
                                   "villager puts a silver bullet in the "+
                                   "beast's head..."]
    
    #message when villager is killed by a lynch vote
    vote_die_message[Role.villager] = ["The air thick with adrenaline, the "+
                                       "villagers grab $target who struggles "+
                                       "furiously, pleading innocence, but "+
                                       "the screams fall on deaf ears. "+
                                       "$target is dragged to the stake at "+
                                       "the edge of the village, and burned "+
                                       "alive. But the villagers shouts and "+
                                       "cheers fade as they realise the moon "+
                                       "is already up - $target was not a "+
                                       "werewolf after all...",
    
                                      "Realising the angry mob is turning, "+
                                      "$target tries to run, but is quickly "+
                                      "seized upon. $target is strung up to "+
                                      "the hanging tree, and a hunter readies "+
                                      "his rifle with a silver slug, as the "+
                                      "block is kicked from beneath them. "+
                                      "But there is a dull snap, and $target "+
                                      "hangs, silent, motionless. The silent "+
                                      "villagers quickly realise their grave "+
                                      "mistake..."]
    
    #message when noone is killed by lynch vote
    vote_die_message[Role.noone] = ["Noone was voted for. The good thingies "+
                                    "will not be happy"]

    ### KILL MESSAGES ###
    
    #message when single wolf kills
    kill_wolf_message = ["You have selected $target for your feast."]

    #message when multiple wolves kill
    kill_wolves_message = ["You have selected $target for your feast, but must "+
                           "wait for brethren."]

    #message when not night
    kill_not_night_message = ["Can only kill at night."]

    #message when not wolf
    kill_not_wolf_message = ["Only wolves can kill."]

    #message when kill message not formatted correctly
    kill_invalid_message = ["Kill message invalid format."]
    
    #message when a wolf tries to attack another wolf
    kill_invalid_wolf_message = ["$target is one of your brethren you can't "+
                                 "attack them."]
    #message when a wolf tries to attack a non player
    kill_invalid_target_message = ["$target is not in the game."]

    kill_die_message = [None for i in xrange(Role.num)]
    #message when villager is killed by a wolf
    kill_die_message[Role.villager] = ["The villagers gather the next morning "+
                                       "in the village center, but $target "+
                                       "does not appear. The villagers "+
                                       "converge on $target's home and find "+
                                       "them decapitated in their bed. After "+
                                       "carrying the body to the church, the "+
                                       "villagers, now hysterical, return to "+
                                       "the village center to decide how to "+
                                       "retaliate...",
    
                                       "As some villagers begin to gather in "+
                                       "the village center, a scream is "+
                                       "heard from the direction of $target's "+
                                       "house. The elderly villager who had "+
                                       "screamed points to the fence, on top "+
                                       "of which, the remains of $target are "+
                                       "impaled, with their intestines "+
                                       "spilling onto the cobbles. "+
                                       "Apparently $target was trying to flee "+
                                       "their attacker...",
    
                                       "When the villagers gather at the "+
                                       "village center, one comes running from "+
                                       "the hanging tree, screaming at others "+
                                       "to follow. When they arrive at the "+
                                       "hanging tree, a gentle creaking echoes "+
                                       "through the air as the body of $target "+
                                       "swings gently in the breeze, its arms "+
                                       "ripped off at the shoulders. It appears "+
                                       "the attacker was not without a sense of "+
                                       "irony...",
    
                                       "As the village priest gathers the "+
                                       "prayer books for the morning's sermon, "+
                                       "he notices a trickle of blood snaking "+
                                       "down the aisle. He looks upward "+
                                       "to see $target impaled on the crucifix "+
                                       "- the corpse has been gutted. He "+
                                       "shouts for help, and the other "+
                                       "villagers pile into the church and "+
                                       "start arguing furiously..."]
    
    #message when seer is killed by a wolf
    kill_die_message[Role.seer] = ["The first villager to arrive at the "+
                                   "center shrieks in horror - lying on the "+
                                   "cobbles is a blood stained Ouija Board, "+
                                   "and atop it sits $target's head. It "+
                                   "appears $target the Seer had been seeking "+
                                   "the guidance of the spirits to root out "+
                                   "the wolves, but apparently the magic "+
                                   "eight ball didn't see THIS one coming..."]
    
    #message when guardian is killed by a wolf
    kill_die_message[Role.guardian] = ["As one of the villagers passes "+
                                       "$target's home, he sees a bloody "+
                                       "mess in front of the door. After "+
                                       "following the trail of blood and gore, "+
                                       "he finds $target's body torn to pieces "+
                                       "with herbs and powder flung all about. "+
                                       "It's too bad $target the Guardian was "+
                                       "unable to ward off these evil beings..."]
    
    #message when nobody is killed by a wolf
    kill_die_message[Role.noone] = ["The villagers gather the next morning in "+
                                    "the village center, to sighs of relief - "+
                                    "it appears there was no attack the "+
                                    "previous night."]


    ### SEE(R) MESSAGES ###
    
    #message when seer enters target
    see_target_message = ["Your predictions will be revealed to you at dawn."]

    #messages when see message not valid
    see_not_night_message = ["You can only see at night."]
    see_not_seer_message = ["You aren't a seer"]
    see_invalid_message = ["Your see message was invalid."]
    see_invalid_target_message = ["$target isn't a player."]

    see_message = [None for i in xrange(Role.num)]
    #message when seer sees wolf
    see_message[Role.wolf] = ["$target is a filthy wolf."]
    
    #message when seer sees angel
    see_message[Role.angel] = ["$target is an angel."]

    #message when seer sees guardian
    see_message[Role.guardian] = ["$target is a guardian."]

    #message when seer sees seer
    see_message[Role.seer] = ["$target is a seer."]

    #message when seer sees villager
    see_message[Role.villager] = ["$target is a villager."]

    ### GUARD MESSAGES ###
    
    guard_target_message = ["You have chosen to guard $target from wolf attacks."]
    
    #messages when see message not valid
    guard_not_night_message = ["You can only guardian at night."]
    guard_not_guard_message = ["You aren't a guardian."]
    guard_invalid_message = ["Your guard message was invalid."]
    guard_invalid_target_message = ["$target isn't a player."]


    ### GOOD KILL ###
    
    #message when player gets killed for not voting
    good_defy_message = [None for i in xrange(Role.num)]
    good_defy_message[Role.villager] = ["$target the villager died for defying "+
                                        "the good."]
    good_defy_message[Role.wolf]     = ["$target the wolf died for defying "+
                                        "the good."]
    good_defy_message[Role.seer]     = ["$target the seer died for defying "+
                                        "the good."]
    good_defy_message[Role.guardian] = ["$target the guardian died for "+
                                        "defying the good."]
    good_defy_message[Role.angel]    = ["$target the wolf died for defying "+
                                        "the good."]
    
    ### NICK KILL ###
    
    nick_kill_message = [None for i in xrange(Role.num)]
    nick_kill_message[Role.villager] = ["$target the villager got killed for "+
                                        "changing nicks."]
    nick_kill_message[Role.wolf]     = ["$target the wolf got killed for changing "+
                                        "nicks."]
    nick_kill_message[Role.seer]     = ["$target the seer got killed for changing "+
                                        "nicks."]
    nick_kill_message[Role.guardian] = ["$target the guardian got killed for "+
                                        "changing nicks."]
    nick_kill_message[Role.angel]    = ["$target the angel got killed for changing "+
                                        "nicks."]

    ### LEAVE KILL ###
    
    leave_kill_message = [None for i in xrange(Role.num)]
    leave_kill_message[Role.villager] = ["$target the villager got killed for "+
                                         "leaving the game."]
    leave_kill_message[Role.wolf]     = ["$target the wolf got killed for leaving "+
                                         "the game."]
    leave_kill_message[Role.seer]     = ["$target the seer got killed for leaving "+
                                         "the game."]
    leave_kill_message[Role.guardian] = ["$target the guardian got killed for "+
                                         "leaving the game."]
    leave_kill_message[Role.angel]    = ["$target the angel got killed for "+
                                         "leaving the game."]

    ### WIN ###

    win_wolves_message = ["The wolves have won."]
    win_villagers_message = ["The villagers have won."]

    win_list_message = [None for i in xrange(Role.num)]
    win_list_message[Role.wolf] = ["The wolf was: $roles"]
    win_list_message[Role.seer] = ["The seer was: $roles"]
    win_list_message[Role.guardian] = ["The guard was: $roles"]
    win_list_message[Role.angel] = ["The angel was: $roles"]
    win_list_message[Role.traitor] = ["The traitor was: $roles"]

    win_lists_message = [None for i in xrange(Role.num)]
    win_lists_message[Role.wolf] = ["The wolves were: $roles"]
    win_lists_message[Role.seer] = ["The seers were: $roles"]
    win_lists_message[Role.guardian] = ["The guards were: $roles"]
    win_lists_message[Role.angel] = ["The angels were: $roles"]
    win_lists_message[Role.traitor] = ["The traitors were: $roles"]

    ### MISCELLANEOUS ###
    
    game_starting_message = ["A game is gonna start soon, type !join to join it"]
    game_in_progess_message = ["A game is in progress."]
    randplayer_message = ["Random player is $target."]
    not_player_message = ["Sorry you aren't a player."]
