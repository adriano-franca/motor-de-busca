#Trabalo de Guilher dos reis e Adriano franca
import xml.etree.ElementTree as ET

def carregar_dados(caminho_arquivo):
    tree = ET.parse(caminho_arquivo)
    return tree.getroot()


def buscar(palavras, indice, id_texto):#funcao que busca na biblioteca a/s palavra/s fornecida
    palavras = [palavra.lower() for palavra in palavras]

    for palavra in palavras:#verificacao se nao e um stopword
        if len(palavra)<4:
            print("Palavra fornecida com menos de 4 caracteres")
            return[]

        elif palavra not in indice:
            return []

    if len(palavras) == 1:#quando e passado so uma palavra 
        busca = palavras[0]
        ocorrencias = indice[busca]["ids"]
        ranking = []

        for id_verbete, count in ocorrencias.items():
            proporcao = calcular_ocorrencia(busca, id_verbete, id_texto)#calcula a porcentagem pra colocar numa nova lista que sera exibida
            ranking.append((id_verbete, proporcao))

    elif len(palavras) == 2:#quando e passado duas palavras
        palavra1, palavra2 = palavras
        ids_palavra1 = set(indice[palavra1]["ids"].keys())
        ids_palavra2 = set(indice[palavra2]["ids"].keys())
        ids_com_as_duas_palavras = ids_palavra1 & ids_palavra2#verifica os ids que  tem as duas palavras ao mesmo tempo

        if not ids_com_as_duas_palavras:
            return []

        ranking = []
        for id in ids_com_as_duas_palavras:
            proporcao = calcular_ocorrencia(palavra1, id, id_texto) + calcular_ocorrencia(palavra2, id, id_texto)
            ranking.append((id, proporcao))

    else:
        raise ValueError("A função aceita apenas uma ou duas palavras para busca.")

    ranking.sort(key=lambda x: x[1], reverse=True)
    return ranking


def calcular_ocorrencia(busca, id, id_texto):
    text = id_texto.get(id, {}).get('text', "").lower()
    titulo = id_texto.get(id, {}).get('title', "").lower()
    palavras = [word for word in text.split() if len(word) > 3]#separa todas as palavras do texto se tiverem mais de 3 caracteres
    
    cont_ocorrencias = palavras.count(busca)
    cont_total_palavras = len(palavras)
    resultado = cont_ocorrencias / cont_total_palavras
    if busca in titulo:#faz o acrescimo de 10%
        resultado *= 1.1
    if cont_total_palavras == 0:
        return 0
    
    return resultado


def exibir_resultados(ranking, id_texto, palavras, max_resultados=5):
    total = min(len(ranking), max_resultados)
    
    for i in range(total):
        res_id, proporcao = ranking[i]
        titulo = id_texto.get(res_id, {}).get('title')
        print(f"Título: {titulo}")
        print(f"Proporção para as palavras '{', '.join(palavras)}': {proporcao * 100:.2f}%")
        print(f"ID: {res_id}\n")


def criar_indice(root):
    indice = {}
    id_texto = {}
    
    for child in root:
        id = child.find('id').text.lower()
        title = child.find('title').text.lower()  
        text = child.find('text').text.lower()  
        
        id_texto[id] = {"title": title, "text": text}#cria um indice onde cada id ta atrelado ao seu titulo e texto pra nao precisar percorrrer o arquivo todo toda vez e sim ir direto pro id
        
        for word in text.split():
            if len(word) > 3:
                if word not in indice:
                    indice[word] = {"frequencia_total": 0, "ids": {}}#cria um indice(biblioteca) pra cada palavra onde vao ter as frequencias que foram vistas e uma lista dos id que foram encontradas
                
                indice[word]["frequencia_total"] += 1
                if id in indice[word]["ids"]:
                    indice[word]["ids"][id] += 1
                else:
                    indice[word]["ids"][id] = 1
    
    return indice, id_texto


def main():
    caminho_arquivo = './verbetesWikipedia.xml'
    root = carregar_dados(caminho_arquivo)#criando arvore do arquivo
    
    Biblioteca, id_texto = criar_indice(root)
    continuar = True
    while continuar:#loop pra buscar
        palavras = input("Digite os termos que deseja buscar (uma ou duas palavras): ").split()
        
        if 1 <= len(palavras) <= 2:#condicao pra nao pesquisar mais de 2 palavras
            ranking = buscar(palavras, Biblioteca, id_texto)
            if not ranking:
                print("Nenhum resultado encontrado para o termo.")
            else:
                exibir_resultados(ranking, id_texto, palavras)
            
            teste = input("Digite '1' para continuar ou qualquer outra tecla para sair: ")
            if teste != "1":
                continuar = False
        else:
            print("Sua pesquisa deve conter no máximo duas palavras.")
        

if __name__ == "__main__":
    main()