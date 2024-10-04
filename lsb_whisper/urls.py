from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name="home"),
    path('encrypt/',views.encrypt, name="encrypt"),
    path('decrypt/',views.decrypt, name='decrypt'),
    # path('downloads/',views.success, name='success'),
    # path('message/',views.message,name='message')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

