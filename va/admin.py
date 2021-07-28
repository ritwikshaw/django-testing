from django.contrib import admin

from .models import UserAccount
from .models import Post
from .models import Cpu
from .models import Gpu
from .models import Ram
from .models import OrderItem
from .models import Custom
from .models import (Pcdes, Pcprice, Pcpart, Gamingpc)

admin.site.register(UserAccount)
admin.site.register(Post)
admin.site.register(Cpu)
admin.site.register(Gpu)
admin.site.register(Ram)
admin.site.register(OrderItem)
admin.site.register(Custom)
admin.site.register(Pcdes)
admin.site.register(Pcprice)
admin.site.register(Pcpart)
admin.site.register(Gamingpc)
