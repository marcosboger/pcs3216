#Simulador da Maquina Virtual

#Registradores
PC = 0
CI = 0
ACC = 0
SP = 4095

def analisaInstrucao(instrucao):
    global ACC, PC, CI
    opcode = instrucao[0]
    if(opcode == '0'):
        PC = int(instrucao[1:4],16)
    if(opcode == '1'):
        if(ACC == 0):
            PC = int(instrucao[1:4],16)
    if(opcode == '2'):
        if(ACC < 0):
            PC = int(instrucao[1:4],16)
    if(opcode == '3'):
        return
    if(opcode == '4'):
        posicao = int(instrucao[1:4],16)
        posicaoConvertida = 2*int(instrucao[1:4],16)+1
        ACC = ACC + int(memoria[posicaoConvertida],16)
    if(opcode == '5'):
        posicao = int(instrucao[1:4],16)
        posicaoConvertida = 2*int(instrucao[1:4],16)+1
        ACC = ACC - int(memoria[posicaoConvertida],16)
    if(opcode == '6'):
        posicao = int(instrucao[1:4],16)
        posicaoConvertida = 2*int(instrucao[1:4],16)+1
        ACC = ACC * int(memoria[posicaoConvertida],16)
    if(opcode == '7'):
        posicao = int(instrucao[1:4],16)
        posicaoConvertida = 2*int(instrucao[1:4],16)+1
        ACC = ACC / int(memoria[posicaoConvertida],16)
    if(opcode == '8'):
        posicao = int(instrucao[1:4],16)
        posicaoConvertida = 2*int(instrucao[1:4],16)+1
        ACC = int(memoria[posicaoConvertida],16)
    if(opcode == '9'):
        posicao = int(instrucao[1:4],16)
        posicaoConvertida = 2*int(instrucao[1:4],16)+1
        print(ACC)
        print(posicaoConvertida)
        if(ACC < 16):
            memoria[posicaoConvertida] = '0'+ str(hex(ACC))[2:] 
        else:
            memoria[posicaoConvertida] = str(hex(ACC))[2:] 
    if(opcode == 'a'):
        endereco = str(hex(PC-2))[2:]
        memoria[SP*2+1] = endereco.zfill(4)[0:2]
        memoria[SP*2-1] = endereco.zfill(4)[2:4]
        SP = SP - 2
        PC = int(instrucao[1:4],16)
    if(opcode == 'b'):
        return
    if(opcode == 'c'):
        if(instrucao[1] == '0'):
            with open('./perifericos/entrada.txt', 'r') as arquivoEntrada:
                ACC = int(arquivoEntrada.read(1),16)
        return    


with open('./memoria/memoria.txt', 'r') as arquivoMemoria:
    memoria = arquivoMemoria.read()
    memoria = memoria.split()

restoInstrucao = ''
halt = False
novoComando = ''
comando = raw_input("Aperte Enter para comecar ")
while(novoComando != 'STOP'):
    novoComando = raw_input("Digite um comando para continuar ou STOP para parar: ")
    if(novoComando[0:2] == 'GO'):
        PC = novoComando[3:]
        PC = int(PC, 16)
        while(halt == False):
            instrucao = memoria[2*PC+1]
            PC = PC + 1
            opcode = instrucao[0]
            if(opcode != '3' and opcode != 'B' and opcode != 'C'):
                restoInstrucao = memoria[2*PC+1]
                PC = PC + 1
            print(ACC)
            analisaInstrucao(instrucao+restoInstrucao)
            print(ACC)
            break

