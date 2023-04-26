# make_flower.py 
#
# Cria a arte para o DressPOP utilizando as bibliotecas
# da API do Rhinoceros, Rhino.Compute e Rhino.Inside, baseada
# nos parâmetros fornecidos pelo usuário. Retorna um arquivo
# em JPEG e um arquivo em 3DM.
#

import math
import rhino3dm as r3dm
import compute_rhino3d.Util
from compute_rhino3d import Curve, AreaMassProperties

def PointPolar(radius, phi):
    """
    Transforma coordenadas polares em coordenadas cartesianas
    e cria um Point3d baseado nessas coordenadas.
    A função assume que o plano de rotação é diferente do WorldXY, para
    que se assemelhe ao relógio. Por isso, o valor Phi é subtraído de 90.
    """
    # Calcula o ângulo do ponto em radianos
    angle = math.radians(90 - phi)

    # Calcula o valor das coordenadas X e Y
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)

    # Cria o ponto baseado nas coordenadas obtidas
    point = r3dm.Point3d(x, y, 0)

    return point

def make_flower(date, loc, size, color, id):
    """
    Cria o arquivo 3DM com a geometria necessária para a arte,
    utilizando as funcões do rhino3dm e do Rhino.Compute.
    Essa função retorna o nome do arquivo 3DM após a finalização
    de todas as operações.
    """

    # Inicializa a instância do servidor do Rhino.Compute
    compute_rhino3d.Util.url = "http://localhost:8081/"

    # Cria o arquivo 3DM em que serão feitas as operações
    model = r3dm.File3dm()
    model.Settings.ModelUnitSystem = r3dm.UnitSystem.Centimeters
    model.Layers.AddLayer("Arte", (0, 0, 0, 255))
    model.Layers.AddLayer("Texto", (190, 190, 190, 255))
    model.Layers.AddLayer("Frame", (255, 255, 255, 255))

    # Cria as dimensões básicas para a geração da arte
    width = size
    height = size
    margin = size * 0.05
    radius = (size/2) - margin
    arc = 360/8

    # Calcula o valor de rotação para cada ponto da arte
    r1 = ((arc/4) * date[0])
    r2 = ((arc/10) * date[1]) + arc * 1
    r3 = ((arc/3) * (date[2] + 1)) + arc *2
    r4 = ((arc/10) * date[3]) + arc * 3
    r5 = ((arc/10) * date[4]) + arc * 4
    r6 = ((arc/10) * date[5]) + arc * 5
    r7 = ((arc/10) * date[6]) + arc * 6
    r8 = ((arc/10) * date[7]) + arc * 7
    
    # Cria os pontos da arte baseado nas suas coordenadas polares
    p0 = r3dm.Point3d(0, 0, 0)
    p1 = PointPolar(radius, r1)
    p2 = PointPolar(radius, r2)
    p3 = PointPolar(radius, r3)
    p4 = PointPolar(radius, r4)
    p5 = PointPolar(radius, r5)
    p6 = PointPolar(radius, r6)
    p7 = PointPolar(radius, r7)
    p8 = PointPolar(radius, r8)

    # Cria as linhas base da arte
    model.Objects.AddLine(p0, p1)
    model.Objects.AddLine(p0, p2)
    model.Objects.AddLine(p0, p3)
    model.Objects.AddLine(p0, p4)
    model.Objects.AddLine(p0, p5)
    model.Objects.AddLine(p0, p6)
    model.Objects.AddLine(p0, p7)
    model.Objects.AddLine(p0, p8)

    # Saves the 3DM file after all geometric operations are completed
    model.Write(id + '.3dm')
    
    return

def make_jpeg(filename):
    return

def make_pdf(filename):
    return
