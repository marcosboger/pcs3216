import re
#Arquivo base do montador de 2 passos 

#Tabela de simbolos (dicionario)
tab_simbolos = dict() 

#Tabela de mnemonicos (dicionario)
#Contem todos os mnemonicos definidos, separadas em pseudo ou instrucoes
tab_mnemonicos = {'J':{'tamanho':2}, 
                  'Z':{'tamanho':2}, 
                  'N':{'tamanho':2}, 
                  'C':{'tamanho':1}, 
                  'L':{'tamanho':2}, 
                  'M':{'tamanho':2}, 
                  'S':{'tamanho':2}, 
                  'O':{'tamanho':1}, 
                  'I':{'tamanho':1}, 
                  'JP':{'tamanho':2}, 
                  'JZ':{'tamanho':2}, 
                  'JN':{'tamanho':2}, 
                  'CN':{'tamanho':1}, 
                  '+':{'tamanho':2}, 
                  '-':{'tamanho':2}, 
                  '*':{'tamanho':2}, 
                  '/':{'tamanho':2}, 
                  'LD':{'tamanho':2}, 
                  'MM':{'tamanho':2}, 
                  'SC':{'tamanho':2}, 
                  'OS':{'tamanho':1}, 
                  'IO':{'tamanho':1}}
tab_mnemonicos_pseudo = {'@', '#', '$','K'}
#variaveis
passo = 1 #passo atual do montador 
CI = 0 
acumulador = 0
erro = False #indica se houve erro no passo

if(passo == 1):
    with open('./codigo_fonte/teste.txt', 'r') as arquivo:
        linha = arquivo.readline()
        while(linha != ''):
            palavras = linha.split()
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
            #mnemonico esta definido, tratar operador
            #separo os mnemonicos pelos possiveis tipo de operador (rotulo ou enderecamento direto)
            if(1):
                if((palavras[1] in tab_simbolos and tab_simbolos[palavras[1]]['status'] == 'indefinido') or not(palavras[1] in tab_simbolos)):
                    tab_simbolos[palavras[1]] = {'linha':'-', 'status':'indefinido'}
                    isEnderecoConvertido = False
                if(palavras[1] in tab_simbolos and tab_simbolos[palavras[1]]['status'] == 'definido'):
                    endereco_convertido = tab_simbolos[palavras[1]]['linha']
                    isEnderecoConvertido = True
            elif(palavras[1][0] != '/'):
                print("Erro: Endereco deve ser hexadecimal com valor de 0000 a FFFF comecando com /")
                erro = True
                break
            else:
                endereco_convertido = palavras[1][1]+palavras[1][2]+palavras[1][3]+palavras[1][4]
            
            CI = CI + tab_mnemonicos[palavras[0]]['tamanho']
            linha = arquivo.readline() #le nova linha
    for simbolo in tab_simbolos:
        if(tab_simbolos[simbolo]['status'] == 'indefinido'):
            print("Erro: simbolo não definido (" + simbolo + ")")
            erro = True
    if(erro == True):
        print("Erro ocorrido! Montagem não foi feita com sucesso")
    else: 
        print(CI)
        print(tab_simbolos)   
        passo == 2     
