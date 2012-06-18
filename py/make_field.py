from settings import *
import pymongo

field = [];
for y in range(HEIGHT):
    add = [];
    for x in range(WIDTH):
        add.append(None);
    field.append(add);

db = pymongo.Connection().lifegame;

db.fields.save({"_id": 1, "field": field})

