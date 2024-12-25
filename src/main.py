import logging
from discord.ext import commands, tasks
from datetime import datetime, timezone, timedelta, time
import discord
import requests
import os
from keep_alive import keep_alive
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

TOKEN = os.getenv("DISCORD_TOKEN")
SCHEDULE_URL = os.getenv("SCHEDULE_URL")
INSTRUCTORS_URL = os.getenv("INSTRUCTORS_URL")

logging.basicConfig(level=logging.INFO)

bot = commands.Bot(
    command_prefix="$",  # $コマンド名　でコマンドを実行できるようになる
    case_insensitive=True,  # コマンドの大文字小文字を区別しない ($hello も $Hello も同じ!)
    intents=intents,  # 権限を設定
)

JST = timezone(timedelta(hours=+9), "JST")

scheduled_times = [
    time(hour=10, tzinfo=JST),
    time(hour=12, tzinfo=JST),
    time(hour=16, tzinfo=JST),
]


def get_reservation_emoji(count):
    if count == 0:
        return "⛳️"
    elif count == 1:
        return "🟢"
    elif count == 2:
        return "🟡🟡"
    elif count == 3:
        return "🟡🟡🟡"
    elif count == 4:
        return "🔴🔴🔴🔴"
    elif count == 5:
        return "🔴🔴🔴🔴🔴"
    return ""


def fetch_schedule(today):
    response = requests.get(SCHEDULE_URL.replace("{today}", today)).json()
    return response["data"]["studio_lessons"]["items"]


def fetch_instructors():
    instructors_response = requests.get(INSTRUCTORS_URL).json()
    instructors = instructors_response["data"]["instructors"]["list"]
    return {instructor["id"]: instructor["name"] for instructor in instructors}


def format_schedule(items, instructor_map, instructor_name_filter, date_filter):
    schedule_info = {}
    for item in items:
        instructor_name = instructor_map.get(item["instructor_id"], "不明")
        if instructor_name_filter and instructor_name_filter != instructor_name:
            continue
        start_time = datetime.fromisoformat(item["start_at"]).strftime("%H:%M")
        end_time = datetime.fromisoformat(item["end_at"]).strftime("%H:%M")
        date = item["date"]
        lesson_info = (
            f"  - {start_time} - {end_time} {instructor_name} "
            f"{get_reservation_emoji(item['reservation_count'])}"
        )

        if date not in schedule_info:
            schedule_info[date] = []
        schedule_info[date].append(lesson_info)

    formatted_schedule = []

    if date_filter:
        for date, lessons in schedule_info.items():
            if date == date_filter:
                formatted_schedule.append(f"- {date}")
                formatted_schedule.extend(lessons)
    else:
        for date, lessons in schedule_info.items():
            formatted_schedule.append(f"- {date}")
            formatted_schedule.extend(lessons)

    if len(formatted_schedule) == 0:
        formatted_schedule.append(
            "😌 There are no available lessions for this condistions"
        )
    return formatted_schedule


@bot.event
async def on_ready():
    scheduled_message.start()
    print("Bot is ready!")


@bot.event
async def on_message(message):
    instructor_name_filter = None
    date_filter = None

    if message.content.startswith("!schedule"):
        logging.info(f"Received message: {message.content}")
        parts = message.content.split()
        instructor_name_filter = parts[1] if len(parts) > 1 else None
        date_filter = parts[2] if len(parts) > 2 else None
        await execute(message, instructor_name_filter, date_filter)
    elif message.content.startswith("大竹神"):
        logging.info(f"Received message: {message.content}")
        instructor_name_filter = "大竹"
        await execute(message, instructor_name_filter, date_filter)


async def execute(message, instructor_name_filter, date_filter):
    today = datetime.today().strftime("%Y-%m-%d")
    items = fetch_schedule(today)
    instructor_map = fetch_instructors()
    formatted_schedule = format_schedule(
        items, instructor_map, instructor_name_filter, date_filter
    )

    try:
        await message.reply(">>> " + "\n".join(formatted_schedule)[0:3000])
        logging.info("Message replied successfully")
    except Exception as e:
        logging.error(f"Failed to reply to message: {e}")


# Send Otake's schedule to the channel by specified scheduled times
@tasks.loop(times=scheduled_times)
async def scheduled_message():
    logging.info("Running scheduled message")
    today = datetime.today().strftime("%Y-%m-%d")
    items = fetch_schedule(today)
    instructor_map = fetch_instructors()
    formatted_schedule = format_schedule(items, instructor_map, "大竹", today)

    channel = bot.get_channel(int(os.getenv("CHANNEL_ID")))
    try:
        message_header = "** Alert for O-take's schedule today: **\n"
        await channel.send(
            message_header + ">>> " + "\n".join(formatted_schedule)[0:3000]
        )
        logging.info("Scheduled message sent successfully")
    except Exception as e:
        logging.error(f"Failed to send scheduled message: {e}")


if __name__ == "__main__":
    keep_alive()
    bot.run(TOKEN)
