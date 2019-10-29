from __future__ import division
from grefo.Clases import *
from tkinter.filedialog import *
from tkinter import messagebox
import math
import time
from threading import Thread
from PIL import Image, ImageTk

Ventana = Tk()
Ventana.state("zoomed")
Ventana.title("Mapa de Rutas")
Ventana.iconbitmap('bola.ico')
canvas = Canvas(Ventana, width=1200, height=650, bg="#037E8C", cursor="tcross")#taget
canvas.pack(fill=BOTH, expand=YES)
ancho = 40
li = []



# Crear Grafo
g = grafo()
l = []
img = Image.open('Bola.png')
bola = ImageTk.PhotoImage(img)


# Informacion del vertice
def click(event):
    for vert in g.listav:
        if event.x > vert.x and event.x < vert.x + ancho and event.y > vert.y and event.y < vert.y + ancho:
            info = Toplevel()
            info.title("Informacion del Punto")
            l1 = Label(info, text="Nombre:").grid(row=0, column=0)
            l2 = Label(info, text=vert.nombre).grid(row=0, column=1)
            l3 = Label(info, text="Descripcion:").grid(row=1, column=0)
            l4 = Label(info, text=vert.descripcion).grid(row=1, column=1)
            l5 = Label(info, text="Grado accidentalidad:").grid(row=2, column=0)
            l6 = Label(info, text=str(vert.gaccidente)).grid(row=2, column=1)

# Agregar vertice al mapa
def dobleclick(event):
    # Ingresar Vertice
    ingreso = Toplevel()
    ingreso.title("Agregar Punto")
    tnombre = Label(ingreso, text="Ingrese nombre del vertice:")
    tnombre.grid(row=0, column=0)
    nombrev = Entry(ingreso)
    nombrev.grid(row=0, column=1)
    tdescrip = Label(ingreso, text="Ingrese descripcion del vertice:")
    tdescrip.grid(row=1, column=0)
    descrip = Entry(ingreso)
    descrip.grid(row=1, column=1)
    tgradoa = Label(ingreso, text="Ingrese grado del vertice:")
    tgradoa.grid(row=2, column=0)
    gradoa = Entry(ingreso)
    gradoa.grid(row=2, column=1)
    agregar = Button(ingreso, text="Agregar",
                     command=lambda: agregarv(event.x, event.y, nombrev.get(), descrip.get(), gradoa.get(), ingreso))
    agregar.grid(row=3, columnspan=2)

def agregarv(x, y, nombre, descripcion, gradoa, ingreso):
    try:

        gradoa = float(gradoa)
        if (gradoa < 1 or gradoa > 5):
            ingreso.destroy()
            messagebox.showerror("ERROR", "El grado de accidentalidad no esta permitido")
        else:
            vtemp = vertice(nombre, x, y, descripcion, gradoa)
            g.agregarVertice(vtemp)
            ingreso.destroy()
            actualizar()
    except ValueError:
        ingreso.destroy()
        messagebox.showerror("ERROR", "Usted no digito un grado de accidentalidad correcto")

def agregarA(frm, to, distancia, x1, y1, x2, y2):
    atemp = arista(frm, to, distancia, x1, y1, x2, y2)
    g.agregarArista(atemp)
    actualizar()

# Relacionar vertices
def clickrelacion():
    vrelacion = Toplevel()
    vrelacion.title("Agregar Ruta")
    opciones1 = Listbox(vrelacion, exportselection=0)
    opciones2 = Listbox(vrelacion, exportselection=0)
    for v in g.listav:
        opciones1.insert(END, v.nombre)
        opciones2.insert(END, v.nombre)
    opciones1.pack(side=LEFT)
    opciones2.pack(side=LEFT)
    t1 = Label(vrelacion, text="Desde")
    t1.pack()
    nv1 = Entry(vrelacion)
    nv1.pack()
    t2 = Label(vrelacion, text="Hasta")
    t2.pack()
    nv2 = Entry(vrelacion)
    nv2.pack()
    relacionar = Button(vrelacion, text="Relacionar", command=lambda: relacion(nv1.get(), nv2.get(), vrelacion))
    relacionar.pack()
    relacionar2 = Button(vrelacion, text="Relacionar desde listas",
                         command=lambda: relacion(opciones1.get(opciones1.curselection()),
                                                  opciones2.get(opciones2.curselection()), vrelacion))
    relacionar2.pack()

def relacion(nv1, nv2, vrelacion):
    if (nv1 == nv2):
        vrelacion.destroy()
        messagebox.showinfo("Denegado", "No puede seleccionar el mismo punto de interes")
    else:

        for v in g.listav:
            if (nv1 == v.nombre):
                a = v
                for v in g.listav:
                    if (nv2 == v.nombre):
                        b = v
                        a.vecino(b)
                        d = distancias(a, b)
                        agregarA(a, b, d, a.x, a.y, b.x, b.y)
                        vrelacion.destroy()
        actualizar()

# Eliminar Vertices
def clickeliminarv():
    veliminar = Toplevel()
    veliminar.title("Eliminar Punto")
    t1 = Label(veliminar, text="Nombre punto de interes")
    t1.pack()
    opciones = Listbox(veliminar, exportselection=0)
    for v in g.listav:
        opciones.insert(END, v.nombre)
    opciones.pack()
    nombrev = Entry(veliminar)
    nombrev.pack()
    eliminar = Button(veliminar, text="Eliminar", command=lambda: eliminarv(nombrev.get(), veliminar))
    eliminar.pack()
    eliminar2 = Button(veliminar, text="Elimina desde listas",
                       command=lambda: eliminarv(opciones.get(opciones.curselection()), veliminar))
    eliminar2.pack()

def eliminarv(nombrev, veliminar):
    try:
        for v in g.listav:
            if (nombrev == v.nombre):
                a = v
            for i in v.la:
                if (nombrev == i.nombre):
                    b = i
                    v.la.remove(b)
        g.listav.remove(a)
        c = 0
        indice = []
        for a in g.listaA:
            if nombrev == a.frm.nombre or nombrev == a.to.nombre:
                c += 1
                indice.append(g.listaA.index(a))
        for i in reversed(indice):  # sorted(indice, reverse=True)
            del g.listaA[i]
        veliminar.destroy()
        actualizar()
    except:
        veliminar.destroy()
        messagebox.showerror("ERROR", "El punto no se encuentra")

# Eliminar Aristas
def clickeliminara():
    veliminara = Toplevel()
    veliminara.title("Eliminar Ruta")
    desde = Listbox(veliminara, exportselection=0)
    hasta = Listbox(veliminara, exportselection=0)
    for v in g.listav:
        desde.insert(END, v.nombre)
        hasta.insert(END, v.nombre)
    desde.pack(side=LEFT)
    hasta.pack(side=LEFT)
    t1 = Label(veliminara, text="Desde")
    t1.pack()
    nv1 = Entry(veliminara)
    nv1.pack()
    t2 = Label(veliminara, text="Hasta")
    t2.pack()
    nv2 = Entry(veliminara)
    nv2.pack()
    eliminar = Button(veliminara, text="Eliminar", command=lambda: eliminara(nv1.get(), nv2.get(), veliminara))
    eliminar.pack()
    eliminar2 = Button(veliminara, text="Eliminar desde listas",
                       command=lambda: eliminara(desde.get(desde.curselection()), hasta.get(hasta.curselection()),
                                                 veliminara))
    eliminar2.pack()

def eliminara(desde, hasta, veliminara):
    try:
        for v in g.listav:
            if (desde == v.nombre):
                a = v
                for i in a.la:
                    if (hasta == i.nombre):
                        b = i
                        a.la.remove(b)
        for ar in g.listaA:
            if (desde == ar.frm.nombre and hasta == ar.to.nombre):
                temp = ar
                g.listaA.remove(temp)
        veliminara.destroy()
        actualizar()
    except:
        print("No elimina ruta")

# Calcular Distancias
def distancias(a, b):
    # for v in g.listav:
    #     for v1 in range(len(v.la)):
    #         distancia = math.sqrt(math.pow(v.la[v1].x-v.x, 2)+math.pow(v.la[v1].y-v.y, 2))
    #         v.ld.insert(v1, round(distancia, 2))
    #         # v.agregarpeso(round(distancia))
    #         print distancia
    #         print v.nombre, v.la[v1].nombre
    distancia = math.sqrt(math.pow(b.x - a.x, 2) + math.pow(b.y - a.y, 2))
    return round(distancia, 2)

    # for v in g.listav:
    #     for i in v.ld:
    #         print v.nombre,"distancia", i

# Dijkstra
def clickdijkstra():
    vdijkstra = Toplevel()
    vdijkstra.title("Rutas Mas Cortas")
    t1 = Label(vdijkstra, text="Nombre del punto")
    t1.pack()
    opciones = Listbox(vdijkstra, exportselection=0)
    for v in g.listav:
        opciones.insert(END, v.nombre)
    opciones.pack()
    eliminar = Button(vdijkstra, text="Calcular Distancia",
                      command=lambda: dijkstra(opciones.get(opciones.curselection()), vdijkstra))
    eliminar.pack()

def dijkstra(inicio, vdijkstra):
    for i in g.listav:
        if inicio == i.nombre:
            indice = i
    listad, listap = g.dijkstra(indice)
    if (len(indice.la) == 0):
        messagebox.showinfo("Dijkstra", "El punto seleccionado no tiene rutas")
    else:
        resaltarcaminos(listap, li, indice)
        vdijkstra.destroy()
        mostrardijkstra = Toplevel()
        mostrardijkstra.title("Distancias")
        t1 = Label(mostrardijkstra, text="Distancia de las rutas desde %s : " % (inicio.upper()), font="Verdana 10 bold")
        t1.pack()
        for i in range(len(g.listav)):
            if (listap[i] != None):
                dista = str(listad[i])
                hastaa = g.listav[i].nombre
                hastaa = hastaa.upper()
                dista = dista[0:6]
                t2 = Label(mostrardijkstra, text=" hasta " + hastaa + " es: " + dista+"m")
                t2.pack()

#Dijkstra con peligrosidad
def clickdijkstrapeligro():
    vdijkstra = Toplevel()
    vdijkstra.title("Rutas Menos Peligrosas")
    t1 = Label(vdijkstra, text="Nombre del punto")
    t1.pack()
    opciones = Listbox(vdijkstra, exportselection=0)
    for v in g.listav:
        opciones.insert(END, v.nombre)
    opciones.pack()
    eliminar = Button(vdijkstra, text="Calcular",
                      command=lambda: dijkstrapeligro(opciones.get(opciones.curselection()), vdijkstra))
    eliminar.pack()

def dijkstrapeligro(inicio, vdijkstra):
    for i in g.listav:
        if inicio == i.nombre:
            indice = i
    listagrados, listaprevios = g.dijkstrapeligro(indice)
    if (len(indice.la) == 0):
        messagebox.showinfo("Rutas menos peligrosas", "El punto seleccionado no tiene rutas")
    else:
        resaltarcaminos(listaprevios, li, indice)
        vdijkstra.destroy()
        mostrardijkstrapeligro = Toplevel()
        mostrardijkstrapeligro.title("Ruta Menos Peligrosa")
        t1 = Label(mostrardijkstrapeligro, text="El promedio de accidentalidad desde %s : " % (inicio.upper()), font="Verdana 10 bold")
        t1.pack()
        prom=listagrados[:]
        prom=promedio(listaprevios,prom,indice,n=1)
        for i in range(len(g.listav)):
            if (listaprevios[i] != None):
                promed = str(listagrados[i]/prom[i])
                prom[i]=promed
                hastaa = g.listav[i].nombre
                hastaa = hastaa.upper()
                promed=promed[0:4]
                t2 = Label(mostrardijkstrapeligro, text=" hasta " + hastaa + " es: " + promed)
                t2.pack()

def promedio(listaprevios,listaprom,inicio,n):
    for i in range(len(g.listav)):
        if listaprevios[i] != None and listaprevios[i].nombre == inicio.nombre:
            listaprom[i]=n
            promedio(listaprevios,listaprom,g.listav[i],n+1)
    return listaprom

#Ruta segun experiencia desde un punto elegido
def clickdijsktraxp():
    num=ancho/2
    for aris in li:
        canvas.delete(aris)
    del li[:]
    dijsktraxp = Toplevel()
    dijsktraxp.title("Ruta segun experiencia")
    t1 = Label(dijsktraxp, text="Nombre del punto")
    t1.pack()
    opciones = Listbox(dijsktraxp, exportselection=0)
    for v in g.listav:
        opciones.insert(END, v.nombre)
    opciones.pack()
    prom=Entry(dijsktraxp)
    prom.pack(side=RIGHT)
    text=Label(dijsktraxp,text="Experiencia")
    text.pack()
    eliminar = Button(dijsktraxp, text="Calcular",
                      command=lambda: dijsktraexpe(opciones.get(opciones.curselection()), prom.get(),dijsktraxp))
    eliminar.pack()

def dijsktraexpe(inicio,promed,dijsktraxp):
    try:
        promed=float(promed)
        if(promed< 0 or promed > 5):
            messagebox.showerror("ERROR","Debe ingresar una experiencia entre 1 y 5")
        else:
            for i in g.listav:
                if inicio == i.nombre:
                    indice = i
            lgrados, lprevios = g.dijkstrapeligro(indice)
            if (len(indice.la) == 0):
                dijsktraxp.destroy()
                messagebox.showinfo("Rutas menos peligrosas", "El punto seleccionado no tiene rutas")
            else:
                dijsktraxp.destroy()
                promlista=lgrados[:]
                promlista=promedio(lprevios,promlista,indice,n=1)
                for vert in range(len(promlista)):
                    if (lprevios[vert] != None):
                        promlista[vert]=lgrados[vert]/promlista[vert]

                i, p=(min(enumerate(promlista), key=lambda x: abs(x[1]-promed)))
                lisrecorrido=[]
                lisrecorrido=rec2(indice,lisrecorrido,lprevios,g.listav[i])
                lisrecorrido=list(reversed(lisrecorrido))
                lisrecorrido.append(g.listav[i])
                dibujaxp(lisrecorrido,li)
    except:
        dijsktraxp.destroy()
        messagebox.showerror("ERROR","No se encontro una ruta")

def dibujaxp(ruta,li):
    num=ancho/2
    for aris in li:
        canvas.delete(aris)
    del li[:]
    for i in range(len(ruta)):
        if(i!=(len(ruta)-1)):
            if (ruta[i].x >= ruta[i+1].x and ruta[i].y > ruta[i+1].y):
                    a = canvas.create_line(ruta[i].x + num, ruta[i].y, ruta[i+1].x + ancho, ruta[i+1].y + num,
                                           width=3, fill="DarkGoldenrod1", arrow="last", smooth=True)
                    li.append(a)
            if (ruta[i].x > ruta[i+1].x and ruta[i].y < ruta[i+1].y):
                a = canvas.create_line(ruta[i].x + num, ruta[i].y + ancho, ruta[i+1].x + ancho,
                                       ruta[i+1].y + num, width=3, fill="DarkGoldenrod1", arrow="last", smooth=True)
                li.append(a)
            if (ruta[i].x <= ruta[i+1].x and ruta[i].y > ruta[i+1].y):
                a = canvas.create_line(ruta[i].x + num, ruta[i].y, ruta[i+1].x, ruta[i+1].y + num, width=3,
                                       fill="DarkGoldenrod1", arrow="last", smooth=True)
                li.append(a)
            if (ruta[i].x < ruta[+1].x and ruta[i].y < ruta[i+1].y):
                a = canvas.create_line(ruta[i].x + num, ruta[i].y + ancho, ruta[i+1].x, ruta[i+1].y + num,
                                       width=3, fill="DarkGoldenrod1", arrow="last", smooth=True)
                li.append(a)
        else:
            if (ruta[i-1].x >= ruta[i].x and ruta[i-1].y > ruta[i].y):
                    a = canvas.create_line(ruta[i-1].x + num, ruta[i-1].y, ruta[i].x + ancho, ruta[i].y + num,
                                           width=3, fill="DarkGoldenrod1", arrow="last", smooth=True)
                    li.append(a)
            if (ruta[i-1].x > ruta[i].x and ruta[i-1].y < ruta[i].y):
                a = canvas.create_line(ruta[i-1].x + num, ruta[i-1].y + ancho, ruta[i].x + ancho,
                                       ruta[i].y + num, width=3, fill="DarkGoldenrod1", arrow="last", smooth=True)
                li.append(a)
            if (ruta[i-1].x <= ruta[i].x and ruta[i-1].y > ruta[i].y):
                a = canvas.create_line(ruta[i-1].x + num, ruta[i-1].y, ruta[i].x, ruta[i].y + num, width=3,
                                       fill="DarkGoldenrod1", arrow="last", smooth=True)
                li.append(a)
            if (ruta[i-1].x < ruta[i].x and ruta[i-1].y < ruta[i].y):
                a = canvas.create_line(ruta[i-1].x + num, ruta[i-1].y + ancho, ruta[i].x, ruta[i].y + num,
                                       width=3, fill="DarkGoldenrod1", arrow="last", smooth=True)
                li.append(a)

#Ruta segun experiencia del mapa
def clickrutaxp():
    vrutaxp = Toplevel()
    vrutaxp.title("Ruta segun experiencia")
    prom=Entry(vrutaxp)
    prom.pack(side=RIGHT)
    text=Label(vrutaxp,text="Experiencia")
    text.pack()
    eliminar = Button(vrutaxp, text="Calcular",
                      command=lambda: rutaxp(prom.get(), vrutaxp))
    eliminar.pack()

def rutaxp(promed,vrutaxp):
    promed=float(promed)
    if(promed< 0 or promed > 5):
        messagebox.showerror("Error","Debe digitar una dificultad de 1 a 5")
        vrutaxp.destroy()
    else:
        vrutaxp.destroy()
        sum = 0
        ldis = []
        lprev = []
        lpromd = []
        lipromd = []
        lrutas = []
        lproms = []
        listica = []
        # Dijkstra para todos los vertices
        for v in g.listav:
            lds, lps = g.dijkstra(v)
            ldis.append(lds)
            lprev.append(lps)

        # Lista de todos los caminos
        for i in range(len(ldis)):
            for k in range(len(ldis[i])):
                ltemp = []
                if (ldis[i][k] == 0 or ldis[i][k] == sys.maxsize):
                    continue
                else:
                    ltemp.append(g.listav[k])
                    ltemp.append(lprev[i][k])
                    ltemp = listaprev(lprev[i][k], lprev[i], ltemp)
                    lrutas.append(ltemp)

        # Calcula promedio de rutas
        for l in range(len(lrutas)):
            for m in range(len(lrutas[l])):
                sum += lrutas[l][m].gaccidente
            lproms.append(round(sum/len(lrutas[l]), 2))
            sum = 0
        smin = min(lproms, key=lambda s:abs(s-promed))
        indices = lproms.index(smin)
        hmc = Thread(target=mostrarcamino, args=(list(reversed(lrutas[indices])), li))
        hmc.start()

def rec2(inicio,recorrer,listaprevios,final):
    for i in range(len(g.listav)):
        if listaprevios[i] != None and g.listav[i] == final:
            recorrer.append(listaprevios[i])
            rec2(inicio,recorrer,listaprevios,listaprevios[i])
    return recorrer

# Resaltar Caminos del Dijkstra
def resaltarcaminos(listap, li, inicio):
    for aris in li:
        canvas.delete(aris)
    del li[:]
    h1 = Thread(target=resaltar, args=(listap, li, inicio))
    h1.start()

def resaltar(listap, li, inicio):
    num = ancho / 2
    for i in range(len(g.listav)):
        if listap[i] != None and listap[i].nombre == inicio.nombre:
            time.sleep(0.5)
            if (listap[i].x >= g.listav[i].x and listap[i].y > g.listav[i].y):
                a = canvas.create_line(listap[i].x + num, listap[i].y, g.listav[i].x + ancho, g.listav[i].y + num,
                                       width=3, fill="DarkGoldenrod1", arrow="last", smooth=True)
                li.append(a)
            if (listap[i].x > g.listav[i].x and listap[i].y < g.listav[i].y):
                a = canvas.create_line(listap[i].x + num, listap[i].y + ancho, g.listav[i].x + ancho,
                                       g.listav[i].y + num, width=3, fill="DarkGoldenrod1", arrow="last", smooth=True)
                li.append(a)
            if (listap[i].x <= g.listav[i].x and listap[i].y > g.listav[i].y):
                a = canvas.create_line(listap[i].x + num, listap[i].y, g.listav[i].x, g.listav[i].y + num, width=3,
                                       fill="DarkGoldenrod1", arrow="last", smooth=True)
                li.append(a)
            if (listap[i].x < g.listav[i].x and listap[i].y < g.listav[i].y):
                a = canvas.create_line(listap[i].x + num, listap[i].y + ancho, g.listav[i].x, g.listav[i].y + num,
                                       width=3, fill="DarkGoldenrod1", arrow="last", smooth=True)
                li.append(a)
            resaltar(listap, li, g.listav[i])

# Camino
def clickcamino():
    vcamino = Toplevel()
    vcamino.title("Mostrar Ruta")
    desde = Listbox(vcamino, exportselection=0)
    hasta = Listbox(vcamino, exportselection=0)
    for v in g.listav:
        desde.insert(END, v.nombre)
        hasta.insert(END, v.nombre)
    desde.grid(row=1, column=0)
    hasta.grid(row=1, column=1)
    t1 = Label(vcamino, text="Desde")
    t1.grid(row=0, column=0)
    t2 = Label(vcamino, text="Hasta")
    t2.grid(row=0, column=1)
    caminob = Button(vcamino, text="Camino",
                     command=lambda: camino(desde.get(desde.curselection()), hasta.get(hasta.curselection()), vcamino))
    caminob.grid(row=1, column=2)

def camino(desde, hasta, vcamino):
    try:
        for v in g.listav:
            if desde == v.nombre:
                ld, lp = g.dijkstra(v)
        lc = []
        for i in range(len(g.listav)):
            if lp[i] != None:
                if hasta == g.listav[i].nombre:
                    lc.append(g.listav[i])
                    lc.append(lp[i])
                    lc = rec(lp[i], lc, lp)
       # lp[i].x, lp[i].y, g.listav[i].x, g.listav[i].y
        vcamino.destroy()
        mostrarcamino(list(reversed(lc)), li)
        hmc = Thread(target=mostrarcamino, args=(list(reversed(lc)), li))
        hmc.start()
        hm = Thread(target=movimiento, args=(list(reversed(lc)), bola))
        hm.start()
    except:
        messagebox.showerror("ERROR","Camino no encontrado")

def rec(vdestino, lc, lp):
    for i in range(len(g.listav)):
        if vdestino == g.listav[i]:
            if lp[i] != None:
                lc.append(lp[i])
                rec(lp[i], lc, lp)
    return lc

def mostrarcamino(lc, li):
    num = ancho / 2
    for aris in li:
        canvas.delete(aris)
    del li[:]
    for i, j in zip(lc, lc[1:]):
        time.sleep(0.5)
        if i.x >= j.x and i.y > j.y:
            a = canvas.create_line(i.x + num, i.y, j.x + ancho, j.y + num, width=3, fill="DarkGoldenrod1", arrow="last",
                                   smooth=True)
            li.append(a)
        if (i.x > j.x and i.y < j.y):
            a = canvas.create_line(i.x + num, i.y + ancho, j.x + ancho, j.y + num, width=3, fill="DarkGoldenrod1",
                                   arrow="last", smooth=True)
            li.append(a)
        if (i.x <= j.x and i.y > j.y):
            a = canvas.create_line(i.x + num, i.y, j.x, j.y + num, width=3, fill="DarkGoldenrod1", arrow="last",
                                   smooth=True)
            li.append(a)
        if (i.x < j.x and i.y < j.y):
            a = canvas.create_line(i.x + num, i.y + ancho, j.x, j.y + num, width=3, fill="DarkGoldenrod1", arrow="last",
                                   smooth=True)
            li.append(a)

def movimiento(lc, bola):
    if(len(lc)!=0):
        num = ancho / 2
        canvas.delete("obj")
        canvas.create_image(lc[0].x + num, lc[0].y + num, image=bola, tag="obj")
        # m = round((lc[1].y-lc[0].y)/(lc[1].x-lc[0].x),4)|
        aumento = 2
        tiempo=0.05

        for i, j in zip(lc, lc[1:]):
            cords = canvas.coords("obj")
            h1 = Thread(target=muestra, args=(cords[0],cords[1],lc))
            h1.start()
            time.sleep(tiempo)
            if i.x >= j.x and i.y > j.y:
                m = (j.y - i.y) / (j.x - i.x)
                for x in range(i.x, j.x, -aumento):
                    pos = canvas.coords("obj")
                    if pos[0] > j.x+num:
                        canvas.move("obj", -aumento, -aumento * m)
                        canvas.update()
                        time.sleep(tiempo)
                    else:
                        break
            if i.x > j.x and i.y < j.y:
                m = (j.y - i.y) / (j.x - i.x)
                for x in range(i.x, j.x, -aumento):
                    pos = canvas.coords("obj")
                    if pos[0] > j.x+num:
                        canvas.move("obj", -aumento, -aumento * m)
                        canvas.update()
                        time.sleep(tiempo)
                    else:
                        break
            if i.x <= j.x and i.y > j.y:
                m = (j.y - i.y) / (j.x - i.x)
                for x in range(i.x, j.x, aumento):
                    pos = canvas.coords("obj")
                    if pos[0] < j.x+num:
                        canvas.move("obj", aumento, aumento * m)
                        canvas.update()
                        time.sleep(tiempo)
                    else:
                        break
            if i.x < j.x and i.y < j.y:
                m = (j.y - i.y) / (j.x - i.x)
                for x in range(i.x, j.x, aumento):
                    pos = canvas.coords("obj")
                    if pos[0] < j.x+num:
                        canvas.move("obj", aumento, aumento * m)
                        canvas.update()
                        time.sleep(tiempo)
                    else:
                        break
    else:
        messagebox.showerror("ERROR","No se puede calcular la ruta")

def muestra(x,y,lc):
    for vert in g.listav:
        if x > vert.x-15 and x < vert.x+15+ancho and y > vert.y-15 and y < vert.y +15+ ancho:
            info = Toplevel()
            l1 = Label(info, text="Nombre:").grid(row=0, column=0)
            l2 = Label(info, text=vert.nombre).grid(row=0, column=1)
            l3 = Label(info, text="Descripcion:").grid(row=1, column=0)
            l4 = Label(info, text=vert.descripcion).grid(row=1, column=1)
            l5 = Label(info, text="Grado accidentalidad:").grid(row=2, column=0)
            l6 = Label(info, text=str(vert.gaccidente)).grid(row=2, column=1)
            time.sleep(5)
            info.destroy()
        if vert==lc[-2]:
            ultimo = Toplevel()
            l1 = Label(ultimo, text="Nombre:").grid(row=0, column=0)
            l2 = Label(ultimo, text=lc[-1].nombre).grid(row=0, column=1)
            l3 = Label(ultimo, text="Descripcion:").grid(row=1, column=0)
            l4 = Label(ultimo, text=lc[-1].descripcion).grid(row=1, column=1)
            l5 = Label(ultimo, text="Grado accidentalidad:").grid(row=2, column=0)
            l6 = Label(ultimo, text=str(lc[-1].gaccidente)).grid(row=2, column=1)
            time.sleep(5)
            ultimo.destroy()

# Ruta con distancia
def clickdistancia():
    vdist = Toplevel()
    vdist.title("Sugerir Ruta")
    t1 = Label(vdist, text="Distancia \n dispuesto a recorrer")
    t1.grid(row=0, column=0)
    d = Entry(vdist)
    d.grid(row=0, column=1)
    t2 = Label(vdist, text="Promedio \n seguridad")
    t2.grid(row=1, column=0)
    s = Entry(vdist)
    s.grid(row=1, column=1)
    boton = Button(vdist,text="Calcular", command= lambda: rutadistancia(d.get(), s.get(), vdist))
    boton.grid(row=2, columnspan=2)

def rutadistancia(dist, prom, vdist):
    try:
        dist=float(dist)
        prom=float(prom)
        if prom < 0 or prom > 5:
            messagebox.showerror("Error", "Debe digitar un promedio de 1 a 5")
            vdist.destroy()
        else:
            vdist.destroy()
            sum = 0
            ldis = []
            lprev = []
            lpromd = []
            lipromd = []
            lrutas = []
            lproms = []
            listica = []
            for v in g.listav:
                lds, lps = g.dijkstra(v)
                ldis.append(lds)
                lprev.append(lps)
            for i in range(len(ldis)):
                lpromd.append(min(ldis[i], key=lambda x:abs(x-dist)))
                lipromd.append(min(enumerate(ldis[i]), key=lambda x: abs(x[1]-dist)))
            for j in range(len(lpromd)):
                ltemp = []
                p, d = lipromd[j]
                ltemp.append(g.listav[p])
                ltemp.append(lprev[j][p])
                ltemp = listaprev(lprev[j][p], lprev[j], ltemp)
                lrutas.append(ltemp)
            for l in range(len(lrutas)):
                for v in lrutas[l]:
                    sum += v.gaccidente
                lproms.append(round(sum/len(lrutas[l]), 2))
                sum = 0
            smin = min(lproms, key=lambda s:abs(s-prom))
            indices = lproms.index(smin)
            pos, dis = lipromd[indices]
            listica.append(g.listav[pos])
            listica.append(lprev[indices][pos])
            listica = listaprev(lprev[indices][pos], lprev[indices], listica)
            # // Solo con distancias
            # nummin = min(lpromd, key=lambda x:abs(x-dist))
            # indice = lpromd.index(nummin)
            # pos, dis = lipromd[indice]
            # listica.append(g.listav[pos])
            # listica.append(lprev[indice][pos])
            # listica = listaprev(lprev[indice][pos], lprev[indice], listica)
            # //
            hmc = Thread(target=mostrarcamino, args=(list(reversed(listica)), li))
            hmc.start()
    except ValueError:
        vdist.destroy()
        messagebox.showerror("ERROR","Ingrese datos correctos")
    except:
        messagebox.showerror("ERROR","No se encontro la ruta")

def listaprev(previo, listap, listica):
    for i in range(len(g.listav)):
        if g.listav[i] == previo:
            if listap[i] != None:
                listica.append(listap[i])
                listaprev(listap[i], listap, listica)
    return listica

# Cargar Mapa
def cargarmapa():
    try:
        del g.listav[:]
        del g.listaA[:]
        file = askopenfile(title="Abrir mapa", filetypes=[("Archivo de texto", "*.txt")])
        ftemp = []
        for linea in file.readlines():
            informacion = linea.split()
            if informacion[0].isalpha():
                vtemp = vertice(informacion[0], int(informacion[1]), int(informacion[2]), informacion[3],
                                float(informacion[4]))
                g.agregarVertice(vtemp)
                actualizar()
            if (informacion[0].isalnum() == False):
                ftemp.append(informacion)

        cargarrelaciones(ftemp)
        # file.close()
    except:
        messagebox.showerror("No se cargo el mapa", "No se pudo cargar el mapa")

def cargarrelaciones(ftemp):
    for informacion in ftemp:
        temp = informacion[0].split("|")
        # print temp[1], informacion[1]
        relacion(str(temp[1]), str(informacion[1]), Toplevel(Ventana))

# Guardar Mapa
def guardarmapa():
    try:
        global filename
        filename = "mp.txt"
        archivo = asksaveasfile(mode="w", title="Guardar mapa", defaultextension=".txt",
                                filetypes=[("Archivo de texto", "*.txt")])
        # archivo=open(filename, "w")
        for i in g.listav:
            archivo.writelines(
                i.nombre + " " + str(i.x) + " " + str(i.y) + " " + i.descripcion + " " + str(i.gaccidente) + "\n")
            for w in i.la:
                archivo.writelines("|" + i.nombre + " " + w.nombre + " " + str(w.x) + " " + str(w.y) + "\n")
        archivo.close()
    except:
        messagebox.showerror("No se guardo", "No se pudo guardar el mapa")

def mostrarprofundidad():
    l = []
    l = g.profundidad(g.listav[0], l)
    for vert in l:
        print(vert.nombre)

menubar = Menu(Ventana)

menubar.add_command(label="Relacionar", command=clickrelacion)
menubar.add_separator()
menubar.add_command(label="Eliminar Punto", command=clickeliminarv)
menubar.add_separator()
menubar.add_command(label="Eliminar Camino", command=clickeliminara)
menubar.add_separator()
menubar.add_command(label="Rutas Mas Cortas", command=clickdijkstra)
menubar.add_separator()
menubar.add_command(label="Rutas Menos Peligrosas", command=clickdijkstrapeligro)
menubar.add_separator()
menubar.add_command(label="Mostrar Ruta", command=clickcamino)
menubar.add_separator()
menubar.add_command(label="Sugerir Ruta", command=clickdistancia)
menubar.add_separator()
menubar.add_command(label="Sugerir Ruta Exp desde un Punto", command=clickdijsktraxp)
menubar.add_separator()
menubar.add_command(label="Sugerir Ruta Exp", command=clickrutaxp)
menubar.add_separator()
menubar.add_command(label="Cargar Mapa", command=cargarmapa)
menubar.add_separator()
menubar.add_command(label="Guardar Mapa", command=guardarmapa)
menubar.add_separator()

Ventana.config(menu=menubar)
canvas.bind("<Double-1>", dobleclick)
canvas.bind("<Button-1>", click)

def actualizar():
    num = ancho / 2
    canvas.delete("all")
    for i in range(len(g.listav)):
        canvas.create_oval(g.listav[i].x, g.listav[i].y, g.listav[i].x + ancho, g.listav[i].y + ancho, fill="#F24C27", width=0)
        canvas.create_oval(g.listav[i].x+5, g.listav[i].y+5, g.listav[i].x + ancho-5, g.listav[i].y + ancho-5, fill="#F24C27", activefill="#024959", width=0)

    for i in range(len(g.listaA)):

        if g.listaA[i].x1 >= g.listaA[i].x2 and g.listaA[i].y1 > g.listaA[i].y2:
            canvas.create_line(g.listaA[i].x1 + num, g.listaA[i].y1, g.listaA[i].x2 + ancho, g.listaA[i].y2 + num,
                               width=3, fill="white", arrow="last", smooth=True)
        if g.listaA[i].x1 > g.listaA[i].x2 and g.listaA[i].y1 < g.listaA[i].y2:
            canvas.create_line(g.listaA[i].x1 + num, g.listaA[i].y1 + ancho, g.listaA[i].x2 + ancho,
                               g.listaA[i].y2 + num, width=3, fill="white", arrow="last", smooth=True)
        if g.listaA[i].x1 <= g.listaA[i].x2 and g.listaA[i].y1 > g.listaA[i].y2:
            canvas.create_line(g.listaA[i].x1 + num, g.listaA[i].y1, g.listaA[i].x2, g.listaA[i].y2 + num, width=3,
                               fill="white", arrow="last", smooth=True)
        if g.listaA[i].x1 < g.listaA[i].x2 and g.listaA[i].y1 < g.listaA[i].y2:
            canvas.create_line(g.listaA[i].x1 + num, g.listaA[i].y1 + ancho, g.listaA[i].x2, g.listaA[i].y2 + num,
                               width=3, fill="white", arrow="last", smooth=True)

    for i in range(len(g.listaA)):

        if g.listaA[i].x1 >= g.listaA[i].x2 and g.listaA[i].y1 > g.listaA[i].y2:
            tx1 = ((g.listaA[i].x1 + num) + (g.listaA[i].x2 + ancho)) / 2
            ty1 = (g.listaA[i].y1 + (g.listaA[i].y2 - num)) / 2
            canvas.create_text(tx1, ty1 + num, text=str(g.listaA[i].distancia) + "m")
        if g.listaA[i].x1 > g.listaA[i].x2 and g.listaA[i].y1 < g.listaA[i].y2:
            tx1 = ((g.listaA[i].x1 + num) + (g.listaA[i].x2 + ancho)) / 2
            ty1 = ((g.listaA[i].y1 - ancho) + (g.listaA[i].y2 + num)) / 2
            canvas.create_text(tx1, ty1 + ancho, text=str(g.listaA[i].distancia) + "m")
        if g.listaA[i].x1 <= g.listaA[i].x2 and g.listaA[i].y1 > g.listaA[i].y2:
            tx1 = ((g.listaA[i].x1 + num) + g.listaA[i].x2) / 2
            ty1 = (g.listaA[i].y1 + (g.listaA[i].y2 - num)) / 2
            canvas.create_text(tx1, ty1 + num, text=str(g.listaA[i].distancia) + "m")
        if g.listaA[i].x1 < g.listaA[i].x2 and g.listaA[i].y1 < g.listaA[i].y2:
            tx1 = (g.listaA[i].x1 + (num + g.listaA[i].x2)) / 2
            ty1 = ((g.listaA[i].y1 - ancho) + (g.listaA[i].y2 + num)) / 2
            canvas.create_text(tx1, ty1 + ancho, text=str(g.listaA[i].distancia) + "m")

    for i in range(len(g.listav)):
        nombre = str(g.listav[i].nombre)
        if len(nombre) > 5:
            nombre = nombre[0:4] + ".."
        canvas.create_text(g.listav[i].x + num, g.listav[i].y + num, text=nombre, fill="white", font="bold")

Ventana.mainloop()
