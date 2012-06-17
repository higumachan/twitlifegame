from field import Field
import pymongo
import time

from settings import *

def _main():
    conn = pymongo.Connection(DB_HOST);
    db = conn.lifegame;
    field = Field(db.field.sort("_id", -1).limit(1)[0], db);

    while (1):
        field.update();
        field.append_user(db);
        field.save(db);
        time.sleep(1);

if __name__ == "__main__":
    _main();

