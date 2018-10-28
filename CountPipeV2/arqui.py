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
def hallarInmediato(inm):
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

def opTipoR(linea,operacion):
	a=linea.split(' ')
	r1=a[1]
	r2=a[2]
	r3=a[3]
	c1=obtenerRegistro(r1[:3])
	c2=obtenerRegistro(r2[:3])
	c3=obtenerRegistro(r3)
	if operacion == '+':
		registros[c1[0]]=c2[1]+c3[1] #Actualizacion de registros
	elif operacion == '-':
		registros[c1[0]]=c2[1]-c3[1]
	elif operacion == 'MULSIMP':
		registros[c1[0]]=c2[1]*c3[1]
	elif operacion == 'AND': 
		registros[c1[0]]=c2[1]&c3[1]
	elif operacion == 'OR': 
		registros[c1[0]]=c2[1]|c3[1]
	elif operacion == 'SLT': 
		registros[c1[0]]=int(c2[1]<c3[1])

def opTipoI(linea,operacion):
	a=linea.split(' ')
	r1=a[1]
	r2=a[2]
	inmediato= a[3]
	c1=obtenerRegistro(r1[:3])
	if r2!='$0,' and r2!='$zero':
		c2=obtenerRegistro(r2[:3])
	else:
		c2=['zero',0]
	if operacion == '+':
		registros[c1[0]]=c2[1]+hallarInmediato(inmediato) #Actualizacion de registros
	elif operacion == 'ANDI': 
		registros[c1[0]]=c2[1]&hallarInmediato(inmediato)
	elif operacion == 'ORI': 
		registros[c1[0]]=c2[1]|hallarInmediato(inmediato)
	elif operacion == 'SLTI': 
		registros[c1[0]]=int(c2[1]<hallarInmediato(inmediato))
	elif operacion == 'SLL':
		registros[c1[0]]=c2[1]*pow(2,hallarInmediato(inmediato))
	elif operacion == 'SRL':
		registros[c1[0]]=int(c2[1]/pow(2,hallarInmediato(inmediato)))
	elif operacion == 'MULCOMP':
		registros[26]=c1[1]*c2[1] #Guarda el valor en el registro Low
	elif operacion == 'DIV':
		registros[26]=int(c1[1]/c2[1])
		registros[25]=int(c1[1]%c2[1])
#Se supone que los registros se escriben en minusculas y cada parte del código esta separada con espacios

def ciclosPipeline():
	stack=[]
	c=5
	Dic={}
	first=0
	for i in range(len(lista)):
		if (patronLabel.match(lista[i])!=None):
			saveLb=lista[i].split(':')
			Dic[saveLb[0]]=i
			if first==i:
				first=first+1
	print(Dic)
	i=0
	count=0
	while i < len(lista):
		if (patronLabel.match(lista[i])!=None):
			i=i+1
			continue
		a=lista[i].split(' ')
		#Operaciones tipo I
		if(patronAddi.match(a[0]) != None):
			opTipoI(lista[i],'+')
		elif(patronAndi.match(a[0]) != None):
			opTipoI(lista[i],'ANDI')
		elif(patronOri.match(a[0]) != None):
			opTipoI(lista[i],'ORI')
		elif(patronSlti.match(a[0]) != None):
			opTipoI(lista[i],'SLTI')
		elif(patronSll.match(a[0]) != None):
			opTipoI(lista[i],'SLL')
		elif(patronSrl.match(a[0]) != None):
			opTipoI(lista[i],'SRL')
		elif(patronMult.match(a[0]) != None):
			opTipoI(lista[i],'MULCOMP')
		elif(patronDiv.match(a[0]) != None):
			opTipoI(lista[i],'DIV')
		#Operaciones tipo R
		elif(patronAdd.match(a[0]) != None):
			opTipoR(lista[i],'+')
		elif(patronSub.match(a[0]) != None):
			opTipoR(lista[i],'-')
		elif(patronMul.match(a[0]) != None):
			opTipoR(lista[i],'MULSIMP')
		elif(patronAnd.match(a[0]) != None):
			opTipoR(lista[i],'AND')
		elif(patronOr.match(a[0]) != None):
			opTipoR(lista[i],'OR')
		elif(patronSlt.match(a[0]) != None):
			opTipoR(lista[i],'SLT')
		elif(patronLui.match(a[0]) != None):
			tmplui=obtenerRegistro(a[1][:3])
			registros[tmplui[0]]=hallarInmediato(a[2])*pow(16,4)

		if i-first >= 1:
			c=c+1
		print(i+1,"       ",c)

		if (i <= len(lista)-2):
			b=lista[i+1].split(' ')
			if (patronLw.match(a[0]) != None) and (patronSw.match(b[0]) != None)  and ((a[1][:3]==b[1][:3])):
				c=c+1
				i=i+1
				continue
			elif (patronLw.match(a[0]) != None) and (patronLw.match(b[0]) != None):
				splitb=b[2].split('(')
				if((a[1][:3]==b[1][:3])):
					c=c+1
					i=i+1
					continue
			elif(len(b)>3):
				if(patronLw.match(a[0]) != None)  and ((a[1][:3]==b[2][:3]) or (a[1][:3]==b[3][:3])): #Errores en -Lw-,-Sw-,-J-,-B-
					c=c+1
					i=i+1
					continue
				elif(patronLw.match(a[0]) != None) and ((patronBeq.match(b[0]) != None) or (patronBne.match(b[0]) != None)) and ((a[1][:3]==b[2][:3]) or (a[1][:3]==b[1][:3])): #Errores en -Lw-,-Sw-,-J-,B
					c=c+1
					i=i+1
					continue

		if(patronJr.match(a[0]) != None):
			if(a[1][len(a[1])-1]=='\n'):
				a[1]=a[1][:len(a[1])-1]
			c=c+1
			if(stack != []):
				i=stack[len(stack)-1]
				stack=stack[:len(stack)-1]

		elif (patronJal.match(a[0]) != None):
			if(a[1][len(a[1])-1]=='\n'):
				a[1]=a[1][:len(a[1])-1]
			c=c+1
			stack.append(i)
			i=Dic[a[1]]		

		elif (patronJ.match(a[0]) != None):
			if(a[1][len(a[1])-1]=='\n'):
				a[1]=a[1][:len(a[1])-1]
			c=c+1
			i=Dic[a[1]]

		elif (patronBeq.match(a[0]) != None):
			if(a[3][len(a[3])-1]=='\n'):
				a[3]=a[3][:len(a[3])-1]

			if(a[2][0]=='$'):
				tmpbeq1=obtenerRegistro(a[1][:3])
				tmpbeq2=obtenerRegistro(a[2][:3])
				if(tmpbeq1[1]==tmpbeq2[1]):
					c=c+1
					i=Dic[a[3]]
			else:
				tmpbeq1=obtenerRegistro(a[1][:3])
				if(tmpbeq1[1]==hallarInmediato(a[2])):
					c=c+1
					i=Dic[a[3]]

		elif (patronBne.match(a[0]) != None):
			if(a[3][len(a[3])-1]=='\n'):
				a[3]=a[3][:len(a[3])-1]
			if(a[2][0]=='$'):
				tmpbeq1=obtenerRegistro(a[1][:3])
				tmpbeq2=obtenerRegistro(a[2][:3])
				if(tmpbeq1[1]!=tmpbeq2[1]):
					c=c+1
					i=Dic[a[3]]
			else:
				tmpbeq1=obtenerRegistro(a[1][:3])
				if(tmpbeq1[1]!=hallarInmediato(a[2])):
					c=c+1
					i=Dic[a[3]]
		i=i+1
	print ("Numero de ciclos:",c)
	
print(len(lista))
ciclosPipeline()
#for i in range(len(registros)):
#	print(i,". ",hex(registros[i]),"  ",int(registros[i]))
algoritmo.close
