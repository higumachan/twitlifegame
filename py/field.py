# coding: utf-8

import json

from settings import *
import random
from user import User
from copy import deepcopy 

class Field(object):
    
    def __init__(self, field, db):
        self.field = self._load(field, db);
        self.dirs = ((1, 0), (1, 1), (0, 1), (-1, 1));
    
    def update(self):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if (self.field[y][x] != None):
                    user = self.field[y][x];
                    for dir in self.dirs:
                        other = self._get_user(self.field, x, y, dir);
                        user.update(other);
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if (self.field[y][x] != None):
                    user = self.field[y][x];
                    if (user.is_update == False):
                        self._move_user(user, x, y);
                    if (user.is_bread() == True):
                        self._bread_user(user, x, y);
                    if (user.is_die() == True):
                        self.field[y][x] = None;
                    user.is_update = False;

    def append_users(self, db):
        append_queue = list(db.append_queue.find({"appended": False}));

        for append_user in append_queue:
            print "append user"
            user_dic = db.users.find_one({"_id": append_user["user_id"]});
            while True:
                (x, y) = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1));
                if (self.field[y][x] == None):
                    self.field[y][x] = User(SETTING_HP, append_user["user_id"],
                        user_dic["atk"], user_dic["dif"], user_dic["spd"],
                        user_dic["brd"], user_dic["rep"], user_dic["follower"]);
                    break;
            append_user["appended"] = True;
            db.append_queue.save(append_user);

    def _get_user(self, field, x, y, dir):
        if self.is_in(x + dir[0], y + dir[1]) == True:
            return (field[y + dir[1]][x + dir[0]]);
        return (None);

    def _move_user(self, user, x, y):
        dir = (random.randint(-1, 1), random.randint(-1, 1));
        if (self.is_in(x + dir[1], y + dir[0]) == True and self.field[y + dir[0]][x + dir[1]] == None):
            user = self.field[y][x];
            self.field[y][x] = None;
            self.field[y + dir[0]][x + dir[1]] = user;

    def _bread_user(self, user, x, y):
        for i in range(10):
            if (self.field[y][x] == None):
                dir = (random.randint(-1, 1), random.randint(-1, 1));
                if (self.is_in(x + dir[1], y + dir[0]) == True and self.field[y + dir[0]][x + dir[1]] == None):
                    user.hp = 10;
                    self.field[y + dir[0]][x + dir[1]] = deepcopy(user);

    def is_in(self, x, y):
        return (x >= 0 and x < WIDTH and y >= 0 and y < HEIGHT);

    def save(self, db):
        saver = [];
        for y in range(HEIGHT):
            add = [];
            for x in range(WIDTH):
                if (self.field[y][x] == None):
                    add.append(None);
                else:
                    add.append(self.field[y][x].save());
            saver.append(add);
        
        db.fields.insert({
            "_id": db.fields.count() + 1,
            "field": saver,
        });
    def _load(self, field, db):
        result = [];
        for y in range(HEIGHT):
            add = [];
            for x in range(WIDTH):
                dic = field[y][x];
                if (dic != None):
                    print dic;
                    user_dic = db.users.find_one({"_id": dic["user_id"]});
                    user = User(dic["hp"], dic["user_id"],
                        user_dic["atk"], user_dic["dif"], user_dic["spd"],
                        user_dic["brd"], user_dic["rep"], user_dic["follower"]);
                    add.append(user);
                else:
                    add.append(None);
            result.append(add);
        return (result);

