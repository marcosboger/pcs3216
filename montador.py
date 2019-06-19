import re
#Arquivo base do montador de 2 passos 

#Tabela de simbolos (dicionario)
tab_simbolos = dict() 

#Tabela de mnemonicos (dicionario)
#Contem todos os mnemonicos definidos, separadas em pseudo ou instrucoes
tab_mnemonicos = {'JP':{'tamanho':2,'codigo':'0'}, 
                  'JZ':{'tamanho':2,'codigo':'1'}, 
                  'JN':{'tamanho':2,'codigo':'2'}, 
                  'CN':{'tamanho':1,'codigo':'3'}, 
                  '+':{'tamanho':2,'codigo':'4'}, 
                  '-':{'tamanho':2,'codigo':'5'}, 
                  '*':{'tamanho':2,'codigo':'6'}, 
                  '/':{'tamanho':2,'codigo':'7'}, 
                  'LD':{'tamanho':2,'codigo':'8'}, 
                  'MM':{'tamanho':2,'codigo':'9'}, 
                  'SC':{'tamanho':2,'codigo':'A'}, 
                  'OS':{'tamanho':1,'codigo':'B'}, 
                  'IO':{'tamanho':1,'codigo':'C'}
                }
tab_mnemonicos_pseudo = {'@', '#', '$','K'}
#variaveis
passo = 1 #passo atual do montador 
CI = 0 
acumulador = 0
erro = False #indica se houve erro no passo
codigo = ''
codigo_objeto = []
with open('./memoria/memoria.txt', 'r') as arquivoMemoria:
    memoria = arquivoMemoria.read()
    memoria = memoria.split()

if(passo == 1):
    with open('./codigo_fonte/teste.txt', 'r') as arquivo:
        linha = arquivo.readline()
        palavras = linha.split(";")
        palavras = palavras[0].split()
        label = palavras[0]
        while(palavras[0] != '#' and palavras[1] != '#'):
            #Analise do Rotulo
            if(len(palavras) == 3): 
                if(palavras[0] in tab_simbolos and tab_simbolos[palavras[0]]['status'] == 'definido'):
                    print("Erro: Multipla definicao de simbolo ("+palavras[0]+")")
                    erro = True
                    break
                elif(palavras[0] in tab_simbolos and tab_simbolos[palavras[0]]['status'] == 'indefinido'):
                    tab_simbolos[palavras[0]]['status'] = 'definido'
                    tab_simbolos[palavras[0]]['linha'] = CI
                else:
                    tab_simbolos[palavras[0]] = {'linha':CI, 'status':'definido', 'funcao':'endereco'}
                del palavras[0]

            #Analise do Mnemonico
            if(not(palavras[0] in tab_mnemonicos or palavras[0] in tab_mnemonicos_pseudo)):
                print("Erro: Mnemonico invalido ("+palavras[0]+")")
                erro = True
                break

            #Analise do operador
            #separo os mnemonicos pelos possiveis tipo de operador (rotulo ou enderecamento direto)
            if(palavras[0] == '@'):
                 CI = int(palavras[1][2]+palavras[1][3]+palavras[1][4])
            if(not(re.search("^/\d", palavras[1])) and palavras[0] != 'IO' and palavras[0] != 'OS' and palavras[0] != 'CN'):
                if((palavras[1] in tab_simbolos and tab_simbolos[palavras[1]]['status'] == 'indefinido') or not(palavras[1] in tab_simbolos)):
                    if(palavras[0] == 'K'):
                        del memoria[2*CI+1]
                        memoria.insert(2*CI+1,palavras[1])
                        arquivoMemoria.close()
                        tab_simbolos[label] = {'linha':CI, 'status':'definido', 'funcao':'valor'}
                        isEnderecoConvertido = True
                    else:
                        tab_simbolos[palavras[1]] = {'linha':'-', 'status':'indefinido','funcao':'endereco'}
                        isEnderecoConvertido = False
                if(palavras[1] in tab_simbolos and tab_simbolos[palavras[1]]['status'] == 'definido'):
                    endereco_convertido = tab_simbolos[palavras[1]]['linha']
                    isEnderecoConvertido = True
            elif(palavras[0] in tab_mnemonicos and tab_mnemonicos[palavras[0]]['tamanho'] == 2):
                endereco_convertido = palavras[1][1]+palavras[1][2]+palavras[1][3]+palavras[1][4]
            elif(palavras[0] in tab_mnemonicos and tab_mnemonicos[palavras[0]]['tamanho'] == 1):
                endereco_convertido = palavras[1][0]
            if(palavras[0] in tab_mnemonicos):
                CI = CI + tab_mnemonicos[palavras[0]]['tamanho']
            if(palavras[0] == 'K'):
                CI = CI + 1
            linha = arquivo.readline() #le nova linha
            palavras = linha.split(";")
            palavras = palavras[0].split()
            label = palavras[0]
    for simbolo in tab_simbolos:
        if(tab_simbolos[simbolo]['status'] == 'indefinido'):
            print("Erro: simbolo nao definido (" + simbolo + ")")
            erro = True
    if(erro == True):
        print("Erro ocorrido! Montagem nao foi feita com sucesso")
    else: 
        print(CI)
        print(tab_simbolos)   
        passo = 2  
        isEnderecoConvertido = False  

if(passo == 2):
    with open('./codigo_fonte/teste.txt', 'r') as arquivo:
        linha = arquivo.readline()
        palavras = linha.split(";")
        palavras = palavras[0].split()
        while(palavras[0] != '#' and palavras[1] != '#'):
            if(len(palavras) == 3):
                del palavras[0]
            if(palavras[0] in tab_mnemonicos):
                if(palavras[1] in tab_simbolos and tab_simbolos[palavras[1]]['status'] == 'definido'):
                    endereco_convertido = tab_simbolos[palavras[1]]['linha']
                    isEnderecoConvertido = True
                    if(int(endereco_convertido) < 100 and int(endereco_convertido) >= 10):
                        endereco_convertido = '0'+str(int(endereco_convertido))
                        isEnderecoConvertido = True
                    elif(int(endereco_convertido) < 10):
                        endereco_convertido = '00'+str(int(endereco_convertido))
                        isEnderecoConvertido = True
                elif(palavras[0] in tab_mnemonicos and tab_mnemonicos[palavras[0]]['tamanho'] == 2):
                    endereco_convertido = palavras[1][2]+palavras[1][3]+palavras[1][4]
                    isEnderecoConvertido = True
                elif(palavras[0] in tab_mnemonicos and tab_mnemonicos[palavras[0]]['tamanho'] == 1):
                    endereco_convertido = palavras[1][1]
                    isEnderecoConvertido = True
                codigo = tab_mnemonicos[palavras[0]]['codigo']+str(endereco_convertido)
            if(isEnderecoConvertido == True):
                codigo_objeto.append(codigo)
            isEnderecoConvertido = False
            linha = arquivo.readline()
            palavras = linha.split(";")
            palavras = palavras[0].split()
for objeto in codigo_objeto:
    print(objeto)
with open('./memoria/memoria.txt', 'w') as arquivoMemoria:
    for posicao in memoria:
        arquivoMemoria.write(posicao+'\n')
with open('./codigo_objeto/teste.txt', 'w+') as arquivoEscrita:
    for codigo in codigo_objeto:
        arquivoEscrita.write(codigo)
