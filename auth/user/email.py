from fastapi import BackgroundTasks

from auth.confemail import send_email
from auth.confsettings import get_settings
from auth.user.models import User
from auth.user.security import get_str_hash

FORGOT_PASSWORD_CTX = "verify-account"
VERIFY_ACCOUNT_CTX = "password-reset"

settings = get_settings()


async def send_request_verification_email(
        user: User,
        background_tasks: BackgroundTasks,
) -> None:
    user_token = user.user_ctx_token(context=VERIFY_ACCOUNT_CTX)
    hashed_user_token = get_str_hash(user_token)

    activate_url = \
    f"""
    {settings.FRONTEND_HOST}/auth/account-verify?token={hashed_user_token}&email={user.email}
    """

    data = {
        'app_name': settings.app_name,
        "name": user.name,
        'activate_url': activate_url,
    }

    await send_email(
        recipients=[user.email],
        subject=f"Account Verification - {settings.app_name}",
        template_name="user/account-request-verification.html",
        context=data,
        background_tasks=background_tasks,
    )


async def send_welcome_successful_activation_email(
        user: User,
        background_tasks: BackgroundTasks,
)-> None:
    data = {
        'app_name': settings.app_name,
        "name": user.name,
        'login_url': f'{settings.FRONTEND_HOST}',
    }

    await send_email(
        recipients=[user.email],
        subject=f"Welcome - {settings.app_name}",
        template_name="user/account-welcome-confirmation.html",
        context=data,
        background_tasks=background_tasks,
    )


async def send_password_reset_email(
        user: User,
        background_tasks: BackgroundTasks,
) -> None:

    user_token = user.user_ctx_token(context=FORGOT_PASSWORD_CTX)
    hashed_user_token = get_str_hash(user_token)
    reset_url = \
    f"""
    {settings.FRONTEND_HOST}/reset-password?token={hashed_user_token}&email={user.email}
    """

    data = {
        'app_name': settings.app_name,
        "name": user.name,
        'activate_url': reset_url,
    }

    await send_email(
        recipients=[user.email],
        subject= f"Reset Password - {settings.app_name}",
        template_name="user/password-reset.html",
        context=data,
        background_tasks=background_tasks,
    )
