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
codigo = 'teste'
codigo_objeto = []

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
                    tab_simbolos[palavras[0]] = {'linha':CI, 'status':'definido'}
                del palavras[0]

            #Analise do Mnemonico
            if(not(palavras[0] in tab_mnemonicos or palavras[0] in tab_mnemonicos_pseudo)):
                print("Erro: Mnemonico invalido ("+palavras[0]+")")
                erro = True
                break

            #Analise do operador
            #separo os mnemonicos pelos possiveis tipo de operador (rotulo ou enderecamento direto)
            if(not(re.search("^/\d", palavras[1]))):
                if((palavras[1] in tab_simbolos and tab_simbolos[palavras[1]]['status'] == 'indefinido') or not(palavras[1] in tab_simbolos)):
                    if(palavras[0] == 'K'):
                        tab_simbolos[label] = {'valor':palavras[1], 'status':'definido'}
                        isEnderecoConvertido = True
                    else:
                        tab_simbolos[palavras[1]] = {'linha':'-', 'status':'indefinido'}
                        isEnderecoConvertido = False
                    
                if(palavras[1] in tab_simbolos and tab_simbolos[palavras[1]]['status'] == 'definido'):
                    endereco_convertido = tab_simbolos[palavras[1]]['linha']
                    isEnderecoConvertido = True
            elif(palavras[0] in tab_mnemonicos and tab_mnemonicos[palavras[0]]['tamanho'] == 2):
                endereco_convertido = palavras[1][1]+palavras[1][2]+palavras[1][3]+palavras[1][4]
            elif(palavras[0] in tab_mnemonicos and tab_mnemonicos[palavras[0]]['tamanho'] == 1):
                endereco_convertido = palavras[1][1]+palavras[1][2]
            if(palavras[0] in tab_mnemonicos):
                CI = CI + tab_mnemonicos[palavras[0]]['tamanho']
            linha = arquivo.readline() #le nova linha
            palavras = linha.split(";")
            palavras = palavras[0].split()
            label = palavras[0]
    for simbolo in tab_simbolos:
        if(tab_simbolos[simbolo]['status'] == 'indefinido'):
            print("Erro: simbolo não definido (" + simbolo + ")")
            erro = True
    if(erro == True):
        print("Erro ocorrido! Montagem não foi feita com sucesso")
    else: 
        print(CI)
        print(tab_simbolos)   
        passo = 2    

if(passo == 2):
    with open('./codigo_fonte/teste.txt', 'r') as arquivo:
        linha = arquivo.readline()
        palavras = linha.split()
        while(palavras[0] != '#' and palavras[1] != '#'):
            if(len(palavras) == 3):
                del palavras[0]
            if(palavras[0] in tab_mnemonicos):
                if(palavras[1] in tab_simbolos and tab_simbolos[palavras[1]]['status'] == 'definido'):
                    i = 0#endereco_convertido = tab_simbolos[palavras[1]]['linha']
                elif(palavras[0] in tab_mnemonicos and tab_mnemonicos[palavras[0]]['tamanho'] == 2):
                    endereco_convertido = palavras[1][2]+palavras[1][3]+palavras[1][4]
                elif(palavras[0] in tab_mnemonicos and tab_mnemonicos[palavras[0]]['tamanho'] == 1):
                    endereco_convertido = palavras[1][1]
                codigo = tab_mnemonicos[palavras[0]]['codigo']+str(endereco_convertido)
            print(codigo)
            codigo_objeto.append(codigo)
            linha = arquivo.readline()
            palavras = linha.split(";")
            palavras = palavras[0].split()
with open('./codigo_objeto/teste.txt', 'w+') as arquivoEscrita:
    for codigo in codigo_objeto:
        arquivoEscrita.write(codigo)
