from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def default_view(request):
    return HttpResponse("Default view")

urlpatterns = [
    path('', default_view),
    path('admin/', admin.site.urls),
    path('playground/', include('playground.urls'))
]
