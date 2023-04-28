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
from compute_rhino3d import Curve, Intersection

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

def Remap(value, old_domain, new_domain):
    """
    Remapeia um número de um domínio D1 para um domínio D2.
    """
    # Calcula o intervalo do domínio original
    old_range = old_domain[1] - old_domain[0]

    # Calcula o intervalo do novo domínio
    new_range = new_domain[1] - new_domain[0]

    # Remapeia os valores entre domínios
    remapped_value = (((value - old_domain[0]) * new_range)/old_range) + \
                     new_domain[0]

    return remapped_value

def GetTangentCurves(c1, c2):
    """
    Calcula as linhas tangentes a dois circulos, C1 e C2.
    Retorna essas linhas como objetos rhino3dm.Line(p1, p2).
    """
    # Organiza a lista de círculos de acordo com o raio
    c = sorted([c1, c2], key= lambda x:x.Radius)
    
    # Calcula o ponto médio entre o centro dos dois círculos
    line = r3dm.Line(c[0].Center, c[1].Center)
    mid = line.PointAt(0.5)
    
    # Cria o círculo de intersecção entre os dois círculos
    mid_circle = r3dm.Circle(mid, (line.Length)/2)
    
    # Cria o círculo interno ao círculo maior, com raio R - r
    inn_circle = r3dm.Circle(c[1].Center, (c[1].Radius - c[0].Radius))
    
    # Calcula os pontos de intersecção entre os círculos auxiliares
    intersection = Intersection.CurveCurve(mid_circle.ToNurbsCurve(),
                                           inn_circle.ToNurbsCurve(),
                                           0.001, 0.001)
    i1 = r3dm.Point3d(intersection[0]['PointA']['X'], 
                      intersection[0]['PointA']['Y'], 0.0)
    i2 = r3dm.Point3d(intersection[1]['PointA']['X'], 
                      intersection[1]['PointA']['Y'], 0.0)
    
    # Calcula os vetores perpendiculares às curvas tangentes
    length = i1.DistanceTo(c[1].Center)
    v1 = r3dm.Vector3d(((i1.X - c[1].Center.X)/length) * c[1].Radius, 
                       ((i1.Y - c[1].Center.Y)/length) * c[1].Radius, 0.0)
    v2 = r3dm.Vector3d(((i2.X - c[1].Center.X)/length) * c[1].Radius, 
                       ((i2.Y - c[1].Center.Y)/length) * c[1].Radius, 0.0)
    v3 = r3dm.Vector3d(((i1.X - c[1].Center.X)/length) * c[0].Radius, 
                       ((i1.Y - c[1].Center.Y)/length) * c[0].Radius, 0.0)
    v4 = r3dm.Vector3d(((i2.X - c[1].Center.X)/length) * c[0].Radius, 
                       ((i2.Y - c[1].Center.Y)/length) * c[0].Radius, 0.0)    

    # Cria as transformações de movimento para cada ponto baseado nos vetores
    t1 = r3dm.Transform.Translation(v1)
    t2 = r3dm.Transform.Translation(v2)
    t3 = r3dm.Transform.Translation(v3)
    t4 = r3dm.Transform.Translation(v4)

    # Movimenta os pontos centrais de acordo com as transformações criadas
    p1 = c[1].Center.Transform(t1)
    p2 = c[1].Center.Transform(t2)
    p3 = c[0].Center.Transform(t3)
    p4 = c[0].Center.Transform(t4)

    # Cria um polígono fechado composto pelos quatro pontos tangentes
    polygon = r3dm.Polyline([p1, p2, p4, p3, p1])

    return polygon

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

    # Cria o círculo central da arte
    origin = r3dm.Point3d(0, 0, 0)
    center = r3dm.Circle(origin, size/50)

    # Calcula o valor de rotação para cada ponto da arte
    angle = [
        ((arc/4) * date[x]) if x == 0 else 
        ((arc/3) * (date[x] + 1)) + arc * x if x == 2 else
        ((arc/10) * date[x]) + arc * x for x in range(len(date))
        ]

    # Calcula o valor de distância do centro para cada ponto da arte
    fac = [0.45, 0.85]
    scale = [(Remap(date[x], [0, 9], fac) * radius) for x in range(len(date))]

    # Cria os pontos da arte baseado nas suas coordenadas polares
    points = [PointPolar(scale[x], angle[x]) for x in range(len(date))]

    # Cria os círculos que compõem as pétalas da flor
    circles = [r3dm.Circle(points[x], scale[x]/5) for x in range(len(points))]
    plines = [GetTangentCurves(center, circles[x]) for x in range(len(circles))]

    # Cria a união das curvas produzidas, fazendo a forma base da flor
    objects = [center.ToNurbsCurve()]
    for circle in circles:
        objects.append(circle.ToNurbsCurve())
    for pline in plines:
        objects.append(pline.ToNurbsCurve())
    flower = Curve.CreateBooleanUnion(objects)[0]

    # Arredonda as pontas anguladas da geometria
    flower = Curve.CreateFilletCornersCurve(flower, size/100, 0.001, 0.001)
    flower = Curve.CreateFilletCornersCurve(flower, size/200, 0.001, 0.001)

    # Recria a curva utilizando pontos de controle espaçados, para
    # garantir uma transição suave
    control_points = 150
    flower = Curve.Rebuild(flower, control_points, 3, False) 

    # Rotaciona a geometria de base de acordo com os valores de latitude e
    # longitude obtidos
    loc_angle = loc[0] + loc[1]
    loc_rot = r3dm.Transform.Rotation(math.radians(loc_angle),
                                      r3dm.Vector3d(0, 0, 1),
                                      origin)
    backfl = flower.Duplicate()
    backfl.Transform(loc_rot)

    # Move a geometria de base para cima para produzir as curvas intermediárias
    move_up = r3dm.Transform.Translation(r3dm.Vector3d(0, 0, 5))
    flower.Transform(move_up)

    # Ajusta o ponto de início da curva inferior
    point_on_flower = flower.PointAt(0.15)
    param_on_backfl = Curve.ClosestPoint(backfl, point_on_flower)[1]
    backfl.ChangeClosedCurveSeam(param_on_backfl)

    # Cria as curvas intermediárias entre as duas bases
    tween = Curve.CreateTweenCurves(flower, backfl, 120)
    planes = [r3dm.Plane(crv.PointAtStart, r3dm.Vector3d(0, 0, 1)) for crv in tween]

    regions = []
    for i in range(len(tween)):
        region = Curve.CreateBooleanRegions1([tween[i]], planes[i], True, 0.01)
        regions.append(region)

    for region in regions:
        print(region.keys())

    for curve in tween:
        model.Objects.AddCurve(curve)

    # Saves the 3DM file after all geometric operations are completed
    model.Write(id + '.3dm')
    
    return 

def make_jpeg(filename):
    return

def make_pdf(filename):
    return
