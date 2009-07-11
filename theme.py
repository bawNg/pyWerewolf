#!/usr/bin/env python

from player import Role
from command_handler import Command

class Type:
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
        start           = 0 #message when a new game gets started
        started         = 1 #message when players tries to start game when one 
                            #is running alread
        join_starting   = 2 #message when player joins channel and game is in
                            #join phase
        join_running    = 3 #message when player joins channel and game is running
        join_none       = 4 #message when player joins channel and game is not running
        num             = 5 #num game subtypes

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
        not_night       = 2 #message when it's not night
        not_wolf        = 3 #message when you aren't a wolf
        invalid_format  = 4 #message when your kill command is invalidly formatted
        invalid_target  = 5 #message when your target isn't in the game
        invalid_target_wolf = 6 #message when your target is a wolf
        num             = 7 #num kill subtypes
        
    class See:      #see type subtypes
        success         = 0 #message when see command succeeds
        not_night       = 1 #message when it's not night
        not_seer        = 2 #message when you aren't a seer
        invalid_format  = 3 #message when your see command is invalidly formatted
        invalid_target  = 4 #message when your target isn't in the game
        result          = 5 #message to announce the result of your sightings
        num             = 6 #num see subtypes

    class Guard:    #guard type subtypes
        success         = 0 #message when guard command succeeds
        not_night       = 1 #message when it's not night
        not_guardian    = 2 #message when you aren't a guardian
        invalid_format  = 3 #message when your guard command is invalidly formatted
        invalid_target  = 4 #message when your target isn't in the game
        num             = 5 #num guard subtypes

    class Day:      #day type subtypes
        start   = 0 #message when day starts
        num     = 1 #num day subtypes
        
    class Vote:     #vote type subtypes
        start           = 0 #message when voting starts
        success         = 1 #message when vote command succeeds
        not_vote_time   = 2 #message when it's not voting time
        invalid_format  = 3 #message when yoru vote command is invalidly formatted
        invalid_target  = 4 #message when your target isn't in the game
        end             = 5 #message when voting ends
        tie             = 6 #message if there is a tie
        num             = 7 #num vote subtypes

    class Die:      #die type subtypes
        kill        = 0 #message to announce killing by wolves
        vote        = 1 #message to announce lynch killing
        not_voting  = 2 #message to announce death due to not voting for too many turns
        nick        = 3 #message to announce death due to nick change
        leave       = 4 #message to announce death due to leaving game
        num         = 5 #num die subtypes

    class Win:      #win type subtypes
        wolf        = 0 #message to announce win by wolves
        wolf_p      = 1 #same as above but plural
        villager    = 2 #message to announce win by villagers
        villager_p  = 3 #same as above but plural
        draw        = 4 #message to announce draw
        list_role   = 5 #message to announce player role
        list_role_p = 6 #same as above but plural
        num         = 7 #num win subtypes

    class Misc:     #misc type subtypes
        help        = 0 #message containing help information
        randplayer  = 1 #message to announce random player in game
        not_player  = 2 #message to tell user he's not in the game
        dead        = 3 #message to tell user he's dead
        num         = 4 #num misc subtypes
        
    #iterable list of types
    types = [(game, Game), (command, Command), (join, Join), (role, Role), 
             (night, Night), (kill, Kill), (see, See), (guard, Guard), 
             (day, Day), (vote, Vote), (die, Die), (win, Win), (misc, Misc)]
    
class Theme:
    def __init__(self):
        #custom command names
        self.commands = [None for i in xrange(Commands.num)]

        #create 3D array to hold messages
        self.messages = [[[None for k in xrange(Role.num)] 
                         for j in xrange(subtype.num)] 
                         for i, subtype in Type.types]

        ### MESSAGE TOKENS ###
        #TODO: add tokens for chan messages, pvt notices, chan notices and formatting
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
        m = self.messages#alias for messages
        t = Type    #alias for Type
        r = Role    #alias for Role

        ### GAME MESSAGES ###
        m[t.game][r.Game.start][r.noone]         = ["$user started a new game! "+
            "You have $num seconds to join!"]
        m[t.game][r.Game.started][r.noone]       = ["Game already running."]
        m[t.game][r.Game.join_starting][r.noone] = ["A game is starting. Type "+
            "!" + self.commands[Command.join] + " to join it."]
        m[t.game][r.Game.join_running][r.noone]  = ["A game is already running. "+
            " It should finish soon, then you can join the fun. :)"]
        m[t.game][r.Game.join_none][r.noone]     = ["No game is running. Start "+
            "one by typing: !" + self.commands[Command.start]]

        ### COMMAND MESSAGES ###
        m[t.command][r.Command.unknown][r.noone]          = 
            ["$target is an invalid command. Type !" + self.commands[Command.help] +
             "for help"]
        m[t.command][r.Command.game_not_running][r.noone] = 
            ["$target can only be used while a game is running. Start one by " +
             "typing !" + self.commands[Command.start]]

        ### JOIN MESSAGES ###
        m[t.join][r.Join.join][r.noone]     = [""]
        m[t.join][r.Join.rejoin][r.noone]   = [""]
        m[t.join][r.Join.leave][r.noone]    = [""]
        m[t.join][r.Join.nick][r.noone]     = [""]
        m[t.join][r.Join.ended][r.noone]    = [""]
        m[t.join][r.Join.end][r.noone]      = [""]
        m[t.join][r.Join.success][r.noone]  = [""]
        m[t.join][r.Join.fail][r.noone]     = [""]
        
        ### ROLE MESSAGES ###
        m[t.role][r.Role.announce][r.villager] = [""]
        m[t.role][r.Role.announce][r.wolf]     = [""]
        m[t.role][r.Role.announce][r.seer]     = [""]
        m[t.role][r.Role.announce][r.guardian] = [""]
        m[t.role][r.Role.announce][r.angel]    = [""]

        m[t.role][r.Role.other][r.wolf]     = [""]

        m[t.role][r.Role.other_p][r.villager] = [""]

        m[t.role][r.Role.count][r.wolf]     = [""]
        m[t.role][r.Role.count][r.seer]     = [""]
        m[t.role][r.Role.count][r.guardian] = [""]
        m[t.role][r.Role.count][r.angel]    = [""]

        m[t.role][r.Role.count_p][r.wolf]     = [""]
        m[t.role][r.Role.count_p][r.seer]     = [""]
        m[t.role][r.Role.count_p][r.guardian] = [""]
        m[t.role][r.Role.count_p][r.angel]    = [""]

        ### NIGHT MESSAGES ###
        m[t.night][r.Night.first][r.noone]     = [""]
        m[t.night][r.Night.subsequent][r.noone]     = [""]
        
        m[t.night][r.Night.task][r.wolf]     = [""]
        m[t.night][r.Night.task][r.seer]     = [""]
        m[t.night][r.Night.task][r.guardian] = [""]

        m[t.night][r.Night.task_p][r.wolf]     = [""]
        m[t.night][r.Night.task_p][r.seer]     = [""]
        m[t.night][r.Night.task_p][r.guardian] = [""]

        ### KILL MESSAGES ###
        m[t.kill][r.Kill.success][r.noone]              = [""]
        m[t.kill][r.Kill.success_p][r.noone]            = [""]
        m[t.kill][r.Kill.not_night][r.noone]            = [""]
        m[t.kill][r.Kill.not_wolf][r.noone]             = [""]
        m[t.kill][r.Kill.invalid_format][r.noone]       = [""]
        m[t.kill][r.Kill.invalid_target][r.noone]       = [""]
        m[t.kill][r.Kill.invalid_target_wolf][r.noone]  = [""]

        ### SEE MESSAGES ###
        m[t.see][r.See.success][r.noone]        = [""]
        m[t.see][r.See.not_night][r.noone]      = [""]
        m[t.see][r.See.not_seer][r.noone]       = [""]
        m[t.see][r.See.invalid_format][r.noone] = [""]
        m[t.see][r.See.invalid_target][r.noone] = [""]

        m[t.see][r.See.result][r.villager]  = [""]
        m[t.see][r.See.result][r.wolf]      = [""]
        m[t.see][r.See.result][r.seer]      = [""]
        m[t.see][r.See.result][r.guardian]  = [""]
        m[t.see][r.See.result][r.angel]     = [""]

        ### GUARD MESSAGES ###
        m[t.guard][r.Guard.success][r.noone]        = [""]
        m[t.guard][r.Guard.not_night][r.noone]      = [""]
        m[t.guard][r.Guard.not_guardian][r.noone]   = [""]
        m[t.guard][r.Guard.invalid_format][r.noone] = [""]
        m[t.guard][r.Guard.invalid_target][r.noone] = [""]
        
        ### DAY MESSAGES ###
        m[t.day][r.Day.start][r.noone]  = [""]

        ### VOTE MESSAGES ###
        m[t.vote][r.Vote.start][r.noone]            = [""]
        m[t.vote][r.Vote.success][r.noone]          = [""]
        m[t.vote][r.Vote.not_vote_time][r.noone]    = [""]
        m[t.vote][r.Vote.invalid_format][r.noone]   = [""]
        m[t.vote][r.Vote.invalid_target][r.noone]   = [""]
        m[t.vote][r.Vote.end][r.noone]              = [""]
        m[t.vote][r.Vote.tie][r.noone]              = [""]

        ### DIE MESSAGES ###
        m[t.die][r.Die.kill][r.villager]    = [""]
        m[t.die][r.Die.kill][r.wolf]        = [""]
        m[t.die][r.Die.kill][r.seer]        = [""]
        m[t.die][r.Die.kill][r.guardian]    = [""]
        
        m[t.die][r.Die.vote][r.villager]    = [""]
        m[t.die][r.Die.vote][r.wolf]        = [""]
        m[t.die][r.Die.vote][r.seer]        = [""]
        m[t.die][r.Die.vote][r.guardian]    = [""]
        m[t.die][r.Die.vote][r.angel]       = [""]
        
        m[t.die][r.Die.not_voting][r.villager]  = [""]
        m[t.die][r.Die.not_voting][r.wolf]      = [""]
        m[t.die][r.Die.not_voting][r.seer]      = [""]
        m[t.die][r.Die.not_voting][r.guardian]  = [""]
        m[t.die][r.Die.not_voting][r.angel]     = [""]
        
        m[t.die][r.Die.nick][r.villager]    = [""]
        m[t.die][r.Die.nick][r.wolf]        = [""]
        m[t.die][r.Die.nick][r.seer]        = [""]
        m[t.die][r.Die.nick][r.guardian]    = [""]
        m[t.die][r.Die.nick][r.angel]       = [""]
        
        m[t.die][r.Die.leave][r.villager]   = [""]
        m[t.die][r.Die.leave][r.wolf]       = [""]
        m[t.die][r.Die.leave][r.seer]       = [""]
        m[t.die][r.Die.leave][r.guardian]   = [""]
        m[t.die][r.Die.leave][r.angel]      = [""]
        
        ### WIN MESSAGES ###
        m[t.win][r.Win.wolf][r.noone]       = [""]
        m[t.win][r.Win.wolf_p][r.noone]     = [""]
        m[t.win][r.Win.villager][r.noone]   = [""]
        m[t.win][r.Win.villager_p][r.noone] = [""]
        m[t.win][r.Win.draw][r.noone]       = [""]
        
        m[t.win][r.Win.list_role][r.villager]   = [""]
        m[t.win][r.Win.list_role][r.wolf]       = [""]
        m[t.win][r.Win.list_role][r.seer]       = [""]
        m[t.win][r.Win.list_role][r.guardian]   = [""]
        m[t.win][r.Win.list_role][r.angel]      = [""]
        m[t.win][r.Win.list_role][r.traitor]    = [""]

        m[t.win][r.Win.list_role_p][r.villager]   = [""]
        m[t.win][r.Win.list_role_p][r.wolf]       = [""]
        m[t.win][r.Win.list_role_p][r.seer]       = [""]
        m[t.win][r.Win.list_role_p][r.guardian]   = [""]
        m[t.win][r.Win.list_role_p][r.angel]      = [""]
        m[t.win][r.Win.list_role_p][r.traitor]    = [""]

        ### MISC MESSAGES ###
        m[t.misc][r.Misc.help][r.noone]         = [""]
        m[t.misc][r.Misc.randplayer][r.noone]   = [""]
        m[t.misc][r.Misc.not_player][r.noone]   = [""]
        m[t.misc][r.Misc.dead][r.noone]         = [""]

