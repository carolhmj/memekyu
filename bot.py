"""
	First draft for this silly bot
"""

import logging
import random

from aiogram import Bot, Dispatcher, executor, types
from apiclient.discovery import build
from apiclient.errors import HttpError
from bot_info import API_TOKEN, DEVELOPER_KEY

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
MAX_VIDEO_SEARCH_RESULTS = 50
BILL_CHANNEL = 'UCq6aw03lNILzV96UvEAASfQ'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY) 

@dp.message_handler(commands=['miichannel'])
async def mii_channel_video_selector(message: types.Message):
	video_url = select_random_video_by_keyword('mii channel but')
	await bot.send_message(message.chat.id, video_url)

@dp.message_handler(commands=['bill'])
async def bill_wurtz_video_selector(message: types.Message):
	video_url = select_random_video_by_channel(BILL_CHANNEL)
	await bot.send_message(message.chat.id, video_url)

@dp.message_handler()
async def echo(message: types.Message):
    await bot.send_message(message.chat.id, message.text)

def select_random_video_by_keyword(keyword):
	videos = youtube.search().list(q=keyword,
								   part="id,snippet",
								   maxResults=MAX_VIDEO_SEARCH_RESULTS).execute()
	return select_random_video(videos)						  

def select_random_video_by_channel(channel_id):
	videos = youtube.search().list(part="id,snippet",
								   channelId=channel_id,
								   maxResults=MAX_VIDEO_SEARCH_RESULTS).execute()
	return select_random_video(videos)						 

def select_random_video(videos):
	choosen = random.randrange(0,MAX_VIDEO_SEARCH_RESULTS-1)
	video_id = videos["items"][choosen]["id"]["videoId"]
	return build_youtube_url(video_id)

def build_youtube_url(id):
	return "https://www.youtube.com/watch?v="+id		    

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)