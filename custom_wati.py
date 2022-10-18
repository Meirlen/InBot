import asyncio
import inspect
import json
import logging
from asyncio import Queue, CancelledError
from sanic import Blueprint, response
from sanic.request import Request
from sanic.response import HTTPResponse
from typing import Text, Dict, Any, Optional, Callable, Awaitable, NoReturn
from typing import Dict, Text, Any, List, Optional, Callable, Awaitable
from rasa.shared.constants import INTENT_MESSAGE_PREFIX
from rasa.shared.core.constants import USER_INTENT_RESTART
from rasa.shared.exceptions import RasaException
from actions.app_constans import *
from wati import *
from yandex_helper import geo_coder_yandex
from helper.Utils import *
import rasa.utils.endpoints
from rasa.core.channels.channel import (
    InputChannel,
    CollectingOutputChannel,
    UserMessage,
)
from actions.action_helper import send_ask_address_form
logger = logging.getLogger(__name__)


class WatiInput(InputChannel):
    """A custom http input channel.

    This implementation is the basis for a custom implementation of a chat
    frontend. You can customize this to send messages to Rasa and
    retrieve responses from the assistant."""

    @classmethod
    def name(cls) -> Text:
        return "wati"

    @staticmethod
    def _is_location(text) -> bool:
        return 'https://www.google.com/maps/search/' in text
       
    @staticmethod
    async def on_message_wrapper(
        on_new_message: Callable[[UserMessage], Awaitable[Any]],
        text: Text,
        queue: Queue,
        sender_id: Text,
        input_channel: Text,
        metadata: Optional[Dict[Text, Any]],
    ) -> None:
        collector = WaitOutputChannel(queue)

        message = UserMessage(
            text, collector, sender_id, input_channel=input_channel, metadata=metadata
        )
        await on_new_message(message)

        await queue.put("DONE")

    async def _extract_sender(self, req: Request) -> Optional[Text]:
        return req.json.get("waId", None)

    # noinspection PyMethodMayBeStatic
    def _extract_message(self, req: Request) -> Optional[Text]:
        return req.json.get("text", None)
    def _extract_type(self, req: Request) -> Optional[Text]:
        return req.json.get("type", None) 
    def _extract_data(self, req: Request) -> Optional[Text]:
        return req.json.get("data", None)        
    def _extract_listReply(self, req: Request) -> Optional[Text]:
        return req.json.get("listReply", None)
    def _extract_input_channel(self, req: Request) -> Text:
        return req.json.get("input_channel") or self.name()

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
            print('METADATA:', metadata)
    


            try:
                user_id = metadata["waId"]
                chat_id = metadata["waId"]
            except:    
                user_id = None
                chat_id = None

            try:
                username = metadata["senderName"]
            except:    
                username = None


 
            res = {}
            res['user_id'] = user_id
            res['phone_number'] = user_id
            res['user_name'] = username
            res['chat_id'] = chat_id ## send only telegramm users
            res['platform'] = 'whatsapp'

            return res


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
            out_channel = self.get_output_channel()

            sender_id = await self._extract_sender(request)
            text = self._extract_message(request)
            type = self._extract_type(request)


            if type == 'audio':
               data = self._extract_data(request) 
               text = await out_channel._extract_text_from_voice(data)


            listReply = self._extract_listReply(request)
            if listReply!= None:  # user click button or menu item

                text = listReply['title']
                desc = listReply['desription']


                text = text.lower()
      
                if 'coordinates::' in desc:
                    text = desc.replace('coordinates::','').strip()


            # if TELEGRAM_IS_PROD and sender_id == '77774857133':
            #     print('Debug phone number') 
            #     return response.text("Debug phone number 77774857133")

            # if TELEGRAM_IS_PROD == False and sender_id != '77774857133':
            #     print('Debug phone number') 
            #     return response.text("Prod phone number")
   
                 
            pre_map_searh = 'https://www.google.com/maps/search/'
            if text != None:

                if self._is_location(text):
                    lat,lng = text.replace(pre_map_searh,'').split(',')
                    text = geo_coder_yandex(lng,lat)
                    print('Yandex api return: ' + text)


            should_use_stream = rasa.utils.endpoints.bool_arg(
                request, "stream", default=False
            )
            input_channel = self._extract_input_channel(request)
            metadata = self.get_metadata(request)

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
        
                    text = pre_proccess_text(text)


                    if is_template_message(text):  # If user click template message
                        order_id =  get_position_from_template_message(text)
                        metadata['order_id'] = order_id
                        text = "Язева 67" # trigger for address form
                    # order_id =  get_position_from_template_message(text)
                    # call_send_order_template_api_multi_proccess(order_id,sender_id)
                
                    # return response.text("Пользователь нажал на меню шаблонов")


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
                        print("CONFIRM_ORDER_BTN_TITLE")
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
              
                    elif text == CANCEL_BTN_TITLE.lower() or text == CREATE_NEW_ORDER.lower() or text == CONFIRM_BTN_TITLE.lower():
                        if text == CREATE_NEW_ORDER.lower():
                            metadata['add_text'] = CREATE_NEW_ORDER
                        
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



    def get_output_channel(
        self, channel: Optional[Text] = None, thread_id: Optional[Text] = None
    ) -> CollectingOutputChannel:
        # channel = channel or self.slack_channel
        return WaitOutputChannel()     


class WaitOutputChannel(CollectingOutputChannel):
    """Output channel that collects send messages in a list

    (doesn't send them anywhere, just collects them)."""


    @classmethod
    def name(cls) -> Text:
        return "wati"

    # noinspection PyMissingConstructor
    def __init__(self, message_queue: Optional[Queue] = None) -> None:
        self.messages = Queue() if not message_queue else message_queue

    def latest_output(self) -> NoReturn:
        raise NotImplementedError("A queue doesn't allow to peek at messages.")
    
  

    async def _persist_message(self, message: Dict[Text, Any]) -> None:
        await self.messages.put(message)


    async def send_text_message(
        self, recipient_id: Text, text: Text, **kwargs: Any
    ) -> None:


        print('PHONE NUM FROM ACTION: send_text_message',)
        print('PHONE NUM FROM ACTION: ',kwargs)
      

        try:
            print('PHONE NUM FROM ACTION:2 ',kwargs['kwargs']['phone_num'])

            phone_number = kwargs['kwargs']['phone_num']

        
            for message_part in text.strip().split("\n\n"):

                file_path = recipient_id+'_test_case.txt'

                # if message_part == 'данные очищены':
                #     delimetr = f'{message_part} \n--------------------\n--------------------'
                #     self.add_data_to_txt(
                #         delimetr, f'/Users/meirlen/Desktop/bot/dataset/test/{file_path}')
                # else:
                #     self.add_data_to_txt(
                #         f'CallBot:      {message_part} ', f'/Users/meirlen/Desktop/bot/dataset/test/{file_path}')

                if '[login]' in text:
                    text = text.replace('[login]','')
                    name,phone_number = text.split('&&')
                    # send_template(phone_number,create_body_login(name,phone_number))

                    send_message(phone_number,'💁 Привет <b>'+str(name)+'!</b> ✋\n\nДобро пожаловать! С помощью данного бота Вы сможете вызвать такси.')
                else:
                    send_message(phone_number,message_part)

        except:
                print("Error")



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
        print('send_text_with_buttons')

        phone_number = kwargs['kwargs']['phone_num']


        for s in buttons:
            print(s["title"])


        if '[header]' in text:
            
            if TITLE_AFTER_CONFIRMED_ORDER in text:
                # send_message_with_menu(phone_number,create_body_after_order_created_state(text,False))
                send_message_with_buttons(phone_number,create_body_order_confirm_ask(text,False))

            else:
                print("send_message_with_menu", ' 2')
                send_message_with_buttons(phone_number,create_body_order_confirm_ask(text))

                # send_message_with_menu(phone_number,create_body_after_order_created_state(text))
                # send_template(phone_number,create_body_order_confirm())

        elif '[start_address_form]' in text:
            print('[start_address_form]')
            send_ask_address_form(phone_number)

        elif '[ask_apart]' in text:
            from_address = text.replace('[ask_apart]','').strip()
            send_template(phone_number,create_body_ask_apart(from_address))

        elif text == TITLE_MULTIPLE_ADDRESS_FOUND:
            adresses = []
            desc = []
            for s in buttons:
                adresses.append(s["title"])
                desc.append('Coordinates::'+s["payload"])

            send_message_with_menu(phone_number,create_body_multiple_address_case(text,adresses,desc))

        elif '[body_to_adress_ask_form]' in text:
            print('[body_to_adress_ask_form]')
            from_address = text.split('[body_to_adress_ask_form]')[1]
            send_message(phone_number,create_body_ask_to_address(from_address))
        else:
            send_message(phone_number,text)

    async def _extract_text_from_voice(
        self,data
    ) -> Text:
        return get_media(data) 