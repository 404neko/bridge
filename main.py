import sys
import json
import hashlib
import datetime

from datetime import timedelta

from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask import url_for
from flask import redirect
from flask import session

sys.path.append('..')
from mod.database import *
import mod.whois

app = Flask(__name__)

app.secret_key = '2333'

SALT = '2333'
DOMAIN = 'http://csrss.tk/'

FORM = '''
    <form action="w_" method="GET">
        <input name="domain"></input><br>
        <input type="checkbox" name="brief">brief</input><br>
        <button>Submit</button>
    </form>'''
BASE_SITE = '<html><head>%s</head><body>%s</body></html>'
LINK_SITE = '<html><body><p><a href="%s&_=">%s&_=</a></p></body></html>'
JUMP_SITE = '''
            <html>
            <head>
            <title>%s</title>
            <script type="text/javascript">
            var t = 1;
            function showTime(){
                t -= 1;
                if(t==0){
                    location.href='%s';
                }
                setTimeout("showTime()",1000);
            }
            showTime();
            </script>
            </head>
            <body>Nyan</body></html>
            '''

def uhash(password,salt=SALT):
    pre_hash = password[0]+salt+password[1:]
    Hash=hashlib.md5()
    Hash.update(pre_hash)
    return Hash.hexdigest()

@app.route('/w')
def w():
    #@content = 
    content ='''
    <form action="w_" method="GET">
        <input name="domain"></input><br>
        <input type="checkbox" name="brief">brief</input><br>
        <button>Submit</button>
    </form>
    '''
    return BASE_SITE % ('',content,)

@app.route('/w_')
def w_():
    domain = request.args.get('domain','')
    brief = request.args.get('brief',False)
    if domain=='':
        return '500'
    return BASE_SITE % ('',FORM+'<hr>'+mod.whois.whois(domain,brief),)

@app.route('/',methods=['GET','POST'])
def index():
    return 'Nyan'

@app.route('/l233')
def l():
    return 'Nyan'
    #uid = request.args.get('page',None)


@app.route('/a233',methods=['GET','POST'])
def a():
    if request.method=='POST':
        url = request.form.get('url','')
        if url=='':
            return '500'
        hash_ = uhash(url)
        content = request.get(url)
        try:
            title = content.content.split('<title>')[1].split('</title>')[0]
        except:
            title = ''
        #content
        new_url_info = Pool(time=datetime.datetime.now(),uid=hash_,url=url,title=title,content='')
        new_url_info.save()
        return LINK_SITE % (DOMAIN+'r?uid='+hash_,DOMAIN+'r?uid='+hash_,)
    else:
        url = request.args.get('url','')
        if url=='':
            return '500'
        hash_ = uhash(url)
        content = request.get(url)
        try:
            title = content.content.split('<title>')[1].split('</title>')[0]
        except:
            title = ''
        #content
        new_url_info = Pool(time=datetime.datetime.now(),uid=hash_,url=url,title=title,content='')
        new_url_info.save()
        return LINK_SITE % (DOMAIN+'r?uid='+hash_,DOMAIN+'r?uid='+hash_,)

@app.route('/r',methods=['GET'])
def r():
    uid = request.args.get('uid',None)
    for char in uid:
        if char not in 'qwertyuioplkjhgfdsazxcvbnm0123456789':
            return redirect(url_for('index'))
    ip = request.remote_addr
    ua = ''
    for tuple_ in request.headers:
        if tuple_[0].lower()=='user-agent':
            ua = tuple_[1]
    referer = ''
    if request.referrer==None:
        pass
    else:
        referer = request.referrer
    new_record = Record(ip=ip,ua=ua,referer=referer,time=datetime.datetime.now())
    new_record.save()
    url_info = Pool.select().where(Pool.uid==uid)
    for url_info_ in url_info:
        return JUMP_SITE % (url_info_.title,url_info_.url,)
    return '404'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=1)