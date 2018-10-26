import re
algoritmo = open('matriz.asm','r')
lista=algoritmo.readlines()

registros=[]
for i in range(32):
        registros.append(0)

stack=[] #Pila inicialmente vacía 

patrones=[] #Lista de patrones para el reconocimiento de 
patronAdd= re.compile('[aA][dD][dD] ')
patrones.append(patronAdd)
patronAddi= re.compile('[aA][dD][dD][iI]')
patrones.append(patronAddi)
patronLui= re.compile('[lL][uU][iI]')
patrones.append(patronLui)
patronOri= re.compile('[oO][rR][iI]')
patrones.append(patronOri)
patronSll= re.compile('[sS][lL][lL]')
patrones.append(patronSll)
patronBeq= re.compile('[bB][eE][qQ]')
patrones.append(patronBeq)
patronJ= re.compile('[jJ]')
patrones.append(patronJ)
patronJr= re.compile('[jJ][rR]')
patrones.append(patronJr)
patronMul= re.compile('[mM][uU][lL]')
patrones.append(patronMul)
patronLw= re.compile('[lL][wW]')
patrones.append(patronLw)
patronSw= re.compile('[sS][wW]')
patrones.append(patronSw)
patronLabel= re.compile('\w+:')
#print(lista)
#print(patrones)


#Se supone que los registros se escriben en minusculas y cada parte del código esta separada con espacios

def ciclosPipeline():
	c=5
	Dic={}
	for i in range(len(lista)):
		if (patronLabel.match(lista[i])!=None):
			saveLb=lista[i].split(':')
			Dic[saveLb[0]]=[i]

	for i in range(len(lista)):
		if (patronLabel.match(lista[i])!=None):
			continue

		if i >= 1:
			c=c+1

		a=lista[i].split(' ')
		if (i <= len(lista)-2):
			b=lista[i+1].split(' ')
			if(patronLw.match(a[0]) != None) and ((a[1][0-2]==b[2][0-2]) or (a[1][0-2]==b[3][0-2])): #Errores en Lw,Sw,J,B
				c=c+1

		if(patronJr.match(a[0]) != None):
			c=c+1
			if(stack != []):
				i=len(stack)-1
				
		elif (patronJ.match(a[0]) != None):
			c=c+1
			i=Dic[a[1]]
		
		print (c)
	
print(len(lista))
ciclosPipeline()
algoritmo.close
