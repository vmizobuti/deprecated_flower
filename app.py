import tkinter as tk
import json
import string
import random
from tkinter import font, messagebox
from PIL import ImageTk, Image
from ctypes import windll
from os import getcwd, startfile
from dress_flower import make_flower

# Ajuste da resolução de texto do Windows
windll.shcore.SetProcessDpiAwareness(1)

# Inicializa o Tkinter
root = tk.Tk()
root.geometry("530x840")
root.title("DressPOP por Superlimão / v.1.0")
root.resizable(0, 0)
root.iconbitmap(getcwd() + '\\UTIL\\icon.ico')

# Cores
BLACK = '#000000'
WHITE = '#ffffff'
GREEN = '#94d60a'

# Fontes
TIT_FONT = font.Font(family='Founders Grotesk Medium', size=16)
SUB_FONT = font.Font(family='Founders Grotesk Light', size=9)
TXT_FONT = font.Font(family='Founders Grotesk Light', size=11)

# Organização do Grid
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=2)
root.columnconfigure(3, weight=2)

# Títulos e instruções
title = tk.Label(text='DressPOP + Superlimão', font=TIT_FONT, fg=GREEN)
subtitle = tk.Label(text='Versão 1.0.0', font=SUB_FONT, fg=BLACK)
title.grid(row=0, column=0, columnspan=6, pady=30)
subtitle.grid(row=1, column=0, columnspan=6, pady=0)
instructions = tk.Label(text='Preencha os dados abaixo e clique' \
                        ' em gerar arte para criar o seu DressPOP.',
                        font=TXT_FONT, fg=BLACK, 
                        wraplength=300, justify='center')
instructions.grid(row=2, columnspan=6, pady=30)

# Inserção de etiquetas para as informações
date = tk.Label(text='Data: ', font=TXT_FONT, fg=BLACK)
loc = tk.Label(text='Local: ', font=TXT_FONT, fg=BLACK)
color = tk.Label(text='Cor: ', font=TXT_FONT, fg=BLACK)
size = tk.Label(text='Dim.: ', font=TXT_FONT, fg=BLACK)
date.grid(row=3, column=1, columnspan=1, pady=10, sticky=tk.E)
loc.grid(row=4, column=1, columnspan=1, pady=10, sticky=tk.E)
color.grid(row=5, column=1, columnspan=1, pady=10, sticky=tk.E)
size.grid(row=6, column=1, columnspan=1, pady=10, sticky=tk.E)

# Inserção de caixas de texto para coleta de dados
d_box = tk.Entry(font=TXT_FONT, fg=BLACK, width=30)
l_box = tk.Entry(font=TXT_FONT, fg=BLACK, width=30)
d_box.insert(0, 'dd/mm/aaaa')
l_box.insert(0, 'cidade, estado, país')
d_box.grid(row=3, column=2, columnspan=2, padx=20, sticky=tk.W)
l_box.grid(row=4, column=2, columnspan=2, padx=20, sticky=tk.W)


# Inserção de lista de valores para coleta de dados
c_list = [
    'Vermelho', 'Amarelo', 'Verde Claro', 'Verde Musgo', 'Azul Claro',
    'Azul Escuro', 'Lilás', 'Rosa', 'Turquesa', 'Terracota', 'Prata', 'Dourado'
    ]
c_var = tk.StringVar(root)
c_var.set(c_list[0])
c_box = tk.OptionMenu(root, c_var, *c_list, )

s_list = ['31x31', '60x60', '90x90']
s_var = tk.StringVar(root)
s_var.set(s_list[0])
s_box = tk.OptionMenu(root, s_var, *s_list)

c_box.grid(row=5, column=2, columnspan=2, padx=20, sticky=tk.W)
s_box.grid(row=6, column=2, columnspan=2, padx=20, sticky=tk.W)

# Inserção da imagem de conceito
img_path = getcwd() + '\\UTIL\\Concept.png'
img = ImageTk.PhotoImage(Image.open(img_path).resize((500, 375), Image.LANCZOS))
panel = tk.Label(root, image=img)
panel.grid(row=7, column=0, columnspan=6, padx=10, pady=40)

# Definição do evento da geração da arte
def make_json():
    # Verifica se as informações estão corretas
    date = d_box.get().split('/')
    if len(date) != 3:
        messagebox.showinfo('Erro!', 'Confira se inseriu a data com dia,' 
                            ' mês e ano.')
        return
    elif len(date[0]) != 2 or len(date[1]) != 2 or len(date[2]) != 4:
        messagebox.showinfo('Erro!', 'Confira se a data está no formato' 
                            ' DD/MM/AAAA.')
        return
    elif ''.join(date).isnumeric() == False:
        messagebox.showinfo('Erro!', 'Confira se inseriu corretamente a data.')
        return
    loc = l_box.get().split(',')
    if len(loc) != 3:
        messagebox.showinfo('Erro!', 'Confira se colocou corretamente a cidade,'
                            ' o estado e o país no campo de localização.')
        return

    color_dict = {
        'Vermelho': 1, 
        'Amarelo': 2, 
        'Verde Claro': 3, 
        'Verde Musgo': 4, 
        'Azul Claro': 5,
        'Azul Escuro': 6, 
        'Lilás': 7, 
        'Rosa': 8, 
        'Turquesa': 9, 
        'Terracota': 10, 
        'Prata': 11, 
        'Dourado': 12
    }

    # Cria o dicionário com as informações
    input = {
        "data": d_box.get(),
        "cidade": loc[0],
        "estado": loc[1],
        "pais": loc[2],
        "dimensões": int(s_var.get().split('x')[0]),
        "cores": color_dict[c_var.get()]
    }

    # Writing to sample.json
    letters = string.ascii_lowercase
    id = ''.join(random.choice(letters) for i in range(10))
    savepath = getcwd() + '\\JSON\\' + id + '.json'

    with open(savepath, 'w', encoding='utf-8') as outfile:
        json.dump(input, outfile, indent=4, ensure_ascii=False)

    return id

def start_drawing():
    art_id = make_json()
    make_flower(art_id)
    startfile(getcwd() + '\\JPEG\\' + art_id + "_HQ.jpeg")

    return

# Inserção de um botão para geração da arte
button = tk.Button(width=10, height=2, text='Gerar Arte', font=TIT_FONT,
                   fg=GREEN, command=start_drawing)
button.grid(row=5, column=3, rowspan=2, columnspan=1, padx=20)

root.mainloop()