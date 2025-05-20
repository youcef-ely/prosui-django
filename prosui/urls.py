import pretty_errors

from django.contrib import admin
from django.urls import path
from users import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.login_page, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_user, name='logout_user'),
    path('complete-profile/', views.complete_profile, name='complete_profile'),
    path('user-profile/', views.my_profile, name='my_profile'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)