#!/usr/bin/env python

from player import Role
from command_handler import Command
import random

class ThemeMessageType:
    game        = 0     #messages relating to the game
    command     = 1     #messages relating to commands
    join        = 2     #messages relating to joining the game and the join command
    role        = 3     #messages relating to assigning the roles
    night       = 4     #messages relating to the night phase
    kill        = 5     #messages relating to the kill command
    see         = 6     #messages relating to the see command
    guard       = 7     #messages relating to the guard command
    day         = 8     #messages relating to the day phase
    vote        = 9     #messages relating to voting and the vote command
    die         = 10    #messages relating to players dying
    win         = 11    #messages relating to the winning of the game
    misc        = 12    #miscellaneous messages
    num         = 13    #num message types

    class Game:     #game type subtypes
        start_none      = 0 #message when a new game gets started
        start_starting  = 1 #message when a player tries to start a game
                            #when a current one is in the join phase
        start_running   = 2 #message when a player tries to start a game
                            #when on is running
        join_none       = 3 #message when player joins channel and game is not running
        join_starting   = 4 #message when player joins channel and game is in
                            #join phase
        join_running    = 5 #message when player joins channel and game is running
        num             = 6 #num game subtypes

    class Command:  #command type subtypes
        unknown          = 0 #message when you enter an unknown command
        game_not_running = 1 #message when you enter a game command when a game
                             #isn't running
        num              = 2 #num command subtypes

    class Join:     #join type subtypes
        join    = 0 #message when you successfully join a game
        rejoin  = 1 #message when you try to join a game you already joined
        leave   = 2 #message when you leave a game in the joining phase
        nick    = 3 #message when you change your nick in joining phase
        ended   = 4 #message when you try to join when joining has ended
        end     = 5 #message when joining ends
        success = 6 #message when enough players have joined
        fail    = 7 #message when not enough players have joined
        num     = 8 #num join subtypes

    class Role:     #role type subtypes
        announce    = 0 #message to announce roles to players
        other       = 1 #message to tell other player of same role to player
        other_p     = 2 #same as above but plural
        count       = 3 #message to announce the number of each role
        count_p     = 4 #same as above but plural
        num         = 5 #num role subtypes

    class Night:    #night type subtypes
        first       = 0 #message when first night starts
        subsequent  = 1 #message when subsequent nights start
        task        = 2 #message to ask player to fullfil their task
        task_p      = 3 #same as above but plural
        num         = 4 #num night subtypes

    class Kill:     #kill type subtypes
        success         = 0 #message when kill command succeeds
        success_p       = 1 #same as above but plural
        fail            = 2 #message when kill fails due to player ability
        fail_p          = 3 #same as above but plural
        not_night       = 4 #message when it's not night
        not_wolf        = 5 #message when you aren't a wolf
        invalid_format  = 6 #message when your kill command is invalidly formatted
        invalid_target  = 7 #message when your target isn't in the game
        invalid_target_wolf = 8 #message when your target is a wolf
        invalid_target_dead = 9 #message when your target is dead
        num             = 10 #num kill subtypes
        
    class See:      #see type subtypes
        success         = 0 #message when see command succeeds
        not_night       = 1 #message when it's not night
        not_seer        = 2 #message when you aren't a seer
        invalid_format  = 3 #message when your see command is invalidly formatted
        invalid_target  = 4 #message when your target isn't in the game
        invalid_target_dead = 5 #message when your target is dead
        result          = 6 #message to announce the result of your sightings
        num             = 7 #num see subtypes

    class Guard:    #guard type subtypes
        success         = 0 #message when guard command succeeds
        not_night       = 1 #message when it's not night
        not_guardian    = 2 #message when you aren't a guardian
        invalid_format  = 3 #message when your guard command is invalidly formatted
        invalid_target  = 4 #message when your target isn't in the game
        invalid_target_dead = 5 #message when your target is dead
        num             = 6 #num guard subtypes

    class Day:      #day type subtypes
        start   = 0 #message when day starts
        num     = 1 #num day subtypes
        
    class Vote:     #vote type subtypes
        start           = 0 #message when voting starts
        success         = 1 #message when vote command succeeds
        not_vote_time   = 2 #message when it's not voting time
        invalid_format  = 3 #message when yoru vote command is invalidly formatted
        invalid_target  = 4 #message when your target isn't in the game
        invalid_target_dead = 5 #message when your target is dead
        end             = 6 #message when voting ends
        tie             = 7 #message if there is a tie
        num             = 8 #num vote subtypes

    class Die:      #die type subtypes
        kill        = 0 #message to announce killing by wolves
        vote        = 1 #message to announce lynch killing
        not_voting  = 2 #message to announce death due to not voting for too many turns
        nick        = 3 #message to announce death due to nick change
        leave       = 4 #message to announce death due to leaving game
        num         = 5 #num die subtypes

    class Win:      #win type subtypes
        win         = 0 #message to announce the winning of a group
        win_p       = 1 #same as above but plural
        list_role   = 2 #message to announce player role
        list_role_p = 3 #same as above but plural
        num         = 4 #num win subtypes

    class Misc:     #misc type subtypes
        help        = 0 #message containing help information
        randplayer  = 1 #message to announce random player in game
        not_player  = 2 #message to tell user he's not in the game
        dead        = 3 #message to tell user he's dead
        alive_players = 4 #message to tell everyone who is alive
        num         = 5 #num misc subtypes
        
    #iterable list of types
    types = [(game, Game), (command, Command), (join, Join), (role, Role), 
             (night, Night), (kill, Kill), (see, See), (guard, Guard), 
             (day, Day), (vote, Vote), (die, Die), (win, Win), (misc, Misc)]

class ThemeMessageDest: #the destination of a message
    public      = 0 #everyone sees this message
    announce    = 1 #an announcement to everyone
    private     = 2 #only the user sees this message

class Theme:
    def __init__(self):
        #custom command names
        self.commands = [None for i in xrange(Command.num)]

        #create 3D array to hold messages
        self.messages = [[[None for k in xrange(Role.num)] 
                         for j in xrange(subtype.num)] 
                         for i, subtype in ThemeMessageType.types]

        #Message format: -list of possible messages
        #                -each message is a list of lines
        #                -each line is 2-tuple where the first item is the type and 
        #                 second is the actual text

        ### MESSAGE TOKENS ###
        #TODO: add tokens for formatting
        #$bot is the name of the bot
        #$num is the number of times an action has been executed like join
        #$user gets replaced by the current user
        #$target gets replaced by who is targeted by current user
        #$votes gets replaced by current vote tallies
        #$roles gets the names of the roles
        #$alive gets the alive villagers

        ### GAME TOKENS ###
        #$user is the user who sent the command

        ### COMMAND TOKENS ###
        #$user is the user who sent the command
        #$target is the name of the command

        ### JOIN TOKENS ###
        #$user is the user who called the command
        #$num is the num players who have joined the game (so far)

        ### ROLE TOKENS ###
        #$user is the user who is recieving the message
        #$num is the number of players of that role

        ### NIGHT TOKENS ###
        #$bot is the name of the bot

        ### KILL $ SEE $ GUARD TOKENS ###
        #$user is the person issuing the command
        #$target is the target of the user's command
        
        ### DAY TOKENS ###
        #$num is the time left for talking
        
        ### VOTE TOKENS ###
        #$user is the person issuing the command
        #$target is the target of the user's command
        #$votes is the tally of the votes so far

        ### DIE TOKENS ###
        #$target is the target of the killing

        ### WIN TOKENS ###
        #$roles are the list of players with the perticular role

        ### MISC TOKENS ###
        #$user is person calling the command
        #$target is the result of the command
        #$alive is the list of all players who are alive

    def get_message(self, type, subtype, role = Role.noone):
        temp = self.messages[type][subtype][role]
        i = random.randint(0, len(temp)-1)
        return temp[i]

class WerewolfTheme(Theme):
    def __init__(self):
        Theme.__init__(self)
        self.commands[Command.start]        = "start"
        self.commands[Command.help]         = "help"
        self.commands[Command.join]         = "join"
        self.commands[Command.leave]        = "leave"
        self.commands[Command.kill]         = "kill"
        self.commands[Command.guard]        = "guard"
        self.commands[Command.see]          = "see"
        self.commands[Command.vote]         = "vote"
        self.commands[Command.randplayer]   = "randplayer"
        self.commands[Command.admin]        = "admin"

        m   = self.messages     #alias for messages
        t   = ThemeMessageType  #alias for ThemeMessageType
        r   = Role              #alias for Role
        d   = ThemeMessageDest  #alias for ThemeMessageDest

        ### GAME MESSAGES ###
        m[t.game][t.Game.start_none][r.noone] = \
            [[(d.public,    "$user started a new game! You have $num "+
                            "seconds to join!")]]
        m[t.game][t.Game.start_starting][r.noone] = \
            [[(d.private,   "A game is already running. Join it while still can!")]]
        m[t.game][t.Game.start_running][r.noone] = \
            [[(d.private,   "A game is already running.")]]
        m[t.game][t.Game.join_none][r.noone] = \
            [[(d.private,   "No game is running. Start one by typing: !" + 
                            self.commands[Command.start])]]
        m[t.game][t.Game.join_starting][r.noone] = \
            [[(d.private,   "A game is starting. Type " + 
                            self.commands[Command.join] + " to join it.")]]
        m[t.game][t.Game.join_running][r.noone] = \
            [[(d.private,   "A game is already running. It should finish soon, "+
                            "then you can join the fun. :)")]]

        ### COMMAND MESSAGES ###
        m[t.command][t.Command.unknown][r.noone] = \
            [[(d.private,   "$target is an invalid command. Type !" + 
                            self.commands[Command.help] + " for help")]]
        m[t.command][t.Command.game_not_running][r.noone] = \
            [[(d.private,   "$target can only be used while a game is running. "+
                            "Start one by typing !" + self.commands[Command.start])]]

        ### JOIN MESSAGES ###
        m[t.join][t.Join.join][r.noone] = \
            [[(d.public,    "$num. $user joined the hunt!")]]
        m[t.join][t.Join.rejoin][r.noone] = \
            [[(d.private,   "You have already joined the hunt.")]]
        m[t.join][t.Join.leave][r.noone] = \
            [[(d.public,    "$target has left the hunt.")]]
        m[t.join][t.Join.nick][r.noone] = \
            [[(d.public,    "$target has left the hunt.")]]
        m[t.join][t.Join.ended][r.noone] = \
            [[(d.private,   "Sorry the joining has ended.")]]
        m[t.join][t.Join.end][r.noone] = \
            [[(d.public,    "Joining ends.")]]
        m[t.join][t.Join.success][r.noone] = \
            [[(d.public,    "Congratulations, you have $num players in the hunt!")]]
        m[t.join][t.Join.fail][r.noone] = \
            [[(d.public,    "Sorry not enough players have joined.")]]
        
        ### ROLE MESSAGES ###
        m[t.role][t.Role.announce][r.villager] = \
            [[(d.private,   "You are a villager.")]]
        m[t.role][t.Role.announce][r.wolf] = \
            [[(d.private,   "You are a werewolf. rAwr!!!")]]
        m[t.role][t.Role.announce][r.seer] = \
            [[(d.private,   "You are a seer.")]]
        m[t.role][t.Role.announce][r.guardian] = \
            [[(d.private,   "You are a guardian.")]]
        m[t.role][t.Role.announce][r.angel] = \
            [[(d.private,   "You are an angel.")]]

        m[t.role][t.Role.other][r.wolf] = \
            [[(d.private,   "Your brethren is $wolves.")]]
        m[t.role][t.Role.other_p][r.wolf] = \
            [[(d.private,   "Your brethren are: $wolves")]]

        m[t.role][t.Role.count][r.villager] = \
            [[(d.public,    "There is $num villager.")]]
        m[t.role][t.Role.count][r.wolf] = \
            [[(d.public,    "There is $num werewolf.")]]
        m[t.role][t.Role.count][r.seer] = \
            [[(d.public,    "There is $num seer.")]]
        m[t.role][t.Role.count][r.guardian] = \
            [[(d.public,    "There is $num guardian.")]]
        m[t.role][t.Role.count][r.angel] = \
            [[(d.public,    "There is $num angel.")]]
        m[t.role][t.Role.count][r.traitor] = \
            [[(d.public,    "There is $num traitor.")]]

        m[t.role][t.Role.count_p][r.villager] = \
            [[(d.public,    "There are $num villagers.")]]
        m[t.role][t.Role.count_p][r.wolf] = \
            [[(d.public,    "There are $num werewolves.")]]
        m[t.role][t.Role.count_p][r.seer] = \
            [[(d.public,    "There are $num seers.")]]
        m[t.role][t.Role.count_p][r.guardian] = \
            [[(d.public,    "There are $num guardians.")]]
        m[t.role][t.Role.count_p][r.angel] = \
            [[(d.public,    "There are $num angels.")]]
        m[t.role][t.Role.count_p][r.traitor] = \
            [[(d.public,    "There are $num traitors.")]]

        ### NIGHT MESSAGES ###
        m[t.night][t.Night.first][r.noone] = \
            [[(d.public,    "Night descends over the unsuspecting village.")]]
        m[t.night][t.Night.subsequent][r.noone] = \
            [[(d.public,    "Villagers goes to an uneasy sleep.")]]
        
        m[t.night][t.Night.task][r.wolf] = \
            [[(d.public,    "Werewolf type: /msg $bot " + 
                            self.commands[Command.kill] + 
                            " <target> to kill. You have $num seconds.")]]
        m[t.night][t.Night.task][r.seer] = \
            [[(d.public,    "Seer type: /msg $bot " + 
                            self.commands[Command.see] + 
                            " <target> to see. You have $num seconds.")]]
        m[t.night][t.Night.task][r.guardian] = \
            [[(d.public,    "Guardian type: /msg $bot " + 
                            self.commands[Command.guard] + 
                            " <target> to guard. You have $num seconds.")]]

        m[t.night][t.Night.task_p][r.wolf] = \
            [[(d.public,    "Werewolves type: /msg $bot " + 
                            self.commands[Command.kill] + 
                            " <target> to kill. You have $num seconds.")]]
        m[t.night][t.Night.task_p][r.seer] = \
            [[(d.public,    "Seers type: /msg $bot " + 
                            self.commands[Command.see] + 
                            " <target> to see. You have $num seconds.")]]
        m[t.night][t.Night.task_p][r.guardian] = \
            [[(d.public,    "Guardians type: /msg $bot " + 
                            self.commands[Command.guard] + 
                            " <target> to guard. You have $num seconds.")]]

        ### KILL MESSAGES ###
        m[t.kill][t.Kill.success][r.noone] = \
            [[(d.private,   "You have selected $target for your feast.")]]
        m[t.kill][t.Kill.success_p][r.noone] = \
            [[(d.private,   "You have selected $target for your feast, but must "+
                            "wait for brethren to vote.")]]

        m[t.kill][t.Kill.fail][r.guard] = \
            [[(d.private,   "As you approach $target an unknown guardian "+
                            "chases you away with wolf's bane.")]]
        m[t.kill][t.Kill.fail][r.angel] = \
            [[(d.private,   "As you approach $target, they pull out the wolf's "+
                            "bane and you flee.")]]

        m[t.kill][t.Kill.fail_p][r.guard] = \
            [[(d.private,   "As your pack approaches $target an unknown guardian "+
                            "chases you away with wolf's bane.")]]
        m[t.kill][t.Kill.fail_p][r.angel] = \
            [[(d.private,   "As your pack approaches $target, they pull out "+
                            "the wolf's bane and you flee.")]]

        m[t.kill][t.Kill.not_night][r.noone] = \
            [[(d.private,   "You can only kill at night.")]]
        m[t.kill][t.Kill.not_wolf][r.noone] = \
            [[(d.private,   "You aren't a werewolf. Only werewolves can kill.")]]
        m[t.kill][t.Kill.invalid_format][r.noone] = \
            [[(d.private,   "Your " + self.commands[Command.kill] + 
                            " command was invalidly formated.")]]
        m[t.kill][t.Kill.invalid_target][r.noone] = \
            [[(d.private,   "$target isn't a player in the game.")]]
        m[t.kill][t.Kill.invalid_target_wolf][r.noone] = \
            [[(d.private,   "$target is one of your brethren you can't "+
                            "attack them.")]]
        m[t.kill][t.Kill.invalid_target_dead][r.noone] = \
            [[(d.private,   "$target is dead. You can't kill them twice.")]]

        ### SEE MESSAGES ###
        m[t.see][t.See.success][r.noone] = \
            [[(d.private,   "Your predictions will be revealed to you at dawn.")]]
        m[t.see][t.See.not_night][r.noone] = \
            [[(d.private,   "You can only see at night.")]]
        m[t.see][t.See.not_seer][r.noone] = \
            [[(d.private,   "You aren't a seer.")]]
        m[t.see][t.See.invalid_format][r.noone] = \
            [[(d.private,   "Your " + self.commands[Command.kill] + 
                            " command was invalidly formated.")]]
        m[t.see][t.See.invalid_target][r.noone] = \
            [[(d.private,   "$target isn't a player in the game.")]]
        m[t.see][t.See.invalid_target_dead][r.noone] = \
            [[(d.private,   "$target is dead. You don't need to see their "+
                            " true intentions.")]]

        m[t.see][t.See.result][r.villager] = \
            [[(d.private,   "$target is a villager.")]]
        m[t.see][t.See.result][r.wolf] = \
            [[(d.private,   "$target is a filthy werewolf.")]]
        m[t.see][t.See.result][r.seer] = \
            [[(d.private,   "$target is a seer.")]]
        m[t.see][t.See.result][r.guardian] = \
            [[(d.private,   "$target is a guardian.")]]
        m[t.see][t.See.result][r.angel] = \
            [[(d.private,   "$target is an angel.")]]

        ### GUARD MESSAGES ###
        m[t.guard][t.Guard.success][r.noone] = \
            [[(d.private,   "You have chosen to guard $target from werewolf "+
                            "attacks.")]]
        m[t.guard][t.Guard.not_night][r.noone] = \
            [[(d.private,   "You can only guard at night.")]]
        m[t.guard][t.Guard.not_guardian][r.noone] = \
            [[(d.private,   "You aren't a guardian.")]]
        m[t.guard][t.Guard.invalid_format][r.noone] = \
            [[(d.private,   "Your " + self.commands[Command.guard] + 
                            " command was invalidly formated.")]]
        m[t.guard][t.Guard.invalid_target][r.noone] = \
            [[(d.private,   "$target isn't a player in the game.")]]
        m[t.guard][t.Guard.invalid_target_dead][r.noone] = \
            [[(d.private,   "$target is dead. The dead don't need protection.")]]
        
        ### DAY MESSAGES ###
        m[t.day][t.Day.start][r.noone] = \
            [[(d.public,    "The villagers gather. You have $num seconds to "+
                            "make your accusations.")]]

        ### VOTE MESSAGES ###
        m[t.vote][t.Vote.start][r.noone] = \
            [[(d.public,    "Voting has started. Type: !"+ 
                            self.commands[Command.vote] + " <target> to vote for"+
                            "<target>. You have $num seconds to vote.")]]
        m[t.vote][t.Vote.success][r.noone] = \
            [[(d.public,    "$user voted for $target. ($votes)")]]
        m[t.vote][t.Vote.not_vote_time][r.noone] = \
            [[(d.private,   "Sorry you can only vote during voting time.")]]
        m[t.vote][t.Vote.invalid_format][r.noone] = \
            [[(d.private,   "Your " + self.commands[Command.vote] + 
                            " command was invalidly formated.")]]
        m[t.vote][t.Vote.invalid_target][r.noone] = \
            [[(d.private,   "$target isn't a player in the game.")]]
        m[t.vote][t.Vote.invalid_target_dead][r.noone] = \
            [[(d.private,   "$target is dead. You can't lynch the dead.")]]
        m[t.vote][t.Vote.end][r.noone] = \
            [[(d.public,    "Voting has ended. Tallying votes...")]]
        m[t.vote][t.Vote.tie][r.noone] = \
            [[(d.public,    "There was a tie, randomly choosing target.")]]

        ### DIE MESSAGES ###
        m[t.die][t.Die.kill][r.villager] = \
            [[(d.public,    "The villagers gather the next morning "+
                            "in the village center, but $target "+
                            "does not appear. The villagers "+
                            "converge on $target's home and find "+
                            "them decapitated in their bed. After "+
                            "carrying the body to the church, the "+
                            "villagers, now hysterical, return to "+
                            "the village center to decide how to "+
                            "retaliate..."),
              (d.public,    "$target the villager was killed.")],

             [(d.public,    "As some villagers begin to gather in "+
                            "the village center, a scream is "+
                            "heard from the direction of $target's "+
                            "house. The elderly villager who had "+
                            "screamed points to the fence, on top "+
                            "of which, the remains of $target are "+
                            "impaled, with their intestines "+
                            "spilling onto the cobbles. "+
                            "Apparently $target was trying to flee "+
                            "their attacker..."),
              (d.public,    "$target the villager was killed.")],

             [(d.public,    "When the villagers gather at the "+
                            "village center, one comes running from "+
                            "the hanging tree, screaming at others "+
                            "to follow. When they arrive at the "+
                            "hanging tree, a gentle creaking echoes "+
                            "through the air as the body of $target "+
                            "swings gently in the breeze, its arms "+
                            "ripped off at the shoulders. It appears "+
                            "the attacker was not without a sense of "+
                            "irony..."),
              (d.public,    "$target the villager was killed.")],

             [(d.public,    "As the village priest gathers the "+
                            "prayer books for the morning's sermon, "+
                            "he notices a trickle of blood snaking "+
                            "down the aisle. He looks upward "+
                            "to see $target impaled on the crucifix "+
                            "- the corpse has been gutted. He "+
                            "shouts for help, and the other "+
                            "villagers pile into the church and "+
                            "start arguing furiously..."),
              (d.public,    "$target the villager was killed.")]]
        m[t.die][t.Die.kill][r.seer] = \
            [[(d.public,    "The first villager to arrive at the "+
                            "center shrieks in horror - lying on the "+
                            "cobbles is a blood stained Ouija Board, "+
                            "and atop it sits $target's head. It "+
                            "appears $target the Seer had been seeking "+
                            "the guidance of the spirits to root out "+
                            "the wolves, but apparently the magic "+
                            "eight ball didn't see THIS one coming..."),
              (d.public,    "$target the seer was killed.")]]
        m[t.die][t.Die.kill][r.guardian] = \
            [[(d.public,    "As one of the villagers passes "+
                            "$target's home, he sees a bloody "+
                            "mess in front of the door. After "+
                            "following the trail of blood and gore, "+
                            "he finds $target's body torn to pieces "+
                            "with herbs and powder flung all about. "+
                            "It's too bad $target the Guardian was "+
                            "unable to ward off these evil beings..."),
              (d.public,    "$target the guardian was killed.")]]
        m[t.die][t.Die.kill][r.noone] = \
            [[(d.public,    "The villagers gather the next morning in "+
                            "the village center, to sighs of relief - "+
                            "it appears there was no attack the "+
                            "previous night.")]]
        
        m[t.die][t.Die.vote][r.villager] = \
            [[(d.public,    "The air thick with adrenaline, the "+
                            "villagers grab $target who struggles "+
                            "furiously, pleading innocence, but "+
                            "the screams fall on deaf ears. "+
                            "$target is dragged to the stake at "+
                            "the edge of the village, and burned "+
                            "alive. But the villagers shouts and "+
                            "cheers fade as they realise the moon "+
                            "is already up - $target was not a "+
                            "werewolf after all..."),
              (d.public,    "$target the villager was killed.")],

             [(d.public,    "Realising the angry mob is turning, "+
                            "$target tries to run, but is quickly "+
                            "seized upon. $target is strung up to "+
                            "the hanging tree, and a hunter readies "+
                            "his rifle with a silver slug, as the "+
                            "block is kicked from beneath them. "+
                            "But there is a dull snap, and $target "+
                            "hangs, silent, motionless. The silent "+
                            "villagers quickly realise their grave "+
                            "mistake..."),
              (d.public,    "$target the villager was killed.")]]
        m[t.die][t.Die.vote][r.wolf] = \
            [[(d.public,    "After coming to a decision, $target is "+
                            "quickly dragged from the crowd and "+
                            "dragged to the hanging tree. $target is "+
                            "strung up, and the block kicked from "+
                            "beneath their feet. There is a yelp of "+
                            "pain, but $target's neck doesn't snap, "+
                            "and fur begins to sprout from his/her "+
                            "body. A gunshot rings out, as a "+
                            "villager puts a silver bullet in the "+
                            "beast's head..."),
              (d.public,    "$target the werewolf was killed.")]]
        m[t.die][t.Die.vote][r.seer] = \
            [[(d.public,    "$target runs before the mob is organised, "+
                            "dashing away from the village. Tackled to "+
                            "the ground near the lake, $target is tied "+
                            "to a log, screaming, thrown into the water. "+
                            "With no means of escape, $target the Seer "+
                            "drowns, but as the villagers watch, cards "+
                            "float to the surface and their mistake "+
                            "is all too apparent..."),
              (d.public,    "$target the seer was killed.")]]
        m[t.die][t.Die.vote][r.guardian] = \
            [[(d.public,    "$target runs before the mob is "+ 
                            "organised, running for the safety "+
                            "of home. Just before reaching home, "+
                            "$target is hit with a large stone, "+
                            "then another. With no means of escape, "+
                            "$target is stoned to death, his body "+
                            "crushed. One curious villager enters "+
                            "the house to find proof that $target "+
                            "was a Guardian after all..."),
              (d.public,    "$target the guardian was killed.")]]
        m[t.die][t.Die.vote][r.angel] = \
            [[(d.public,    "$target the angel is killed by the angry mob."),
              (d.public,    "$target the angel was killed.")]]
        m[t.die][t.Die.vote][r.noone] = \
            [[(d.public,    "Noone was voted for. The good thingies "+
                            "will not be happy")]]
        
        m[t.die][t.Die.not_voting][r.villager] = \
            [[(d.public,    "$target the villager died for defying "+
                            "the good."),
              (d.public,    "$target the villager has died.")]]
        m[t.die][t.Die.not_voting][r.wolf] = \
            [[(d.public,    "$target the werewolf died for defying "+
                            "the good."),
              (d.public,    "$target the werewolf has died.")]]
        m[t.die][t.Die.not_voting][r.seer] = \
            [[(d.public,    "$target the seer died for defying "+
                            "the good."),
              (d.public,    "$target the seer has died.")]]
        m[t.die][t.Die.not_voting][r.guardian] = \
            [[(d.public,    "$target the guardian died for "+
                            "defying the good."),
              (d.public,    "$target the guardian has died.")]]
        m[t.die][t.Die.not_voting][r.angel] = \
            [[(d.public,    "$target the angel died for defying "+
                            "the good."),
              (d.public,    "$target the angel has died.")]]
        
        m[t.die][t.Die.nick][r.villager] = \
            [[(d.public,    "$target the villager got killed for "+
                            "changing nicks."),
              (d.public,    "$target the villager has died.")]]
        m[t.die][t.Die.nick][r.wolf] = \
            [[(d.public,    "$target the werewolf got killed for changing "+
                            "nicks."),
              (d.public,    "$target the werewolf has died.")]]
        m[t.die][t.Die.nick][r.seer] = \
            [[(d.public,    "$target the seer got killed for changing "+
                            "nicks."),
              (d.public,    "$target the seer has died.")]]
        m[t.die][t.Die.nick][r.guardian] = \
            [[(d.public,    "$target the guardian got killed for "+
                            "changing nicks."),
              (d.public,    "$target the guardian has died.")]]
        m[t.die][t.Die.nick][r.angel] = \
            [[(d.public,    "$target the angel got killed for changing "+
                            "nicks."),
              (d.public,    "$target the angel has died.")]]
        
        m[t.die][t.Die.leave][r.villager] = \
            [[(d.public,    "$target the villager got killed for "+
                            "leaving the game."),
              (d.public,    "$target the villager has died.")]]
        m[t.die][t.Die.leave][r.wolf] = \
            [[(d.public,    "$target the werewolf got killed for "+
                            "leaving the game."),
              (d.public,    "$target the werewolf has died.")]]
        m[t.die][t.Die.leave][r.seer] = \
            [[(d.public,    "$target the seer got killed for leaving "+
                            "the game."),
              (d.public,    "$target the seer has died.")]]
        m[t.die][t.Die.leave][r.guardian] = \
            [[(d.public,    "$target the guardian got killed for "+
                            "leaving the game."),
              (d.public,    "$target the guardian has died.")]]
        m[t.die][t.Die.leave][r.angel] = \
            [[(d.public,    "$target the angel got killed for "+
                            "leaving the game."),
              (d.public,    "$target the angel has died.")]]
        
        ### WIN MESSAGES ###
        m[t.win][t.Win.win][r.wolf] = \
            [[(d.public,    "The werewolf has won.")]]
        m[t.win][t.Win.win_p][r.wolf] = \
            [[(d.public,    "The werewolves have won.")]]
        m[t.win][t.Win.win][r.villager] = \
            [[(d.public,    "The villager has won.")]]
        m[t.win][t.Win.win_p][r.villager] = \
            [[(d.public,    "The villagers have won.")]]
        m[t.win][t.Win.win][r.noone] = \
            [[(d.public,    "No one is left alive. The town is desolate. "+
                            "The game ends in adraw.")]]
        
        m[t.win][t.Win.list_role][r.villager] = \
            [[(d.public,    "The villager was: $roles")]]
        m[t.win][t.Win.list_role][r.wolf] = \
            [[(d.public,    "The werewolf was: $roles")]]
        m[t.win][t.Win.list_role][r.seer] = \
            [[(d.public,    "The seer was: $roles")]]
        m[t.win][t.Win.list_role][r.guardian] = \
            [[(d.public,    "The guardian was: $roles")]]
        m[t.win][t.Win.list_role][r.angel] = \
            [[(d.public,    "The angel was: $roles")]]
        m[t.win][t.Win.list_role][r.traitor] = \
            [[(d.public,    "The traitor was: $roles")]]

        m[t.win][t.Win.list_role_p][r.villager] = \
            [[(d.public,    "The villagers were: $roles")]]
        m[t.win][t.Win.list_role_p][r.wolf] = \
            [[(d.public,    "The werewolves were: $roles")]]
        m[t.win][t.Win.list_role_p][r.seer] = \
            [[(d.public,    "The seers were: $roles")]]
        m[t.win][t.Win.list_role_p][r.guardian] = \
            [[(d.public,    "The guardian were: $roles")]]
        m[t.win][t.Win.list_role_p][r.angel] = \
            [[(d.public,    "The angels were: $roles")]]
        m[t.win][t.Win.list_role_p][r.traitor] = \
            [[(d.public,    "The traitors were: $roles")]]

        ### MISC MESSAGES ###
        m[t.misc][t.Misc.help][r.noone] = \
            [[(d.private,   "To start of a game of Werewolf type: !"+
                            self.commands[Command.start]),
              (d.private,   "To join a running game, while joins are being "+
                            "accepted, type: !"+
                            self.commands[Command.join]),
              (d.private,   "While a game is running and talking is "+
                            "allowed, to name a random player type: !"+
                            self.commands[Command.randplayer]),
              (d.private,   "The rest of the commands will be explained "+
                            "in the game.")]]
        m[t.misc][t.Misc.randplayer][r.noone] = \
            [[(d.public,    "The random player is: $target")]]
        m[t.misc][t.Misc.not_player][r.noone] = \
            [[(d.private,   "Sorry, you aren't a player of the current game. "+
                            "Join the next game to be part of the fun!")]]
        m[t.misc][t.Misc.dead][r.noone] = \
            [[(d.private,   "Sorry, the dead can't do anything.")]]
        m[t.misc][t.Misc.alive_players][r.noone] = \
            [[(d.private,   "The alive players are: $alive")]]


