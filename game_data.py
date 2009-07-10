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
    
    #message when the joining ends
    join_end_message = ["Joining ends."]
    
    #message when joining succeeds
    join_success_message = ["Congratulations you have $num players in the hunt!"]

    #message when joining fails
    join_fail_message = ["Sorry not enough players have joined."]
    
    ### LYNCH MESSAGES ###
    
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
    
    ### KILL MESSAGES ###
    
    #message when villager is killed by a wolf
    kill_die_villager_message = ["The villagers gather the next morning in the \
                                 village center, but $target does not appear. \
                                 The villagers converge on $target's home and \
                                 find him/her decapitated in their bed. After \
                                 carrying the body to the church, the villagers,\
                                 now hysterical, return to the village center \
                                 to decide how to retaliate...",
    
                                "As some villagers begin to gather in the village \
                                center, a scream is heard from the direction of \
                                $target's house. The elderly villager who had \
                                screamed points to the fence, on top of which, \
                                the remains of $target are impaled, with his/her \
                                intestines spilling onto the cobbles. \
                                Apparently $target was trying to flee their \
                                attacker...",
    
                                "When the villagers gather at the village \
                                center, one comes running from the hanging tree,\
                                screaming at others to follow. When they arrive \
                                at the hanging tree, a gentle creaking echoes \
                                through the air as the body of $target swings \
                                gently in the breeze, its arms ripped off at \
                                the shoulders. It appears the attacker was not \
                                without a sense of irony...",
    
                                "As the village priest gathers the prayer books \
                                for the morning's sermon, he notices a trickle \
                                of blood snaking down the aisle. He looks upward\
                                to see $target impaled on the crucifix - the \
                                corpse has been gutted. He shouts for help, and \
                                the other villagers pile into the church and \
                                start arguing furiously..."]
    
    #message when seer is killed by a wolf
    kill_die_seer_message = ["The first villager to arrive at the center shrieks\
                             in horror - lying on the cobbles is a blood stained \
                             Ouija Board, and atop it sits $target's head. It \
                             appears $target the Seer had been seeking the \
                             guidance of the spirits to root out the wolves, \
                             but apparently the magic eight ball didn't see THIS\
                             one coming..."]
    
    #message when guardian is killed by a wolf
    kill_die_guardian_message = ["As one of the villagers passes $target's home,\
                                 he sees a bloody mess in front of the door. \
                                 After following the trail of blood and gore, \
                                 he finds $target's body torn \
                                 to pieces with herbs and powder flung all about.\
                                 It's too bad $target the Guardian was unable \
                                 to ward off these evil beings..."]
    
    #message when nobody is killed by a wolf
    kill_none_message = ["The villagers gather the next morning in the village \
                         center, to sighs of relief - it appears there was no \
                         attack the previous night."]