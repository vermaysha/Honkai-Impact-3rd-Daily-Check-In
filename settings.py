# settings
import logging
import json
import requests
import os
import re
from requests.exceptions import HTTPError

__all__ = ['log', 'CONFIG', 'req']

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S')

log = logger = logging

class _Config:
    GIH_VERSION = 'No one cares about the version anyways'
    LOG_LEVEL = logging.INFO
    # LOG_LEVEL = logging.DEBUG

    # HoYoLAB
    LANG = 'en-us'
    OS_ACT_ID = 'e202110291205111'
    OS_REFERER_URL = 'https://act.hoyolab.com/bbs/event/signin-bh3/index.html?act_id={}'.format(OS_ACT_ID)
    OS_REWARD_URL = 'https://sg-public-api.hoyolab.com/event/mani/home?lang={}&act_id={}'.format(LANG, OS_ACT_ID)
    OS_ROLE_URL = 'https://api-os-takumi.mihoyo.com/binding/api/getUserGameRolesByCookie?game_biz={}'.format('bh3_global')
    OS_INFO_URL = 'https://sg-public-api.hoyolab.com/event/mani/info?lang={}&act_id={}'.format(LANG, OS_ACT_ID)
    OS_SIGN_URL = 'https://sg-public-api.hoyolab.com/event/mani/sign?lang={}'.format(LANG)
    WB_USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E150'


class HttpRequest(object):
    @staticmethod
    def to_python(json_str: str):
        return json.loads(json_str)

    @staticmethod
    def to_json(obj):
        return json.dumps(obj, indent=4, ensure_ascii=False)

    def request(self, method, url, max_retry: int = 2,
            params=None, data=None, json=None, headers=None, **kwargs):
        for i in range(max_retry + 1):
            try:
                s = requests.Session()
                response = s.request(method, url, params=params,
                    data=data, json=json, headers=headers, **kwargs)
                # print("Request Headers: ", response.request.headers)
                # print("Response Headers: ", response.headers)
                # print("Response Content: ", response.content)
            except HTTPError as e:
                log.error(f'HTTP error:\n{e}')
                log.error(f'The NO.{i + 1} request failed, retrying...')
            except KeyError as e:
                log.error(f'Wrong response:\n{e}')
                log.error(f'The NO.{i + 1} request failed, retrying...')
            except Exception as e:
                log.error(f'Unknown error:\n{e}')
                log.error(f'The NO.{i + 1} request failed, retrying...')
            else:
                return response

        raise Exception(f'All {max_retry + 1} HTTP requests failed, die.')


req = HttpRequest()
CONFIG = _Config()
log.basicConfig(level=CONFIG.LOG_LEVEL)
if os.environ.get('USER_AGENT'):
    CONFIG.WB_USER_AGENT = os.environ.get('USER_AGENT')

MESSAGE_TEMPLATE = '''
    {today:#^28}
    
    {nick_name} — AR{level}
    [{region_name}] {uid}
    Today's rewards: {award_name} × {award_cnt}
    Monthly Check-In count: {total_sign_day} days
    Check-in result: {status}
    
    {end:#^28}'''

CONFIG.MESSAGE_TEMPLATE = MESSAGE_TEMPLATE