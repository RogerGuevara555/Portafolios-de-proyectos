# x^2 + 4x + 7
pol_1 = [1, 4, 7]
# 4x^3 + 9x^2 + 5x +3
pol_2 = [4, 9, 5, 3]


def agregar_ceros(a : list ,b : list):
    ac, bc = a.copy(), b.copy()
    ceros_a_agregar = int(len(a) - len(b))
    
    if ceros_a_agregar >= 0: ind = 2
    if ceros_a_agregar < 0: ind = 1
    menor = {
        1 : ac,
        2 : bc
    }.get(ind)
    
    for i in range(abs(ceros_a_agregar)):
        menor.insert(0, 0)
        
    return ac, bc

def suma_de_polinomios(a : list ,b : list):
    a, b = agregar_ceros(a,b)
    pol_3 =[]
    
    for i in range(len(a)):
        pol_3.append( a[i] + b[i] )
        
    return pol_3

def producto_de_polinomios(a : list ,b : list):
    pol_3 = []
    contador = 0
    contador2 = 0
    
    for i in a:
        termino_de_b = 0
        for j in b:
            monomio = i * j  
            
            if contador == 0: pol_3.append(monomio)
            elif j == b[-1]: pol_3.append(monomio)
            else: pol_3[termino_de_b + contador2 + 1] += monomio
                
            termino_de_b += 1
            
        contador += 1
        if contador >= 2: contador2 += 1
    
    return pol_3     
    
def imprimir_polinomio(pol):
    grado = len(pol)
    contador = -1
    repre = ''
    
    while (-1*contador <= grado):
    
        factor = pol[contador]
        if factor != 0:
            if factor > 0: signo = f' + '
            else:           signo = f' - '
            
            if (factor == 1 or factor == -1) and contador != -1: numero = ''
            elif factor >= 0:                                    numero = f'{factor}'
            else:                                                numero = f'{-1*factor}'
            
            if contador == -1:   variable = ''
            elif contador == -2: variable = 'x'
            else:                variable = f'x^{-1*contador - 1}'
        
            repre = signo + numero + variable + repre
            
        contador -= 1
        
    return repre[2:]
    
pol_4 = [4, 2, 5]

print(imprimir_polinomio(pol_4))

#print(imprimir_polinomio(suma_de_polinomios(pol_1, pol_2)))
    
