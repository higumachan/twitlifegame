#!/usr/bin/python
# -*- coding: utf-8 -*-

import tweepy
import Cookie
import os
import cgi
import cgitb
from flask import *
from TwitterPlugin import *
import settings

class Twitter:
    def __init__(self, request):
        self.ck = request.cookies;
        self.oauth = tweepy.OAuthHandler(settings.key, settings.secret); 

    def oauth_request(self, url):
        resp = make_response(redirect(self.oauth.get_authorization_url()));
        resp.set_cookie('request_token_key', self.oauth.request_token.key);
        resp.set_cookie('request_token_secret', self.oauth.request_token.secret);
        resp.set_cookie('next', url);
        return resp;

    def oauth_callback(self, request):
        pin = request.args["oauth_verifier"];
        req_key = request.cookies.get("request_token_key");
        req_sec = request.cookies.get("request_token_secret");
        self.oauth.set_request_token(req_key, req_sec);

        self.oauth.get_access_token(pin);
        return (self.oauth.access_token.key, self.oauth.access_token.secret);
    
    def get_API(self, key=None, secret=None):
        if (self.ck.has_key("twackey") and self.ck.has_key("twsckey")):
            self.oauth.set_access_token(self.ck["twackey"], self.ck["twsckey"]);
            return (tweepy.API(self.oauth));
        elif (key != None and secret != None):
            self.oauth.set_access_token(key, secret);
            return (tweepy.API(self.oauth));
        return (None);
    def get_screenname(self, key=None, secret=None):
        api = self.get_API(key, secret);
        if (api != None):
            return (api.me().screen_name);
        return (None);

