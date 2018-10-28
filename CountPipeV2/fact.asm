main:
addi $s1, $0, 3
jal factorial
j salir
factorial:
beq $s1, 0, retornar
addi $sp, $sp, -8
sw $ra, 4($sp)
sw $s1, 0($sp)
addi $s1, $s1, -1
jal factorial
lw $t2, 0($sp)
lw $ra, 4($sp)
addi $sp, $sp, 8
mul $s1, $s1, $t2
jr $ra
retornar:
addi $s1, $0, 1
jr $ra
salir:
jr $ra
