from pathlib import Path

from fastapi.background import BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr

from auth.confsettings import get_settings, mail_settings

settings = get_settings()

conf = ConnectionConfig(
    **mail_settings.model_dump(),
    TEMPLATE_FOLDER=Path(__file__).parent.joinpath("templates"),
)
# print("***********"*20)
# print(conf)
fm = FastMail(conf)


async def send_email(
    recipients: list[EmailStr],
    subject: str,
    context: dict,
    template_name: str,
    background_tasks: BackgroundTasks,
) -> None :
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        template_body=context,
        subtype=MessageType.html,
    )

    background_tasks.add_task(fm.send_message, message, template_name=template_name)
