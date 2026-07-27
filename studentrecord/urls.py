"""
URL configuration for studentrecord project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, include
from student.views import *
from django.conf import settings
from django.conf.urls.static import static
from student import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('adminhome/',adminhome,name='adminhome'),
    path('add_student/',add_student, name='add_student'),
    path('view_student/',view_student,name='view_student'),
    path('edit_student/<int:id>',edit_student,name='edit_student'),
    path("delete_student/<int:id>/", views.delete_student, name="delete_student"),
    path('search_student/',search_student,name='search_student'),
    path('admin_logout/',admin_logout,name='admin_logout'),
    path('change_password/',change_password,name='change_password'),
    path("update_password/",update_password,name="update_password"),
    path("student_home/",student_home,name='student_home'),
    path("edit_profile/",edit_profile,name="edit_profile"),
    path("fee_details/",fee_details,name='fee_details'),
    path("fee_receipt/",fee_receipt,name='fee_receipt')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)