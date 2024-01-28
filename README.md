# DiscordBitcoinStatsBot

Python3 is required
some other packages are required also:
requests
bs4
discord

to install packages on Mac:
python3 -m pip install requests bs4 discord

Linux:
pip3 install requests bs4 discord

You need a Discord Bot + token:
https://discord.com/developers/docs/intro
once you are inside your discord application and have a bot, click on the bot tab
![image](https://github.com/AnonymousBitcoinClub/DiscordBitcoinStatsBot/assets/54378383/34a33f60-b5ed-46ab-876a-5548122d0071)
and copy your TOKEN ![image](https://github.com/AnonymousBitcoinClub/DiscordBitcoinStatsBot/assets/54378383/5986bb05-bf0a-42c1-b0f3-48b5d1d5c779)

inside the file dtoken.py replace the token with your own & save file

now we setup discord channels:
inside your discord create a voice channel for each variable we are using, in this case 6 vchat channels, in permissions for the channels set view as True & connect as False

copy all 6 channel IDs to DiscordStats.py (may need to turn discord developer on in your discord settings)

inside of DiscordStats.py
BTC_PRICE_CHANNEL_ID = 1231231231231231231
BTC_BLOCK_CHANNEL_ID = 1231231231231231231
BTC_FEES_CHANNEL_ID = 1231231231231231231
ORDINAL_NUMBER_CHANNEL_ID = 1231231231231231231
DISCORD_MEMBERS_COUNT_CHANNEL_ID = 1231231231231231231
FLOOR_PRICE_CHANNEL_ID = 1231231231231231231  # Replace with the actual channel ID

and now if your collection is on ordinalswallet change this URL in DiscordStats.py to your projects URL:
url = 'https://ordinalswallet.com/collection/abc'

YOU ARE DONE AND CAN RUN THE ENTIRE BOT!

If you wish not to run certain stats, simply comment out their loops in the on_ready() function.
heres an example removing the floor price and block number:
async def on_ready():
    delay = 30
    print(f"We have logged in as {bot.user}")
    update_bitcoin_price.start()
    await asyncio.sleep(delay)
    #update_bitcoin_block.start()
    #await asyncio.sleep(delay)
    update_bitcoin_fees.start()
    await asyncio.sleep(delay)
    update_ordinal_number.start()
    await asyncio.sleep(delay)
    update_discord_members_count.start()
    await asyncio.sleep(delay)
    #update_floor_price.start()

if you have any more question, jump into the Anonymous Bitcoin Club discord and ask for help:
https://discord.gg/77nExvqXBv
