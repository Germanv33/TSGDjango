from django.contrib import admin
from core.models import Articles, Documents, User, Water, WaterKeep, Letter


# Register your models here.
admin.site.register(Articles)
admin.site.register(Documents)
admin.site.register(User)
admin.site.register(WaterKeep)
admin.site.register(Water)
admin.site.register(Letter)

