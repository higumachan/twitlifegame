from field import Field
import pymongo
import time

from settings import *

def _main():
    conn = pymongo.Connection(DB_HOST);
    db = conn.lifegame;

    field = Field(db.fields.find().sort("_id", -1).limit(1)[0]["field"], db);

    while (1):
        start = time.time();
        field.update();
        field.append_users(db);
        field.save(db);
        time.sleep(1 - (time.time() - start));

if __name__ == "__main__":
    _main();

