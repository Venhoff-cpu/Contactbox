"""warsztat_mailbox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from mailbox_app.views import Main, PersonDetail, AddAddress, AddPerson, AddPhone, AddEmail, ModifyPerson, \
    DeletePerson, GroupsList, GroupDetail, AddGroup, AddPersonToGroup, DeletePhone, DeleteEmail, DeleteGroup

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Main.as_view(), name="main"),
    path('person/<int:person_id>', PersonDetail.as_view(), name="person"),
    path('person/<int:person_id>/add-phone', AddPhone.as_view(), name="add_phone"),
    path('person/<int:person_id>/add-email', AddEmail.as_view(), name="add_email"),
    path('person/<int:person_id>/modify', ModifyPerson.as_view(), name="modify_person"),
    path('new-person/', AddPerson.as_view(), name="add_person"),
    path('add-address', AddAddress.as_view(), name="add_address"),
    path('delete/<int:person_id>', DeletePerson.as_view(), name="delete"),
    path('delete-phone/<int:phone_id>', DeletePhone.as_view(), name="delete_phone"),
    path('delete-email/<int:email_id>', DeleteEmail.as_view(), name="delete_email"),
    path('groups/', GroupsList.as_view(), name="groups"),
    path('groups/<int:group_id>', GroupDetail.as_view(), name="group_detail"),
    path('groups/<int:group_id>/add-person', AddPersonToGroup.as_view(), name="add_person_to_group"),
    path('add-group/', AddGroup.as_view(), name="add_group"),
    path('delete/<int:group_id>', DeleteGroup.as_view(), name="delete_group"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)