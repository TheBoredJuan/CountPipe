main:
addi $s1, $0, 4
jal fibo
j salir
fibo:
beq $s1, 0, retornar
beq $s1, 1, retornar
ciclo:
addi $s1, $s1, -1
addi $sp, $sp, -12
sw $s1, 0($sp)
sw $ra, 4($sp)
jal fibo
addi $t2, $s1, 0
lw $s1, 0($sp)
sw $t2, 8($sp)
addi $s1, $s1, -1
jal fibo
lw $t2, 8($sp)
add $s1, $s1, $t2
lw $ra, 4($sp)
addi $sp, $sp, 12
jr $ra
retornar:
addi $s1, $0, 1
jr $ra
salir:
jr $ra