import logging
from typing import Dict

import requests
from bs4 import BeautifulSoup
from telegram import (InputMedia, KeyboardButton, Location, ParseMode,
                      ReplyKeyboardMarkup, ReplyKeyboardRemove, Update)
from telegram.ext import (CallbackContext, CommandHandler, ConversationHandler,
                          Filters, MessageHandler, Updater)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = "5470929952:AAEwtUHStfTEhwFt1oisEzBTnmfoxZCr4Es"

def start_keyboard():
    return ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton("Sotib olish"), 
             KeyboardButton("Ijaraga olish")]
        ],
        resize_keyboard=True
    )
BUY = 0
RENT = 0

def start(update:Update, context: CallbackContext):
    update.message.reply_text(text=f"Salom {update.message.from_user.first_name}.\n\nSiz 1000kvartir.uz saytining Telegram botidan foydalanyapsiz.", reply_markup=start_keyboard())


def rent_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
                [KeyboardButton(text=str(i)) for i in range(1,5)],
                [KeyboardButton(text=str(i)) for i in range(5,9)],
                ],
        resize_keyboard=True
    )


def rent(update:Update, context:CallbackContext):
    update.message.reply_text(
        text="Ijaraga olmoqchi bo'lsangiz, unda quyidagi sonlardan birini bosing, va men sizga vebsaytning o'sha betidagi natijalarni yuboraman", reply_markup=rent_keyboard())
    return RENT


def buy_results(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    page_number = update.message.text

    try:
        url = ""
        if page_number == "1":
            url = "https://www.1000kvartir.uz/mr/sale"
        else:
            url = f"https://www.1000kvartir.uz/mr/sale?page={page_number}"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

        page = requests.get(url.strip(), headers=headers, timeout=10)
        soup = BeautifulSoup(page.text, "html.parser")

        general_descriptions = soup.find_all(
            "div", attrs={"class": "list-offers list-offers_mod"})
        for general_desc in general_descriptions:
            location = general_desc.find(
                "h4", attrs={"style": "margin-top:0; margin-bottom:10px;"}).text.strip()
            area = general_desc.find("li", attrs={"title": "Площадь"}).text.strip()
            floor = general_desc.find(
                "li", attrs={"title": "Этажность"}).text.strip()
            roomNum = general_desc.find(
                "li", attrs={"title": "Кол-во комнат"}).text.strip()
            price = general_desc.find(
                "span", attrs={"class": "desc-of1__price-of desc-of1__price-of_mod"}).text.strip()
            image = general_desc.find(
                "img", attrs={"class": "carousel-img"})["src"]
            imag = general_desc.find(
                "img", attrs={"class": "carousel-img"})
            link = imag.find_parent("a")["href"]

            image_src = f"https://www.1000kvartir.uz{image}"
            caption = f"{location}\n\n{area}\t{floor}\t{roomNum}\n\n{price}\n\nFor more: https://www.1000kvartir.uz{link}"
            context.bot.send_photo(chat_id, image_src, caption)
    except:
        context.bot.send_message(
                chat_id, "Kechirasiz, sotuvga hech nima topilmadi 🤔", reply_markup=start_keyboard())
    return ConversationHandler.END
  

def buy_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=str(i)) for i in range(1,5)],
            [KeyboardButton(text=str(i)) for i in range(5,9)]
            ],
        resize_keyboard=True
    )


def buy(update: Update, context: CallbackContext):
    update.message.reply_text(
        text="Sotib olmoqchi bo'lsangiz, unda quyidagi sonlardan birini bosing, va men sizga vebsaytning o'sha betidagi natijalarni yuboraman", reply_markup=buy_keyboard())
    return BUY

def rent_results(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    page_number = update.message.text
    
    try:
        url = ""
        if page_number == "1":
            url = "https://www.1000kvartir.uz/mr/rent"
        else:
            url = f"https://www.1000kvartir.uz/mr/rent?page={page_number}"
            
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

        page = requests.get(url.strip(), headers=headers, timeout=10)
        soup = BeautifulSoup(page.text, "html.parser")

        general_descriptions = soup.find_all("div", attrs={"class": "list-offers list-offers_mod"})
        for general_desc in general_descriptions:
            location = general_desc.find(
                "h4", attrs={"style": "margin-top:0; margin-bottom:10px;"}).text.strip()
            area = general_desc.find("li", attrs={"title": "Площадь"}).text.strip()
            floor = general_desc.find(
                "li", attrs={"title": "Этажность"}).text.strip()
            roomNum = general_desc.find(
                "li", attrs={"title": "Кол-во комнат"}).text.strip()
            price = general_desc.find(
                "span", attrs={"class": "desc-of1__price-of desc-of1__price-of_mod"}).text.strip()
            image = general_desc.find(
                "img", attrs={"class": "carousel-img"})["src"]
            imag = general_desc.find(
                "img", attrs={"class": "carousel-img"})
            link = imag.find_parent("a")["href"]

            image_src = f"https://www.1000kvartir.uz{image}"
            caption = f"{location}\n\n{area}\t{floor}\t{roomNum}\n\n{price}\n\nFor more: https://www.1000kvartir.uz{link}"
            context.bot.send_photo(chat_id, image_src, caption)
        context.bot.send_message(
            chat_id, "Mana senga olam-olam uuuuuy! 🎶\nEtagingga siqqanicha oooool! 😂")
    except:
        context.bot.send_message(
            chat_id, "Kechirasiz, ijaraga hech nima topa olmadim 🤔", reply_markup=start_keyboard())
    return ConversationHandler.END

def main():
    
    updater = Updater(TELEGRAM_TOKEN)
    
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    
    buy_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(
            Filters.text("Sotib olish"), buy)],
        states = {
            BUY: [MessageHandler(Filters.text(str(i)), buy_results) for i in range(1,9)]
        },
        fallbacks=[CommandHandler("start", start)]
        )
    rent_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(
            Filters.text("Ijaraga olish"), rent)],
        states={
            RENT: [MessageHandler(Filters.text(str(i)), rent_results) for i in range(1, 9)]
        },
        fallbacks=[CommandHandler("start", start)]
        )
    
    
    dispatcher.add_handler(buy_conv_handler)
    dispatcher.add_handler(rent_conv_handler)
    

    updater.start_polling()
    updater.idle()
    
if __name__=="__main__":
    main()