#coding: utf-8

import json

from settings import *

class User(object):

    def __init__(self, id, hp, atk, dif, spd, brd, rep, follower):
        self.id = id;
        self.hp = hp;
        self.atk = atk;
        self.spd = spd;
        self.dif = dif;
        self.brd = brd;
        self.rep = rep;
        self.follower = follower;
        self.is_update = False;

    def update(self, other):
        if (other != None):
            if (self.is_follow(other) == True):
                other.damage(self.atk);
            else:
                other.repair(self.rep);
            if (other.is_follow(self) == True):
                self.damage(self.atk);
            else:
                other.repair(self.rep);
            self.is_update = True;
    
    def is_follow(self, other):
        return (self.follower in other.id);
    
    def damage(self, atk):
        dam = atk - self.dif;
        self.hp -= dam;
    
    def repair(self, rep):
        self.hp += rep;

    def save(self):
        result = {
            "user_id": self.id,
            "hp": self.hp,
        };

        return (json.dumps(result));

