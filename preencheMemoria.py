with open('./memoria/memoria.txt', 'r') as arquivoMemoria:
    memoria = arquivoMemoria.read()
    memoria = memoria.split()
    for i in range(2*4096):
        if(i%2 == 1):
            memoria.insert(i, '0')
with open('./memoria/memoria.txt', 'w') as arquivoMemoria:
    for posicao in memoria:
        arquivoMemoria.write(posicao+'\n')