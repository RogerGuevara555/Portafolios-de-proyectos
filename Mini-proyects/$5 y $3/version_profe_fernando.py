# Versión de mi profesor de programación
 
from cinco_y_tres_pesos import mostrar_todas

def pagar(n, l):
    if (n == 0):
        return(l)
    if (n < 0):
        return (l + [-1])
    nuevalista = pagar(n - 5, l + [5])
    if (nuevalista[-1] != -1):
        return (nuevalista)
    else:
        nuevalista = pagar(n - 3, l + [3])
        if (nuevalista[-1] != -1):
            return (nuevalista)
        else:
            return (l + [-1])

mostrar_todas(pagar, 84) # Esto de acá lo hice yo