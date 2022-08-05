

from . import views
from django.urls import include, path


urlpatterns = [
    path('', views.home),
    path('indicadores', views.getAssets, name='indicadores'),
    path('graficos', views.graficos, name='graficos'),
    path('coin_detail/<symbol>/<date>', views.coin_detail, name='coin_detalle'),

    
]
