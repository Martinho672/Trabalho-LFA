import xml.etree.ElementTree as ET
from src.automatos.AFD import AFD
from src.automatos.AFN import AFN


# noinspection SpellCheckingInspection
class ManipularArquivo:

    def afd_para_xml(self, nome_arquivo: str, af: AFD) -> None:
        estrutura = ET.Element('structure')
        tipo = ET.SubElement(estrutura, 'type')
        tipo.text = "fa"
        automato = ET.SubElement(estrutura, "automaton")

        id_estados = [i for i in af.estados]
        estados_xml = [ET.SubElement(automato, "state") for _ in id_estados]

        # Percorrendo-se os estados
        for i in range(0, len(estados_xml)):
            estados_xml[i].set("id", str(id_estados[i]))
            estados_xml[i].set("name", str(id_estados[i]))

            if id_estados[i] == af.inicial:
                ET.SubElement(estados_xml[i], "initial")
            if id_estados[i] in af.finais:
                ET.SubElement(estados_xml[i], "final")

        # Percorrendo-se as transições
        trans = list()
        for (orig, letra) in af.transicoes:
            trans.append(ET.SubElement(automato, "transition"))
            ultima_trans = trans[-1]

            origem = ET.SubElement(ultima_trans, "from")
            origem.text = str(orig)

            destino = ET.SubElement(ultima_trans, "to")
            destino.text = str(af.transicoes[(orig, letra)])

            palavra = ET.SubElement(ultima_trans, "read")
            palavra.text = str(letra)

        # Escrevendo para o arquivo
        dados = ET.tostring(estrutura)
        arquivo = open(nome_arquivo, "w")
        arquivo.write(str(dados, "utf-8"))

    def extrair_alfabeto_do_xml(self, nome_arquivo: str) -> str:
        root = ET.parse(nome_arquivo).getroot()
        alfabeto = ""

        for child in root:
            for tag in child:
                if tag.tag == "transition":
                    for t in tag:
                        if t.tag == "read":
                            if t.text is not None and t.text not in alfabeto:
                                alfabeto += t.text

        return "".join(sorted(alfabeto))

    def __is_xml_nao_determinista(self, nome_arquivo: str) -> bool:
        root = ET.parse(nome_arquivo).getroot()
        trans_passadas = list()

        for child in root:
            for tag in child:
                if tag.tag == "transition":
                    origem = -1
                    letra = ""
                    for trans in tag:
                        if trans.tag == "from":
                            origem = int(trans.text)
                        elif trans.tag == "read":
                            # Caso de transição vazia (não determinismo)
                            if trans.text is None:
                                return True
                            letra = trans.text
                    trans_passadas.append((origem, letra))

        # Verificando se há um estado de origem e letra duplicados (caso de não determinismo)
        res = list(set([e for e in trans_passadas if trans_passadas.count(e) > 1]))
        if len(res) >= 1:
            return True

        return False

    def afn_para_xml(self, nome_arquivo: str, af: AFN):
        estrutura = ET.Element('structure')
        tipo = ET.SubElement(estrutura, 'type')
        tipo.text = "fa"
        automato = ET.SubElement(estrutura, "automaton")

        id_estados = [i for i in af.estados]  # s
        estados_xml = [ET.SubElement(automato, "state") for _ in id_estados]  # states

        # Percorrendo-se os estados
        for i in range(0, len(estados_xml)):
            estados_xml[i].set("id", str(id_estados[i]))
            estados_xml[i].set("name", str(id_estados[i]))

            if id_estados[i] in af.iniciais:
                ET.SubElement(estados_xml[i], "initial")
            if id_estados[i] in af.finais:
                ET.SubElement(estados_xml[i], "final")

        # Percorrendo-se as transições
        transicoes = list()
        for s in id_estados:
            transicao = af.get_transicoes_from_estado(s)

            for t in transicao:
                # Percorrendo-se os estados de destino do AFN
                for d in t[1]:
                    transicoes.append(ET.SubElement(automato, "transition"))
                    ultima_trans = transicoes[-1]

                    origem = ET.SubElement(ultima_trans, "from")
                    origem.text = str(s)

                    destino = ET.SubElement(ultima_trans, "to")
                    destino.text = str(d)

                    palavra = ET.SubElement(ultima_trans, "read")
                    if t[0] == "":
                        palavra.text = None
                    else:
                        palavra.text = str(t[0])

        # Escrevendo para o arquivo
        dados = ET.tostring(estrutura)
        arquivo = open(nome_arquivo, "w")
        arquivo.write(str(dados, "utf-8"))

    def xml_para_afd(self, nome_arquivo: str, alfabeto: str) -> AFD or None:
        root = ET.parse(nome_arquivo).getroot()

        # Se o xml for de um AFN, retorna nada
        if self.__is_xml_nao_determinista(nome_arquivo):
            return None

        # Caso contrário, continua o processo de extrair os dados do xml para o AFD
        afd = AFD(alfabeto)

        for child in root:
            for tag in child:
                # Percorrendo estados do xml
                if tag.tag == "state":
                    afd.cria_estado(int(tag.attrib["id"]))
                    for state in tag:
                        if state.tag == "initial":
                            afd.muda_estado_inicial(int(tag.attrib["id"]))
                        if state.tag == "final":
                            afd.muda_estado_final(int(tag.attrib["id"]), True)
                # Percorrendo transições do xml
                elif tag.tag == "transition":
                    origem = -1
                    palavra = ""
                    destino = -1
                    for trans in tag:
                        if trans.tag == "from":
                            origem = int(trans.text)
                        elif trans.tag == "read":
                            if trans.text is not None:
                                palavra = trans.text
                        elif trans.tag == "to":
                            destino = int(trans.text)

                    afd.cria_transicao(origem, destino, palavra)

        return afd

    def xml_para_afn(self, nome_arquivo: str, alfabeto: str) -> AFN:
        root = ET.parse(nome_arquivo).getroot()
        afn = AFN(alfabeto)

        for child in root:
            for tag in child:
                # Percorrendo estados do xml
                if tag.tag == "state":
                    afn.cria_estado(int(tag.attrib["id"]))
                    for state in tag:
                        if state.tag == "initial":
                            afn.muda_estado_inicial(int(tag.attrib["id"]))
                        if state.tag == "final":
                            afn.muda_estado_final(int(tag.attrib["id"]), True)
                # Percorrendo transições do xml
                elif tag.tag == "transition":
                    origem = -1
                    palavra = ""
                    destino = -1
                    for trans in tag:
                        if trans.tag == "from":
                            origem = int(trans.text)
                        elif trans.tag == "read":
                            if trans.text is None:
                                palavra = ""
                            else:
                                palavra = trans.text
                        elif trans.tag == "to":
                            destino = int(trans.text)

                    afn.cria_transicao(origem, destino, palavra)

        return afn
