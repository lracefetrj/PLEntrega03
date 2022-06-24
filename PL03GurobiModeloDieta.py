import gurobipy as gp

from gurobipy import GRB


#def solucionar(persona, categorias, qtdMinNutrientes, qtdMaxNutrientes, indicadores, indValor, alimentos, carboidratos, nutrientes):
def solucionar(persona, categorias, qtdMinNutrientes, qtdMaxNutrientes, alimentos, carboidratos, nutrientes):
   
    # Modelo
    m = gp.Model("dieta")

    # Criar a variável de decisão
    porcao = m.addVars(alimentos, vtype=GRB.INTEGER, name="P")
  
    # Definir a função objetivo
    m.setObjective(porcao.prod(carboidratos), GRB.MINIMIZE)

    # Restrições sobre nutrientes
    m.addConstrs((gp.quicksum(nutrientes[a, c] * porcao[a] for a in alimentos) ==
                 [qtdMinNutrientes[c], qtdMaxNutrientes[c]] for c in categorias))

    #for a in alimentos:
    #    for i in indicadores:
    #        m.addConstr( (nutrientes[a, i] * porcao[a] <= indValor[i] * porcao[a]),  name="ind[%d,%s]" % (a, i))
   
    #Incluir restrição da porção
    m.addConstr(porcao.sum() <= 20)
    
    for a in alimentos:
        m.addConstr( porcao[a] == [0, 3])

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
    m.write('data/Model400-' + persona + '.lp')
    