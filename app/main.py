#!/bin/python
import discord, asyncio, os, pathlib, time
from discord.ext import commands
from pony import orm

class CustomBot(commands.Bot):
    def __init__(self):
        super().__init__()
        self.db = orm.Database()

def main():
    bot = CustomBot()
    bot.intents.all()

    for x in range(0,15):
        time.sleep(3)
        try:
            bot.db.bind(provider='mysql', host='db', 
                user=os.getenv('MYSQL_USER'), 
                passwd=os.getenv('MYSQL_PASSWORD'), 
                db=os.getenv('MYSQL_DATABASE'))   
            break
        except Exception as e:
            print(e)

    current_dir = pathlib.Path(__file__).parent.resolve()
    bot.load_extension('cogs.init')
    for filename in os.listdir('%s/cogs' % current_dir):
        if filename.endswith('.py') and filename[:-3] != 'init':
            bot.load_extension(f'cogs.{filename[:-3]}')
    bot.db.generate_mapping(create_tables=True)
    bot.run(os.getenv('DISCORD_BOT_TOKEN'))

if __name__ == "__main__":
    main()
