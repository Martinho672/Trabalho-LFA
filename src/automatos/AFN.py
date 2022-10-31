from copy import deepcopy
from src.automatos.AFD import AFD


class AFN:
    def __init__(self, alfabeto):
        alfabeto = str(alfabeto)

        # Parâmetros do autômato
        self.estados = set()
        self.alfabeto = alfabeto
        self.transicoes = dict()
        self.iniciais = set()
        self.finais = set()

    def limpa_afn(self):
        # Resetando parâmetros de início
        self.__deu_erro = False
        self.__estado_atual = self.iniciais

    def cria_estado(self, id, inicial=False, final=False):
        estado = int(id)

        # Estado já presente no autômato
        if estado in self.estados:
            return False

        # Adicionando o novo estado
        self.estados = self.estados.union({estado})

        if inicial:
            self.iniciais = self.iniciais.union({estado})
        if final:
            self.finais = self.finais.union({estado})
        return True

    def cria_transicao(self, orig, dest, simb):
        origem = int(orig)
        destino = int(dest)
        simbolo = str(simb)

        if simb == "":
            # Checando se os estados e a cadeia pertencem ao autômato
            if not origem in self.estados:
                return False
            if not destino in self.estados:
                return False
        else:
            # Checando se os estados e a cadeia pertencem ao autômato
            if not origem in self.estados:
                return False
            if not destino in self.estados:
                return False
            if len(simbolo) != 1 or not simbolo in self.alfabeto:
                return False

        if (origem, simbolo) in self.transicoes:
            self.transicoes[(origem, simbolo)] = self.transicoes[(origem, simbolo)].union({destino})
        else:
            self.transicoes[(origem, simbolo)] = set()
            self.transicoes[(origem, simbolo)] = set.union({destino})

        return True

    def muda_estado_inicial(self, id):
        if not id in self.estados:
            return

        self.iniciais = self.iniciais.union({id})

    def muda_estado_final(self, id, final):
        if not id in self.estados:
            return

        if final:
            self.finais = self.finais.union({id})
        else:
            self.finais = self.finais.difference({id})

    def deu_erro(self):
        return self.__deu_erro

    def estado_autal(self):
        return self.__estado_atual

    def estado_final(self, id):
        return id in self.finais

    def get_transicoes_from_estado(self, estado):
        resp = list()
        for (e, s) in self.transicoes:
            if e == estado:
                resp.append((s, self.transicoes[(e, s)]))

        return resp

    ######################################################################
    #
    # - Métodos para conversão de AFNs para AFDs
    #
    ######################################################################

    # Algoritmo que converte um AFN com transições vazias para um AFN sem transições vazias
    def converte_afn_lambda_para_afn(self, afn_lambda):
        afn_retorno = self.copiar_afn()

        if self.has_transicoes_vazias(afn_retorno):
            tabela_fecho_lambda = dict()
            for s in afn_retorno.estados:
                # Calcula-se o fecho-lambda para cada estado
                calc_lambda = self.__fecho_lambda(s, afn_retorno)

                """ Insere-se na tabela os valores de fecho-λ com cada símbolo da alfebto e seus respectivos destino
                    pelos seus fechos-λ """
                for letra in afn_retorno.alfabeto:
                    consumindo_letra = self.__calcular_transicoes_por_simbolo_pelo_fecho_lambda(letra, calc_lambda,
                                                                                                afn_retorno)

                    # Estados de destino do AFN convertido sem transições vazias
                    estados_destino_lambda = set()
                    for e in consumindo_letra:
                        estados_destino_lambda = estados_destino_lambda.union(self.__fecho_lambda(e, afn_retorno))

                    tabela_fecho_lambda[str(s) + " " + letra] = {
                        "fecho-lambda": calc_lambda,
                        letra: consumindo_letra,
                        "fecho-destino": estados_destino_lambda
                    }

            # Removendo-se as transições vazias do AFN-λ
            self.__remover_transicoes_vazias(afn_retorno)

            """ Após a construção da tabela, o conjunto de estados do "fecho-destino" serão o destino de cada estado
                consumindo a respectiva letra da tabela """
            for estado_letra in tabela_fecho_lambda:
                dupla_estado_letra = estado_letra.split(" ")

                origem = int(dupla_estado_letra[0])
                simbolo = dupla_estado_letra[1]
                estados_destino = tabela_fecho_lambda[estado_letra]["fecho-destino"]
                if len(estados_destino) > 0:
                    for destino in estados_destino:
                        afn_retorno.cria_transicao(origem, destino, simbolo)

            return afn_retorno

        return None

    def converte_afn_para_afd(self, afn) -> AFD:
        afn_a_converter = afn.copiar_afn()
        if afn.has_transicoes_vazias(afn):
            afn_a_converter = afn.converte_afn_lambda_para_afn(afn)

        afd = AFD(afn_a_converter.alfabeto)
        tabela_transicoes_afn, conjunto_estados_descobertos = self.__monta_tabela_transicoes_afn(afn)

        # Cada conjunto de estados descoberto será um estado único novo do AFD convertido
        label_estado = 0
        mapa_conjunto_estado_unico = dict()
        for c in conjunto_estados_descobertos:
            mapa_conjunto_estado_unico[str(c)] = label_estado
            label_estado += 1

        # Percorrendo-se a tabela e adicionando as transições ao autômato
        for conjunto_letra in tabela_transicoes_afn:
            estado_letra_separados = conjunto_letra.split("-")

            origem = mapa_conjunto_estado_unico[str(estado_letra_separados[0])]
            simbolo = estado_letra_separados[1]
            destino = mapa_conjunto_estado_unico[str(tabela_transicoes_afn[conjunto_letra]["destino"])]

            afd.cria_estado(origem)
            afd.cria_estado(destino)
            afd.cria_transicao(origem, destino, simbolo)

            value = tabela_transicoes_afn[conjunto_letra]

            if "inicial" in value:
                afd.muda_estado_inicial(origem)
            if "final" in value:
                afd.muda_estado_final(origem, True)

        return afd

    def __monta_tabela_transicoes_afn(self, afn) -> tuple:
        tabela_transicoes = dict()
        conjunto_estados_descobertos = list()
        conjunto_estados_descobertos.append(afn.iniciais)

        # Lista de estados usadas para a construção da tabela de transições
        conjunto_estados = list()
        conjunto_estados.append(afn.iniciais)

        # Primeiro, coloca-se o estado inicial no começo da tabela
        trans_destino = set()
        inicial_final = False

        for s in afn.alfabeto:
            # Resetando as transições de destino
            trans_destino = trans_destino.difference(trans_destino)

            for e in afn.iniciais:
                if (e, s) in afn.transicoes:
                    trans_destino = trans_destino.union(afn.transicoes[(e, s)])
                    if e in afn.finais:
                        inicial_final = True

            # Inserindo na tabela de transições que será convertida para o AFD
            if len(trans_destino) > 0:
                if inicial_final:
                    tabela_transicoes[str(afn.iniciais) + "-" + s] = {
                        "destino": trans_destino,
                        "inicial": True,
                        "final": True
                    }
                else:
                    tabela_transicoes[str(afn.iniciais) + "-" + s] = {
                        "destino": trans_destino,
                        "inicial": True
                    }

                # Caso haja um conjunto de estados novo descoberto, insere-o na lista de conjunto de estados descobertos
                if trans_destino not in conjunto_estados_descobertos:
                    conjunto_estados_descobertos.append(trans_destino)
                    conjunto_estados.append(trans_destino)

        # Tirando-se o estado inicial do conjunto de estados descobertos
        conjunto_estados.remove(afn.iniciais)

        # Percorrendo-se a lista de conjuntos para ir descobrindo os novos conjuntos de estados
        while len(conjunto_estados) > 0:
            conjunto_atual = conjunto_estados.pop(0)

            for s in afn.alfabeto:
                trans_destino = trans_destino.difference(trans_destino)

                for e in conjunto_atual:
                    if (e, s) in afn.transicoes:
                        trans_destino = trans_destino.union(afn.transicoes[(e, s)])

                # Verificando-se se há um conjunto de estado finais entre o conjunto atual
                if_final = False

                for estado in conjunto_atual:
                    if estado in afn.finais:
                        if_final = True

                # Insere-se na tabela de transições a transição nova descoberta

                if len(trans_destino) > 0:
                    if if_final:
                        tabela_transicoes[str(conjunto_atual) + "-" + s] = {
                            "destino": trans_destino,
                            "final": True
                        }
                    else:
                        tabela_transicoes[str(conjunto_atual) + "-" + s] = {
                            "destino": trans_destino
                        }

                    if trans_destino not in conjunto_estados_descobertos:
                        conjunto_estados_descobertos.append(trans_destino)
                        conjunto_estados.append(trans_destino)

        return tabela_transicoes, conjunto_estados_descobertos

    def __remover_transicoes_vazias(self, afn_lambda):
        for (orig, letra) in list(afn_lambda.transicoes):
            if letra == "":
                del afn_lambda.transicoes[(orig, letra)]

    def __calcular_transicoes_por_simbolo_pelo_fecho_lambda(self, simbolo: str, fecho_lambda: set, afn_lambda) -> set:
        estados_destino = set()

        for s in fecho_lambda:
            for (orig, letra) in afn_lambda.transicoes:
                if orig == s and letra == simbolo:
                    destino = afn_lambda.transicoes[(orig, letra)]
                    estados_destino = estados_destino.union(destino)

        return estados_destino

    # Verifica se o AFN dado possui transições vazias ou não
    def has_transicoes_vazias(self, afn_lambda):
        for (orig, letra) in afn_lambda.transicoes:
            if letra == "":
                return True

        return False

    # Calcula-se o fecho lambda do estado dado como parâmetro
    def __fecho_lambda(self, estado, afn_lambda):
        fecho_lambda = set()
        estados_acessiveis_por_lambda = list()
        estados_acessiveis_por_lambda.append(estado)

        while len(estados_acessiveis_por_lambda) > 0:
            estado_atual = estados_acessiveis_por_lambda.pop(0)
            fecho_lambda = fecho_lambda.union({estado_atual})

            for (orig, letra) in afn_lambda.transicoes:
                if orig == estado_atual and letra == "" and afn_lambda.transicoes[(orig, letra)] not in fecho_lambda:
                    estados_alcancados = afn_lambda.transicoes[(orig, letra)]
                    estados_acessiveis_por_lambda.extend(list(estados_alcancados))

        return fecho_lambda

    # Função para transicionar o autômato (mover entre estados atrvés da string de entrada)
    # AFN não poderá mais ter move e sim antes deverá converter de AFD
    def move(self, cadeia):
        afd_convertido = self.converte_afn_para_afd(self)
        afd_convertido.limpa_afd()
        parada = afd_convertido.move(cadeia)
        if not afd_convertido.deu_erro() and afd_convertido.estado_final(parada):
            return True
        return False

    def copiar_afn(self):
        return deepcopy(self)

    def __str__(self):
        # Retorna uma string descrevendo o autômato
        s = "AFN (E, A, T, I, F): \n"
        s += '\tE = { '
        for e in self.estados:
            s += '{}, '.format(str(e))

        s += ' } \n'
        s += '\tA = { '
        for a in self.alfabeto:
            s += "'{}', ".format(a)

        s += ' } \n'
        s += '\tT = { '
        for (e, a) in self.transicoes.keys():
            d = self.transicoes[(e, a)]
            s += "({}, '{}') --> ".format(e, a)
            s += "{ "
            for t in d:
                s += "{}, ".format(t)
            s += "}, "

        s += ' } \n'
        s += '\tI = { '
        for i in self.iniciais:
            s += '{}, '.format(str(i))
        s += ' } \n'

        s += '\tF = { '
        for e in self.finais:
            s += '{}, '.format(str(e))

        s += ' }'
        return s
