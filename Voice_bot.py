import logging
import time
import os

from telegram import Update
from telegram.ext import Application, ApplicationBuilder, CommandHandler, MessageHandler, filters
import pyttsx3

TOKEN = "7122328284:AAHpZEAIWSV0u2exmvEBQ2cymTqSxHZXXzQ"

def convert_text_to_audio(text):
    """Converts text to audio and returns the path to the audio file."""
    engine = pyttsx3.init()
    tmp_file_name = f"sms_{int(time.time())}"
    file_path = f"data/{tmp_file_name}.mp3"
    engine.save_to_file(text, file_path)
    engine.runAndWait()
    return file_path

async def hello(update, context):
    await update.message.reply_text(f"Здраствуйте, Сэр {update.effective_user.first_name}, ваша овсянка на столе")

async def help(update, context):
    await update.message.reply_text("Бот создан для преобразования текста в голосовое сообщение")

async def start(update, context):
    await update.message.reply_text("Я и так включен, давай свой текст")

async def echo(update, context):
    """Echo the user message."""
    text = update.message.text
    audio_file_path = convert_text_to_audio(text)
    await context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(audio_file_path, 'rb'))
    os.remove(audio_file_path)  

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

app.run_polling()