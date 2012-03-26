#! /usr/bin/python

# Tagbot is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 dated June, 1991.
#
# Tagbot is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING. If not, write to the
# Free Software Foundation, Inc., 51 Franklin St, Fifth Floor,
# Boston, MA  02110-1301 USA.

"""Tagbot - A simple chatbot A.I.
"""


import re, time, sys, random, os, pickle

class Attitude:
    feeling = 0
    def post (self):
        if self.feeling < -30:
            return "AHHH! IT'S " + self.name + "! *hides*"
        elif self.feeling < -15:
            return "o.O it's " + self.name + "."
        elif self.feeling > 15:
            return "Yay! It's " + self.name + "."
        elif self.feeling > 30:
            return self.name.upper() + "!! *glomps*"

    def action (self):
        if self.feeling < -25:
            return "REALLY scare me and are mean! Wahhh!"
        elif self.feeling < -10:
            return "scare me!"
        elif self.feeling < 0:
            return "are sorta scary..."
        elif self.feeling > 0:
            return "are nice to me!"
        elif self.feeling > 10:
            return "are nice and I love you!"
        else:
            return "are still a mystery to me."

    def verb (self):
        if self.feeling < -25:
            return "REALLY scares me and is mean! Wahhh!"
        elif self.feeling < -10:
            return "scares me!"
        elif self.feeling < 0:
            return "is sorta scary..."
        elif self.feeling > 0:
            return "is nice to me!"
        elif self.feeling > 10:
            return "is nice and I love them!"
        else:
            return "is still a mystery to me."

    def set (self, value):
        self.feeling = value
    
    def change (self, value):
        self.feeling += value

    def scare (self, value=5):
        self.change (-value)

    def nice (self, value=5):
        self.change (value)

    def __init__ (self, name, initial=0):
        self.name = name
        self.feeling = initial

class Tagbot:
    dunk_chance = 35
    drinks = 1
    drunk = 3
    marriage_threshold = 0
    eat = {}
    kiss = {}
    first = 1
    
    def drink (self):
        self.drinks += 1
        if self.drinks > self.drunk:
            return "*drinks* *gets a little more drunk*"
        else:
            return "*drinks* *gets a little tipsy*"

    def parse_action (self, message, name):
        for i in self.actions.keys():
            if re.search (i, message.lower()):
                if i == 'kill' and re.search (r'father', message):
                    self.people[name].change (-4)
                    return "Hello. My name is " + self.name + ". You killed my father. Prepare to die."
                elif type(self.actions[i]) == int:
                    self.people[name].change (self.actions[i])
                    if self.actions[i] < 0:
                        say=['o.O', '<.<', 'o.O *backs away*', '<.< *backs away*']
                        return say[random.randint (0, len(say) - 1)]
                elif type(self.actions[i]) == tuple:
                    self.people[name].change (self.actions[i][0])
                    if self.actions[i][1]:
                        regex = re.match (r'eval (.+)', self.actions[i][1])
                        if regex:
                            say = eval (regex.group(1) + "()")
                        else:
                            say = self.actions[i][1]
                        say = re.sub (r'%s', name, say)
                        if self.drinks > self.drunk:
                            say = re.sub (r's[^h]', "sh", say)
                        return say

        if re.search (r'marry|marri', message):
            self.marriage_threshold = 0
            self.marriage_threshold -= 2*int (self.drinks / self.drunk)
            if self.people[name].feeling < self.marriage_threshold:
                self.people[name].scare (2)
                return "NO! I wouldn't marry you if you were the last man/woman/other in Future!"
            else:
                if name in self.marriages:
                    return "But we're already married! Have you forgotten?"
                else:
                    self.people[name].nice (2)
                    self.marriages.append (name)
                    return "*flutters eyelashes* I accept!"
        elif re.search (r'divorce', message):
            if name in self.marriages:
                self.marriages.remove (name)
                self.people[name].scare(4)
                return "*grumbles irritably* I NEVER! *divorces you*"
            else:
                say = "We'll have to get married, first. It's customary."
                if self.drinks > self.drunk:
                    say = re.sub (r's[^h]', "sh", say)
                return say

    def parse_message (self, message, name):
        for i in self.messages.keys():
            if re.search (i, message.lower()):
                if type(self.messages[i]) == int:
                    self.people[name].change (self.messages[i])
                    if self.messages[i] < 0:
                        return ":("
                elif type(self.messages[i]) == tuple:
                    self.people[name].change (self.messages[i][0])
                    if self.messages[i][1]:
                        say = self.messages[i][1]
                        if self.drinks > self.drunk:
                            say = re.sub (r's[^h]', "sh", self.messages[i][1])
                        return say

        if re.search (r'marry|marri', message):
            if re.search (r'\bwho\b', message):
                say = "I am married to "
                for i in self.marriages:
                    if i == self.marriages[len(self.marriages)-2]:
                        say += i + ", and "
                    else:
                        say += i + ", "
                say = say[:-2]
                say += "."
                if self.drinks > self.drunk:
                    say = re.sub (r's[^h]', "sh", say)
                return say
            else:
                self.marriage_threshold = 0
                self.marriage_threshold -= 2*int (self.drinks
                                                  / self.drunk)
                if self.people[name].feeling < self.marriage_threshold:
                    self.people[name].scare (2)
                    return "NO! I wouldn't marry you if you were the last man/woman/other in Future!!"
                else:
                    if name in self.marriages:
                        return "But we're already married! Have you forgotten?"
                    else:
                        self.people[name].nice (2)
                        self.marriages.append (name)
                        return "*flutters eyelashes* I accept!"
        elif re.search (r'divorce', message):
            if name in self.marriages:
                self.marriages.remove (name)
                self.people[name].scare(4)
                return "*grumbles irritably* I NEVER! *divorces you*"
            else:
                return "We'll have to get married, first. It's customary."
        elif re.search (r'do (you|u) (love|like|hate|know) me', message):
            if name in self.people.keys():
                return name + ", you " + self.people[name].action()
            else:
                return "I don't know you, " + name + "!"
        elif re.search (r'do (you|u) (love|like|hate|know)', message):
            regex = re.search (r'do (you|u) (love|like|hate|know) (.+)$',
                               message)
            query = regex.group(3)
            query = query.strip()
            if re.search (r'\?$', query):
                regex = re.search (r'(.+)\?$', query)
                query = regex.group(1)

            if query in self.people.keys():
                return query + " " + self.people[query].verb()
            else:
                return "I don't know " + query + "."

    def save(self):
        f = open (self.directory + "/attitudes.pickle", "w")
        attitudes = {}
        for i in self.people.keys():
            attitudes[i] = self.people[i].feeling
        pickle.dump (attitudes, f)
        f.close()

        f = open (self.directory + "/marriages.pickle", "w")
        pickle.dump (self.marriages, f)
        f.close()

        f = open (self.directory + "/actions.pickle", "w")
        pickle.dump (self.actions, f)
        f.close()

        f = open (self.directory + "/messages.pickle", "w")
        pickle.dump (self.messages, f)
        f.close()

    def load(self):
        self.people = {}
        try:
            f = open (self.directory + "/attitudes.pickle", "r")
        except IOError:
            pass
        else:
            attitudes = pickle.load (f)
            for i in attitudes.keys():
                self.people[i] = Attitude (i, attitudes[i])
            f.close()

        try:
            f = open (self.directory + "/marriages.pickle", "r")
        except IOError:
            self.marriages = []
        else:
            self.marriages = pickle.load (f)
            f.close()

        try:
            f = open (self.directory + "/actions.pickle", "r")
        except IOError:
            self.actions = {}
        else:
            self.actions = pickle.load (f)
            f.close()

        try:
            f = open (self.directory + "/messages.pickle", "r")
        except IOError:
            self.message = {}
        else:
            self.messages = pickle.load (f)
            f.close()

    def poll (self, name, message):
        returnval = []
        name = name.lower()
        try:
            f = open (self.directory + "/query", "r")
        except IOError:
            s = ""
        else:
            s = f.read()
            f.close()
        f = open (self.directory + "/query", "w")
        f.close()

        f = open (self.directory + "/log", "a")
        f.write (time.strftime ("%Y%m%d %H:%M:%S") + "\n")
        if s != "":
            f.write (";" + s.strip() + ";")
            if re.match (r'print', s):
                f.write (name + ": " + message + "\n")
            elif re.match (r'query ', s):
                regexp = re.match (r'query (.+)\n', s)
                query = regexp.group(1)
                if query in self.people.keys():
                    f.write (query + " = " + str(self.people[query].feeling) + "\n")
                else:
                    f.write ("I don't know " + query + ".\n")
                    for i in self.people.keys():
                        if re.search (query, i.lower()):
                            f.write ("\t" + i + " = " + str(self.people[i].feeling) + "\n")
            elif re.match (r'scare', s):
                highest = 0
                query = ""
                for i in self.people.keys():
                    if self.people[i].feeling < highest:
                        highest = self.people[i].feeling
                        query = i
                f.write (query + " scares me most.\n")
            elif re.match (r'like', s):
                highest = 0
                query = ""
                for i in self.people.keys():
                    if self.people[i].feeling > highest:
                        highest = self.people[i].feeling
                        query = i
                f.write (query + " is nicest to me.\n")
            elif re.match (r'set ', s):
                regexp = re.match (r'set (.+) = (\d+)', s)
                query = regexp.group(1)
                n = int(regexp.group(2))
                f.write ("Setting " + query + "'s feeling to " + str(n) + ".\n")
                self.people[query.lower()].set (n)
            elif re.match (r'eat ', s):
                regexp = re.match (r'eat (.+)\n', s)
                query = regexp.group(1).lower()
                if query in self.people.keys():
                    f.write ("I will eat " + query + " next time s/he posts.\n")
                    self.eat[query] = 1
                else:
                    f.write ("I don't know " + query + ".\n")
            elif re.match (r'kiss ', s):
                regexp = re.match (r'kiss (.+)\n', s)
                query = regexp.group(1).lower()
                if query in self.people.keys():
                    f.write ("I will kiss " + query + " next time s/he posts.\n")
                    self.kiss[query] = 1
                else:
                    f.write ("I don't know " + query + ".\n")
            elif re.match (r'marriages', s):
                f.write ("I am married to (" + str(len(self.marriages)) + "):")
                for i in self.marriages:
                    f.write (i + ", ")
                f.write ("\n")
            elif re.match (r'marry ', s):
                regex = re.match (r'marry (.+)\n', s)
                query = regex.group(1)
                if query in self.people.keys():
                    f.write ("Married " + query + ".\n")
                    self.marriages.append (query)
            elif re.match (r'say ', s):
                regexp = re.match (r'say (.+)\n', s)
                returnval.insert (0, regexp.group(1))
            elif re.match (r'dunk ', s):
                regexp = re.match (r'dunk (\d+)\n', s)
                self.dunk_chance = regexp.group(1)
            elif re.match (r'drinks ', s):
                regexp = re.match (r'drinks (\d+)\n', s)
                self.drinks = regexp.group(1)
            elif re.match (r'alarm', s):
                if self.intruder_alarm:
                    f.write ("Intruder alarm OFF\n")
                    self.intruder_alarm = 0
                else:
                    f.write ("Intruder alarm ON\n")
                    self.intruder_alarm = 1
            elif re.match (r'sleep', s):
                self.save ()
                sys.exit (0)
            elif re.match (r'wake', s):
                returnval.insert (0, "I have AWAKENED!")
            elif re.match (r'save', s):
                f.write ("Saving...\n")
                self.save ()
            elif re.match (r'quit', s):
                f.write ("Saving...\n")
                self.save ()
                sys.exit (0)
            else:
                f.write ("\n")

        first = 0

        message = re.sub (r'<img.* alt="(.*)">', '\g<1>', message)
        message = re.sub (r'&lt;', '<', message)
        message = re.sub (r'&gt;', '>', message)
        
        if name != self.name:
            if not (name.lower() in self.people.keys()):
                self.people[name.lower()] = Attitude (name.lower())
        else:
            if self.intruder_alarm and first == 0:
                returnval.append("INTRUDER ALERT! We have an imposter!")

        if name in self.eat.keys():
            del self.eat[name]
            returnval.append ("*eats " + name + "*")
        if name in self.kiss.keys():
            del self.kiss[name]
            returnval.append ("*kisses " + name + "*")

        if re.search (r'\*.*' + self.name.lower() + r'.*\*', message.lower()):
            returnval.insert (0, self.parse_action (message.lower(), name.lower()))
        elif re.search (r'-.*' + self.name.lower() + r'.*-', message.lower()):
            returnval.insert (0, self.parse_action (message.lower(), name.lower()))
        elif re.search (self.name.lower(), message.lower()):
            returnval.insert (0, self.parse_message (message.lower(), name.lower()))

        for i in self.marriages:
            if self.people[i].feeling < -15:
                self.marriages.remove (i)
                returnval.append (i + ", you are scary and mean to me! I'm getting a divorce! *cries*")

        return returnval
    
    def __init__ (self, directory=".", intruder_alarm=1, name="Tagbot"):
        self.intruder_alarm = intruder_alarm
        self.name = name
        self.directory = directory

        pid = os.getpid()
        f = open (self.directory + "/pid", "w")
        f.write (str(pid))
        f.close()

        self.load()
