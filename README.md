# Sreality.cz Telegram bot

Here is a simple bot for searching real estate in Czech republic via sreality.cz
How it works
1. It runs continuously in background
2. Once a new Ad is published, it is parsed and sent to you via Telegram

How to setup 
1. Find a VM (you can do that on Azure, Digital Ocean, Google Cloud etc)
2. Install dependencies ```python3 -m pip install -r requirements.txt```
3. Insert your Telegram bot token into bot.py. You can read about how to get it [here](https://core.telegram.org/bots#6-botfather)
4. Find a chat where you want to receive messages. You can read about how to get it [here](https://core.telegram.org/bots/api#chatid)
5. Run the bot ```python3 bot.py```
6. Add this script to crontab to run it every 2-3 minutes. 

PS, this is a quickly developed bot. It is not perfect. But it helped to find an apartment for me ;) 