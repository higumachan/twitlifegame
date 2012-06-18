from flask import *
import pymongo
import  json
import random
from logging.handlers import *
from flask_twitter.TwitterPlugin import *
import datetime

app = Flask(__name__);

formatter = logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
)
error_log = os.path.join(app.root_path, 'logs/error.log')
error_file_handler = RotatingFileHandler(
    error_log, maxBytes=100000, backupCount=10
)    
error_file_handler.setLevel(logging.ERROR)
error_file_handler.setFormatter(formatter)
app.logger.addHandler(error_file_handler)

@app.before_request
def before_request():
    g.conn = pymongo.Connection();
    g.db = g.conn.lifegame; 

@app.teardown_request
def teardown_request(exception):
    g.conn.disconnect();
    g.db = None;



@app.route("/")
def index():
    id = g.db.fields.count();
    return (render_template("index.html", id=id));

@app.route("/get-field")
def get_field():
    id = int(request.args["id"]);
    
    field = g.db.fields.find_one({"_id": id});

    return (json.dumps(field));
    
@app.route("/get-max-id")
def get_max_id():
    return (g.db.fields.count());

@app.route("/get-users")
def get_users():
    result = [];
    for user in g.db.users.find():
        user["create_at"] = None;
        result.append(user);
    return json.dumps(result);

@app.route("/append-user")
@twitter_login
def append_user(api):
    me = api.me();
    id = me.id;

    user = g.db.users.find_one({"_id": id});
    if (user == None):
        user = {
            "_id": id,
            "screen_name": me.screen_name,
            "atk": random.randint(1, 10),
            "dif": random.randint(1, 10),
            "spd": random.randint(1, 10),
            "brd": random.randint(1, 10),
            "rep": random.randint(1, 10),
            "follower": api.friends_ids(),
            "create_at": datetime.datetime.now(),
        };
    else:
        user["follower"] = api.friends_ids();
    g.db.users.save(user);
    g.db.append_queue.insert({
        "_id": g.db.append_queue.count() + 1,
        "user_id": me.id,
        "appended": False,
        "create_at": datetime.datetime.now(),
    });

    return "OK";

@app.route("/twitter/callback")
@twitter_callback
def callback(api):
    next = request.cookies["next"];
    return (make_response(redirect(next)));


if __name__ == "__main__":
    app.debug = True;
    app.run();

