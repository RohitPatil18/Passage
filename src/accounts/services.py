from django.db import transaction
from accounts.models import Company, CompanyUser


@transaction.atomic
def add_user_company_information(user, data):
    company = Company.objects.create(**data)
    CompanyUser.objects.create(company=company, user=user)
    return company
