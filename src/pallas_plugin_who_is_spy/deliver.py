"""向玩家投递词语/投票说明：群临时会话 → 好友私聊 → QQ 邮箱。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

from nonebot import logger
from nonebot.adapters.onebot.v11.exception import (
    ActionFailed,
    ApiNotAvailable,
    NetworkError,
)
from pallas.api.utils import (
    MailConfig,
    build_mail_config,
    send_mail,
    send_private_msg_compat,
)

from .config import get_spy_config

if TYPE_CHECKING:
    from nonebot.adapters.onebot.v11 import Bot

DeliveryChannel = Literal["private", "temp", "email", "failed"]
_SEND_ERRORS = (ActionFailed, ApiNotAvailable, NetworkError)


def qq_mail(user_id: int) -> str:
    return f"{int(user_id)}@qq.com"


def mail_config_for(recipient: str) -> MailConfig | None:
    cfg = get_spy_config()
    if not cfg.spy_email_fallback:
        return None
    mail = build_mail_config(recipient)
    if not mail.check_params():
        return None
    return mail


@dataclass(frozen=True)
class DeliveryOutcome:
    channel: DeliveryChannel
    ok: bool


async def send_private(bot: Bot, user_id: int, message: str, *, group_id: int | None = None) -> bool:
    try:
        await send_private_msg_compat(bot, user_id, message, group_id=group_id)
        return True
    except _SEND_ERRORS as err:
        logger.debug(
            "Bot [{}] failed to send a private message to user [{}] (group [{}]): {}",
            bot.self_id,
            user_id,
            group_id,
            err,
        )
        return False


async def send_email(user_id: int, *, subject: str, body: str) -> bool:
    mail = mail_config_for(qq_mail(user_id))
    if mail is None:
        return False
    err = await send_mail(subject, body, mail)
    if err:
        logger.warning("who_is_spy: email to {} failed: {}", qq_mail(user_id), err)
        return False
    return True


async def deliver_player_message(
    bot: Bot,
    *,
    group_id: int,
    user_id: int,
    private_text: str,
    email_subject: str,
    email_body: str,
) -> DeliveryOutcome:
    if await send_private(bot, user_id, private_text, group_id=group_id):
        return DeliveryOutcome("temp", True)

    if await send_private(bot, user_id, private_text):
        return DeliveryOutcome("private", True)

    if await send_email(user_id, subject=email_subject, body=email_body):
        return DeliveryOutcome("email", True)

    return DeliveryOutcome("failed", False)
