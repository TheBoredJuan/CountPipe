Lui $s0, 0x1000
Ori $s0, $s0, 0x0020 #dirección base en registro s0
Addi $s1, $0, 10
Addi $s2, $0, 0 # i fila
Sll $t1, $s1, 2
Addi $t3, $0, 40
Ciclo1:
Beq $s2, $s1, FinCiclo1
Addi $s3, $0, 0 # j columna
Ciclo2:
Beq $s3, $s1, FinCiclo2
Sll $t2, $s3, 2 #j*4
Mul $t4, $s2, $t3 #i*40
Add $t4, $t4, $t2 # calcular el offset exacto (j*4) + (i*40)
Add $t4, $t4, $s0 # suma base + offset
Add $t1, $t1, $s3
Add $t1, $t1, $s2
Lw $s5, 0($t4)
Add $t1, $t1, $s5
Sw $t1, 0($t4)
Sll $t2, $s3, 2 #j*4
Mul $t4, $s2, $t3 #i*40
Add $t4, $t4, $t2 # calcular el offset exacto (j*4) + (i*40)
Add $t4, $t4, $s0 # suma base + offset
Add $t1, $t1, $s3
Add $t1, $t1, $s2
Lw $s5, 0($t4)
Add $t1, $t1, $s5
Sw $t1, 0($t4)
Addi $s3, $s3, 2
J Ciclo2
FinCiclo2: 
addi $s2, $s2, 2
J Ciclo1
FinCiclo1: 
jr $ra