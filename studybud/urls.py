from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from django.http import HttpResponse

# def home(request):
#   return HttpResponse('Home page')
  

# def room(request):
#   return HttpResponse('Room page')
  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('api/', include('base.api.urls')), # connect api route to project

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)