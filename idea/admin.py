from django.contrib import admin
from .models import UserIdea
from .models import ThreadComment

admin.site.register(UserIdea)
admin.site.register(ThreadComment)
