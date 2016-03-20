#0.py
#data: { domain: 'chinaz.com',whoisServer:'whois.ename.com',deskey:'pGPyXrlN7P|INU4xqVt2JtCkUz7p1Pb9' },
import re
import json
import requests

def dict2sorted_list(dict_,keys,brief=False):
    dict__ = []
    for key in keys:
        if key in dict_:
            dict__.append(key+': '+dict_[key])
    if not brief:
        dict__.append(' ')
        for key in dict_:
            if key not in keys:
                dict__.append(key+': '+dict_[key])
    return dict__

def text2dict(text):
    text_list = text.split('\n')
    dict_ = {}
    for item in text_list:
        item = item.replace('\r','')
        item_list = item.split(':')
        if len(item_list)==1:
            pass
            continue
            #print 'Not a dict string.'
        key = item_list[0]
        value = ':'.join(item_list[1:])
        dict_[key.strip()] = value.strip()
    try:
        dict_.pop('')
    except:
        pass
    return dict_

def parse_domain(url):
    if url[:2]=='ht':
        re_find = re.findall('(http|https)://(.*?)/',url)
        if len(re_find)>=1:
            return re_find[0][1]
        else:
            return None
    else:
        buffer_ = ''
        while url[0]=='/':
            url = url[1:]
        for char in url:
            if char!='/':
                buffer_+=char
            else:
                return buffer_
        return buffer_

header = '''
Accept: */*
Origin: http://whois.7c.com
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36
Content-Type: application/x-www-form-urlencoded
Referer: http://whois.7c.com/
Accept-Encoding: gzip, deflate
Accept-Language: en,zh-CN;q=0.8,zh;q=0.6
'''

def whois(url,brief=False):
    #session = requests.session()
    #respon = session.get('http://whois.chinaz.com/?DomainName='+url+'&ws=whois.ename.com',headers = header)
    #whois_json = re.findall('data: ({ domain:.*\})',respon.content)[0]
    #for key in eval(whois_json):
    #domain=www.instra.com&strdo=dm
    data = 'domain='+parse_domain(url)+'&strdo=dm'
    respon = requests.post('http://whois.7c.com/hander/WhoIsServices.ashx',headers=text2dict(header),data=data)
    not_found = respon.content[:64].find('NOT FOUND')
    if respon.content.find('Whois Server Version')==-1:
        return respon.content
    if not not_found!=-1:
        data = respon.content.split('<br/>')[1:-1]
        dict_ = text2dict('\n'.join(data))
        keys = [
            'Domain Name',
            'Registrar Registration Expiration Date',
            'Updated Date',
            'Creation Date',
            'Registrant Email',
            'Registrant Name'
        ]
        #print '<br/>'.join(dict2sorted_list(dict_,keys,brief=brief))
        return '<br/>'.join(dict2sorted_list(dict_,keys,brief=brief))
    else:
        return 'NOT FOUND'