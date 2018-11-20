"""
	First draft for this silly bot
"""

import logging
import random

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ChatType, ParseMode, ContentTypes
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

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

BAD_CONTENT = ContentTypes.PHOTO & ContentTypes.DOCUMENT & ContentTypes.STICKER & ContentTypes.AUDIO

#Photo sending states
class PhotoUpload(StatesGroup):
	started = State()
	sent = State()
	processed = State()     

@dp.message_handler(commands=['miichannel'])
async def mii_channel_video_selector(message: types.Message):
	video_url = select_random_video_by_keyword('mii channel but')
	await bot.send_message(message.chat.id, video_url)

@dp.message_handler(commands=['bill'])
async def bill_wurtz_video_selector(message: types.Message):
	video_url = select_random_video_by_channel(BILL_CHANNEL)
	await bot.send_message(message.chat.id, video_url)

@dp.message_handler(commands=['deepfry'])
async def deepfry_start(message: types.Message):
	await PhotoUpload.started.set()
	await bot.send_message(message.chat.id, "Send a photo to be deep fried")	

@dp.message_handler(content_types=ContentTypes.PHOTO, state=PhotoUpload.started)
async def deepfry_wait_photo(message: types.Message):
	await PhotoUpload.next()
	res = await deepfry_photo(message.photo)
	await bot.send_photo(message.chat.id, res)

async def deepfry_photo(photo):
	downloaded = await bot.download_file_by_id(photo[0].file_id)
	print (downloaded)
	return downloaded

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