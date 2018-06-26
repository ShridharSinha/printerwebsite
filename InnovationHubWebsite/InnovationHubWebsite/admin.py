from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Job)
admin.site.register(FeaturedPrint)
admin.site.register(RecentPrint)
