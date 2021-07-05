from django.contrib import admin

from .models import UserAccount
from .models import Post
from .models import Cpu
from .models import Gpu
from .models import Ram
from .models import OrderItem

admin.site.register(UserAccount)
admin.site.register(Post)
admin.site.register(Cpu)
admin.site.register(Gpu)
admin.site.register(Ram)
admin.site.register(OrderItem)
