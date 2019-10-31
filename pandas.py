import pandas as pd
import numpy as np


##Ejercicio1
my_list = list("abcedfghijklmnopqrstuvwxyz")
myarr= np.arange(18)
df= pd.DataFrame(my_list)
df



#Ejercicio2
##Combinar dos series
ser1 = pd.Series(list('abcedfghijklmnopqrstuvwxyz'))
ser2 = pd.Series(np.arange(26)) 

mylist = [x for x in 'abcedfghijklmnopqrstuvwxyz']
myarr = list (range(0,len(mylist)))
ser = pd.DataFrame({"col1": mylist, "col2": myarr})
ser



##Ejercicio3 
##Filtrar elementos que no esten en una serie
ser1 = pd.Series([1, 2, 3, 4, 5])
ser2 = pd.Series([4, 5, 6, 7, 8])

result = ser1.isin(ser2)
ser1[~result]



##Ejercicio4
##Convertir numpy arr a dataframe de un tama�o espec�fico.

ser= np.random.randint(1,10,35)
ser2= np.resize(ser,(7,5))
df =pd.DataFrame(ser2)
df


##Ejercicio5
##Manipular un dataframe de strings
# Word list
words = pd.Series(['how', 'to', 'kick', 'ass?'])

# Lambda function that get the first char, make it uppercase
# and put together the word
y = lambda x: x[0].upper() + x[1:]

# Map the lambda function to the series
re = words.map(y)

#Print it
re



##Ejercicio6
##Calcular distancia euclidiana entre dos vectores

import math 

p= pd.Series([1,2,3,4,5,6,7,8,9,10])
q=pd.Series([10,9,8,7,6,5,4,3,2,1])

diff=p-q
result= sum(diff**2)
math.sqrt(result)



