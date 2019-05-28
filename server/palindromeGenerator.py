'''
Generador de palíndromos para GINtelligence. Prueba de reclutamiento.
Programada por: M.C. Antonio Arista Jalife

Notas del programador:
Cuando programo suelo hacerlo en inglés, ya que no se quien podría leer el código. Sin embargo sigo ciertas convenciones:
    -La documentación siempre va arriba de cada método programado, de tal manera que la lectura del código sea fluída y sencilla.
    -Las variables que utilizo son descriptivas por si solas, y prefiero código entendible a código corto y críptico.
    -En zonas donde la optimización es importante suelo hacer comentarios extra, ya que eso ayuda a familiarizarse al lector.

Notas de implementación:
    -Este sistema utiliza Flask para operar, para correr el sistema se debe utilizar en ambiente linux:
        $> export FLASK_APP=palindromeGenerator.py
        $> flask run --host=0.0.0.0
'''
#------------------------------------------------------------------------
#Imports requeridos: Flask, jsonify.
#------------------------------------------------------------------------

from flask import Flask, jsonify

#------------------------------------------------------------------------

#El objeto flask que utilizaremos para añadir la operación GET a la función.
myFlaskObject = Flask(__name__)


'''
-------------------------------------------------------------------------
Función: isPalindrome(string a revisar)
-------------------------------------------------------------------------
Notas: 

Esta es la función que mas veces se va a llamar y es importante
que la función sea lo mas óptima posible. Entre mas operaciones tenga que
hacer, mas lento será el sistema en general. Por ende, comentaré cada 
línea.

Recibe: Un string para revisar si es un palíndromo (funciona también con
capícuas!)
Retorna: un valor booleano que indica si es o no un palíndromo.
-------------------------------------------------------------------------
'''

def isPalindrome(strToCheck):
    result = True;                                       #Colocamos la bandera en True desde el inicio.
    length = len(strToCheck)                             #Calculamos una sola vez la longitud con len()
    stopCriteria = int(length/2)                         #Obtenemos una sola vez el criterio de paro del ciclo.
    for i in range(0,stopCriteria):                      #Utilizamos un ciclo con range para ser lo mas rápidos posibles.
        if(strToCheck[i] != strToCheck[(length-1)-i]):   #En el momento en que la condición de palíndromo se rompe.
            result = False;                              #Colocamos la bandera en false y rompemos el procesamiento.
            break;            
    return result;

'''
-------------------------------------------------------------------------
Función: isDoubleBasePalindrome(Valor entero a revisar)
-------------------------------------------------------------------------
Notas: 

La segunda función mas llamada que calcula si es palíndromo en base 10 y 2.
Hay una manera de optimizar esta función: No es necesario que se haga un 
chequeo binario si el decimal no es palíndromo ya que es necesario que 
ambas condiciones se cumplan, y es mucho mas rápido el calcular la 
condición de "585" que de "1001001001"


Recibe: Un valor entero para revisar si es palíndromo doble o no.
Retorna: un valor booleano que indica si es o no un palíndromo doble
-------------------------------------------------------------------------
'''
def isDoubleBasePalindrome(valueToCheck):
    result = False
    if isPalindrome(str(valueToCheck)):                #Solamente si esta condición de base 10 se cumple...
        if isPalindrome(bin(valueToCheck)[2:]):        #revisamos si la función es palíndroma en binario (bin(valueToCheck[2:])
            result = True
    return result


'''
-------------------------------------------------------------------------
Función: getAllPalindromesInRange(valor tope):
-------------------------------------------------------------------------
Notas: 
Dado un rango, se genera una sumatoria, una colección (lista) de valores
de palíndromos, y una lista binaria de valores de palíndromos. Si la 
condición del contador se cumple, los valores se suman y agregan a la lista.

Recibe: El valor tope del palíndromo en el rango.
Retorna: Tres variables: la suma, la lista de palindromos en decimal, 
         y en binario.
-------------------------------------------------------------------------
'''

def getAllPalindromesInRange(rangeToUse):
    sumOfAllPalindromes = 0
    colOfAllPalindromes = []
    colOfAllPalindromes_binary = []
    for counter in range(0,rangeToUse+1):
        if(isDoubleBasePalindrome(counter)):
            sumOfAllPalindromes += counter
            colOfAllPalindromes.append(counter)
            colOfAllPalindromes_binary.append(bin(counter)[2:])
    return sumOfAllPalindromes, colOfAllPalindromes, colOfAllPalindromes_binary


'''
-------------------------------------------------------------------------
Función: dataCheck(valor desconocido):
-------------------------------------------------------------------------
Notas: 
A manera de seguridad, revisamos que el dato presentado realmente sea un
valor entero positivo. Si bien es cierto que el front-end hace esta 
simple verificación automáticamente y Flask limita la variable, no 
sabemos si algo se conectará al back-end o a este código en un futuro ;)

Recibe: Un valor con tipo de dato desconocido.
Retorna: True si es un entero positivo. False en otro caso.
-------------------------------------------------------------------------
'''
def dataCheck(dataToCheck):
    if type(dataToCheck) is not int:
        return False
    if(dataToCheck < 0):
        return False
    return True


'''
-------------------------------------------------------------------------
Función conectada a Flask: generatePalindromes(Criterio tope):
-------------------------------------------------------------------------
Notas: 
Flask se conectará a esta función a manera de EndPoint. La función está
diseñada para enviar texto plano (no un JSON, eso es en la siguiente 
función...) y su objetivo es servir de prueba en el backend.

Flask Decorator: http://<path>/getPalindrome/<ValorEntero>
Recibe: Un valor para el criterio de tope.
Retorna: Un texto plano.
-------------------------------------------------------------------------
'''

@myFlaskObject.route('/getPalindrome/<int:topCriteria>')
def generatePalindromes(topCriteria):
    textToSend = ""
    if(dataCheck(topCriteria) == False):
         return "BadNumber"
    [sumAll, colAll, colAllBin] = getAllPalindromesInRange(topCriteria)
    textToSend = "Sum="+str(sumAll)+"|All="+str(colAll)+"|AllBin="+str(colAllBin)
    return textToSend
    

'''
-------------------------------------------------------------------------
Función conectada a Flask: generatePalindromes_json(Criterio tope):
-------------------------------------------------------------------------
Notas: 
Flask se conectará a esta función a manera de EndPoint. Esta función 
genera el palíndromo y retorna todos los datos en formato JSON.

Flask Decorator: http://<path>/getPalindromeJSON/<ValorEntero>
Recibe: Un valor para el criterio de tope.
Retorna: Un archivo JSON utilizable para Android / Retrofit. como ejemplo,
El formato del JSON para el numero 585 es:

{
    "All":[0,1,3,5,7,9,33,99,313,585],
    "Bin":["0","1","11","101","111","1001","100001","1100011","100111001","1001001001"],
    "Sum":1055
}
-------------------------------------------------------------------------
'''
@myFlaskObject.route('/getPalindromeJSON/<int:topCriteria>')
def generatePalindromes_json(topCriteria):
    if(dataCheck(topCriteria) == False):
         return jsonify(Sum=-1, All = [-1], Bin = [-1])
    [sumAll, colAll, colAllBin] = getAllPalindromesInRange(topCriteria)
    return jsonify(Sum=sumAll, All = colAll, Bin = colAllBin)



