# coding=utf-8
import requests
import random
import re
import json
import os
import time
import sys
from lxml import etree


def push(key, title, content):  # 函数用来发送填报失败信息
    url = 'http://www.pushplus.plus/send'
    data = {
        "token": key,
        "title": title,
        "content": "<xmp>" + content + "</xmp>"
    }
    body = json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=body, headers=headers)


def login():
    userinfo = os.getenv('USERINFO')
    # userinfo格式 = """{
    #     "user": "123456789",
    #     "password": "123456789",
    #     "send_key": "123456789"
    #     }"""
    global send_key
    try:
        userid = json.loads(userinfo).get('user')
        password = json.loads(userinfo).get('password')

        send_key = json.loads(userinfo).get('send_key')
    except:
        print('环境变量userinfo格式错误')
        sys.exit()

    # 产生随机验证码（其实没必要，服务端不验证，输入固定的验证码即可）
    selectChar = ["2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "j", "k", "m", "n",
                  "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "J",
                  "K", "L", "M", "N", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    codeInput = ''
    for i in range(4):
        codeInput += selectChar[random.randint(0, 54)]

    # 先创建一个session，方便后续post和get
    session = requests.session()
    # 设置浏览器headers，这里用的我的浏览器信息，需要改的话，自己修改
    session.headers = {'Connection': 'keep-alive', 'Cache-Control': 'max-age=0', 'Upgrade-Insecure-Requests': '1',
                       'Origin': 'http://xgb.ahstu.edu.cn', 'Content-Type': 'application/x-www-form-urlencoded',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.70',
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                       'Referer': 'http://xgb.ahstu.edu.cn/SPCP/Web/',
                       'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'}

    # 登录信息，其中userid是学号，password是密码，codeInput是上面生成的验证码
    data = {'StuLoginMode': '1', 'txtUid': userid, 'txtPwd': password, 'codeInput': codeInput}

    try:
        # 登录账号，获取cookies
        response_login = session.post('http://xgb.ahstu.edu.cn/SPCP/Web/', data=data, verify=False,
                                      allow_redirects=False)
    except:
        print('疫情填报登录失败，请检查平台是否能正常访问！')
        push(send_key, '安徽科技学院 - 疫情填报登陆失败', '疫情填报登录失败，请检查平台是否能正常访问！')
        sys.exit()
    return session


def get_info(session):
    try:
        # 打开疫情填报页面，获取所需信息
        response = session.get('http://xgb.ahstu.edu.cn/SPCP/Web/Report/Index', verify=False)

        # 接下来一大段都是通过正则表达式和lxml模块获取对应的Data信息，以实现自动填报
        info = response.text

        if ('当前采集日期已登记！' in info):
            print('疫情填报失败：今日已填报！')
            push(send_key, '安徽科技学院 - 疫情填报失败', info)
            Data = None
        else:
            html = etree.HTML(info)
            result = html.xpath('//*[@id="form1"]/div[1]/div[4]/div[2]/select[1]')
            result = etree.tostring(result[0], encoding='utf-8').decode()
            Province = re.findall('''<option value="(.*?)" selected="selected"''', result)[0]

            html = etree.HTML(info)
            result = html.xpath('//*[@id="form1"]/div[1]/div[5]/div[2]/select[1]')
            result = etree.tostring(result[0], encoding='utf-8').decode()
            FaProvince = re.findall('''<option value="(.*?)" selected="selected">''', result)[0]

            html = etree.HTML(info)
            result = html.xpath('//*[@id="7d2ffcb7-2101-478a-a0dc-b0bac9539b16"]')
            result = etree.tostring(result[0], encoding='utf-8').decode()

            Data = {
                'StudentId': re.findall(
                    '''<input name="StudentId" type="text" id="StudentId" readonly="readonly" class="input-style" style=" {8}border: none;" value="(.*?)" />''',
                    info)[0],
                'Name': re.findall(
                    '''<input name="Name" type="text" id="Name" readonly="readonly" class="input-style" style=" {8}border: none;" value="(.*?)" />''',
                    info)[0],
                'Sex': re.findall('''<input id="Sex" name="Sex" type="hidden" value="(.*?)" />''', info)[0],
                'SpeType': re.findall('''<input id="SpeType" name="SpeType" type="hidden" value="(.*?)" />''', info)[0],
                'CollegeNo':
                    re.findall('''<input id="CollegeNo" name="CollegeNo" type="hidden" value="(.*?)" />''', info)[0],
                'SpeGrade': re.findall('''<input id="SpeGrade" name="SpeGrade" type="hidden" value="(.*?)" />''', info)[
                    0],
                'SpecialtyName':
                    re.findall('''<input id="SpecialtyName" name="SpecialtyName" type="hidden" value="(.*?)" />''',
                               info)[0],
                'ClassName':
                    re.findall('''<input id="ClassName" name="ClassName" type="hidden" value="(.*?)" />''', info)[0],
                'MoveTel': re.findall(
                    '''<input name="MoveTel" type="text" id="MoveTel" class="required validate input-style" vtype="TelPhone" value="(.*?)" />''',
                    info)[0],
                'Province': Province,
                'City': re.findall(
                    '''<select name="City" onchange="CityChange\(this\);" data-defaultValue="(.*?)" class="select-style required validate"></select>''',
                    info)[0],
                'County': re.findall(
                    '''<select name="County" data-defaultValue="(.*?)" class="select-style required validate"></select>''',
                    info)[0],
                'ComeWhere': re.findall(
                    '''<input name="ComeWhere" type="text" maxlength="50" value="(.*?)" class="required validate input-style" placeholder="例：XX街道XX社区XX号" />''',
                    info)[0],
                'FaProvince': FaProvince,
                'FaCity': re.findall(
                    '''<select name="FaCity" onchange="CityChange\(this\);" data-defaultValue="(.*?)" class="select-style required validate"></select>''',
                    info)[0],
                'FaCounty': re.findall(
                    '''<select name="FaCounty" data-defaultValue="(.*?)" class="select-style required validate"></select>''',
                    info)[0],
                'FaComeWhere': re.findall(
                    '''<input name="FaComeWhere" type="text" maxlength="50" value="(.*?)" class="required validate input-style" placeholder="例：XX街道XX社区XX号" />''',
                    info)[0]
            }


            PZData = []
            # 单选框
            radio = re.findall(r'<input name=\'radio_.+\' id="(.*?)"', info)
            for i, r in enumerate(radio):
                html = etree.HTML(info)
                result = html.xpath(f'//*[@id="{r}"]')
                if (('checked="checked"' in etree.tostring(result[0], encoding='utf-8').decode())):
                    pzd = {
                        "OptionName": result[0].attrib.get("data-optionname"),
                        "SelectId": r,
                        "TitleId": result[0].xpath("..")[0].attrib.get('data-tid'),
                        "OptionType": "0"
                    }
                    PZData.append(pzd)
                    Data['radio_'+str(i+1)] = r

            # 填空题
            text = re.findall(r'name="text_(.*?)"', info)
            for i, r in enumerate(text):
                html = etree.HTML(info)
                result = html.xpath(f'//*[@name="text_{r}"]')
                if (result[0].attrib.get('value') != ''):
                    pzd = {
                        "OptionName": result[0].attrib.get("value"),
                        "SelectId": result[0].xpath("..")[0].attrib.get('data-sid'),
                        "TitleId": result[0].xpath("..")[0].attrib.get('data-tid'),
                        "OptionType": "2"
                    }
                    if(not pzd['SelectId']):
                        pzd['SelectId'] = ""
                    PZData.append(pzd)
                    Data['text_'+str(i+1)] = result[0].attrib.get('value')

            Data = {**Data,**{
                'Other': re.findall('''<textarea name="Other" id="Other" rows="3">(.*?)</textarea>''',info)[0],
                'GetAreaUrl': '/SPCP/Web/Report/GetArea',
                'IdCard': re.findall('''<input id="IdCard" name="IdCard" type="hidden" value="(.*?)" />''', info)[0],
                'ProvinceName':
                    re.findall('''<input id="ProvinceName" name="ProvinceName" type="hidden" value="(.*?)" />''', info)[
                        0],
                'CityName': re.findall('''<input id="CityName" name="CityName" type="hidden" value="(.*?)" />''', info)[
                    0],
                'CountyName':
                    re.findall('''<input id="CountyName" name="CountyName" type="hidden" value="(.*?)" />''', info)[0],
                'FaProvinceName':
                    re.findall('''<input id="FaProvinceName" name="FaProvinceName" type="hidden" value="(.*?)" />''',
                               info)[0],
                'FaCityName':
                    re.findall('''<input id="FaCityName" name="FaCityName" type="hidden" value="(.*?)" />''', info)[0],
                'FaCountyName':
                    re.findall('''<input id="FaCountyName" name="FaCountyName" type="hidden" value="(.*?)" />''', info)[
                        0],
                'radioCount': str(len(radio)),
                'checkboxCount': '0',
                'blackCount': str(len(text)),
                'PZData': str(PZData),
                'ReSubmiteFlag': re.findall('''<input name="ReSubmiteFlag" type="hidden" value="(.*?)" />''',info)[0]
            }
                    }
    except:
        print('获取个人信息失败！')
        push(send_key, '安徽科技学院 - 疫情填报失败', '获取个人信息失败！')
        Data = None
    return session, Data


def Temper(session, time):
    if (time == 0):
        date = ['0', '0']
    elif (time == 1):
        date = ['4', '1']
    else:
        date = ['8', '2']
    # 随机体温
    Temper = random.randint(0, 9)
    data = {'TimeNowHour': date[0], 'TimeNowMinute': date[1], 'Temper1': '36', 'Temper2': Temper}
    # 体温填报
    try:
        response_Temper = session.post('http://xgb.ahstu.edu.cn/SPCP/Web/Temperature/StuTemperatureInfo', data=data)
        # 输出结果
        if ('填报成功！' in response_Temper.text):
            print('体温填报-填报成功！')
        else:
            print('第' + str(time + 1) + '次体温填报失败')
            push(send_key, '安徽科技学院 - 体温填报' + str(time + 1) + '失败', response_Temper.text)
    except:
        print('体温填报' + str(time + 1) + '失败')
        push(send_key, '安徽科技学院 - 体温填报' + str(time + 1) + '失败', '请手动填报')


def yiqing(session, Data):
    # 疫情填报
    try:
        response = session.post('http://xgb.ahstu.edu.cn/SPCP/Web/Report/Index', data=Data)
        if ('提交成功！' in response.text):
            print('疫情填报-提交成功！')
        else:
            print('疫情填报失败')
            push(send_key, '安徽科技学院 - 疫情填报失败', response.text)
    except:
        print('疫情填报失败')
        push(send_key, '安徽科技学院 - 疫情填报失败', '疫情填报失败，请手动填报！')


def main_handler(a, b):
    session = login()
    session, Data = get_info(session)
    time_temper = 3
    for i in range(time_temper):
        Temper(session, i)
        time.sleep(1)
    if (Data != None):
        yiqing(session, Data)


if __name__ == '__main__':
    main_handler(None, None)
