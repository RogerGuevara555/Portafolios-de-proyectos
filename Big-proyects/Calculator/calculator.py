import re
#import regex 


class Operator():
    
    def calculate(self, search):    # Recive el search y el operador
        m, operation, entry = search
        
        if operation == '+()':      # Para resolver casos como:  -(-3) = 3
            
            # Configuraciones generales
            patern_sign = r'\-?\d+'
            if m.group(0).count('.') == 1:
                patern_sign = r'\-?\d+\.\d+'
            sign = 1
            if m.group(0)[0] == '-':
                sign = -1
                
            # Multiplicar el 1 o -1 de afuera del paréntesis por el número de dentre
            num = float(re.findall(patern_sign, m.group(0))[0])
            sustitution = num * sign   
             
        else:       # Para calculos normales
            
            # Configuraciones generales
            value = 1                       
            if m.group(0).count('/') == 1:
                value = -1
                    
            # Separar números
            x = float(re.search(r'^((|\+|\-)\d+\.\d+ | (|\+|\-)\d+)', m.group(0), re.VERBOSE).group(0))
            y = re.search(r'\(? ( \-?\d+\.\d+ | \-?\d+ ) \)?$', m.group(0), re.VERBOSE).group(0)
            if y[0] == '(':
                y = float(y[1 : len(y)-1]) ** value
            else:
                y = float(y) ** value
            
            # Elegir operación
            sustitution = {         # 3.0
                '+' : x + y,
                '·' : x * y
            }.get(operation)
            
        # Quitar el .0 o agregar un + como operador (en caso de que el resultado sea positivo para que se opere luego)
        if re.match(r'\-?\d+\.0$', str(sustitution)):
            sustitution = int(sustitution)
        if sustitution >= 0:
            sustitution = f'+{sustitution}'
        else:
            sustitution = str(sustitution)
        
        return entry.replace(m.group(0), sustitution)


class Searcher():
     
    def find(self, operator, entry):        # Busca una coincidencia con el patrón de la operación indicada
        pattern = {
            '()' : r'\([\d\D]+?\)', 
            
            '+()' : r'(\+|\-) \( \-?\d+ \)  |  (\+|\-) \( \-?\d+\.\d+ \)',
            
            '+' : r'(\-?\d+ | \-?\d+\.\d+) (\+|\-) (\d+\.\d+ | \d+)',
            
            '·' : r'((|\+|\-)\d+ | \-?\d+\.\d+) (·|/) (\d+ | \d+\.\d+)  |  (|\+|\-)(\d+ | \d+\.\d+) (|·|/) \( (\-?\d+ | \-?\d+\.\d+) \)'
        }.get(operator)
        
        # Devuelve un search y el operador
        return [re.search(pattern, entry, re.VERBOSE), operator, entry]


class Manager():
    def __init__(self, operator, searcher):
        self.operator = operator
        self.searcher = searcher
    
    def operate(self, entry_new, mode= 'combinada', pre_entry= None):
        a = 0
        entry = entry_new
        while True:
            if a == 0 and mode == 'combinada':
                print('\n' ,entry, end= ' ')
                a += 1
                p = input()
            elif a == 0 and mode == 'paréntesis':
                print('\n' ,entry)
                a += 1
            
            par = self.searcher.find('()', entry)[0]
            if self.searcher.find('+()', entry)[0]:
                entry = self.operator.calculate(self.searcher.find('+()', entry)) 
            elif self.searcher.find('·', entry)[0]:
                entry = self.operator.calculate(self.searcher.find('·', entry))
            elif par and re.match(r'\(\-?\d+\)|\(\-?\d+\.\d+\)', par.group(0)):
                entry = entry.replace(par.group(0), par.group(0)[1: len(par.group(0))-1 ])
            elif self.searcher.find('()', entry)[0]:
                p = self.searcher.find('()', entry)[0].group(0)
                entry = self.operate(p[1 : len(p)-1 ], 'paréntesis', entry)
            elif self.searcher.find('+', entry)[0]:
                entry = self.operator.calculate(self.searcher.find('+', entry))
        
            if re.match(r'^\+\d+', entry):
                entry = entry[1:]

            if mode == 'combinada' or mode == 'paréntesis':
                print('=', entry)
    
            match = re.match(r'^\-?\d+$ | ^\-?\d+\.\d+$', entry, re.VERBOSE)
            if match:
                if mode == 'combinada':
                    print('\nOperación concluida. De nada :)')
                break
        
        if mode == 'resultado':
            return entry
        elif mode == 'paréntesis':
            return pre_entry.replace(entry_new, entry)
    
    
entry_new = '(5+4(2))/(8-9·2)'
operator = Operator()
searcher = Searcher()
manager = Manager(operator, searcher)


manager.operate(entry_new)
