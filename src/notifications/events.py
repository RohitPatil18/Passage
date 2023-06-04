USER_PASSWORD_RESET_LINK = {
    "name": "User password reset link.",
    "script": "notifications.scripts.forgot_password.PasswordResetLinkNotification",
    "email": {
        "status": True,
        "script": "notifications.scripts.forgot_password.PasswordResetLinkMail",
    },
    "sms": {"status": False},
    "app_notification": {"status": False},
}
