#!/usr/bin/env python

from random import randint

class Commands:
    game = ["join", "vote", "kill", "guard", "see", "randplayer", "join_end"]

class Mode:
    join        = 0
    night       = 1
    day_talk    = 2
    day_vote    = 3
    processing  = 4 #temporary mode

class Theme:
    def __init__(self):
        self.tokens = ["num", "user", "role", "target", "votes", "wolves", "alive"]
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
        
    ### Role Names ###
    role_names = ["Villager", "Werewolf", "Seer", "Guardian", "Angel"]

    ### Game Text Messages ###

    #Message format: <group or command>_<action of group or command>_message
    #TODO: add tokens for chan messages, pvt notices, chan notices and formatting
    #$num is the number of times an action has been executed like join
    #$user gets replaced by the current user
    #$role gets the role of $user
    #$target gets replaced by who is targeted by current user
    #$votes gets replaced by current vote tallies
    #$wolves gets the names of the wolves
    #$alive gets the alive villagers

    #message when game starts
    game_start_message = ["$user started a new game!"]

    #message when someone new joins hunt
    join_new_message = ["$num. $user joined the hunt!"]
    
    #message when someone tries to rejoin the hunt
    join_old_message = ["You have already joined the hunt."]
    
    #message when the joining has ended
    join_ended_message = ["Sorry the joining has ended."]

    #message when the joining ends
    join_end_message = ["Joining ends."]

    #message when your role gets known
    role_wolf_message = ["You are a wolf. rAwr!!!"]
    role_seer_message = ["You are a seer."]
    role_guardian_message = ["You are a guardian."]
    role_angel_message = ["You are an Angel."]
    role_villager_message = ["You are a villager."]

    #message sent to wolf when there are more than one wolf
    role_other_wolf_message = ["Your brethren is $wolves."]
    role_other_wolves_message = ["Your brethren are: $wolves"]

    #message sent when there are more than one of special roles
    role_num_wolves_message = ["There are $num wolves."]
    role_num_seers_message = ["There are $num seers."]
    role_num_gaurdians_message = ["There are $num guardians."]
    role_num_angels_message = ["There are $num angels."]

    #message when joining succeeds
    join_success_message = ["Congratulations you have $num players in the hunt!"]

    #message when joining fails
    join_fail_message = ["Sorry not enough players have joined."]
    
    #message when voting starts
    vote_start_message = ["Voting has started. Type: !vote <target> to vote."]

    #message when validly voted
    vote_target_message = ["$user voted for $target. ($votes)"]

    #message when not valid vote
    vote_invalid_message = ["Sorry you can only vote during voting time."]
    
    #message when voting ends
    vote_end_message = ["Voting has ended"]

    #message when noone is killed by lynch vote
    vote_die_noone_message = ["Noone was voted for. The good thingies \
                               will not be happy"]
    
    #message when seer is killed by a lynch vote
    vote_die_seer_message = ["$target runs before the mob is organised, dashing \
                             away from the village. Tackled to the ground near \
                             to the lake, $target is tied to a log, screaming, \
                             and thrown into the water. With no means of escape,\
                             $target the Seer drowns, but as the villagers watch, \
                             tarot cards float to the surface and their mistake \
                             is all too apparent..."]
    
    #message when gaurdian is killed by a lynch vote
    vote_die_guardian_message = ["$target runs before the mob is organised, \
                                 running for the safety of home. Just before \
                                 reaching home, $target is hit with a large \
                                 stone, then another. With no means of escape, \
                                 $target is stoned to death, his body crushed. \
                                 One curious villager enters the house to find \
                                 proof that $target was a Guardian after all..."]
    
    #message when wolf is killed by a lynch vote
    vote_die_wolf_message = ["After coming to a decision, $target is quickly \
                             dragged from the crowd and dragged to the hanging \
                             tree. $target is strung up, and the block kicked \
                             from beneath their feet. There is a yelp of pain, \
                             but $target's neck doesn't snap, and fur begins to \
                             sprout from his/her body. A gunshot rings out, as \
                             a villager puts a silver bullet in the beast's \
                             head..."]
    
    #message when villager is killed by a lynch vote
    vote_die_villager_message = ["The air thick with adrenaline, the villagers \
                                 grab $target who struggles furiously, pleading \
                                 innocence, but the screams fall on deaf ears. \
                                 $target is dragged to the stake at the edge of \
                                 the village, and burned alive. But the \
                                 villagers shouts and cheers fade as they \
                                 realise the moon is already up - $target was \
                                 not a werewolf after all...",
                                "Realising the angry mob is turning, $target \
                                tries to run, but is quickly seized upon. $target\
                                is strung up to the hanging tree, and a hunter \
                                readies his rifle with a silver slug, as the \
                                block is kicked from beneath them. But there is \
                                a dull snap, and $target hangs, silent, \
                                motionless. The silent villagers quickly realise\
                                their grave mistake..."]

