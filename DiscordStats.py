#coded by BitcoinJake09 in Anonymous Bitcoin Club
import os
import requests
import json
import discord
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from discord.ext import commands, tasks
from dtoken import TOKEN

COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
BLOCKCHAIR_API_URL = "https://api.blockchair.com/bitcoin/stats"
ORD_URL = 'https://turbo.ordinalswallet.com'
BTC_PRICE_CHANNEL_ID = 1231231231231231231
BTC_BLOCK_CHANNEL_ID = 1231231231231231231
BTC_FEES_CHANNEL_ID = 1231231231231231231
ORDINAL_NUMBER_CHANNEL_ID = 1231231231231231231
DISCORD_MEMBERS_COUNT_CHANNEL_ID = 1231231231231231231
FLOOR_PRICE_CHANNEL_ID = 1231231231231231231  # Replace with the actual channel ID
url = 'https://ordinalswallet.com/collection/abc'
    
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
bot = commands.Bot(command_prefix="!", intents=intents)
taskDelay = 10


async def get_floor_price():
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        floor_price_element = soup.find('div', {'class': 'CollectionStat_value__wetim text-sm semibold'})

        if floor_price_element:
            floor_price = floor_price_element.text.strip()
            return floor_price
    return None


async def get_inscriptions():
    print("test 2")
    res = requests.get(f"{ORD_URL}/inscriptions")
    if res.status_code != 200:
        print(f"Failed to fetch inscriptions: {res.status_code}. Retrying in 10 seconds.")
        return {}
    return res.json()

async def get_bitcoin_price():
    async with aiohttp.ClientSession() as session:
        async with session.get(COINGECKO_API_URL) as response:
            data = await response.json()
            return data["bitcoin"]["usd"]

async def get_blockchair_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(BLOCKCHAIR_API_URL) as response:
            data = await response.json()
            return data["data"]

@bot.event
async def on_ready():
    delay = 30
    print(f"We have logged in as {bot.user}")
    update_bitcoin_price.start()
    await asyncio.sleep(delay)
    update_bitcoin_block.start()
    await asyncio.sleep(delay)
    update_bitcoin_fees.start()
    await asyncio.sleep(delay)
    update_ordinal_number.start()
    await asyncio.sleep(delay)
    update_discord_members_count.start()
    await asyncio.sleep(delay)
    update_floor_price.start()



@tasks.loop(minutes=taskDelay)
async def update_bitcoin_price():
    price = await get_bitcoin_price()
    channel = bot.get_channel(BTC_PRICE_CHANNEL_ID)
    await channel.edit(name=f"BTC: ${price:.2f}")

@tasks.loop(minutes=taskDelay)
async def update_bitcoin_block():
    data = await get_blockchair_data()
    block = data["blocks"]
    channel = bot.get_channel(BTC_BLOCK_CHANNEL_ID)
    await channel.edit(name=f"Block: {block}")

@tasks.loop(minutes=taskDelay)
async def update_bitcoin_fees():
    data = await get_blockchair_data()
    fees = data["suggested_transaction_fee_per_byte_sat"]
    channel = bot.get_channel(BTC_FEES_CHANNEL_ID)
    await channel.edit(name=f"Fees: {fees} sat/vByte")

@tasks.loop(minutes=taskDelay)
async def update_ordinal_number():
    print("test 1")
    data = await get_inscriptions()

    if not any(item.get('content_type') for item in data):
        print("No data received. Retrying in 10 seconds.")
    else:
        print("test 3")
        # Extract values
        content_types = [item['content_type'] for item in data if item.get('content_type')]
        ids = [item['id'] for item in data if item.get('id')]
        nums = [item['num'] for item in data if item.get('num')]
        #print(f"Nums: {nums}")
        highest_value = max(nums)
        channel = bot.get_channel(ORDINAL_NUMBER_CHANNEL_ID)
        await channel.edit(name=f"Ord: {highest_value}")

@tasks.loop(minutes=taskDelay)
async def update_discord_members_count():
    guild = bot.guilds[0]
    members_count = guild.member_count
    channel = bot.get_channel(DISCORD_MEMBERS_COUNT_CHANNEL_ID)
    await channel.edit(name=f"Members: {members_count}")

@tasks.loop(minutes=taskDelay)
async def update_floor_price():
    floor_price = await get_floor_price()
    if floor_price:
        channel = bot.get_channel(FLOOR_PRICE_CHANNEL_ID)
        await channel.edit(name=f"OW/Floor $: {floor_price} BTC")
    else:
        print("Failed to fetch the floor price.")

update_bitcoin_price.before_loop
async def before_update_bitcoin_price():
    await bot.wait_until_ready()

bot.run(TOKEN)
