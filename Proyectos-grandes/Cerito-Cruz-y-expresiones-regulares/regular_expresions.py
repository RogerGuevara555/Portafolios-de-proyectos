class Regex():
    
    def __init__(self):
        self.icons = ['?', '/']
        
        self.abc = ['a', 'b', 'c', 'd', 'e', 
                    'f', 'g', 'h', 'i', 'j', 
                    'k', 'l', 'm', 'n', 'ñ', 
                    'o', 'p', 'q', 'r', 's', 
                    't', 'u', 'v', 'w', 'x', 
                    'y', 'z', 'X', 'O']
        
        self.nums = ['1', '2', '3', '4', '5', 
                     '6', '7', '8', '9', '0']
        
        self.alls = ['a', 'b', 'c', 'd', 'e', 
                    'f', 'g', 'h', 'i', 'j', 
                    'k', 'l', 'm', 'n', 'ñ', 
                    'o', 'p', 'q', 'r', 's', 
                    't', 'u', 'v', 'w', 'x', 
                    'y', 'z', 'X', 'O',
                    '1', '2', '3', '4', '5', 
                    '6', '7', '8', '9', '0',
                    '?', '/', '&', '@', ' ']
    
    
    def search_in(self, text, pattern):                 # se realizarán todas las búsquedas en del patrón sumando una posición extra:
            for j in range(len(text)):                  #  (variable index) en caso de no encontrar el patrón hasta terminar el texto
                match = self.match(text, pattern, j)
                m = match[0]
                if not m:      
                    continue
                else:
                    return match
            return False, '0'
    
    
    def find_in_groups(self, icon, chase, text, index, pattern, i):     #  verifica si el caracter x del texto está en el grupo de 
            group_find = {                                           # caracteres del signo del patron
                '/' : self.abc,
                '?' : self.nums,
                '@' : self.icons,
                '&' : self.alls
            }.get(icon)                     
            if pattern[i] == icon:
                if text[i + index] not in group_find:
                    return False
                chase.append(text[i + index])
                return True
            
            
    def match(self, text, pattern, index):          # busca si en x parte del texto hay una coincidencia con el patrón
        chase = []
        if index + len(pattern) > len(text):          # si el patrón es mayor que el texto se retorna False
            return False, '0'
        
        for i in range(len(pattern)):                    # la búsqueda se realiza caracter por carcter
            
            if pattern[i] in ['/', '?', '@', '&']:
                if not self.find_in_groups(pattern[i], chase, text, index, pattern, i):
                    return False, '0'   
            elif pattern[i] != text[i + index]:
                return False, '0'                       # si no coincide con ninguna búsqueda, retorna False y termina el método 
            else:
                chase.append(text[i + index])
        
        chase = ''.join(chase)     
        return True, chase                   # de lo contrario, retorna este True
    

class Interpreter():
    def __init__(self, regex):
        self.regex = regex
    
    def search_in(self, text, pattern):
        expan_pattern = pattern
        while True:
            expan_pattern = expan_pattern.replace( self.regex.search_in(expan_pattern, '&·?')[1] , self.expand_repetition(expan_pattern) )
            if not self.regex.search_in(expan_pattern, '&·?')[0]:
                break
        return self.regex.search_in(text, expan_pattern)
        
    def expand_repetition(self, pattern):
        match, chase = self.regex.search_in(pattern, '&·?')
        if match:
            num = chase[2:]
            new_chase = chase[0] * int(num)
            return new_chase
        return pattern
                
            
list = ['X', 'X', 'X',   
        ' ', 'O', 'O',  
        'O', ' ', 'O']

list.insert(3, 'l')
list.insert(7, 'l')
list.insert(11, 'l')

for k in range(len(list)):
    list[k] = str(list[k])

list = ''.join(list)

#print(list)

re = Regex()
re_new = Interpreter(re)

#print(re_new.expand_repetition('?&·2?&·2?&·3'))

a, b = re_new.search_in(list, 'X&·2X&·2X')       # creciente diagonal
a, b = re_new.search_in(list, 'X&·3X&·3X')       # perpendicular
a, b = re_new.search_in(list, 'X&·4X&·4X')       # decreciente diagonal
a, b = re_new.search_in(list, 'X·3')             # horizontal


