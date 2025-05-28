import pretty_errors
from django.urls import path
from django.conf import settings
from django.contrib import admin
import users.views as users_views
import projects.views as projects_views


from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', users_views.login_page, name='login'),
    path('home/', users_views.home, name='home'),
    path('logout/', users_views.logout_user, name='logout_user'),
    path('complete-profile/', users_views.complete_profile, name='complete_profile'),
    path('user-profile/', users_views.my_profile, name='my_profile'),
    path('myteam/', users_views.my_team, name='my_team_members'),
    path('myprofile/change_password/', users_views.CustomPasswordChangeView.as_view(), name='change_password'),
    path('myprofile/edit/', users_views.update_profile, name='edit_profile'),
    path('myteam/<int:user_id>/', users_views.member_details, name='member_details'),


    #######################################################################################################
    path('myprojects/', projects_views.my_projects, name='my_projects'),
    path('add-project/', projects_views.add_project, name='create_project'),
    path('delete-project/<int:project_id>/', projects_views.detele_project, name='delete_project'),
    path('add-task/', projects_views.add_task, name='add_task'),
    path('add-document/', projects_views.add_document, name='add_document'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)