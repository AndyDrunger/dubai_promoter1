from typing import TypeVar, Type

from telethon.sessions import StringSession

from classes.acc import Acc, AccStatus
from classes.acc_chat import AccChatStatus, AccChat
from classes.promo_script import Ask, Response, PromoScript
from classes.proxy import Proxy
from database.models import AsksResponsesModel, AccsModel

T = TypeVar("T")

def map_model_to_business(model: object, business_class: Type[T]) -> T:
    return business_class(**{
        attr: getattr(model, attr)
        for attr in business_class.__annotations__
        if hasattr(model, attr)
    })


def map_asks_responses_to_promo_script(ar_model: AsksResponsesModel) -> PromoScript:
    ask = Ask(id=ar_model.ask.id, text=ar_model.ask.text)
    response = Response(id=ar_model.response.id, text=ar_model.response.text)
    return PromoScript(id=ar_model.id, ask=ask, response=response)


def map_acc_model_to_business(model: AccsModel) -> Acc:
    model.string_session = model.string_session.strip()

    return Acc(
        id=model.id,
        api_id=model.api_id,
        api_hash=model.api_hash,
        proxy_id=model.proxy_id,
        profile_id=model.profile_id,
        string_session=StringSession(model.string_session),
        status=AccStatus(model.status),  # предполагается, что строка
        proxy=map_model_to_business(model.proxy, Proxy),               # можно замапить через отдельную функцию, если нужно
        # profile=model.profile,           # аналогично
        chats=[
            AccChat(
                id=ac.chat.id,
                username=ac.chat.username,
                inv_link=ac.chat.inv_link,
                captcha=ac.chat.captcha,
                status=AccChatStatus(ac.status) if ac.status else None
            )
            for ac in model.accs_chats
        ]
    )