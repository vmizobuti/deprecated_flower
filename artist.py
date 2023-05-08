# artist.py 
#
# Finaliza o modelo 3DM de acordo com as cores fornecidas pelo usuário 
# e cria funções para exportar o resultado em JPEG (para a versão Web)
# e em Adobe PDF (para produção).
#

from os import getcwd
from math import ceil
import numpy as np
import rhinoinside

rhinoinside.load()

import System
import Rhino
from Rhino.Geometry import Point3d, Vector3d, Curve, Hatch
from System.Collections.Generic import List
from System.Drawing import Color, Bitmap

def MakeGradient(colors, n):
    """
    Cria uma lista de N cores em um gradiente entre as cores C1 e C2.
    As cores de entrada são em HEX e a lista de saída é em RGB.
    """
    # Transforma as cores fornecidas em HEX para RGB decimal
    c1 = np.array(colors[0])/255
    c2 = np.array(colors[1])/255
    
    # Cria os valores intermediários entre as cores fornecidas
    stops = [x/(n-1) for x in range(n)]
    rgb = [((1 - stop) * c1 + (stop * c2)) for stop in stops]

    # Cria a lista de cores em RGB-255
    gradient = [
        [round(v[0] * 255), round(v[1] * 255), round(v[2] * 255)] for v in rgb
        ]
    
    return gradient

def paint(filename, colors):
    """
    Cria todas as camadas de hatches e cores para o modelo 3DM fornecido, de 
    acordo com a lista de cores. A lista de cores deve fornecer duas cores e 
    uma quantidade N de cores intermediárias entre as duas cores.
    Essa função retorna o nome do arquivo utilizado.
    """
    # Abre o arquivo Rhino com base no nome do arquivo fornecido
    doc = Rhino.RhinoDoc.Open(filename)[0]

    # Gera o gradiente de cores e separa as cores em seus respectivos canais    
    gradient = MakeGradient([colors[0][1], colors[0][2]], colors[1] + 2)

    # Configura a layer ativa para a layer 'Arte'
    doc.Layers.SetCurrentLayerIndex(doc.Layers.FindName('Arte').Index, True)
    
    # Coleta todas as curvas da layer 'Arte' para criação dos hatches
    curves = doc.Objects.FindByLayer(doc.Layers.FindName('Arte'))
    
    # Cria os hatches com base em operações booleanas de cada curva
    for i in range(len(curves)):
        clist = List[Curve]()
        clist.Add(curves[i].Geometry)
        plane = curves[i].Geometry.TryGetPlane()[1]
        region = Curve.CreateBooleanRegions(clist, plane,
                                            True, 0.01)
        
        # Cria os hatches de acordo com as cores da lista de cores
        for j in range(region.RegionCount):
            for k in range(len(region.RegionCurves(j))):
                # Cria o hatch com base nas curvas da operação booleana
                hatch = Hatch.Create(region.RegionCurves(j)[k], 1, 0, 1, 0.01)
                
                # Define os atributos do objeto, para garantir o output
                # nas cores corretas
                stop = gradient[i]
                color = Color.FromArgb(255, stop[0], stop[1], stop[2])
                att = Rhino.DocObjects.ObjectAttributes()
                att.LayerIndex = 4
                att.ColorSource = Rhino.DocObjects.ObjectColorSource(1)
                att.PlotColorSource = Rhino.DocObjects.ObjectPlotColorSource(1)
                att.PlotColor = color
                att.ObjectColor = color

                # Adiciona o hatch ao modelo
                doc.Objects.AddHatch(hatch[0], att)
                
        # Deleta a curva original utilizada para criar o hatch
        doc.Objects.Delete(curves[i])

    # Configura a layer ativa para a layer 'Texto'
    doc.Layers.SetCurrentLayerIndex(doc.Layers.FindName('Texto').Index, True)
    
    # Coleta todas as curvas da layer 'Texto' para criação dos hatches
    outline = doc.Objects.FindByLayer(doc.Layers.FindName('Texto'))

    # Cria os hatches com base em operações booleanas de cada curva
    t_list = List[Curve]()
    for i in range(len(outline)):
        t_list.Add(outline[i].Geometry)
    t_hatch = Hatch.Create(t_list, 1, 0, 1, 0.01)
    for hatch in t_hatch:
        color = Color.FromArgb(255, 210, 210, 210)
        att = Rhino.DocObjects.ObjectAttributes()
        att.LayerIndex = 1
        att.ColorSource = Rhino.DocObjects.ObjectColorSource(1)
        att.PlotColorSource = Rhino.DocObjects.ObjectPlotColorSource(1)
        att.PlotColor = color
        att.ObjectColor = color
        doc.Objects.AddHatch(hatch, att)
    
    # Deleta as curvas de texto após criação dos hatches
    for curve in outline:
        doc.Objects.Delete(curve)

    # Salva e fecha o arquivo após finalizar todas as operações    
    doc.Save()
    doc.Dispose()

    return filename

def export_jpeg(size, res, filename, id):
    """
    Exporta o modelo 3DM em dois possíveis arquivos JPEG para visualização, um
    em baixa resolução (thumbnail) e outro em alta resolução (zoom).
    """
    # Abre o arquivo do Rhino conforme nome fornecido
    doc = Rhino.RhinoDoc.Open(filename)[0]

    # Configura a viewport ativa para a vista superior
    viewport = Rhino.Display.RhinoViewport()
    viewport.SetToPlanView(Point3d(0, 0, 0), 
                           Vector3d(1, 0, 0),
                           Vector3d(0, 1, 0), True)
    doc.Views.ActiveView.ActiveViewport.PushViewInfo(
        Rhino.DocObjects.ViewInfo(viewport), False
        )
    
    # Define as configurações de saída do JPEG
    view = doc.Views.ActiveView
    dpi = 72
    if res == 0:
        frame = System.Drawing.Size(600, 600)
    elif res == 1:
        frame = System.Drawing.Size(3200, 3200)
    settings = Rhino.Display.ViewCaptureSettings(view, frame, dpi)
    settings.RasterMode = False
    settings.ViewArea = Rhino.Display.ViewCaptureSettings.ViewAreaMapping(1)

    # Cria a captura da página especificada
    bitmap = Rhino.Display.ViewCapture.CaptureToBitmap(settings)
    
    # Salva o arquivo bitmap de saída
    if res == 0:
        savepath = getcwd() + "\\JPEG\\" + id + "_LQ.jpeg"
    elif res == 1:
        savepath = getcwd() + "\\JPEG\\" + id + "_HQ.jpeg"
    bitmap.Save(savepath, System.Drawing.Imaging.ImageFormat.Jpeg)

    # Fecha o documento após finalizar o seu uso
    doc.Dispose()

    return

def export_pdf(size, filename, id):
    """
    Exporta o modelo 3DM em um arquivo PDF para produção.
    """
    # Abre o arquivo do Rhino conforme nome fornecido
    doc = Rhino.RhinoDoc.Open(filename)[0]

    # Configura a viewport ativa para a vista superior
    viewport = Rhino.Display.RhinoViewport()
    viewport.SetToPlanView(Point3d(0, 0, 0), 
                           Vector3d(1, 0, 0),
                           Vector3d(0, 1, 0), True)
    doc.Views.ActiveView.ActiveViewport.PushViewInfo(
        Rhino.DocObjects.ViewInfo(viewport), False
        )

    # Cria o arquivo PDF de saída
    pdf = Rhino.FileIO.FilePdf.Create()

    # Define as configurações do arquivo de saída
    view = doc.Views.ActiveView
    dpi = 300
    px_size = ceil((size/2.54) * dpi)
    frame = System.Drawing.Size(px_size, px_size)
    settings = Rhino.Display.ViewCaptureSettings(view, frame, dpi)
    settings.RasterMode = False
    settings.ViewArea = Rhino.Display.ViewCaptureSettings.ViewAreaMapping(1)
    pdf.AddPage(settings)

    # Salva o arquivo PDF na sua devida localização
    savepath = getcwd() + "\\PDF\\" + id + ".pdf"
    pdf.Write(savepath)

    # Fecha o documento após finalizar o seu uso
    doc.Dispose()

    return savepath