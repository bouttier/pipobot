#! /usr/bin/env python
#-*- coding: utf-8 -*-
import random
from lib.modules import SyncModule, answercmd

class CmdRPS(SyncModule):
    def __init__(self, bot):
        desc = """Rock Paper Scissors:
rps init : lance une nouvelle partie
rps bot : pour se mesurer au bot !!!
rps (Rock|Paper|Scissor) : pour jouer"""
        SyncModule.__init__(bot, 
                                    desc = desc,
                                    command = "rps")
        self.choices = ["Rock", "Paper", "Scissors"]
        self.players = 0
        self.manche = {}

    #TODO split module to user decorators
    @answercmd
    def answer(self, sender, message):
        if not hasattr(self.bot, "rps"): 
            self.bot.rps = self

        args = message.split()
        if len(args) == 0:
            return "Regarde le help au lieu de vouloir jouer comme ça !"
        cmd = args[0].strip()
        if cmd == "init":
            if int(args[1]) > len(self.bot.jids):
                return "Ouais bah invite des amis avant de vouloir faire ça !"
            try:
                self.players = int(args[1])
                self.manche = {}
                return "Game initialized with %s players"%(int(args[1]))
            except (ValueError, IndexError):
                return "Va apprendre à faire un init !!"
        elif cmd == "bot":
            self.manche[self.bot.name] = random.choice(self.choices)
            left = self.players - len(self.manche.keys())
            if left == 0:
                self.bot.say("I've played !")
                res = self.results()
                self.players = 0
                self.manche = {}
                self.bot.say(res)
            elif left == 1:
                self.bot.say("I have played, only %s answer is expected. Come on!"%(left))
            else:
                self.bot.say( "I have played, %s answers are expected"%(left))

        if message in self.choices:
            if sender in self.manche.keys():
                l = ["You must be stupid.", "What else?!"]
                return "You have already played... " + random.choice(l)
            elif self.players == 0:
                return "There is no game launched"
            else:
                self.manche[sender] = message
                left = self.players - len(self.manche.keys())
                if left == 0:
                    l = ["%s: You were very looooooooooong to answer..."%(sender), "%s: You are the last and perhaps the least!"%(sender), "%s has finally played."%(sender)]
                    self.bot.say(random.choice(l))
                    res = self.results()
                    self.players = 0
                    self.manche = {}
                    self.bot.say(res)
                elif left == 1:
                    self.bot.say("%s has played, only %s answer is expected. Come on!"%(sender, left))
                else:
                    self.bot.say("%s has played, %s answers are expected."%(sender, left))

    @staticmethod
    def beats(choice1, choice2):
        return (choice1 == "Paper" and choice2 == "Rock") or (choice1 == "Scissors" and choice2 == "Paper") or (choice1 == "Rock" and choice2 == "Scissors")
            
    def results(self):
        res = {}
        ret = ""
        for player, pchoice in self.manche.iteritems():
            loose = False
            for opponent, ochoice in self.manche.iteritems():
                if opponent != player:
                    if CmdRPS.beats(ochoice, pchoice):
                        loose = True
                        break
            res[player] = loose
        else:
            resultats = ", ".join(["%s: %s"%(player, score) for player, score in self.manche.iteritems()])
            ret = ", ".join(["%s"%(player) for player, status in res.iteritems() if not status])
            if len(ret) == 0:
                return "No winner! Just losers!"
            if ret.count(',') == 0:
                return "Results: %s, Winner: %s"%(resultats, ret)
            else:
                return "Results: %s, Winners: %s"%(resultats, ret)
