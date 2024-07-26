import os
import telebot
from dotenv import load_dotenv
from meilisearchdata import meili_search_text
from model import get_chat_response
import whisper
import tempfile

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, parse_mode='HTML')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hi Monika, how are you doing?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

def transcribe_audio_file(downloaded_file):
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(downloaded_file)
        temp_file_path = tmp_file.name

    model = whisper.load_model("base")

    result = model.transcribe(temp_file_path)

    os.remove(temp_file_path)

    return result["text"]

@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    try:
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        transcription = transcribe_audio_file(downloaded_file)
        bot.reply_to(message, transcription)

        handle_search_query(message, transcription)
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")

def handle_search_query(message, query):
    try:
        chat_id = message.chat.id
        
        bot.send_message(chat_id, "Searching ...")
        
        search_results = meili_search_text(query)
        
        if search_results:
            prompt = f"User query: {query}\n\nSearch results:\n"
            for result in search_results:
                prompt += f"\n{result}\n"
            
            response_text = get_chat_response(prompt)
            bot.send_message(chat_id, response_text, parse_mode='HTML')
        else:
            bot.send_message(chat_id, "No results found.")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred while searching: {str(e)}")

bot.infinity_polling()
