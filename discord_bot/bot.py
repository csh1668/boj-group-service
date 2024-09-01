import aiohttp
async def get_score():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:8080/point') as response:
                return await response.text()  # 또는 response.json() 사용
    except aiohttp.ClientConnectorError:
        return "서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요."
    except Exception as e:
        return f"알 수 없는 오류가 발생했습니다: {e}"

import os, db, datetime
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("BOT_CHANNEL_ID"))

COMMAND_PREFIX = "!"
DATETIME_FORMAT = "%Y-%m-%d/%H:%M:%S"

def str2datetime(s):
    return datetime.datetime.strptime(s, DATETIME_FORMAT)

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

@bot.event
async def on_ready():
    print('Logged on as {0}'.format(bot.user.name))
    # await bot.change_presence(status=discord.Status.online, activity=discord.Game("대기"))

@bot.command()
async def load(ctx):
    if ctx.channel.id != CHANNEL_ID: return
    await ctx.send("로드 중..")
    os.system('python3.11 crawling/main.py')
    await ctx.send("로드 성공!")

@bot.command()
async def score(ctx):
    data = await get_score()
    await ctx.send(data)

@bot.command()
async def event(ctx, *args):
    if ctx.channel.id != CHANNEL_ID: return

    message = [
        "명령어```",
        "!event list",
        "!event truncate",
        "!event add [description] [start_time] [end_time] [problem_id]",
        "!event delete [id|description]```"
    ]
    if len(args) >= 1:
        if args[0] == "list":
            response = db.get_event()
            message = [
                "ID\tDESCRIPTION\tSTART_TIME\tEND_TIME\tPROBLEM_ID"
            ]
            for row in response:
                message.append('\t'.join(map(str,row)))
        elif args[0] == "truncate":
            rows = db.truncate_event()
            message = [
                f"{rows}개의 행을 지웠습니다."
            ]
        elif args[0] == "add" and len(args) >= 5:
            try:
                start_time = str2datetime(args[2])
                end_time = str2datetime(args[3])
                db.add_event(args[1], start_time, end_time, args[4])
                message = [
                    "이벤트를 추가했습니다."
                ]
            except:
                message = [
                    f"시간 형식은 다음과 같습니다. ```{DATETIME_FORMAT}```"
                ]
        elif args[0] == "delete" and len(args) >= 2:
            rows = 0
            try:
                id = int(args[1])
                rows = db.delete_event_by_id(id)
            except:
                rows = db.delete_event_by_description(args[1])
            message = [
                f"{rows}개의 행을 지웠습니다."
            ]
    await ctx.send('\n'.join(message))

bot.run(TOKEN)
db.close()