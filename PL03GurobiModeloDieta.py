import gurobipy as gp

from gurobipy import GRB


def solucionar(persona, categorias, qtdMinNutrientes, qtdMaxNutrientes, alimentos, carboidratos, nutrientes):
   
    # Modelo
    m = gp.Model("dieta")

    # Criar a variável de decisão
    porcao = m.addVars(alimentos, vtype=GRB.INTEGER, name="P")

    # Definir a função objetivo
    m.setObjective(porcao.prod(carboidratos), GRB.MINIMIZE)

    # Restrições sobre nutrientes
    m.addConstrs((gp.quicksum(nutrientes[f, c] * porcao[f] for f in alimentos) ==
                 [qtdMinNutrientes[c], qtdMaxNutrientes[c]] for c in categorias))

    # Incluir restrição da porção
    m.addConstr(porcao.sum() <= 15)
    
    for f in alimentos:
        m.addConstr( porcao[f] == [0, 2])

    def imprimirSolucao():
        if m.status == GRB.OPTIMAL:

            print('\nCarboidratos: %g' % m.ObjVal)
            print('\nPorção  \ID')
            
            qtdNutrientes = {}
            for i in alimentos:
                if porcao[i].X > 0.0001:
                    print('%g \t\t %g' % (porcao[i].X, i))
                    for c in categorias:
                        if c in qtdNutrientes:
                            qtdNutrientes[c] += (porcao[i].X * nutrientes[i, c])
                        else:
                            qtdNutrientes[c] = (porcao[i].X * nutrientes[i, c])
            
            print('\n')
        
            print('\nNutriente  \tQuantidade')
            for c in categorias:
                print('%s \t %g' % (c, qtdNutrientes[c]))

        else:
            print('Infactível')

    # Solucionar o modelo
    m.optimize()

    # Imprime a solução
    imprimirSolucao()

    # Exportar o modelo
    m.write('data/Model' + persona + '.lp')
    