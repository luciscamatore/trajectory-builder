import numpy as np

# detalii robot
R = 0.05
a = 0.094
b = 0.126

# matricea pt viteze
A = [[1, -1, -(a+b)],
     [1, 1, (a+b)],
     [1 ,1, -(a+b)],
     [1, -1, (a+b)]]

# output si traiectorie
output = []
traiectorie = []

#daca un numar e float
def isFloat(n):
    try:
        float(n)
        return True
    except:
          return False

# citim fisierul cu coordonate
def readInput():
    inputFile = open("input.txt", "r")
    try:
        for lines in inputFile.readlines():
            traj = [float(i) for i in lines.split(',') if isFloat(i)]
    finally:
        inputFile.close()
    for i in range(0,len(traj)-1,2):
        traiectorie.append([traj[i],traj[i+1]])

# calculam vitezele rotilor pentru un vector de input
def calculareViteza(A, input):
    vectorCoordonata = np.array([input[0], input[1], 0])
    w = (1/R)*(np.matmul(A,vectorCoordonata))
    return w

# generam coordonatele
def generareCoordonate(traiectorie):
    coordonate = []
    coordonate.append(traiectorie[0][0])
    coordonate.append(traiectorie[0][1])

    for i in range(1,len(traiectorie)):
        for j in range(0,2):
            coordonate.append(traiectorie[i][j] - traiectorie[i-1][j])
    return coordonate

# generam tot output-ul care merge spre robot
def generareOutput(coordonate):
    matrice=[]
    for i in range(0, len(coordonate)-1,2):
        matrice.append(calculareViteza(A,[coordonate[i], coordonate[i+1]]))
    for j in range(0,len(matrice)):
        output.append([matrice[j][0],matrice[j][1],matrice[j][2],matrice[j][3]])
    print(output)
    return output

readInput()
coordonate = generareCoordonate(traiectorie)
viteze = generareOutput(coordonate)

outputFile = open("viteze.txt", "w")

try:
    for i in viteze:
        outputFile.write(str(i).replace("[","").replace("]", "").replace(",","") + "\n")
finally:
    outputFile.close()
