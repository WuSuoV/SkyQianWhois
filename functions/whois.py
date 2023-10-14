import datetime
import random
import time

import requests
from whois21 import WHOIS


class Whois:
    def __init__(self, domain):
        self.domain = domain
        self.timeout = 5
        self.headers = {
            'User-Agent': random_headers(),
        }

    def status(self, status):
        """判断域名注册状态"""
        if status:
            return '已注册'
        else:
            return '未注册'

    def dnssec(self, dnssec):
        """判断DNSSEC的状态"""
        if dnssec is None:
            return None
        if 'signedDelegation' in dnssec:
            return '已配置'
        elif 'unsigned' in dnssec:
            return '未配置'
        else:
            return None

    def domain_long(self, create_time):
        """代表域名创建时间"""
        if create_time is None:
            return None

        try:
            create_year = str(create_time)[:4]
            now = time.strftime('%Y')

            long = int(now) - int(create_year)

            if long >= 20:
                result = ['twentyYearsOld', f'{long}年古董域名']
            elif long >= 10:
                result = ['tenYearsOld', f'{long}年老域名']
            elif long > 0:
                result = ['newRegister', f'{long}年域名']
            else:
                result = ['newRegister', f'未满一年']

            return [result]
        except:
            return None

    def domain_status(self, l):
        newl = []
        for i in l:
            newl.append(str(i).split(' ')[0])

        status = {
            'ok': '正常',
            'active': '正常',
            'addperiod': '注册局设置的域名新注册期',
            'clientdeleteprohibited': '注册商设置禁止删除',
            'serverdeleteprohibited': '注册局设置禁止删除',
            'clientupdateprohibited': '注册商设置禁止更新',
            'serverupdateprohibited': '注册局设置禁止更新',
            'clienttransferprohibited': '注册商设置禁止转移',
            'servertransferprohibited': '注册局设置禁止转移',
            'pendingverification': '注册信息审核期',
            'clienthold': '注册商设置暂停解析',
            'serverhold': '注册局设置暂停解析',
            'inactive': '非激活状态',
            'clientrenewprohibited': '注册商设置禁止续费',
            'serverrenewprohibited': '注册局设置禁止续费',
            'pendingtransfer': '注册局设置转移过程中',
            'redemptionperiod': '注册局设置赎回期',
            'pendingdelete': '注册局设置待删除/赎回期'
        }

        status2 = []
        for i in newl:
            k = status.get(i.lower())
            if k is None:
                status2.append(i)
            else:
                status2.append(k)

        return status2

    def time_to_8(self, t):
        """时间转东八区"""
        try:
            if len(t) == 20:
                gs = '%Y-%m-%dT%H:%M:%SZ'
            else:
                gs = '%Y-%m-%dT%H:%M:%S.%fZ'
            result = datetime.datetime.strptime(t, gs) + datetime.timedelta(hours=8)
            return result.strftime('%Y-%m-%d %H:%M:%S') + ' (北京时间)'
        except:
            return t

    def del_dict_none(self, d: dict):
        """删除字典中值为None的键"""
        l = []
        for k, v in d.items():
            if v is None or v == '' or v == []:
                l.append(k)
        return [d.pop(i, None) for i in l]

    def whois(self):
        whois_data = whois_answer(self.domain)
        if whois_data.get('register'):
            answer = {
                'code': 200,
                'domain': whois_data['domain'],
                'domain_code': whois_data['domain'],
                'info': whois_data['raw'],
                'status': self.status(whois_data['register']),
                'data': {
                    'DNS': whois_data['dns'],
                    'DNSSEC': self.dnssec(whois_data['dnssec']),
                    'IANA_ID': whois_data['iana'],
                    "whois-ser": whois_data['whois-ser'],
                    "域名": whois_data['domain'],
                    "更新日": self.time_to_8(whois_data['updated_date']),
                    "注册商": whois_data['ser-name'],
                    "注册商网址": whois_data['ser-url'],
                    "注册日": self.time_to_8(whois_data['creation_date']),
                    "状态": self.domain_status(whois_data['status']),
                    "过期日": self.time_to_8(whois_data['expired_date']),
                    "状态描述": self.domain_long(whois_data['creation_date']),
                    "更新时间": self.time_to_8(whois_data['update_db_date'])
                }
            }
            # 去除None值的键
            self.del_dict_none(answer['data'])

            names = [
                "域名",
                "注册商",
                "whois-ser",
                "更新日",
                "注册日",
                "过期日",
                "IANA_ID",
                "状态",
                "DNS",
                "DNSSEC",
                "更新时间"
            ]
            answer['data']['顺序'] = [i for i in names if i in answer['data'].keys()]
        else:
            answer = {
                'code': 201,
                'domain': self.domain,
                'domain_code': self.domain,
                'info': whois_data['raw'],
                'status': self.status(whois_data['register']),
                'data': {
                    '域名': self.domain
                }
            }

        return answer

    def premium(self, p):
        """判断是否溢价"""
        if p == 'false':
            return 0
        elif p == 'true':
            return 1
        else:
            return None

    def price(self):
        try:
            url = f'https://api.tian.hu/whois.php?domain={self.domain}&action=checkPrice'
            response = requests.get(url=url, timeout=self.timeout, headers=self.headers)

            raw_json = response.json()
            raw_data = raw_json.get('data')
            answer = {
                'code': 200,
                'domain': self.domain,
                'domain_code': self.domain,
                'new1': raw_data.get('register'),
                'premium': self.premium(raw_data.get('premium')),
                'status': '',
                'registrar1': '',
                'renew1': raw_data.get('renew')
            }
            return answer
        except:
            return {
                "code": 200,
                "domain": self.domain,
                "domain_code": self.domain,
                "new1": "??",
                "premium": 0,
                "registrar1": "",
                "renew1": "??",
                "status": ""
            }

    def icp(self):
        url = f'https://v.api.aa1.cn/api/icp/index.php?url={self.domain}'
        try:
            response = requests.post(url=url, timeout=self.timeout, headers=self.headers)
            raw_json = response.json()
            if raw_json.get('name') is None:
                answer = {
                    'code': 201,
                    'domain': self.domain,
                    'msg': '未查到信息'
                }
            else:
                answer = {
                    'code': 200,
                    'domain': self.domain,
                    'msg': '查询成功',
                    'data': [
                        raw_json.get('icp'),
                        raw_json.get('name'),
                        raw_json.get('tyle'),
                        raw_json.get('updateRecordTime')
                    ]
                }
            return answer
        except:
            return {
                'code': 201,
                'domain': self.domain,
                'msg': '未查到信息'
            }


def random_headers():
    lists = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36',
        'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; pl-PL; rv:1.0.1) Gecko/20021111 Chimera/0.6',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/418.8 (KHTML, like Gecko, Safari) Cheshire/1.0.UNOFFICIAL',
        'Mozilla/5.0 (X11; U; Linux i686; nl; rv:1.8.1b2) Gecko/20060821 BonEcho/2.0b2 (Debian-1.99+2.0b2+dfsg-1)',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
        'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
        'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
        'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0.6',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36']
    return random.choice(lists)


def whois_answer(domain):
    try:
        result = WHOIS(domain=domain, timeout=5)

        status = result.get('DOMAIN STATUS')
        if type(status) is not list:
            status = [status]

        domain_name = result.get('DOMAIN NAME')
        if domain_name is None:
            register = False
        else:
            register = True

        answer = {
            'code': 200,
            'domain': str(domain_name).lower(),
            'iana': result.get('REGISTRAR IANA ID'),
            'whois-ser': result.get('REGISTRAR WHOIS SERVER'),
            'ser-url': result.get('REGISTRAR URL'),
            'updated_date': result.get('UPDATED DATE'),
            'creation_date': result.get('CREATION DATE'),
            'expired_date': result.get('REGISTRY EXPIRY DATE'),
            'ser-name': result.get('REGISTRAR'),
            'status': status,
            'dns': result.get('NAME SERVER'),
            'dnssec': result.get('DNSSEC'),
            'update_db_date': result.get('LAST UPDATE OF WHOIS DATABASE'),
            'raw': result.raw.decode('utf-8'),
            'register': register
        }
        return answer
    except Exception as e:
        print('>>>', e)
        return {
            'code': 500,
            'msg': e
        }


if __name__ == '__main__':
    result = Whois('iaaaaa.com').whois()
    print(result)
