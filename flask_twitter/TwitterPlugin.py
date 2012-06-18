# -*- coding: utf-8 -*-

from flask import *
import twitter

def twitter_login(func):
    import functools
    @functools.wraps(func)
    def wrapper(*args, **kwards):
        twi = twitter.Twitter(request);
        api = twi.get_API();
        if (api == None):
            return twi.oauth_request(request.path);
        if (kwards.has_key("username") and kwards["username"] != twi.get_screenname()):
            return (u"違うユーザ");
        kwards["api"] = api;
        return func(*args, **kwards);
    return wrapper;

def twitter_callback(func):
    import functools
    @functools.wraps(func)
    def wrapper(*args, **kwards):
        twi = twitter.Twitter(request);
        (key, secret) = twi.oauth_callback(request);
        api = twi.get_API(key, secret);
        kwards["api"] = api;
        result = func(*args, **kwards);
        result.set_cookie("twackey", key);
        result.set_cookie("twsckey", secret);
        return result
    return wrapper;

