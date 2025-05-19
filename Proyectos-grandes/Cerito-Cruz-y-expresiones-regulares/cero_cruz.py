import os
import random
from abc import ABC, abstractmethod
#from regular_expresions import re_new


# region FUNCIONES PARA EL JUEGO: #
class ToolsTable():
    
    def print_tablero(self, lista : list, position = None) -> bool:
        #  Esta función se encarga de imprimir y actualizar el tablero con los valores de los símbolos de cada casilla
        # o de verificar si la posición que se le pase está ocupada o no para evitar (en otra parte del código) que los
        # jugadores editen casillas ocupadas durante el juego
        
        condition = position or position == 0 #Porque 0 cuenta como "None"
        if condition:
            if lista[position] == ' ':
                return False
            else:
                return True
    
        else: 
            self.sustitution(lista)
            a,b,c,d,e,f,g,h,i = lista
            print(f'''
             |     |
          {a}  |  {b}  |  {c}
        _____|_____|_____  
             |     |
          {d}  |  {e}  |  {f} 
        _____|_____|_____ 
             |     |
          {g}  |  {h}  |  {i}
             |     |
            ''')
           
    def sustitution(self, lista : list):
        #  Esta función sustituye los números por sus respectuvos símbolos para imprimirlos correctamente dentro de la tabla 
        # en la consola
        
        dopp = {
            0 : ' ',
            1 : 'X',
            -1 : 'O',
            2 : 'O'
        }
        
        for i in range(len(lista)):
            if lista[i] in dopp.keys():
                lista[i] = dopp.get(lista[i])
    
    def recharge(self, lista : list, ocupado= 0, no_enter= False):      
        #  Esta función se encarga de recargar la consola de forma limpia y de recibir la jugada de el/los jugador(es) o no 
        # segun sea conveniente, ya que en algunos casos como las victorias y empates, ya no es necesaria ninguna entrada.
        
        if ocupado == 0:
            os.system('cls')
            
            start_text = '''
                Para jugar usa los numeros de la derecha del teclado como las posiciones del tablero. 
                Si no funciona, asegurate de tener desactivado el boton Num Lock presionándolo.
            '''
            print(start_text)
            
            #print(lista)
            self.print_tablero(lista)
            
        if not no_enter:    # con entrada
            if ocupado == 1:    
                print('Casilla ocupada')
            t = input()
            return t


class VictorySearcher(ABC):
    @abstractmethod
    def win_search(self, lista : list) -> bool:
        pass


class PreVictorySearcher(ABC):
    @abstractmethod
    def possible_victorys(self, lista : list, pc_sign : str):
        pass


class Separater():
    def l_separate(self, lista1 : list) -> list:
        # Sirve para poner un tope identificable al final de cada fila de la lista de posiciones del tablero
        # Retorna una copia de la lista con las condiciones indicadas
        lista = lista1.copy()
        lista.insert(3, 'l')
        lista.insert(7, 'l')
        lista.insert(11, 'l')
        return lista


'''class VictorySearchByRE(VictorySearcher, Separater):
    
    def win_search(self, lista : list) -> bool:
        lista1 = self.l_separate(lista)
        
        for k in range(len(lista1)):
            lista1[k] = str(lista1[k])

        lista1 = ''.join(lista1)
            
        for i in [
            'X&·2X&·2X',
            'X&·3X&·3X',
            'X&·4X&·4X',
            'X·3',
            'O&·2O&·2O',
            'O&·3O&·3O',
            'O&·4O&·4O',
            'O·3'
        ]:
            if re_new.search_in(lista1, i)[0]:
                return True
        return False
'''


class OptimeVictorySearch(VictorySearcher, Separater):
    
    def win_search(self, lista : list) -> bool:
        # Esta función detecta vicorias de forma más óptima para terminar los partidos
        
        list_join = self.l_separate(lista)
        suma = [5, 4, 3, 1]
        signs = ['X', 'O']
        for i in range(9):
            for line in suma:
                for sign_scale in range(len(signs)):
                    try:
                        posibles_victorias : bool = (
                            list_join[i] == signs[sign_scale] and 
                            list_join[i+line] == signs[sign_scale] and 
                            list_join[i+2*line] == signs[sign_scale]
                        )
                    except:
                        continue
                    if posibles_victorias:
                        print(line)
                        return True
        print(False)
        return False                


class PreVictorySearcher_1(PreVictorySearcher, Separater):
    
    def possible_victorys(self, lista : list, pc_sign : str):
        # Esta función detecta las posibles vicorias para que la PC no las pase por alto y las juegue
        '''0 | 1 | 2 | L
           3 | 4 | 5 | L
           6 | 7 | 8 | L'''
        '''0 | 1 | 2 | 3L
           4 | 5 | 6 | 7L
           8 | 9 | 10 | 11L'''
        
        list_join = self.l_separate(lista)
        suma = [5, 4, 3, 1]
        signs1 = [' ', pc_sign, pc_sign]
        signs2 = [pc_sign, ' ', pc_sign]
        signs3 = [pc_sign, pc_sign, ' ']
        for i in range(9):
            for line in suma:
                for sign_scale in range(len(signs1)):
                    try:
                        posibles_victorias : bool = (
                            list_join[i] == signs1[sign_scale] and 
                            list_join[i+line] == signs2[sign_scale] and 
                            list_join[i+2*line] == signs3[sign_scale]
                        )
                    except:
                        continue
                    if posibles_victorias:
                        if line != 1: line -= 1
                        if i > 3 and i < 7: i -= 1
                        elif i > 7: i -= 2
                        #print(i, sign_scale, line)
                        return i, sign_scale, line
        ''' 
        i, sign_scale, line = possible_victorys(lista, pc_sign):
        if line:
            lista[i+sign_scale*line] = pc_sign     # Usar esta cláusula después para hacer la jugada de la PC.
        else:
            pass
        '''
        return False, False, False


class ToolsSearch():
    def __init__(self, table, w_s):
        self.table : ToolsTable = table
        self.w_s : VictorySearcher = w_s

    def drow_search(self, lista : list) -> bool:
        for i in range(len(lista)):
            if not self.table.print_tablero(lista, i):
                return False
        return True  

    def search_final(self, lista : list, player : int) -> bool:
        #  Esta función se encarga de verificar el final del juego, buscando victorias o empates
        
        if self.w_s.win_search(lista):
            if player == -1: player = 2     #(player == -1 and start == 1) or (player == 1 and start == -1)
            self.table.recharge(lista, 0, True)
            print(f'HA GANADO EL JUGADOR {player}!!!')
            return True
                
        elif self.drow_search(lista):
            self.table.recharge(lista, 0, True)
            print('EMPATE!!!')
            return True  
# endregion-----------------------#


# region DIFICULTADES DEL JUEGO # 
class Dificult(ABC):
    @abstractmethod
    def pc_played(self, player, start, lista : list):
        pass


class RandomePlayed():
    
    def randome_played(self, player, start, lista : list):
        #  Esta función cuenta como la jugada de la PC, de forma aleatoria ya que es el modo facil. 
        # Funciona creando una lista con todas las posiciones vacias del tablero y seleccionando una al azar.
        
        list_void = lista.copy() 
        for i in range(len(list_void.copy())):
            if list_void[i] == ' ':
                list_void[i] = i
            else:
                list_void[i] = None
        list_void = list(filter(lambda x : x != None, list_void))
        
        t = random.choice(list_void)
        lista[t] = player * start


class Dificult1(Dificult, RandomePlayed):
            
    def pc_played(self, player, start, lista: list):
        self.randome_played(player, start, lista)


class Dificult2(Dificult, RandomePlayed, PreVictorySearcher_1):
    
    def pc_played(self, player, start, lista : list):
        # Esta función es igual que la anterior, pero sin desperdiciar las posibles victorias en su turno
        
        list_join = lista.copy()
        pc_sign = {
            -1 : 'X', 
            1 : 'O'
            }
        
        i, sign_scale, line = self.possible_victorys(list_join, pc_sign.get(start))
        if line:
            lista[i+sign_scale*line] = pc_sign.get(start)
        else:
            self.randome_played(player, start, lista)


class Dificult3(Dificult, RandomePlayed, PreVictorySearcher_1):
    
    def pc_played(self, player, start, lista : list):
        # Igual que la anterior, pero además tapa las posibles victorias del jugador
        
        list_join = lista.copy()
        pc_sign = {
            -1 : 'X', 
            1 : 'O'
            }
        
        i, sign_scale, line = self.possible_victorys(list_join, pc_sign.get(start))
        i1, sign_scale1, line1 = self.possible_victorys(list_join, pc_sign.get(-1*start))
        if line:
            lista[i+sign_scale*line] = pc_sign.get(start)
        elif line1:
            lista[i1+sign_scale1*line1] = pc_sign.get(start)
        else:
            self.randome_played(player, start, lista)
# endregion---------------------#


# EL JUEGO #
class Game():
    def __init__(self, table, search, dificult):
        self.table : ToolsTable = table
        self.search : ToolsSearch = search
        self.dificult : Dificult = dificult
        self.lista = [0, 0, 0,
                      0, 0, 0,
                      0, 0, 0]

    def game(self, multiplayer= 'Y'):  
        '''En el inicio de cada partida se determina si se jugará contra la PC y la dificultad en caso de que sí. 
         Luego se crean las variables -player-, para indicar el turno del jugador, y -start- para diferenciar quién comenzó la partida, 
         o sea quién juega con las "X" y quién con los "O"           
         (player = 1: Jugador1, player = -1: Computadora/Jugador2) 
         
           |start = 1|start = -1
        P1 |    X    |     O
        P-1|    O    |     X
        '''
        
        if multiplayer == 'N':                  
            player = random.choice([1 , -1])                              
            if player == -1:
                t = random.randint(0,8) 
                self.lista[t] = 1
                start = -1                      
                player *= -1 
            else:
                start = 1
        else:
            player = 1
            start = 1
        ocupado = 0
        
        #  De este bucle se rige el resto de la partida. A al inicio de este el usuario juega, y luego la PC, 
        # comprobando despues de cada jugada si hay victoria o empate.
        while True:
            
            # Lógica de Jugada del humano
            t = self.table.recharge(self.lista, ocupado)
            ocupado = 0
            
            try:
                t = int(t)
            except:
                continue
            if t >= 0 and t < 10:
                if t > 6:
                    t -= 7
                elif t == 0:
                    print('GAME OVER!!!')
                    break
                elif t < 4:
                    t += 5
                else:
                    t -= 1
            else:
                continue
            
            ocupated = self.table.print_tablero(self.lista, t)
            if ocupated:
                ocupado = 1
            else:
                self.lista[t] = player * start
                self.table.sustitution(self.lista)
                if self.search.search_final(self.lista, player):
                    break
                
                player *= -1  

            # Lógica de Jugada de la PC
            if player == -1 and multiplayer == 'N':
                self.dificult.pc_played(player, start,self.lista)
                self.table.sustitution(self.lista)
                if self.search.search_final(self.lista, player):
                    break
                
                player *= -1 


if __name__ == '__main__':
    table = ToolsTable()
    #win_search_re = VictorySearchByRE()
    win_search_op = OptimeVictorySearch()
    searcher1 = ToolsSearch(table, win_search_op)
    dificult1 = Dificult1()
    dificult2 = Dificult2()
    dificult3 = Dificult3()

    game = Game(table, searcher1, dificult3)

    game.game('N')

# Aproximadamente 250 líneas de código sin líneas vacías ni comentariosa