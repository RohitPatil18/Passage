from django.db import transaction

from accounts.models import Company, CompanyUser


@transaction.atomic
def add_user_company_information(user, data):
    company = Company.objects.create(**data)
    CompanyUser.objects.create(company=company, user=user)
    return company


def reset_user_password(request, user, password):
    user.set_password(password)
    user.save()
    """
    @TODO: Store Information related to password reset request
    like timestamp, device, location and send a mail to user
    to inform about the activity
    """
    return user
