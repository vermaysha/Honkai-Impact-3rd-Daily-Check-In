# Honkai Impact 3rd Login Helper Guide

## 1. Make a WayScript Account
https://wayscript.com

## 2. Clone the Script
Go here and clone this script 
https://wayscript.com/script/DWZlmtT4

![enter image description here](https://i.imgur.com/6ZTfNBV.png)


## 3. Set up the time
![enter image description here](https://i.imgur.com/qBGiXmc.png)
![enter image description here](https://i.imgur.com/TyGbKpX.png)

## 4. Set up the secrets

Add the keys `OS_COOKIE` and `USER_AGENT`, the `DISCORD_WEBHOOK` is optional, see at end of page for webhook instructions

![enter image description here](https://i.imgur.com/9xCkMWk.png)

### 4.1 How to get OS_COOKIE ?
1. Go to the Daily Check-In event website https://act.hoyolab.com/bbs/event/signin-bh3/index.html?act_id=e202110291205111
2. Login with your account
_If you have never checked in before, manually check in once to ensure that your cookies are set properly._
3. Open the developer tools on your web browser (F12 on firefox/chrome)
4. Click on the “Console” tab
5. Type in  `document.cookie`  in the console
6. Copy all text output from console without quotes `'`
7. **PLEASE DON'T SHARE YOUR COOKIE TO ANYONE**

![enter image description here](https://i.imgur.com/TXdwjDp.png)

### 4.2 How to get USER_AGENT ?
You can get your user agent like so:
![enter image description here](https://i.imgur.com/Jy07NPf.png)

### 4.3 How to get DISCORD_WEBHOOK ? (OPTIONAL)
This is an  **OPTIONAL**  step to let the script send you a notification on Discord whenever it runs a check-in.
1. Create your own discord server and private channel.
2. Edit channel settings
![enter image description here](https://i.imgur.com/SjkvGmN.png)
3. Go into Integrations and view webhooks.
![enter image description here](https://i.imgur.com/7JtyoY9.png) 
4. Create a new webhook and copy the URL.![enter image description here](https://i.imgur.com/8wgtMEk.png)
5. Go back to the “.secrets” tab and add a new secret called DISCORD_WEBHOOK.

## 5. Run the script

![enter image description here](https://i.imgur.com/G71bFuS.png)

Result
![enter image description here](https://i.imgur.com/IrwlZ51.png)