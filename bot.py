from telegram import ChatAction, Update
from telegram.ext import CommandHandler, Updater, CallbackContext
import logging
from os import environ, remove
from tempfile import mkstemp
from gtts import gTTS

TOKEN = environ['TOKEN']
CHAT_ID = environ['CHAT_ID']


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

    

def text_to_audio(message_text: str):
        fd, path = mkstemp(suffix='.mp3')
        tts = gTTS(message_text, lang='id')
        tts.save(path)

        return path

def start(update: Update, context: CallbackContext) -> None:
    if str(update.message.chat_id) == str(CHAT_ID):
        update.message.reply_text("Hai, subscribe ke deryl and darren channel ya 😁😁")

def say(update: Update, context: CallbackContext) -> None:
    if str(update.message.chat_id) == str(CHAT_ID):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.RECORD_AUDIO)
        audio_path = text_to_audio(" ".join(filter(lambda x:x[0]!='/', update.message.text.split())))

        with open(audio_path, 'rb') as f:
            update.message.reply_voice(f, reply_to_message_id=update.message.message_id)
        
        # this is not safe, but...
        remove(audio_path)


def main():
    # Set up the telegram interface
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('tts', say))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
