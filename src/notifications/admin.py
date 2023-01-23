from django.contrib import admin

from notifications import models

admin.site.register(models.NotificationLog)
admin.site.register(models.EmailLog)
