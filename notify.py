import os
from discord_webhook import DiscordWebhook, DiscordEmbed
from settings import log, req


class Notify(object):
    """
    :param PUSH_CONFIG: JSON-formatted parameters for creating a web request to a user-specified social media API.
        Format:
            {"method":"post","url":"","data":{},"text":"","code":200,"data_type":"data","show_title_and_desp":false,
            "set_data_title":"","set_data_sub_title":"","set_data_desp":""}
        Details:
            method: REQUIRED, HTTP method e.g. post
            url: REQUIRED, address of request.
            data: OPTIONAL, parameters sent in the body of the request.
            text: REQUIRED, key of expected response code
            code: REQUIRED, expected response code, e.g. 0
            data_type: OPTIONAL,format of parameters sent, CHOOSE one of: params|json|data

            ## no idea what any of the following is meant to do, don't ask
            show_title_and_desp: OPTIONAL, 是否将标题(应用名+运行状态)和运行结果合并.默认: false.
            set_data_title: REQUIRED,填写推送方式data中消息标题的key.例如: server酱的为text.
            set_data_sub_title: OPTIONAL,填写推送方式data中消息正文的key.有的推送方式正文的key有次级结构,
                需配合set_data_title构造子级,与set_data_desp互斥.
                例如: 企业微信中,set_data_title填text,set_data_sub_title填content.
            set_data_desp: OPTIONAL,填写推送方式data中消息正文的key.例如: server酱的为desp.
                与set_data_sub_title互斥,两者都填则本项不生效.

    :param DISCORD_WEBHOOK:
        ## https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks
    """
    # Github Actions -> Settings -> Secrets
    # Ensure that the Name exactly matches the parameter names required here
    # And the Value contains the data to be used

    def __init__(self):
        # Custom Push Config
        self.PUSH_CONFIG = ''
        if 'PUSH_CONFIG' in os.environ:
            self.PUSH_CONFIG = os.environ['PUSH_CONFIG']
        # Discord Webhook
        self.DISCORD_WEBHOOK = ''
        if 'DISCORD_WEBHOOK' in os.environ:
            self.DISCORD_WEBHOOK = os.environ['DISCORD_WEBHOOK']

    def pushTemplate(self, method, url, params=None, data=None, json=None, headers=None, **kwargs):
        name = kwargs.get('name')
        # needs = kwargs.get('needs')
        token = kwargs.get('token')
        text = kwargs.get('text')
        code = kwargs.get('code')
        if not token:
            log.info(f'{name} SKIPPED')
            return False
        try:
            response = req.to_python(req.request(
                method, url, 2, params, data, json, headers).text)
            rspcode = response[text]
        except Exception as e:
            log.error(f'{name} FAILED\n{e}')
        else:
            if rspcode == code:
                log.info(f'{name} SUCCESS')
            else:
                log.error(f'{name} FAILED\n{response}')
        return True

    def custPush(self, text, status, desp):
        PUSH_CONFIG = self.PUSH_CONFIG

        if not PUSH_CONFIG:
            log.info(f'Custom Notifications SKIPPED')
            return False
        cust = req.to_python(PUSH_CONFIG)
        title = f'{text} {status}'
        if cust['show_title_and_desp']:
            title = f'{text} {status}\n\n{desp}'
        if cust['set_data_title'] and cust['set_data_sub_title']:
            cust['data'][cust['set_data_title']] = {
                cust['set_data_sub_title']: title
            }
        elif cust['set_data_title'] and cust['set_data_desp']:
            cust['data'][cust['set_data_title']] = title
            cust['data'][cust['set_data_desp']] = desp
        elif cust['set_data_title']:
            cust['data'][cust['set_data_title']] = title
        conf = [cust['url'], cust['data'], 'Custom Notifications', cust['text'], cust['code']]
        url, data, name, text, code = conf

        if cust['method'].upper() == 'GET':
            return self.pushTemplate('get', url, params=data, name=name, token='token', text=text, code=code)
        elif cust['method'].upper() == 'POST' and cust['data_type'].lower() == 'json':
            return self.pushTemplate('post', url, json=data, name=name, token='token', text=text, code=code)
        else:
            return self.pushTemplate('post', url, data=data, name=name, token='token', text=text, code=code)

    def discordWebhook(self, text, status, desp):
        DISCORD_WEBHOOK = self.DISCORD_WEBHOOK

        if not DISCORD_WEBHOOK:
            log.info(f'Discord SKIPPED')
            return False

        webhook = DiscordWebhook(url=DISCORD_WEBHOOK)
        embed = DiscordEmbed(title=f'{text} {status}', description=desp, color='03b2f8')
        webhook.add_embed(embed)
        response = webhook.execute()
        if (response.status_code == 200):
            log.info(f'Discord SUCCESS')
        else:
            log.error(f'Discord FAILED\n{response}')
        return True

    def send(self, app='Honkai Impact 3rd Daily Sign-In', status='', msg='', **kwargs):
        hide = kwargs.get('hide', '')
        if isinstance(msg, list) or isinstance(msg, dict):
            # msg = self.to_json(msg)
            msg = '\n\n'.join(msg)
        if not hide:
            log.info(f'Sign-In result: {status}\n\n{msg}')

        if self.PUSH_CONFIG or self.DISCORD_WEBHOOK:
            log.info('Sending push notifications...')
            self.custPush(app, status, msg)
            self.discordWebhook(app, status, msg)
        else:
            log.info('No social media notifications configured to be sent.')


if __name__ == '__main__':
    Notify().send(app='Honkai Impact 3rd Check-In Helper', status='Test Run', msg='Testing integration with social media APIs')