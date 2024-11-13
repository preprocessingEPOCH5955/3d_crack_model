"""
URL configuration for myProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from myapp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home1, name='home'),
    # path('home', home1, name='home'),

    path('about/', about, name='about'),
    path('get_started/', get_started, name='get_started'),
    path('report/', report, name='report'),
    path('visualise/', visualise_results, name='visualise'),
    path('mymodel/', mymodel_new, name='mymodel'),
    path('latest_crack_coordinates', update_coordinates, name='update_coordinates'),
    path('reset_report', reset_coordinates, name='reset_coordinates'),
    path('login', login, name='login'),
    path('signup', signup, name='signup'),
    path('admin1', admin1, name="admin1"),
    path('logout/',logout, name="logout"),
    path("usr_d/<int:id>", user_projects_view, name = 'usr_d'),


    path("reset/" , reset, name="reset"),
    path("side_btn/<int:side_id>", side_btn, name="side_btn"),
    
    
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)