

from . import views
from django.urls import include, path


urlpatterns = [
    path('', views.home),
    path('indicadores', views.getAssets, name='indicadores'),
    path('graficos', views.graficos, name='graficos'),
    path('coin_detail/<symbol>', views.coin_detail, name='coin_detalle'),
    path('graficos1/<symbol>', views.graficos1, name='graficos1'),

    
]
