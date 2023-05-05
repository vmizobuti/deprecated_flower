# geolocation.py 
#
# Utiliza o módulo geopy e a base de dados Nominatim-OSM para
# coletar os valores decimais de latitude e longitude de uma
# localização fornecida pelo usuário.
#

from geopy.geocoders import Nominatim

def coordinates(cidade, estado, pais):
    """
    Utiliza o módulo geopy para coletar os valores de latitude
    e longitude de uma localização. Caso a localização não exista,
    ou o geolocator retorne alguma exceção, a função retorna um
    valor vazio.
    """
    # Formata os valores de entrada para um dicionário de query estruturado
    address = {'city': cidade, 'state': estado, 'country': pais}
    
    # Inicializa o localizador utilizando o Nominatim-OSM
    geolocator = Nominatim(user_agent="DressPOP")
    
    # Inicia a busca pela localização do endereço. Caso uma exceção
    # surja, retorna um valor vazio. Do contrario, retorna a localização.
    try:
        location = geolocator.geocode(address, addressdetails=True)
    except:
        return None

    return location