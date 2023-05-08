# colors.py 
#
# Esse arquivo organiza as cores das artes do DressFlower 
# para retornar o conjunto de valores
# e em Adobe PDF (para produção).
#

VERMELHO = ['#ffcdcc', '#93222d', '#e03c31']

AMARELO = ['#fff5cc', '#eaaa00', '#ffd833']

VERDE_CLARO = ['#f0ffcc', '#6cc24a', '#cfe89c']

VERDE_MUSGO = ['#a6b798', '#2d3f22', '#5c7f45']

AZUL_CLARO = ['#ccf4ff', '#2691bc', '#9edcf2']

AZUL_ESCURO = ['#ccccff', '#2e2ecc', '#06038d']

LILAS = ['#e7ccff', '#785cc6', '#c19bdd']

ROSA = ['#ffcce4', '#cc2348', '#ff8fbf']

TURQUESA = ['#ccfffb', '#00a1a5', '#88e2de']

TERRACOTA = ['#ffd4cc', '#7a2b15', '#c9644c']

PRATA = ['#ffffff', '#7c7c7b', '#c6c6c6']

DOURADO = ['#fff0cc', '#c18a00', '#edce7a']

def hex_to_rgb(hex):
    """
    Transforma valores de cores em HEX para RGB.
    """
    return [int(hex[i:i+2], 16) for i in range(1, 6, 2)]

def color_table(val):
    """
    Tabela de composição das cores pré-definidas para o DressPOP.
    """
    if val == 1:
        colors = [hex_to_rgb(val) for val in VERMELHO]
        return colors
    elif val == 2:
        colors = [hex_to_rgb(val) for val in AMARELO]
        return colors
    elif val == 3:
        colors = [hex_to_rgb(val) for val in VERDE_CLARO]
        return colors
    elif val == 4:
        colors = [hex_to_rgb(val) for val in VERDE_MUSGO]
        return colors
    elif val == 5:
        colors = [hex_to_rgb(val) for val in AZUL_CLARO]
        return colors
    elif val == 6:
        colors = [hex_to_rgb(val) for val in AZUL_ESCURO]
        return colors
    elif val == 7:
        colors = [hex_to_rgb(val) for val in LILAS]
        return colors
    elif val == 8:
        colors = [hex_to_rgb(val) for val in ROSA]
        return colors
    elif val == 9:
        colors = [hex_to_rgb(val) for val in TURQUESA]
        return colors
    elif val == 10:
        colors = [hex_to_rgb(val) for val in TERRACOTA]
        return colors
    elif val == 11:
        colors = [hex_to_rgb(val) for val in PRATA]
        return colors
    elif val == 12:
        colors = [hex_to_rgb(val) for val in DOURADO]
        return colors
