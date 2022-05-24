import sys
import os
import xlrd
import PL03GurobiModeloDieta as pgmd

arquivo = xlrd.open_workbook(os.path.join("", "data", "alimentos-172.xls"))

nrp = str(sys.argv[1])

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
        i = i + 1
    except IndexError:
        break

sh = arquivo.sheet_by_name("Alimentos")
alimentos = []
carboidratos = {}
i = 1
while True:
    try:
        f = int(sh.cell_value(i, 0))
        alimentos.append(f)
        carboidratos[f] = float(sh.cell_value(i, 1))
        i = i + 1
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
    i += 1

pgmd.solucionar(persona, categorias, qtdMinima, qtdMaxima, alimentos, carboidratos, nutrientes)
