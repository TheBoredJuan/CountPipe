import re
archivo=str(input("Ingrese el archivo a leer  : "))
algoritmo = open(archivo,'r')
lista=algoritmo.readlines()

registros=[]
for i in range(27):
        registros.append(0)

 #Pila inicialmente vacía 

patronAdd= re.compile('[aA][dD][dD]')
patronAnd= re.compile('[aA][nN][dD]')
patronOr= re.compile('[oO][rR]')
patronSlt= re.compile('[sS][lL][tT]')
patronMult= re.compile('[mM][uU][lL][tT]')
patronMul= re.compile('[mM][uU][lL]')
patronDiv= re.compile('[dD][iI][vV]')
patronSub= re.compile('[sS][uU][bB]')
patronAddi= re.compile('[aA][dD][dD][iI]')
patronAndi= re.compile('[aA][nN][dD][iI]')
patronOri= re.compile('[oO][rR][iI]')
patronSlti= re.compile('[sS][lL][tT][iI]')
patronLui= re.compile('[lL][uU][iI]')
patronSll= re.compile('[sS][lL][lL]')
patronSrl= re.compile('[sS][rR][lL]')
patronBeq= re.compile('[bB][eE][qQ]')
patronBne= re.compile('[bB][nE][eE]')
patronJ= re.compile('[jJ]')
patronJr= re.compile('[jJ][rR]')
patronJal= re.compile('[jJ][aA][lL]')
patronMul= re.compile('[mM][uU][lL]')
patronLw= re.compile('[lL][wW]')
patronSw= re.compile('[sS][wW]')
patronLabel= re.compile('\w+:')
#print(lista)
#print(patrones)

patronCiclo= re.compile('[cC][iI][cC][lL][oO]')
patronFinCiclo= re.compile('[fF][iI][nN][cC][iI][cC][lL][oO]')


def hallarInmediato(inm):
	inm=str(inm)
	if (inm[len(inm)-1]=='\n' or inm[len(inm)-1]==','):
		inm=inm[:len(inm)-1]
	if (len(inm)>2):
		if((inm[0]=='0') and (inm[1]=='x' or inm[1]=='X')):
			return int(inm,16)
		elif((inm[0]=='0') and (inm[1]=='b' or inm[1]=='B')):
			return int(inm,2)
		else:
			return int(inm)
	else:
		return int(inm)

def entreLista(i,DicP):
	rango=[0,0,False]
	l=list(DicP.values())
	for j in l:
		if(i>hallarInmediato(j)):
			rango[0]=hallarInmediato(j)
			for k in l:
				if(i<hallarInmediato(k)):
					rango[1]=hallarInmediato(k)
					rango[2]=True
					return rango
	return rango

def buscarDic(i,DicP):
	l=list(DicP.keys())
	for j in l:
		if patronFinCiclo.match(j)!=None and (i in j):
			return DicP[j]

def obtenerRegistro(r):
	if (r=='$0,' or r=='$ze'):
		return ['zero',0]
	reg=[]
	#print(r)
	if r=='$sp' or r=='$SP':
		reg.append(0)
		reg.append(registros[0])	
	elif r[1]=='v' or r[1]=='V':
		reg.append(1+int(r[2]))
		reg.append(registros[1+int(r[2])])	
	elif r[1]=='a' or r[1]=='A':
		reg.append(3+int(r[2]))
		reg.append(registros[3+int(r[2])])	
	elif r[1]=='t' or r[1]=='T':
		reg.append(7+int(r[2]))
		reg.append(registros[7+int(r[2])])
	elif r[1]=='s' or r[1]=='S':
		reg.append(17+int(r[2]))
		reg.append(registros[17+int(r[2])])	
	return reg


#Se supone que los registros se escriben en minusculas y cada parte del código esta separada con espacios

def desenrollado(inicio,fin):
	stack=[]
	newAlgoritmo=[]
	registrosBranch=[]
	Dic={}
	separador=' '
	first= 0
	actcont= 0
	jump= 0
	for i in range(len(lista)):
		if (patronLabel.match(lista[i])!=None):
			saveLb=lista[i].split(':')
			Dic[saveLb[0]]=i
			if first==i:
				first=first+1

	for i in range(len(lista)):
		rango=entreLista(i,Dic)
		if(rango[2]):
			a=lista[i].split(' ')
			if (patronBeq.match(a[0]) != None):
				if(a[3][len(a[3])-1]=='\n'):
					a[3]=a[3][:len(a[3])-1]

				if(a[2][0]=='$'):
					tmpbeq1=a[1][:3]
					tmpbeq2=a[2][:3]
					registrosBranch.append(tmpbeq1)
					registrosBranch.append(tmpbeq2)
				else:
					tmpbeq1=obtenerRegistro(a[1][:3])
					registrosBranch.append(tmpbeq1)
				
			elif (patronBne.match(a[0]) != None):
				if(a[3][len(a[3])-1]=='\n'):
					a[3]=a[3][:len(a[3])-1]
				if(a[2][0]=='$'):
					tmpbeq1=obtenerRegistro(a[1][:3])
					tmpbeq2=obtenerRegistro(a[2][:3])
					registrosBranch.append(tmpbeq1)
					registrosBranch.append(tmpbeq2)
				else:
					tmpbeq1=obtenerRegistro(a[1][:3])
					registrosBranch.append(tmpbeq1)
		
	i=inicio
	count=0
	iniciociclo=0
	findelciclo=0
	while i < fin:
		print (i)
		if (patronLabel.match(lista[i])!=None):
			newAlgoritmo.append(lista[i])
			print(lista[i])
			if(patronCiclo.match(lista[i])!=None and patronFinCiclo.match(lista[i])==None):
				tmpCi1=lista[i].split(":")
				if tmpCi1[0][4]=='o':
					tmpCi2=tmpCi1[0].split('o')
				else:
					tmpCi2=tmpCi1[0].split('O')
				tmpCi3=tmpCi2[1]
				iniciociclo=i+1
				findelciclo=buscarDic(tmpCi3,Dic)
				#print(iniciociclo,findelciclo)
				newAlgoritmo=newAlgoritmo+desenrollado(iniciociclo,findelciclo)+[lista[findelciclo]]
			i=findelciclo+1

			continue

		rango=entreLista(i,Dic)
		huv=rango[2] and rango[0]>first-1
		print (huv)
		if(rango[2] and rango[0]>first-1):
			a=lista[i].split(' ')

			if (patronBeq.match(a[0]) != None):
				newAlgoritmo.append(lista[i])
				i=i+1
				continue
				
			elif (patronBne.match(a[0]) != None):
				newAlgoritmo.append(lista[i])
				i=i+1
				continue
			hiv=patronAddi.match(a[0]) != None
			print(hiv)
			print(registrosBranch)
			if (patronAddi.match(a[0]) != None):
						if(a[1][:3] in registrosBranch):
							if a[2][:3] =="$0," or a[2][:3] =="$ze":
								newAlgoritmo.append(lista[i])
							else:
								a[3]=str(hallarInmediato(a[3])*2)
								string=separador.join(a)
								actcont=string
			elif(patronJr.match(a[0]) != None or patronJ.match(a[0]) != None):
				jump=lista[i]
			else:
				stack.append(lista[i])
		else:
			newAlgoritmo.append(lista[i])
		i=i+1
	#print (stack)
	for des in range(2):
		for itstack in stack:
			newAlgoritmo.append(itstack)
	#print (actcont,jump)
	if actcont != 0:
		newAlgoritmo.append(actcont+'\n')
	if jump != 0:
		newAlgoritmo.append(jump)
	return newAlgoritmo
	
print(len(lista))
codigoRes=desenrollado(0,len(lista))
newFile=open(archivo[:len(archivo)-4]+"Des.asm",'w')
for i in codigoRes:
	newFile.write(i)
newFile.close()
#for i in range(len(registros)):
#	print(i,". ",hex(registros[i]),"  ",int(registros[i]))
algoritmo.close
