# Implementação do Conceito Flor para a DressPOP 
#
# Autor: Vinicius Mizobuti / Superlimão
# 
# Versão: 1.0.0

import json
import sys

from geolocation import coordinates
from make_flower import make_flower, make_jpeg, make_pdf

def load_input(file):
    """
    Carrega os valores de entrada à partir de um arquivo JSON e formata
    eles de acordo com o esquema necessário para a geração da arte.
    """

    # Carrega os valores de entrada
    input = json.load(file)

    # Avalia se os valores de entrada da data estão corretos
    date = input['data'].split('/')
    if len(date) != 3:
        raise ValueError('Confira se inseriu a data com dia, mês e ano.')
    elif len(date[0]) != 2 or len(date[1]) != 2 or len(date[2]) != 4:
        raise ValueError('Confira se a data está no formato DD/MM/AAAA.')
    elif ''.join(date).isnumeric() == False:
        raise ValueError('Confira se inseriu corretamente a data.')

    # Formata a data como uma lista de números inteiros
    date = ''.join(date)
    date = [int(x) for x in date]

    # Avalia se os valores de entrada de localização estão corretos
    geo_loc = coordinates(input['cidade'], input['estado'], input['pais'])
    if geo_loc == None:
        raise ValueError('Localização inserida não foi encontrada.')
    
    # Formata a localização como uma lista de coordenadas
    loc = [geo_loc.latitude, geo_loc.longitude]

    # Avalia se o valor de entrada para o tamanho da arte está correto
    if type(input['dimensões']) != int:
        raise TypeError('Valor de entrada para a dimensão não é compatível.')
    else:
        size = input['dimensões']
    
    # Avalia se o valor de entrada para as cores está correto
    if type(input['cores']) != int:
        raise TypeError('Valor de entrada para as cores não é compatível.')
    elif input['cores'] < 1 or input['cores'] > 10:
        raise ValueError('Não existe valor compatível com a cor selecionada.')
    else:
        color = input['cores']

    return date, loc, size, color

def main():
    
    # Formata o nome do arquivo JSON de entrada, e retorna um aviso caso um 
    # arquivo não tenha sido encontrado ou a ID não tenha sido fornecida
    if len(sys.argv) != 2:
        raise ValueError('Insira o ID da arte.')
    try:
        filename = sys.argv[1] + '.json'
        file = open(filename, encoding='utf-8')
    except:
        raise ValueError('Não foi encontrado arquivo JSON com o ID fornecido.')

    # Carrega os valores de entrada à partir de um arquivo JSON
    input = load_input(file)
    art_id = str(sys.argv[1])

    # Gera a arte à partir dos valores de entrada
    file3dm = make_flower(input[0], input[1], input[2], input[3], art_id)

if __name__ == '__main__':
    main()