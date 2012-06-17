# coding: utf-8

import json

from settings import *

class Field(object):
    
    def __init__(self, field, db):
        self.field = self._load(field, db);
        self.width = WIDTH;
        self.height = HEIGHT;
        self.dirs = ((1, 0), (1, 1), (0, 1), (-1, 1));
    
    def update(self):
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                if (self.field[y][x] != None):
                    user = self.field[y][x];
                    for dir in self.dirs:
                        other = self._get_user(field, x, y, dir);
                        user.update(other);
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                if (self.field[y][x] != None):
                    user = self.field[y][x];
                    if (user.is_update == False):
                        self._move_user(user, x, y);
                    user.is_update = False;

    def _get_user(self, field, x, y, dir):
        return (field[y + dir[1]][x + dir[0]]);

    def _move_user(self, user, x, y):
        dir = (random.randint(0, 1), random.randint(0, 1));
        user = self.field[y][x];
        self.field[y][x] = None;
        self.field[y + dir[0]][x + dir[1]] = user;

    def save(self, db):
        saver = [];
        for y in range(self.HEIGHT):
            add = [];
            for x in range(self.WIDTH):
                if (field[y][x] == None):
                    add.append(None);
                else:
                    add.append(field[y][x].save);
            saver.append(add);
        
        db.fields.insert({
            "_id": db.fields.count() + 1,
            "field": json.dumps(saver),
        });
    def _load(self, field, db):
        result = [];
        for y in range(HEIGHT):
            add = [];
            for x in range(WIDTH):
                dic = field[y][x];
                if (dic != None):
                    user_dic = db.users.find_one(dic["user_id"]);
                    user = User(dic["hp"], dic["id"],
                        user_dic["atk"], user_dic["dif"], user_dic["spd"],
                        user_dic["brd"], user_dic["rep"], user_dic["follower"]);
                    add.append(user);
                else:
                    add.append(None);
            result.append(add);
        self.field = result;

