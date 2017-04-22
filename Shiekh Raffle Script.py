import requests
from bs4 import BeautifulSoup as bs
from time import sleep
from random import getrandbits

def entries(amount):
    for i in range(1, amount):
        session = requests.session()
        url = "http://app.bronto.com/public/webform/render_form/az29kh7x0eyaepdiyjrpwnoaucqqy/8d8606e3ebfefedc32115d645e3832e7/addcontact"
        post_url = "http://app.bronto.com/public/webform/process/"
        response = session.get(url)
        soup = bs(response.content, 'html.parser')
        fid = soup.find("input", {"name": "fid"})["value"]
        sid = soup.find("input", {"name": "sid"})["value"]
        sitekey = soup.find("div", {"class": "g-recaptcha"})["data-sitekey"]
        API_KEY = "HERE" #Replace HERE with your 2captcha key
        site_key = sitekey
        captcha_id = session.post("http://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}".format(API_KEY, site_key,url)).text.split('|')[1]
        recaptcha_answer = session.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(API_KEY, captcha_id)).text
        while 'CAPCHA_NOT_READY' in recaptcha_answer:
            sleep(5)
            recaptcha_answer = session.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(API_KEY, captcha_id)).text
        captcha_retrieved = recaptcha_answer.split('|')[1]
        email = 'silaymannagi+{}@gmail.com'.format(getrandbits(40))
        data = {
            "fid": fid,
            "sid": sid,
            "delid": "",
            "subid": "",
            "td": "",
            "formtype": "addcontact",
            "90298[29288859]": "Name",  ## Replace Name with your first name
            "90299[29288860]": "Lastname", ## Replace Lastname with your last name
            "90300": email,
            "90301[29288866]" : "9", #Replace 9 with your size or keep it lol
            "90302[29289136]": "",
            "90303[29289137]": "Agree to Terms",
            "90307[899049]": "true",
            "g-recaptcha-response": captcha_retrieved
        }
        response = session.post(post_url, data)
        print('{} out of {} entered with email: {}.'.format(i, amount, email))
if __name__ == '__main__':
    entries(100000)
