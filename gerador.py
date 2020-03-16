from base64 import b64decode
import requests
import numpy as np

def document(dados):
    tam = len(dados["cdbv"])
    vetor = np.empty([tam, 2], dtype="S20")

    for a in range(tam):
        vetor[a][0] = dados["cdbv"][a]["document"]
        vetor[a][1] = dados["cdbv"][a]["nameOrCompany"]

    return vetor

while True:  # Loop
    read_ccb = input("CCB: \n")

    parametros = {"ccbNumber": read_ccb}
    
    # Link da API
    dadosgeral = requests.get('link_api1', params=parametros)
    status_api = dadosgeral.status_code

    # Verificar status da API 1
    if status_api != 200:  # CCB inválida
        print("Valor inválido!\n")
        continue

    dadosjson = dadosgeral.json()

    # document é o número referente a cada investidor em um determinado projeto

    dadosdocument = document(dadosjson)

    for i in range(len(dadosdocument)):
    
        # Inserir o link da API
        link = "link_api2" + read_ccb + "/" + str(dadosdocument[i][0]).lstrip("b'").strip("'")

        print(link)

        dadosespecifico = requests.get(link)

        # Verificar status da API 2
        status_api = dadosespecifico.status_code

        if status_api != 200:  # CCB inválida
            print("Valor inválido!\n")
            continue

        dadosespecificojson = dadosespecifico.json()

        b64 = dadosespecificojson["pdfDocument"].strip('data:application/pdf;base64,')

        arq = b64decode(b64, validate=True)

        filename = str(dadosdocument[i][1]).lstrip("b'").strip("'") + ".pdf"
        f = open(filename, 'wb')
        f.write(arq)
        f.close()
