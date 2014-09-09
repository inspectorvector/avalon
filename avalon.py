import willie
import random
from threading import Timer

# Good and evil ratio for player amounts: if 5: 3g 2e, if 6: 4g 2e, if 7: 4g 3e, if 8: 5g 3e, if 9: 6g 3e, if 10: 6g 4e
# initially, special roles will be Merlin and Assassin only. Others will simply be Loyal servants of Arthur or the Minions of Mordred.

# fix game state stuff, SORT NOTIFICATIONS - evils need to know other evils

@willie.module.commands('init') # manually initializes stuff, as i couldn't get setup working.
def initialise(bot, trigger):
    bot.say('Initialised. You may now begin a new game of avalon. Type .avalon to start.')
    bot.seats_available = True
    bot.game_leader = None
    bot.people_seated = []
    bot.lsoa = [] # loyal servants of arthur: the good team
    bot.mom = [] # minions of mordred: the evil team
    bot.merlin = None
    bot.assassin = None
    bot.current_king = None
    bot.game_state = 'NOGAME'  # states for the game to be in: NOGAME, SIGNUPS, KING_CHOOSING, APPROVAL, ON_QUEST, ASSASSINATION
    bot.turn_order = []

@willie.module.commands('avalon')
def avalon(bot, trigger):
    if bot.game_state == 'NOGAME':
        bot.say('A game of Avalon is already underway.')
        return
    bot.game_state = 'SIGNUPS'
    bot.game_leader = trigger.nick
    bot.say(bot.game_leader + ' wants to play Avalon. Type .sit to take a seat at the round table. ' + bot.game_leader + ', type .start when everyone is ready to begin the game.')

@willie.module.commands('sit')
def sit(bot, trigger):
    if bot.game_state == 'SIGNUPS' and bot.seats_available:
        if trigger.nick not in bot.people_seated:
            bot.people_seated.append(trigger.nick)
            bot.say(trigger.nick + ' is now seated at the round table.')
            return
        elif trigger.nick in bot.people_seated:
            bot.say('You are already sat at the round table, ' + trigger.nick)
    else:
        bot.say('You may not sit at the round table at this time.')

@willie.module.commands('stand')
def stand(bot, trigger):
    if bot.game_state == 'SIGNUPS' and bot.seats_available:
        if trigger.nick in bot.people_seated:
            bot.people_seated.remove(trigger.nick)
            bot.say(trigger.nick + ' is no longer seated at the round table.')
            return
        elif trigger.nick not in bot.people_seated:
            bot.say('You are not sat at the round table, ' + trigger.nick)
    else:
        bot.say('You may not leave the round table at this time.')



@willie.module.commands('start')
def start(bot, trigger):
    if bot.game_leader == trigger.nick:
        bot.say('Welcome to a new game of Avalon!')
        bot.seats_available = False
        allocate_teams(bot, trigger)
        if not bot.seats_available:
            for name in bot.mom:
                if name == bot.assassin:
                    bot.msg(name, name + ', you are the feared ASSASSIN! (evil team). Tell no one.')
                else:
                    bot.msg(name, name + ', you are a Minion of Mordred (evil team). Your team mates are ' + 'Do not tell anyone!')
            for name in bot.lsoa:
                if bot.merlin == name:
                    bot.msg(name, name + ', you are the wizard Merlin (good team). The evil team members are ' + bot.mom[0:] + '. Do NOT reveal yourself! If the Minions of Mordred guess your identity, evil will win the game!')
                bot.msg(name, name + ', you are a Loyal Servant of Arthur (good team).')
        first_king(bot, trigger)

    else:
        bot.say('You are not the current game leader, or a game of Avalon has not been started.')


def first_king(bot, trigger):
    bot.turn_order = bot.people_seated
    random.shuffle(bot.turn_order)
    bot.say(bot.turn_order[0] + ' , you shall be the first king!')


def allocate_teams(bot, trigger):
    random.shuffle(bot.people_seated)
    if len(bot.people_seated) < 5:
        bot.say('Sorry, not enough people are seated at the round table for a game to be played.')
        initialise(bot, trigger)
        return
    elif len(bot.people_seated) > 10:
        bot.say('Too many adventurers! A maximum of ten players can go on the quest.')
    elif len(bot.people_seated) == 5:
        bot.lsoa = bot.people_seated[0:3]
        bot.mom = bot.people_seated[3:5]
    elif len(bot.people_seated) == 6:
        bot.lsoa = bot.people_seated[0:4]
        bot.mom = bot.people_seated[4:6]
    elif len(bot.people_seated) == 7:
        bot.lsoa = bot.people_seated[0:4]
        bot.mom = bot.people_seated[4:7]
    elif len(bot.people_seated) == 8:
        bot.lsoa = bot.people_seated[0:5]
        bot.mom = bot.people_seated[5:8]
    elif len(bot.people_seated) == 9:
        bot.lsoa = bot.people_seated[0:6]
        bot.mom = bot.people_seated[6:9]
    elif len(bot.people_seated) == 10:
        bot.lsoa = bot.people_seated[0:6]
        bot.mom = bot.people_seated[6:10]
    bot.merlin = bot.lsoa[0]
    bot.assassin = bot.mom[0]