#coding: utf-8

import json

from settings import *

class User(object):

    def __init__(self, hp, id, atk, dif, spd, brd, rep, follower):
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
                other.repair(self.atk);
            else:
                other.damage(self.rep);
            if (other.is_follow(self) == True):
                self.repair(self.atk);
            else:
                self.damage(self.rep);
            self.is_update = True;

    def is_bread(self):
        return (self.hp > 100);
    
    def is_follow(self, other):
        return (other.id in self.follower);

    def is_die(self):
        return (self.hp <= 0);
    
    def damage(self, atk):
        dam = abs(atk - self.dif);
        self.hp -= dam;
        print self.id, "damage", dam
    
    def repair(self, rep):
        print self.id, "repair"
        self.hp += rep;

    def save(self):
        result = {
            "user_id": self.id,
            "hp": self.hp,
        };

        return (result);

