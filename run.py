import sqlite3
import telebot
import time
from configure import months, replace_first_args, replace_second_args

bot = telebot.TeleBot("1602990129:AAHzVZVs4FkPWQrIqrZr3ja5jFwhO_6BCkk")
bot.config['api_key'] = "1602990129:AAHzVZVs4FkPWQrIqrZr3ja5jFwhO_6BCkk"
channel_name = "@old_sports"

def norm(text):
    if "ИВНПМО" in text:
        return False
    else:
        for first in replace_first_args:
            for second in replace_second_args:
                text.replace(first+second, first+"\n"+second)
        
        return text

def filter(content):
    first_line = "{} {} {}".format(content[3], months[str(content[2])], content[1])
    second_line = content[4][1:]
    third_line = norm(content[5])
    if third_line !=False:
        return first_line + "\n\n" + second_line + "\n\n" + third_line
    else:
        return False
while True:
    conn = sqlite3.connect("posts_copy")
    cursor = conn.cursor()
    cursor.execute("SELECT rowid, * FROM posts ORDER BY RANDOM() LIMIT 1;")
    content = cursor.fetchall()
    delete = conn.cursor()
    delete.execute("DELETE FROM posts where rowid = {0}".format(content[0][0]))
    result = filter(content[0])
    if result!=False:
        conn.commit()
        conn.close()
        try:
            bot.send_message(channel_name, result)
            print("post published")
            time.sleep(600)
        except telebot.apihelper.ApiTelegramException:
            pass
    else:
        pass