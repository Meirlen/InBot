import asyncio
import inspect
import json
import logging
from asyncio import Queue, CancelledError
from sanic import Blueprint, response
from sanic.request import Request
from sanic.response import HTTPResponse
from typing import Text, Dict, Any, Optional, Callable, Awaitable, NoReturn
from actions.app_constans import *
import rasa.utils.endpoints
from rasa.core.channels.channel import (
    InputChannel,
    CollectingOutputChannel,
    UserMessage,
)
from callbot_api import send_smpp_message
from yandex_stt import update_token
from wati import update_whatsapp_token
from local_db_for_actions import search_user_by_phone_number,update_status_by_admin
from actions.action_helper import clear_address_form_slots_after_car_arrived,send_ask_address_form
from rasa_api import get_order_status_by_conversation_id
from telegram_admin_api import send_to_admin_simple_message
from wati import *
import multiprocessing
logger = logging.getLogger(__name__)


def add_data_to_txt(contents,file_path):
        file = open(file_path,"a")
        file.writelines(contents+'\n')
        file.close()  

def call_send_info_msg(chat_id,text,platform):
    p = multiprocessing.Process(target=send_info_msg,args=(chat_id,text,platform))
    p.start() 


def send_info_msg(chat_id,text,platform):
        status = get_order_status_by_conversation_id(chat_id)
        print("USER_PHONE_NUMBER_FROM_DB"+": "+chat_id)
        if status == 'wait_car':
            update_status_by_admin(chat_id,'car_arrived',text)
        if status == 'wait_car' or status == 'car_arrived':
            if 'выехал' in text.lower():
                update_status_by_admin(chat_id,'car_arrived',text)
                clear_address_form_slots_after_car_arrived(chat_id)

                if platform == 'whatsapp':
                    send_message_with_menu(chat_id,create_body_finish_state("🚕 *К ВАМ ВЫЕХАЛА МАШИНА!* \n\n "+text))
                    # send_message_to_whatsapp(chat_id,"🚕 <b>К ВАМ ВЫЕХАЛА МАШИНА!</b> \n\n "+text)
                else:    
                    send_message_to_telegram_chat(chat_id,"🚕 <b>К ВАМ ВЫЕХАЛА МАШИНА!</b> \n\n "+text)
            elif 'ожидает' in text.lower():
                clear_address_form_slots_after_car_arrived(chat_id)
                if platform == 'whatsapp':
                    send_message_with_menu(chat_id,create_body_finish_state("🚕 *МАШИНА ПОДЬЕХАЛА!* \n\n "+text))
                    send_ask_address_form(chat_id)

                    # send_message_with_menu(chat_id,create_body_finish_state("🚕 *МАШИНА ПОДЬЕХАЛА!* \n\n "+text))
                    # send_message_to_whatsapp(chat_id,"🚕 <b>МАШИНА ПОДЬЕХАЛА!</b> \n\n "+text)
                else:    
                    send_message_to_telegram_chat(chat_id,"🚕 <b>МАШИНА ПОДЬЕХАЛА!</b> \n\n "+text)
                    send_ask_address_form(chat_id)

class RestInput(InputChannel):
    """A custom http input channel.

    This implementation is the basis for a custom implementation of a chat
    frontend. You can customize this to send messages to Rasa and
    retrieve responses from the assistant."""

    @classmethod
    def name(cls) -> Text:
        return "rest"

    @staticmethod
    async def on_message_wrapper(
        on_new_message: Callable[[UserMessage], Awaitable[Any]],
        text: Text,
        queue: Queue,
        sender_id: Text,
        input_channel: Text,
        metadata: Optional[Dict[Text, Any]],
    ) -> None:
        collector = QueueOutputChannel(queue)

        message = UserMessage(
            text, collector, sender_id, input_channel=input_channel, metadata=metadata
        )
        await on_new_message(message)

        await queue.put("DONE")

    async def _extract_sender(self, req: Request) -> Optional[Text]:
        return req.json.get("sender", None)

    # noinspection PyMethodMayBeStatic
    def _extract_message(self, req: Request) -> Optional[Text]:
        return req.json.get("message", None)

    def _extract_input_channel(self, req: Request) -> Text:
        return req.json.get("input_channel") or self.name()

    def stream_response(
        self,
        on_new_message: Callable[[UserMessage], Awaitable[None]],
        text: Text,
        sender_id: Text,
        input_channel: Text,
        metadata: Optional[Dict[Text, Any]],
    ) -> Callable[[Any], Awaitable[None]]:

        async def stream(resp: Any) -> None:
            q = Queue()
            task = asyncio.ensure_future(
                self.on_message_wrapper(
                    on_new_message, text, q, sender_id, input_channel, metadata
                )
            )
            while True:
                result = await q.get()
                if result == "DONE":
                    break
                else:
                    await resp.write(json.dumps(result) + "\n")
            await task

        return stream

    def blueprint(
        self, on_new_message: Callable[[UserMessage], Awaitable[None]]
    ) -> Blueprint:
        custom_webhook = Blueprint(
            "custom_webhook_{}".format(type(self).__name__),
            inspect.getmodule(self).__name__,
        )

        # noinspection PyUnusedLocal
        @custom_webhook.route("/", methods=["GET"])
        async def health(request: Request) -> HTTPResponse:
            return response.json({"status": "ok"})

        @custom_webhook.route("/webhook", methods=["POST"])
        async def receive(request: Request) -> HTTPResponse:
            sender_id = await self._extract_sender(request)
            text = self._extract_message(request)
            should_use_stream = rasa.utils.endpoints.bool_arg(
                request, "stream", default=False
            )
            input_channel = self._extract_input_channel(request)
            metadata = self.get_metadata(request)

            file_path = 'call_'+str(sender_id) +'_test_case.txt'


            if sender_id.lower()=='web_app':
                 text = 'история  история  история  web_app'
            if sender_id.lower()=='admin':
                # "87771786656&&к вам выехала мазда 666 с гос номером 897
                # find chat_id by phone_number
                # send msg to telegram by chat_id 
                # save slot order status in chat 

                print('From http with sender id:',text)
                if text == 'backup':
                    # send_file_to_telegram_chat(ADMIN_CHAT_ID)
                    text = 'история backup'
                elif text == 'human_help_disable': # отключаем режим помошника
                     print('отключаем режим помошника')
                    #  Settings().change_human_help_mode(False)
                    #  print("ttt",Settings().get_human_ability())

                     return response.text("Не нужно отвечать на сообщени админстратора")

                elif text == 'human_help_enable': # включаем режим помошника
                     print('включаем режим помошника')
                    #  Settings().change_human_help_mode(True)
                     return response.text("Не нужно отвечать на сообщени админстратора")

                elif 'new token:' in text:
                    token = text.replace("new token:",'').strip()
                    update_token(token)
                    text = 'история backup'
                elif 'new wati token:' in text:
                    token = text.replace("new wati token:",'').strip()
                    update_whatsapp_token(token)
                    text = 'история backup'   
                elif "&&" in text: 
                    # digital ocean
                    msg_parts = text.split('&&')
                    phone_number = msg_parts[0]
                    text = msg_parts[1]
                    users_info = search_user_by_phone_number(phone_number)
                    if len(users_info)>0:
                        # if the user by phone nymber exist we need to send info message
                        chat_id,status,message,platform =  users_info[0].split('&&')
                        call_send_info_msg(chat_id,text,platform)

                    # send_to_admin_simple_message(text)
                    return response.text("Сообщение о прибытий авто получено")
                
                else:    

                    text = 'история история история история история&&'+ text

                # return response.stream(
                #     self.stream_response(
                #         on_new_message, text, sender_id, input_channel, metadata
                #     ),
                #     content_type="text/event-stream",
                # )


            # if text == 'история' or text == 'очисти историю':
            #     delimetr = f'{text} \n--------------------\n--------------------'
            #     add_data_to_txt(delimetr,f'/Users/meirlen/Desktop/bot/dataset/test/{file_path}')
            # else:
            #     add_data_to_txt(f'User:      {text} ',f'/Users/meirlen/Desktop/bot/dataset/test/{file_path}')

            if should_use_stream:
                return response.stream(
                    self.stream_response(
                        on_new_message, text, sender_id, input_channel, metadata
                    ),
                    content_type="text/event-stream",
                )
            else:

                collector = CollectingOutputChannel()
                # noinspection PyBroadException
                try:
                    await on_new_message(

                        UserMessage(
                            text,
                            collector,
                            sender_id,
                            input_channel=input_channel,
                            metadata=metadata,
                        )
                    )
                except CancelledError:
                    logger.error(
                        f"Message handling timed out for " f"user message '{text}'."
                    )
                except Exception:
                    logger.exception(
                        f"An exception occured while handling "
                        f"user message '{text}'."
                    )
                return response.json(collector.messages)

        return custom_webhook

from typing import (
    Text,
    List,
    Dict,
    Any,
    Optional,
    Callable,
    Iterable,
    Awaitable,
    NoReturn,
)

class QueueOutputChannel(CollectingOutputChannel):
    """Output channel that collects send messages in a list

    (doesn't send them anywhere, just collects them)."""

    @classmethod
    def name(cls) -> Text:
        return "queue"


    @staticmethod
    def _message(
        recipient_id: Text,
        text: Text = None,
        image: Text = None,
        buttons: List[Dict[Text, Any]] = None,
        attachment: Text = None,
        custom: Dict[Text, Any] = None,
    ) -> Dict:
        """Create a message object that will be stored."""

        obj = {
            "recipient_id": recipient_id,
            "text": text,
            "image": image,
            "buttons": buttons,
            "attachment": attachment,
            "custom": custom,
        }


        # filter out any values that are `None`
        return {k: v for k, v in obj.items() if v is not None}
    # noinspection PyMissingConstructor
    def __init__(self, message_queue: Optional[Queue] = None) -> None:
        super().__init__()
        self.messages = Queue() if not message_queue else message_queue

    def latest_output(self) -> NoReturn:
        raise NotImplementedError("A queue doesn't allow to peek at messages.")

    async def _persist_message(self, message: Dict[Text, Any]) -> None:
        await self.messages.put(message)
