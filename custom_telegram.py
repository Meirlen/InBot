import logging
from tkinter.messagebox import NO
import requests
from copy import deepcopy
from sanic import Blueprint, response
from sanic.request import Request
from sanic.response import HTTPResponse, text
from telebot import TeleBot
from telebot.apihelper import ApiTelegramException
from telebot.types import (
    InlineKeyboardButton,
    Update,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    Message,
)
import shutil

from typing import Dict, Text, Any, List, Optional, Callable, Awaitable
from helper.Utils import *

from rasa.core.channels.channel import InputChannel, UserMessage, OutputChannel
from rasa.shared.constants import INTENT_MESSAGE_PREFIX
from rasa.shared.core.constants import USER_INTENT_RESTART
from rasa.shared.exceptions import RasaException
from actions.app_constans import *
from sanic.request import Request
from yandex_helper import geo_coder_yandex
from yandex_stt import transcribe_audio
from rasa_api import *
from telegram_admin_api import send_to_admin_simple_message
logger = logging.getLogger(__name__)


class TelegramOutput(TeleBot, OutputChannel):
    """Output channel for Telegram."""

    # skipcq: PYL-W0236
    @classmethod
    def name(cls) -> Text:
        return "telegram"

    def __init__(self, access_token: Optional[Text]) -> None:
        super().__init__(access_token)

    def add_data_to_txt(self, contents, file_path):
        file = open(file_path, "a")
        file.writelines(contents+'\n')
        file.close()

    



    def get_metadata(self, request: Request) -> Optional[Dict[Text, Any]]:
        """Extracts additional information from the incoming request.

        Implementing this function is not required. However, it can be used to extract
        metadata from the request. The return value is passed on to the
        ``UserMessage`` object and stored in the conversation tracker.

        Args:
            request: incoming request with the message of the user

        Returns:
            Metadata which was extracted from the request.
        """

        metadata = request.json
        print('Telegram metadata:' , metadata)
        try:
            user_id = metadata["message"]["from"]["id"]
            username = metadata["message"]["from"]["first_name"]
            chat_id = metadata["message"]["chat"]["id"]  

            res = {}
            res['user_id'] = user_id
            res['user_name'] = username
            res['chat_id'] = chat_id
            res['platform'] = 'telegram'

        except:
            user_id = metadata["callback_query"]["from"]["id"]
            username = metadata["callback_query"]["from"]["first_name"]
 
            res = {}
            res['user_id'] = user_id
            res['user_name'] = username
            res['platform'] = 'telegram'

        # print('get_metadata:_______',user_id)
        # print('get_metadata:_______',res)
        # print('get_metadata:_______',metadata)

        return res

    async def _extract_text_from_voice(self, msg: Message, sender_id) -> Text:
        bot_token = self.token
        file_id = msg.voice.file_id
        file_path_url = 'https://api.telegram.org/bot{}/getFile?file_id={}'.format(
            bot_token, file_id
        )
        file_path = requests.get(file_path_url)
        file_path = file_path.json().get('result').get('file_path')
        download_path = 'https://api.telegram.org/file/bot{}/{}'.format(
            bot_token, file_path
        )

        # print('Path audio:  '+download_path)

        local_filename = 'user_audio.ogg'
        with requests.get(download_path, stream=True) as r:
            with open(local_filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

        text = transcribe_audio().lower()

        file_path = str(sender_id)+'_test_case.txt'

        print(f'\033[1m User: \033[0m {text}')
        # self.add_data_to_txt(
        #     f'User:         {text}', f'/Users/meirlen/Desktop/bot/dataset/test/{file_path}')
        if text != None:
           return text.strip()
        else :
           return None   


    async def send_text_message(
        self, recipient_id: Text, text: Text, **kwargs: Any
    ) -> None:
        for message_part in text.strip().split("\n\n"):

            file_path = recipient_id+'_test_case.txt'

            # if message_part == 'данные очищены':
            #     delimetr = f'{message_part} \n--------------------\n--------------------'
            #     self.add_data_to_txt(
            #         delimetr, f'/Users/meirlen/Desktop/bot/dataset/test/{file_path}')
            # else:
            #     self.add_data_to_txt(
            #         f'CallBot:      {message_part} ', f'/Users/meirlen/Desktop/bot/dataset/test/{file_path}')



            print(f'CallBot:      {message_part} ')

            self.send_message(recipient_id, message_part.lower(), parse_mode='html')

    async def send_image_url(
        self, recipient_id: Text, image: Text, **kwargs: Any
    ) -> None:
        self.send_photo(recipient_id, image)

    async def send_text_with_buttons(
        self,
        recipient_id: Text,
        text: Text,
        buttons: List[Dict[Text, Any]],
        button_type: Optional[Text] = "inline",
        **kwargs: Any,
    ) -> None:
        """Sends a message with keyboard.

        For more information: https://core.telegram.org/bots#keyboards

        :button_type inline: horizontal inline keyboard

        :button_type vertical: vertical inline keyboard

        :button_type reply: reply keyboard
        """
        if button_type == "inline":
            print('INLINE BUTTON')
            reply_markup = InlineKeyboardMarkup(row_width=1)

            # web_info = {'url':'https://test-js-app123.herokuapp.com/'}
            # ,web_app = web_info 
            button_list = [
                InlineKeyboardButton(s["title"], callback_data=s["payload"])
                for s in buttons
            ]
            reply_markup.add(*button_list)

        elif button_type == "vertical":
            reply_markup = InlineKeyboardMarkup()
            [
                reply_markup.row(
                    InlineKeyboardButton(
                        s["title"], callback_data=s["payload"])
                )
                for s in buttons
            ]

        elif button_type == "reply":

            # drop button_type from button_list
            button_list = [b for b in buttons if b.get("title")]

            row_width=2
            if len(button_list) > 2:
                row_width=2

            reply_markup = ReplyKeyboardMarkup(
                resize_keyboard=False, one_time_keyboard=True,row_width=row_width
            )

            for idx, button in enumerate(buttons):
                if button["title"] == '\U000026F3 Отправить геопозицию':
                    reply_markup.row(KeyboardButton(
                        button["title"], request_location=True))
                elif button["title"] == '\U0001F4F1 Отправить мой номер телефона':
                    reply_markup.row(KeyboardButton(
                        button["title"], request_contact=True))
                else:
                    if isinstance(button, list):
                        reply_markup.row(KeyboardButton(
                            s["title"]) for s in button)
                    else:
                        reply_markup.row(KeyboardButton(button["title"]))
        else:
            logger.error(
                "Trying to send text with buttons for unknown "
                "button type {}".format(button_type)
            )
            return
        # , parse_mode='HTML'
        self.send_message(recipient_id, text.lower(),
                          reply_markup=reply_markup, parse_mode='html')

    async def send_custom_json(
        self, recipient_id: Text, json_message: Dict[Text, Any], **kwargs: Any
    ) -> None:
        json_message = deepcopy(json_message)

        recipient_id = json_message.pop("chat_id", recipient_id)

        send_functions = {
            ("text",): "send_message",
            ("photo",): "send_photo",
            ("audio",): "send_audio",
            ("document",): "send_document",
            ("sticker",): "send_sticker",
            ("video",): "send_video",
            ("video_note",): "send_video_note",
            ("animation",): "send_animation",
            ("voice",): "send_voice",
            ("media",): "send_media_group",
            ("latitude", "longitude", "title", "address"): "send_venue",
            ("latitude", "longitude"): "send_location",
            ("phone_number", "first_name"): "send_contact",
            ("game_short_name",): "send_game",
            ("action",): "send_chat_action",
            (
                "title",
                "decription",
                "payload",
                "provider_token",
                "start_parameter",
                "currency",
                "prices",
            ): "send_invoice",
        }

        for params in send_functions.keys():
            if all(json_message.get(p) is not None for p in params):
                args = [json_message.pop(p) for p in params]
                api_call = getattr(self, send_functions[params])
                api_call(recipient_id, *args, **json_message)


class TelegramInput(InputChannel):
    """Telegram input channel"""

    @classmethod
    def name(cls) -> Text:
        return "telegram"

    @classmethod
    def from_credentials(cls, credentials: Optional[Dict[Text, Any]]) -> InputChannel:
        if not credentials:
            cls.raise_missing_credentials_exception()

        return cls(
            credentials.get("access_token"),
            credentials.get("verify"),
            credentials.get("webhook_url"),
        )

    def __init__(
        self,
        access_token: Optional[Text],
        verify: Optional[Text],
        webhook_url: Optional[Text],
        debug_mode: bool = True,
    ) -> None:
        self.access_token = access_token
        self.verify = verify
        self.webhook_url = webhook_url
        self.debug_mode = debug_mode

    @staticmethod
    def _is_location(message: Message) -> bool:
        if message == None:
           return False
        return message.location is not None

    @staticmethod
    def _is_contact(message: Message) -> bool:
        if message == None:
           return False
        return message.contact is not None

    @staticmethod
    def _is_user_message(message: Message) -> bool:
        if message == None:
           return False
        return message.text is not None

    @staticmethod
    def _is_voice_message(message) -> bool:
        if message == None:
           return False
        return message.voice is not None

    @staticmethod
    def _is_edited_message(message: Update) -> bool:
        return message.edited_message is not None

    @staticmethod
    def _is_button(message: Update) -> bool:
        return message.callback_query is not None

    def blueprint(
        self, on_new_message: Callable[[UserMessage], Awaitable[Any]]
    ) -> Blueprint:
        telegram_webhook = Blueprint("telegram_webhook", __name__)
        out_channel = self.get_output_channel()

        @telegram_webhook.route("/", methods=["GET"])
        async def health(_: Request) -> HTTPResponse:
            return response.json({"status": "ok"})

        @telegram_webhook.route("/set_webhook", methods=["GET", "POST"])
        async def set_webhook(_: Request) -> HTTPResponse:
            s = out_channel.setWebhook(self.webhook_url)
            if s:
                logger.info("Webhook Setup Successful")
                return response.text("Webhook setup successful")
            else:
                logger.warning("Webhook Setup Failed")
                return response.text("Invalid webhook")

        @telegram_webhook.route("/webhook", methods=["GET", "POST"])
        async def message(request: Request) -> Any:
            if request.method == "POST":

                request_dict = request.json
                update = Update.de_json(request_dict)
                if not out_channel.get_me().username == self.verify:
                    logger.debug(
                        "Invalid access token, check it matches Telegram")
                    return response.text("failed")

                if self._is_button(update):
                    msg = update.callback_query.message
                    text = update.callback_query.data

                elif self._is_edited_message(update):

                    msg = update.edited_message
                    text = update.edited_message.text
                else:
                    msg = update.message
        
                    if self._is_user_message(msg):
                        if msg.text != None:
                           text = msg.text.replace("/bot", "")

                    elif self._is_contact(msg):
                        text = msg.contact.phone_number
                        print('Contact is: ' + text)

                    elif self._is_location(msg):
                        text = '{{"lng":{0}, "lat":{1}}}'.format(
                            msg.location.longitude, msg.location.latitude
                        )
                        text = geo_coder_yandex(str(msg.location.longitude),str(msg.location.latitude))
                        print('Yandex api return: ' + text)

                    elif self._is_voice_message(msg):
                        # text = "История"
                        text = await out_channel._extract_text_from_voice(msg, msg.chat.id)
                        message_type = 'audio'
                    else:
                        print('Here 5')
                        return response.text("success")
                sender_id = msg.chat.id

                if sender_id == ADMIN_CHAT_ID:
                    print('ADMIN:' , text )
                    try:
                        action_name,conversation_id = text.split(',')
                        if action_name.isdigit(): # price, example: 500,77714857133
                            new_price = action_name
                            call_update_slot_by_api_multi_proccess(conversation_id,new_price)
                            send_to_admin_simple_message("Спасибо")
                            call_custom_action_im_multi_proccess(conversation_id,"action_admin_price_submit")

                        elif action_name == "price_no_correct": 
                            call_update_slot_by_api_multi_proccess(conversation_id,None)
                            send_to_admin_simple_message("Спасибо")
                            call_custom_action_im_multi_proccess(conversation_id,"action_admin_price_submit")

                        else:
                            call_custom_action_im_multi_proccess(conversation_id,action_name)
                            send_to_admin_simple_message("Спасибо")
                    except:
                         print('Some admin error')
                    return response.text("Не нужно отвечать на сообщени админстратора")

                # print(f' Sender_id: {sender_id}')
                metadata = out_channel.get_metadata(request)
                print('Metadata AAA: '+str(metadata))
                try:
                    text = pre_proccess_text(text)

                    print('User said: '+text)

                    if text == (INTENT_MESSAGE_PREFIX + USER_INTENT_RESTART):
                        await on_new_message(
                            UserMessage(
                                text,
                                out_channel,
                                sender_id,
                                input_channel=self.name(),
                                metadata=metadata,
                            )
                        )
                        await on_new_message(
                            UserMessage(
                                "/start",
                                out_channel,
                                sender_id,
                                input_channel=self.name(),
                                metadata=metadata,
                            )
                        )
                    elif text == CONFIRM_ORDER_BTN_TITLE.lower():
                        await on_new_message(
                            UserMessage(
                                "Хорошо",
                                out_channel,
                                sender_id,
                                input_channel=self.name(),
                                metadata=metadata,
                            )
                        )

                    elif text == ORDER_TAXI.lower():
                        await on_new_message(
                            UserMessage(
                                "/start",
                                out_channel,
                                sender_id,
                                input_channel=self.name(),
                                metadata=metadata,
                            )
                        )    
                
                    elif text == CANCEL_BTN_TITLE.lower() or text == CONFIRM_BTN_TITLE.lower():
                        await on_new_message(
                            UserMessage(
                                "/restart",
                                out_channel,
                                sender_id,
                                input_channel=self.name(),
                                metadata=metadata,
                            )
                        )    
                    else:
                        await on_new_message(
                            UserMessage(
                                text,
                                out_channel,
                                sender_id,
                                input_channel=self.name(),
                                metadata=metadata,
                            )
                        )
                except Exception as e:
                    logger.error(
                        f"Exception when trying to handle message.{e}")
                    logger.debug(e, exc_info=True)
                    if self.debug_mode:
                        raise
                    pass

                return response.text("success")

        return telegram_webhook

    def get_output_channel(self) -> TelegramOutput:
        """Loads the telegram channel."""
        channel = TelegramOutput(self.access_token)

        try:
            channel.set_webhook(url=self.webhook_url)
        except ApiTelegramException as error:
            raise RasaException(
                "Failed to set channel webhook: " + str(error)
            ) from error

        return channel
