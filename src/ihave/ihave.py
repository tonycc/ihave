# -*- coding: utf-8 -*-
'''
Created on 2013-1-29

@author: Tony
'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2013-1-27

@author: Tony
'''
import os.path
import tornado.web
import tornado.database
import tornado.httpserver
import tornado.ioloop
import tornado.options
from weiboapi.weibo import APIClient


from tornado.options import define,options

APP_KEY = '1279033890' # app key
APP_SECRET = '392001a59101bc9bee428429247f6251' # app secret
CALLBACK_URL = 'http://127.0.0.1:8000/login_check' # callback url

define("port",default=8000,help="run on the gieve port",type=int)
define("mysql_host",default="127.0.0.1:3306",help="database host")
define("mysql_database",default="ihave",help="database name")
define("mysql_user",default="root",help="database user")
define("mysql_password",default="",help="database password")

class Application(tornado.web.Application):
    def __init__(self):
        handlers=[
            (r"/",HomeHandler),
            (r"/auth/login",AuthLoginHandler),
            (r"/login_check",LoginCheckHandler),
        ]
        settings=dict(
            title=u"I Have",
            template_path=os.path.join(os.path.dirname(__file__),"templates"),
            static_path=os.path.join(os.path.dirname(__file__),"static"),
            xsrf_cookies=True,
            cookie_secret="",
            login_url="/auth/login",
            autoescape=None,
        )
        tornado.web.Application.__init__(self,handlers,**settings)
        
        self.db=tornado.database.Connection(
            host=options.mysql_host,database=options.mysql_database,
            user=options.mysql_user,password=options.mysql_password)


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db



class HomeHandler(BaseHandler):
    def get(self):
        self.render("home.html")

class AuthLoginHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        client=APIClient(app_key=APP_KEY,app_secret=APP_SECRET,redirect_uri=CALLBACK_URL)
        url=client.get_authorize_url()
        self.redirect(url)

class LoginCheckHandler(BaseHandler):
    def get(self):
        code=self.get_argument('code')
        client=APIClient(app_key=APP_KEY,app_secret=APP_SECRET,redirect_uri=CALLBACK_URL)
        r=client.request_access_token(code)
        access_token=r.access_token
        expires_in=r.expires_in
        uid=r.uid
        client.set_access_token(access_token,expires_in)
        
        userinfo=client.users__show(uid=uid)
        if userinfo:
            self.db.execute("INSERT INTO users(uid,username,province,city,location,gender,profile_image_url,verified,followers_count,friends_count,avatar_large,verified_reason,bi_followers_count) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                            userinfo['id'],userinfo['screen_name'],userinfo['province'],userinfo['city'],userinfo['location'],userinfo['gender'],userinfo['profile_image_url'],userinfo['verified'],userinfo['followers_count'],userinfo['friends_count'],userinfo['avatar_large'],userinfo['verified_reason'],userinfo['bi_followers_count'])
        else:
            return
         
        self.render("home.html")

def main():
    tornado.options.parse_command_line()
    http_server=tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__=="__main__":
    main()