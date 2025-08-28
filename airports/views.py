from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import requests
import json

#  Contiene la lógica para procesar las peticiones a la API de Airport Gap

def airport_distance_view(request):
    """Vista principal que muestra el formulario"""
    return render(request, 'airport_distance.html')

@csrf_exempt
def calculate_distance(request):
    """Vista que procesa el cálculo de distancia entre aeropuertos"""
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            aeropuerto_origen = request.POST.get('aeropuerto_origen', '').strip().upper()
            aeropuerto_destino = request.POST.get('aeropuerto_destino', '').strip().upper()
            
            # Validar que ambos campos estén llenos
            if not aeropuerto_origen or not aeropuerto_destino:
                return JsonResponse({
                    'success': False,
                    'error': 'Debe ingresar ambos códigos de aeropuerto'
                })
            
            # Validar que los códigos tengan 3 caracteres
            if len(aeropuerto_origen) != 3 or len(aeropuerto_destino) != 3:
                return JsonResponse({
                    'success': False,
                    'error': 'Los códigos IATA deben tener exactamente 3 caracteres'
                })
            
            # URL de la API
            base_url = "https://airportgap.com/api/airports"
            
            # Datos para el POST request
            airports_data = {
                "from": aeropuerto_origen,
                "to": aeropuerto_destino
            }
            
            # Realizar la petición POST
            response_post = requests.post(f"{base_url}/distance", json=airports_data, timeout=10)
            
            if response_post.status_code == 200:
                datos = response_post.json()
                
                # Extraer información de la respuesta
                result_data = {
                    'success': True,
                    'codigo': datos["data"]["id"],
                    'aeropuerto_origen': {
                        'nombre': datos["data"]["attributes"]["from_airport"]["name"],
                        'ciudad': datos["data"]["attributes"]["from_airport"]["city"],
                        'codigo': aeropuerto_origen
                    },
                    'aeropuerto_destino': {
                        'nombre': datos["data"]["attributes"]["to_airport"]["name"],
                        'ciudad': datos["data"]["attributes"]["to_airport"]["city"],
                        'codigo': aeropuerto_destino
                    },
                    'distancia_km': datos["data"]["attributes"]["kilometers"],
                    'distancia_millas': datos["data"]["attributes"]["miles"],
                    'distancia_millas_nauticas': datos["data"]["attributes"]["nautical_miles"]
                }
                
                return JsonResponse(result_data)
            
            elif response_post.status_code == 422:
                return JsonResponse({
                    'success': False,
                    'error': 'Uno o ambos códigos de aeropuerto no son válidos'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': f'Error en la API: {response_post.status_code}'
                })
                
        except requests.exceptions.Timeout:
            return JsonResponse({
                'success': False,
                'error': 'Tiempo de espera agotado. Intente nuevamente.'
            })
        except requests.exceptions.ConnectionError:
            return JsonResponse({
                'success': False,
                'error': 'Error de conexión. Verifique su conexión a internet.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error inesperado: {str(e)}'
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Método no permitido'
    })
