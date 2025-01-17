import ptbot
from pytimeparse import parse
import os
from dotenv import load_dotenv


def notify_progress(secs_left, chat_id, id, start_time):
    progress = render_progressbar(start_time, start_time-secs_left)
    bot.update_message(chat_id, id, "Осталось {} секунд!\n{}".format(secs_left, progress))


def create_countdown(chat_id, message):
    time = parse(message)
    message_id = bot.send_message(chat_id, f"Осталось {time} секунд")
    bot.create_countdown(
        time,
        notify_progress,
        chat_id=chat_id,
        id=message_id,
        start_time=time
    )
    bot.create_timer(time, send_finish, chat_id=chat_id)


def send_finish(chat_id):
    bot.send_message(chat_id, "Время вышло")


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


if __name__ == "__main__":
    load_dotenv()
    TG_TOKEN = os.getenv("TG_TOKEN")
    bot = ptbot.Bot(TG_TOKEN)
    bot.reply_on_message(create_countdown)
    bot.run_bot()