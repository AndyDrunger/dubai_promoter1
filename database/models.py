from sqlalchemy import ForeignKey, BigInteger, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Annotated
from db import Base

bigintpk = Annotated[int, mapped_column(BigInteger, primary_key=True, autoincrement=False)]
intpkai = Annotated[int, mapped_column(Integer, primary_key=True, autoincrement=True)]



class AsksModel(Base):
    __tablename__ = 'asks'

    id: Mapped[intpkai]
    text: Mapped[str]

    asks_responses: Mapped[list["AsksResponsesModel"]] = relationship(back_populates="ask")


class ResponsesModel(Base):
    __tablename__ = 'responses'

    id: Mapped[intpkai]
    text: Mapped[str]

    asks_responses: Mapped[list["AsksResponsesModel"]] = relationship(back_populates="response")


class AsksResponsesModel(Base):
    __tablename__ = 'asks_responses'

    id: Mapped[intpkai]
    ask_id: Mapped[int] = mapped_column(ForeignKey("asks.id", ondelete="CASCADE"))
    response_id: Mapped[int] = mapped_column(ForeignKey("responses.id", ondelete="CASCADE"))

    ask: Mapped['AsksModel'] = relationship(back_populates="asks_responses")
    response: Mapped['ResponsesModel'] = relationship(back_populates="asks_responses")


class ChatsModel(Base):
    __tablename__ = 'chats'

    id: Mapped[bigintpk]
    username: Mapped[str | None]
    inv_link: Mapped[str | None]
    captcha: Mapped[bool]

    accs_chats: Mapped[list["AccsChatsModel"]] = relationship(back_populates="chat")


class AccsModel(Base):
    __tablename__ = 'accs'

    id: Mapped[bigintpk]
    api_id: Mapped[int]
    api_hash: Mapped[str]
    status: Mapped[str] = mapped_column(default="free")
    proxy_id: Mapped[int] = mapped_column(ForeignKey("proxies.id"))
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"))
    string_session: Mapped[str] = mapped_column(String(354))

    profile: Mapped["ProfilesModel"] = relationship(back_populates="accs")
    accs_chats: Mapped[List["AccsChatsModel"]] = relationship(back_populates="acc")
    proxy: Mapped["ProxiesModel"] = relationship(back_populates='accs')


class AccsChatsModel(Base):
    __tablename__ = 'accs_chats'

    acc_id: Mapped[int] = mapped_column(ForeignKey("accs.id", ondelete="CASCADE"), primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE"), primary_key=True)
    status: Mapped[str] = mapped_column(default="unjoined")

    acc: Mapped[AccsModel] = relationship(back_populates="accs_chats")
    chat: Mapped[ChatsModel] = relationship(back_populates="accs_chats")


class ProxiesModel(Base):
    __tablename__ = 'proxies'

    id: Mapped[intpkai]
    proxy_type: Mapped[str] = mapped_column(default="socks5")
    addr: Mapped[str]
    port: Mapped[int]
    username: Mapped[str] = mapped_column(default="l9xclcjl22-mobile-country-ID-hold-session-session-6820ff0460394")
    password: Mapped[str] = mapped_column(default="n9xhA0fMlmpgM3v1")
    rdns: Mapped[int] = mapped_column(default=1)
    country: Mapped[str]

    accs: Mapped[list["AccsModel"]] = relationship(back_populates="proxy")


class ProfilesModel(Base):
    __tablename__ = 'profiles'

    id: Mapped[intpkai]
    about: Mapped[str] = mapped_column(String(70), nullable=True)
    first_name: Mapped[str] = mapped_column(String(45))
    last_name: Mapped[str] = mapped_column(String(45), nullable=True)
    user_name: Mapped[str] = mapped_column(String(45), nullable=True)
    status: Mapped[str] = mapped_column(String(45), default="free")

    accs: Mapped[list["AccsModel"]] = relationship(back_populates="profile")



