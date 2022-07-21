#!/usr/bin/env python3.7

import sys
import os
import xlrd
import PL03GurobiModeloDieta as Pgmd

nma = "Alimentos-400-SL.xls"
nrp = "4" #str(sys.argv[1])

arquivo = xlrd.open_workbook(os.path.join("", "data", nma))

persona = "Persona" + nrp

sh = arquivo.sheet_by_name(persona)
categorias = []
qtdMinima = {}
qtdMaxima = {}
i = 1
while True:
    try:
        c = sh.cell_value(i, 0)
        categorias.append(c)
        qtdMinima[c] = float(sh.cell_value(i, 1))
        qtdMaxima[c] = float(sh.cell_value(i, 2))
        i += 1
    except IndexError:
        break

#indicadores = []
#indValor = {}
#i = 1
#while True:
#    try:
#        ind = sh.cell_value(i, 4)
#        if ind:
#            indicadores.append(ind)
#            indValor[ind] = int(sh.cell_value(i, 5))
#        i += 1
#    except IndexError:
#        break

sh = arquivo.sheet_by_name("Alimentos")
alimentos = []
carboidratos = {}
i = 1
while True:
    try:
        f = int(sh.cell_value(i, 0))
        alimentos.append(f)
        carboidratos[f] = float(sh.cell_value(i, 1))
        i += 1
    except IndexError:
        break

sh = arquivo.sheet_by_name("Nutrientes")
nutrientes = {}
i = 1
for alimento in alimentos:
    j = 1
    for categoria in categorias:
        nutrientes[alimento, categoria] = float(sh.cell_value(i, j))
        j += 1

    #for indicador in indicadores:
    #    nutrientes[alimento, indicador] = int(sh.cell_value(i, j))
    #    j += 1

    i += 1

#Pgmd.solucionar(persona, categorias, qtdMinima, qtdMaxima, indicadores, indValor, alimentos, carboidratos, nutrientes)
Pgmd.solucionar(persona, categorias, qtdMinima, qtdMaxima, alimentos, carboidratos, nutrientes)
