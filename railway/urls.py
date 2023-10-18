
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from Trainstation import views

urlpatterns = [
    # path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    # path('admin/', include(admin.site.urls)),
    path('jet/', include('jet.urls', 'jet')),
        # Django JET URLS
    path('admin/', admin.site.urls),

    
    path("",include("Trainstation.urls"))
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 