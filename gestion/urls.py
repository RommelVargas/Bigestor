# gestion/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # 1. Pantalla de Inicio (URL: /)
    path('', views.inicio, name='inicio'),
    
    # 2. Dashboard (URL: /dashboard/)
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # 3. Nueva Mezcla (URL: /mezcla/)
    path('mezcla/', views.nueva_mezcla, name='nueva_mezcla'),
    
    # 4. Monitoreo (URL: /monitoreo/)
    path('monitoreo/', views.monitoreo, name='monitoreo'),

    # 5. Nutrientes / Impacto (URL: /nutrientes/)
    path('nutrientes/', views.nutrientes, name='nutrientes'),

    # 6. Soporte / Servicio al Cliente (URL: /soporte/)
    path('soporte/', views.servicio_al_cliente, name='servicio_al_cliente'),
    
    # 7. Tablas Teóricas (URL: /tablas-teoricas/)
    path('tablas-teoricas/', views.tablas_teoricas, name='tablas_teoricas'),
]
