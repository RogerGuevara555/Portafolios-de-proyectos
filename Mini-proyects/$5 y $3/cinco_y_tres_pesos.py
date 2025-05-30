# Mi versión

def pay(amount : int, money_list : list = []) -> list:
    # Pagar cualquier cantidad de dinero mayor que $7 con billetes de cinco y tres pesos. 
    
    if amount == 0:
        money_list.sort(reverse= True)
        return money_list
    elif amount < 8 and amount != 3 and amount != 5 and amount != 6:
        return 'ERROR'
    
    billete = [5, 3]    
    for i in billete:
        if amount % i == 0: 
            return pay(amount - i, money_list + [i])
    else:
        return pay(amount - 3, money_list + [3])
        
def all_payment_combinations(bills : list, initiated = False) -> list: 
    # Retorna una lista con todas las posibles formas de pago en listas
    
    if not initiated:
        while bills.count(5) >= 3:
            for _ in range(3): bills.remove(5)
            for _ in range(5): bills.append(3)
        return all_payment_combinations(bills, True)
    
    else:
        combinations = [bills.copy()]
        while bills.count(3) >= 5:
            for _ in range(5): bills.remove(3)
            for _ in range(3): bills.append(5)
            bills.sort(reverse=True)
            combinations.append(bills.copy())
        return combinations

def mostrar(paga):
    cincos = paga.count(5)
    tres = paga.count(3)
    print(f'{sum(paga)}: -----> {cincos} veces 5 + {tres} veces 3 = {5*cincos + 3*tres}')

def mostrar_todas(pay, monto):
    formas_de_pago = all_payment_combinations(pay(monto, []))
    for i in formas_de_pago:
        mostrar(i)

#print(sum([5,3]))
#print(pay(19))

#for i in range(8, 100):
#    mostrar(pay(i, []))

#monto = [5, 5, 5, 5, 5, 5, 5, 3, 3, 3]
#all_payment_combinations(monto)

if __name__ == "__main__":
    monto = 99
    mostrar_todas(pay, monto)