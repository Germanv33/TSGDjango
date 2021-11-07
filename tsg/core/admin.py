from django.contrib import admin
from core.models import Articles, Documents, User


# Register your models here.
admin.site.register(Articles)
admin.site.register(Documents)
admin.site.register(User)

