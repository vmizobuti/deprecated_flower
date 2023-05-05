# geometry.py 
#
# Cria o modelo 3DM para o DressPOP utilizando as bibliotecas
# da API do Rhinoceros e Rhino.Compute, baseada nos parâmetros 
# fornecidos pelo usuário. Retorna um arquivo em 3DM.
#

import math
import rhino3dm as r3dm
import compute_rhino3d.Util
from compute_rhino3d import Curve, GeometryBase, Intersection
from os import getcwd

X_AXIS = r3dm.Vector3d(1, 0, 0)
Y_AXIS = r3dm.Vector3d(0, 1, 0)
Z_AXIS = r3dm.Vector3d(0, 0, 1)

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

def GetCorners(points):
    """
    Calcula os extremos das coordenadas de uma lista de pontos.
    Retorna dois pontos que representam os extremos.
    """
    # Cria as listas de valores de X, Y e Z dos pontos selecionados
    x_val = []
    y_val = []
    z_val = []

    # Aloca os valores das coordenadas em cada uma das listas
    for point in points:
        x_val.append(point.X)
        y_val.append(point.Y)
        z_val.append(point.Z)
    
    # Cria os pontos extremos baseado nas coordenadas da lista
    min_point = r3dm.Point3d(min(x_val), min(y_val), min(z_val))
    max_point = r3dm.Point3d(max(x_val), max(y_val), max(z_val))

    return min_point, max_point

def draw_geometry(date, loc, size, text, id):
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
    model.Layers.AddLayer('Arte', (0, 0, 0, 255))
    model.Layers.AddLayer('Texto', (210, 210, 210, 255))
    model.Layers.AddLayer('Frame', (255, 255, 255, 255))
    model.Layers.AddLayer('Curvas', (255, 255, 255, 255))
    model.Layers.FindName('Curvas', 0).PlotColor = (255, 255, 255, 40)
    model.Layers.FindName('Curvas', 0).PlotWeight = size/400

    # Cria as dimensões básicas para a geração da arte
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

    # Rotaciona a geometria de base de acordo com os valores de latitude e
    # longitude obtidos
    loc_angle = loc[0] + loc[1]
    loc_rot = r3dm.Transform.Rotation(math.radians(loc_angle), Z_AXIS, origin)
    backfl = flower.Duplicate()
    backfl.Transform(loc_rot)

    # Move a geometria de base para cima para produzir as curvas intermediárias
    move_up = r3dm.Transform.Translation(0, 0, 5)
    flower.Transform(move_up)

    # Ajusta o ponto de início da curva superior
    param_on_flower = 0.15
    flower.ChangeClosedCurveSeam(param_on_flower)

    # Ajusta o ponto de início da curva inferior
    point_on_flower = flower.PointAt(param_on_flower)
    param_on_backfl = Curve.ClosestPoint(backfl, point_on_flower)[1]
    backfl.ChangeClosedCurveSeam(param_on_backfl)

    # Cria as curvas intermediárias entre as duas bases
    tween = Curve.CreateTweenCurvesWithMatching(flower, backfl, 120)

    # Agrupa as geometrias para alinhamento com o quadro
    model.Groups.Add(r3dm.Group())
    model.Groups.FindIndex(0).Name = 'Curvas'
    att = r3dm.ObjectAttributes()
    att.LayerIndex = 0
    att.AddToGroup(0)
    model.Objects.AddCurve(flower, att)
    for curve in tween:
        model.Objects.AddCurve(curve, att)
    model.Objects.AddCurve(backfl, att)

    # Projeta as curvas de sobreposição ao plano superior
    top_plane = r3dm.Plane(r3dm.Point3d(0, 0, 10), Z_AXIS)
    project = []
    project.append(Curve.ProjectToPlane(flower, top_plane))
    project.append(Curve.ProjectToPlane(backfl, top_plane))
    for curve in tween:
        project.append(Curve.ProjectToPlane(curve, top_plane))
    
    # Adiciona as curvas de sobreposição ao modelo
    satt = r3dm.ObjectAttributes()
    satt.LayerIndex = 3
    for curve in project:
        model.Objects.AddCurve(curve, satt)

    # Calcula o ponto central do conjunto das curvas
    box1 = GeometryBase.GetBoundingBox(flower, True)
    box2 = GeometryBase.GetBoundingBox(backfl, True)
    corners = GetCorners([box1.Min, box2.Min, box1.Max, box2.Max])
    bbox = r3dm.BoundingBox(corners[0], corners[1])

    # Cria o vetor de transformação das geometrias
    vec = r3dm.Vector3d(-bbox.Center.X, -bbox.Center.Y, -2.5)
    move_center = r3dm.Transform.Translation(vec)

    # Move os objetos de acordo com o vetor de transformação
    for object in model.Objects:
        object.Geometry.Transform(move_center)
    
    # Cria o texto da arte de acordo com os textos recebidos
    pln_txt = r3dm.Plane(r3dm.Point3d((-size/2) + margin/2, 
                                      (-size/2) + margin/2, 0), Z_AXIS)
    crv_txt = Curve.CreateTextOutlines(text, 'Founders Grotesk Light', 0.3, 
                                       0, True, pln_txt, 1.0, 0.01)

    # Cria a moldura da arte de acordo com as dimensões recebidas
    f1 = r3dm.Point3d(size/2, size/2, 0.0)
    f2 = r3dm.Point3d(-size/2, size/2, 0.0)
    f3 = r3dm.Point3d(-size/2, -size/2, 0.0)
    f4 = r3dm.Point3d(size/2, -size/2, 0.0)
    frame = r3dm.Polyline([f1, f2, f3, f4, f1])

    # Adiciona as curvas de texto ao modelo
    tatt = r3dm.ObjectAttributes()
    tatt.LayerIndex = 1
    for curve in crv_txt:
        model.Objects.AddCurve(curve, tatt)
    
    # Adiciona a curva do frame ao modelo
    fatt = r3dm.ObjectAttributes()
    fatt.LayerIndex = 2
    model.Objects.AddCurve(frame.ToNurbsCurve(), fatt)

    # Salva o arquivo 3DM após todas as operações serem finalizadas
    filename = getcwd() + "\\3DM\\" + id + '.3dm'
    model.Write(filename)
    
    return filename