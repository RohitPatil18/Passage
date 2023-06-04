def reset_user_password(request, user, password):
    user.set_password(password)
    user.save()
    """
    @TODO: Store Information related to password reset request
    like timestamp, device, location and send a mail to user
    to inform about the activity
    """
    return user
