from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/<version>(v1|v2)/', include('music.urls'))
]
