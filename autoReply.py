#coding=utf8
import requests
import config
import logging
import re
import identify_code
import enchant

logging.basicConfig(level=logging.DEBUG,filename='logEvent.log',format='%(levelname)s - %(message)s - %(asctime)s')
baseurl='https://www.douban.com/group/topic/167917187/'
contentSent='阿sir~'

def auto_reply(baseurl,contentSent):
    url = baseurl+'add_comment'
    data = {
    "rv_comment": contentSent,
    "ck": "aubV",
    'start': '0',
    'submit_btn': '发送'
    }#发送的数据格式


    logging.debug(baseurl+' reply start')
    success=False

    while not success:
        rval = requests.get(baseurl+'?start=5000#last',headers=config.header)
        #检验是否需要输入验证码?
        data['ck'] = re.search('ck=(\w+)', rval.text).group(1)#获取ck值
        mat = re.search('src=\"(.*?captcha.*?)\"', rval.text)
        if mat:
            #需要识别验证码
            captcha_url = mat.group(1)#获取验证码图片地址
            logging.debug('captcha_url of '+baseurl+':'+captcha_url)#记录该帖验证码日志
            try:
                code = identify_code.recognize_url(captcha_url)#识别验证码
                logging.debug(baseurl+'的验证码为:'+str(code))

            except:
                logging.debug("error in recognition of captcha of "+baseurl)
                continue
            data['captcha-solution'] = code
            data['captcha-id'] = re.search('id=(.*?)&', captcha_url).group(1)#补充验证码信息
            d = enchant.Dict("en_US")
            try:
                if d.check(code):
                    continue
            except:
                continue
        success=True
        rval = requests.post(url=url, data=data, headers=config.header)

    logging.debug(baseurl+' reply end')