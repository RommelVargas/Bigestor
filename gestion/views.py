# gestion/views.py
from django.shortcuts import render, redirect
from .forms import MezclaForm, MonitoreoForm
from decimal import Decimal
# gestion/views.py


# 1. Pantalla de Inicio
def inicio(request):
    # Redirige al Dashboard si se pulsa "Iniciar" (aunque el botón irá a la URL del dashboard)
    return render(request, 'gestion/inicio.html')

# 2. Dashboard
def dashboard(request):
    context = {
        'biogas_dia': 15.5,
        'biogas_acumulado': 350.2,
        'biofertilizante_dia': 500,
        'biofertilizante_acumulado': 12000,
        # Lógica simple para el estado: (verde = bien, amarillo = ajustar, rojo = problema)
        'estado_biodigestor': 'verde', 
        'mensaje_estado': 'Funcionando de manera óptima'
    }
    return render(request, 'gestion/dashboard.html', context)

# 3. Nueva Mezcla
def nueva_mezcla(request):
    form = MezclaForm()
    resultado = None

    if request.method == 'POST':
        form = MezclaForm(request.POST)
        if form.is_valid():
            pulpa = form.cleaned_data['pulpa_cafe_kg']
            rastrojo_kg = form.cleaned_data['rastrojo_kg']
            
            # --- CÁLCULO DE AGUA Y VOLUMEN ---
            volumen_ocupado_L = (pulpa / Decimal(0.5)) + (rastrojo_kg / Decimal(0.5))
            CAPACIDAD_SEGURA_L = MezclaForm.CAPACIDAD_IBC_L * Decimal(0.9)
            agua_requerida = max(Decimal(0), CAPACIDAD_SEGURA_L - volumen_ocupado_L)
            
            form.fields['agua_litros_necesarios'].initial = round(agua_requerida, 2)
            
            volumen_total_L = volumen_ocupado_L + agua_requerida
            
            # --- CÁLCULO C/N ---
            C_total = (pulpa * Decimal(25)) + (rastrojo_kg * Decimal(40))
            N_total = (pulpa * Decimal(1.5)) + (rastrojo_kg * Decimal(0.5))
            
            if N_total == 0:
                 cn = Decimal(0)
            else:
                 cn = C_total / N_total
            
            # --- CÁLCULO DE NUTRIENTES (NPK TEÓRICO) ---
            # Estimación teórica del NPK total en la mezcla, asumiendo 80% de N se conserva
            # Valores teóricos por kg: N: 1.5, P: 0.8, K: 1.2
            
            # NPK total en la mezcla (g)
            N_total_g = (pulpa * Decimal(15)) + (rastrojo_kg * Decimal(5)) # Estimación N total en gramos
            P_total_g = (pulpa * Decimal(3)) + (rastrojo_kg * Decimal(2))
            K_total_g = (pulpa * Decimal(10)) + (rastrojo_kg * Decimal(8))
            
            # Concentración final (g/L)
            N_final_gL = (N_total_g * Decimal(0.8)) / volumen_total_L # N se reduce por gasificación
            P_final_gL = P_total_g / volumen_total_L
            K_final_gL = K_total_g / volumen_total_L

            # --- RECOMENDACIÓN C/N ---
            recomendacion = ""
            if 28 <= cn <= 32: 
                recomendacion = "✅ Mezcla en el rango de oro (28:1 a 32:1) para biogás."
                clase_alerta = "success"
            elif cn < 28:
                recomendacion = "⚠️ La relación C/N es baja (ácida). Agregue más material rico en carbono (rastrojo)."
                clase_alerta = "warning"
            else: 
                recomendacion = "⚠️ La relación C/N es alta. Agregue más pulpa de café para optimizar."
                clase_alerta = "warning"
            
            resultado = {
                'cn': round(cn, 2), 
                'recomendacion': recomendacion, 
                'alerta': clase_alerta,
                'nutrientes': {
                    'N': round(N_final_gL, 2),
                    'P': round(P_final_gL, 2),
                    'K': round(K_final_gL, 2),
                    'volumen': round(volumen_total_L, 2)
                }
            }

    return render(request, 'gestion/nueva_mezcla.html', {'form': form, 'resultado': resultado})

# 4. Monitoreo
def monitoreo(request):
    form = MonitoreoForm()
    interpretacion = None

    if request.method == 'POST':
        form = MonitoreoForm(request.POST)
        if form.is_valid():
            pH = form.cleaned_data['ph']
            temp = form.cleaned_data['temperatura_ambiente']
            
            if 6.5 <= pH <= 7.5:
                mensaje = "pH en rango óptimo ✅. El proceso es estable."
                clase_alerta = "success"
            elif pH < 6.5:
                mensaje = "El pH está bajo ⚠️ → Añadir más material rico en carbono. Riesgo de acidificación."
                clase_alerta = "danger"
            else:
                mensaje = "El pH está alto ⚠️ → Podría indicar sobrecarga de amoníaco o falta de agitación."
                clase_alerta = "warning"
            
            interpretacion = {'mensaje': mensaje, 'alerta': clase_alerta, 'ph': pH, 'temp': temp}

    return render(request, 'gestion/monitoreo.html', {'form': form, 'interpretacion': interpretacion})


# 5. Predicción de Nutrientes e Impacto Ambiental
def nutrientes(request):
    data = {
        'nitrogeno': 1.5,   # g/L
        'fosforo': 0.8,     # g/L
        'potasio': 1.2,     # g/L
        'comparacion': [
            {'fertilizante': 'Biofertilizante (SDGC)', 'n': 1.5, 'p': 0.8, 'k': 1.2},
            {'fertilizante': 'Químico Estándar', 'n': 2.0, 'p': 1.0, 'k': 1.5},
        ],
        'co2_ahorro': 50, # kg
    }
    return render(request, 'gestion/nutrientes.html', data)

# 6. Soporte / Servicio al Cliente
def servicio_al_cliente(request):
    """Muestra la página de soporte y contacto."""
    return render(request, 'gestion/servicio_al_cliente.html')

# 7. Tablas Teóricas
def tablas_teoricas(request):
    """Muestra las tablas de referencia con mezclas precalculadas."""
    
    # --- Datos para BIOGÁS (enfocados en C/N) ---
    mezclas_biogas = [
        {'id': 1, 
         'nombre': 'Mezcla Balanceada (Óptima C/N)', 
         'pulpa_kg': 100, 
         'rastrojo_kg': 35, 
         'agua_L': 670, 
         'cn_ratio': '30.5:1', 
         'recomendaciones': 'Mejor mezcla para biogás (C/N ideal).', 
         'alerta': 'success'},
        
        {'id': 2, 
         'nombre': 'Mezcla para Alta Carga', 
         'pulpa_kg': 150, 
         'rastrojo_kg': 50, 
         'agua_L': 550, 
         'cn_ratio': '29.8:1', 
         'recomendaciones': 'Balanceada, alto rendimiento de metano.', 
         'alerta': 'success'},
         
        {'id': 3, 
         'nombre': 'Mezcla Conservadora', 
         'pulpa_kg': 80, 
         'rastrojo_kg': 25, 
         'agua_L': 750, 
         'cn_ratio': '31.2:1', 
         'recomendaciones': 'Bajo riesgo de acidificación.', 
         'alerta': 'success'},
    ]

    # --- Datos para NUTRIENTES (enfocados en NPK) ---
    mezclas_nutrientes = [
        {'id': 1, 
         'nombre': 'Mezcla Balanceada', 
         'pulpa_kg': 100, 
         'rastrojo_kg': 35, 
         'N_gL': 1.6, 
         'P_gL': 0.85, 
         'K_gL': 1.35,
         'recomendaciones': 'Rendimiento estándar NPK y biogás equilibrado.',
         'alerta': ''},
         
        {'id': 2, 
         'nombre': 'Mezcla para Nutrientes (Alto K/N)', 
         'pulpa_kg': 120, 
         'rastrojo_kg': 20, 
         'N_gL': 1.8, 
         'P_gL': 0.9, 
         'K_gL': 1.5,
         'recomendaciones': 'Mejor mezcla para extraer nutrientes, alto Potasio.',
         'alerta': 'info'},

        {'id': 3, 
         'nombre': 'Mezcla Bajo N (Alto Rastrojo)', 
         'pulpa_kg': 70, 
         'rastrojo_kg': 40, 
         'N_gL': 1.4, 
         'P_gL': 0.7, 
         'K_gL': 1.1,
         'recomendaciones': 'Para suelos que requieren bajo aporte de nitrógeno.',
         'alerta': ''},
    ]

    context = {
        'mezclas_biogas': mezclas_biogas,
        'mezclas_nutrientes': mezclas_nutrientes,
    }
    return render(request, 'gestion/tablas_teoricas.html', context)