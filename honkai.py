import os

from settings import log, CONFIG
from sign import Sign
from notify import Notify

if __name__ == '__main__':

    notify = Notify()
    msg_list = []
    ret = success_num = fail_num = 0
    """
    HoYoLAB Community's COOKIE
    :param OS_COOKIE: HoYoLAB cookie(s) for one or more accounts.
        Separate cookies for multiple accounts with the hash symbol #
        e.g. cookie1text#cookie2text
        Do not surround cookies with quotes "" if using Github Secrets.
    """

    OS_COOKIE = ''
    token = ''

    if os.environ.get('OS_COOKIE', '') != '':
        OS_COOKIE = os.environ.get('OS_COOKIE')
    else:
        log.error("'OS_COOKIE' not found, ensure that variable exists")
        raise Exception("OS_COOKIE not found, ensure that it exists and set exactly to OS_COOKIE")

    cookie_list = OS_COOKIE.split('#')
    log.info(f'Number of account cookies read: {len(cookie_list)}')
    for i in range(len(cookie_list)):
        log.info(f'Preparing NO.{i + 1} Account Check-In...')
        try:
            #ltoken = cookie_list[i].split('ltoken=')[1].split(';')[0]
            token = cookie_list[i].split('cookie_token=')[1].split(';')[0]
            msg = f'	NO.{i + 1} Account:{Sign(cookie_list[i]).run()}'
            msg_list.append(msg)
            success_num = success_num + 1
        except IndexError:
            cookie_values = ["login_ticket","account_id","cookie_token","ltoken","ltuid","mi18nLang","_MHYUUID"]
            for j in cookie_values:
                if not(j in cookie_list[i]):
                    log.error(f'{j} not found')
            fail_num = fail_num + 1
            ret = -1
            log.info(f"\n\nTry these troubleshooting steps and grab the cookie again:\n -Log out and log back in\n -Ensure you are on the Daily Rewards page and not the HoyoLab Forums page\n -Try incognito mode\n -Try clearing your browser history/cache\n -Try using another browser\n")
        except Exception as e:
            if (len(cookie_list)>1):
                log.error("If you are using multiple accounts, refer to the screenshot here https://i.imgur.com/kYRZlF1.png")
            if not token:
                log.error("Cookie token not found, please try to relog on the check-in page.")

            msg = f'	NO.{i + 1} Account:\n    {e}'
            msg_list.append(msg)
            fail_num = fail_num + 1
            log.error(msg)
            ret = -1
        continue
    notify.send(status=f'\n  -Number of successful sign-ins: {success_num} \n  -Number of failed sign-ins: {fail_num}', msg=msg_list)
    if ret != 0:
        log.error('program terminated with errors')
        exit(ret)
    log.info('exit success')
    log.info("You can safely ignore the message below if the sign in is successful 'SCRIPT TERMINATED: Script haulted due to an error from the python_code module.'")
