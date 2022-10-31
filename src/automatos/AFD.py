from copy import deepcopy
from src.utils.enum_tabela_estados import CelulasTabela
from src.utils.enum_operacoes_conjuntos import OperaceosConjuntos


class AFD:
    def __init__(self, alfabeto):
        alfabeto = str(alfabeto)

        # Parâmetros do autômato
        self.estados = set()
        self.alfabeto = alfabeto
        self.transicoes = dict()  # No AFN as transições vão ser diferentes (o destino é um conjunto de estados)
        self.inicial = None  # No AFN pode ter mais de 1 estado inicial
        self.finais = set()

    def limpa_afd(self):
        # Resetando os parâmetros para o início da execução do autômato
        self.__deu_erro = False
        self.__estado_atual = self.inicial

    # Cria-se um estado com o identificador "id"
    def cria_estado(self, id, inicial=False, final=False):
        estado = int(id)

        # Estado já presente no autômato
        if estado in self.estados:
            return False

        # Faz-se a união de conjuntos com os estados do autômato com o estado novo para adicioná-lo no conjunto
        self.estados = self.estados.union({estado})
        if inicial:
            self.inicial = estado
        if final:
            self.finais = self.finais.union({estado})
        return True

    # Cria a transição (origem, simbolo) --> destino
    def cria_transicao(self, orig, dest, simb):
        origem = int(orig)
        destino = int(dest)
        simbolo = str(simb)

        # Checando se os estados e a cadeia pertencem ao autômato
        if not origem in self.estados:
            return False
        if not destino in self.estados:
            return False
        if len(simbolo) != 1 or not simbolo in self.alfabeto:
            return False

        self.transicoes[(origem, simbolo)] = destino
        return True

    def muda_estado_inicial(self, id):
        if not id in self.estados:
            return

        self.inicial = id

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

    ######################################################################
    #
    # - Métodos para minimização e equivalência de estados e automatos
    #
    ######################################################################

    # Método para retornar um conjunto contendo os estados inacessíveis do AFD
    def __encontrar_estados_inacessiveis(self, afd_minimizado) -> set:
        estados_acessiveis = list()
        estados_retorno = list()
        estados_acessiveis.append(afd_minimizado.inicial)

        while len(estados_acessiveis) > 0:
            estado_atual = estados_acessiveis.pop(0)
            estados_retorno.append(estado_atual)

            for s in afd_minimizado.alfabeto:
                for (orig, letra) in afd_minimizado.transicoes:
                    if orig == estado_atual and letra == s and afd_minimizado.transicoes[(orig, letra)] not in \
                            estados_retorno:
                        estados_acessiveis.append(afd_minimizado.transicoes[(orig, letra)])

        return afd_minimizado.estados.difference(set(estados_retorno))

    # Método para determinar se 2 AFD são equivalentes
    def is_afds_equivalentes(self, af1, af2) -> bool:
        af_unico = self.__transforma_2_afs_em_um_unico(af1, af2)
        tabela_estados = self.__constroi_tabela_estados(af_unico)

        if self.__is_afd_completo(af_unico):
            # Marcando os estados trivialmente não equivalentes
            self.__marca_trivialidade_estados(tabela_estados, af_unico)

            # Percorrendo-se cada célula da tabela
            for (e1, e2) in list(tabela_estados):
                if tabela_estados[(e1, e2)]["res"] == CelulasTabela.INDETERMINADO:
                    # Checando-se as transições dos 2 estados e atualizando a tabela
                    self.__checa_transicoes_estados(e1, e2, af_unico, tabela_estados)

                if ((e1 == af1.inicial and e2 == af2.inicial) or (e2 == af1.inicial and e1 == af2.inicial)) and \
                        tabela_estados[(e1, e2)]["res"] == CelulasTabela.NAO_EQUIVALENTE:
                    return False

            # Os estados que sobraram com marcações de "indeterminado" são equivalentes
            estados_equivalentes = list()
            for (e1, e2) in tabela_estados:
                if tabela_estados[(e1, e2)]["res"] == CelulasTabela.INDETERMINADO:
                    estados_equivalentes.append((e1, e2))

            """ Agora, na tabela de estados, se os estados iniciais dos 2 automatos são equivalentes, então
                os automatos são equivalentes"""
            for (e1, e2) in estados_equivalentes:
                if (e1 == af1.inicial and e2 == af2.inicial) or (e2 == af1.inicial and e1 == af2.inicial):
                    return True

        return False

    # Método para considerar os 2 AFs como um só na construção do método de equivalência
    def __transforma_2_afs_em_um_unico(self, af1, af2):
        novo_alfabeto = af1.alfabeto
        for s in af2.alfabeto:
            if s not in novo_alfabeto:
                novo_alfabeto += s

        # Colocando-se os estados de cada AFD
        af_unico = AFD(novo_alfabeto)
        af_unico.estados = af1.estados.union(af2.estados)
        af_unico.finais = af1.finais.union(af2.finais)

        # Colocando-se as transições de cada AFD
        for (orig1, letra1) in af1.transicoes:
            af_unico.transicoes[(orig1, letra1)] = af1.transicoes[(orig1, letra1)]
        for (orig2, letra2) in af2.transicoes:
            af_unico.transicoes[(orig2, letra2)] = af2.transicoes[(orig2, letra2)]

        return af_unico

    # Método para minimizar o AFD
    def minimiza_afd(self):
        afd_minimizado = self.copiar_afd()

        estados_inacessiveis = self.__encontrar_estados_inacessiveis(afd_minimizado)
        self.__remover_estados_inacessiveis(estados_inacessiveis, afd_minimizado)
        tabela_estados = self.__constroi_tabela_estados(afd_minimizado)

        # Apenas minimiza se o AFD for completo.
        # A implementação descarta automaticamente os estados inacessíveis no processo
        if self.__is_afd_completo(afd_minimizado):
            self.__marca_trivialidade_estados(tabela_estados, afd_minimizado)

            # Percorrendo-se cada célula da tabela
            for (e1, e2) in list(tabela_estados):
                if tabela_estados[(e1, e2)]["res"] == CelulasTabela.INDETERMINADO:
                    # Checando-se as transições dos 2 estados e atualizando a tabela
                    self.__checa_transicoes_estados(e1, e2, afd_minimizado, tabela_estados)

            # Os estados que sobraram com marcações de "indeterminado" são equivalentes
            estados_equivalentes = list()
            for (e1, e2) in tabela_estados:
                if tabela_estados[(e1, e2)]["res"] == CelulasTabela.INDETERMINADO:
                    estados_equivalentes.append((e1, e2))

            # Mudando-se as transições do autômato minimzado
            while len(estados_equivalentes) > 0:
                eq1, eq2 = estados_equivalentes.pop(0)
                afd_minimizado.estados = afd_minimizado.estados.difference({eq1})

                if eq1 == afd_minimizado.inicial:
                    afd_minimizado.muda_estado_inicial(eq2)

                if eq1 in afd_minimizado.finais:
                    afd_minimizado.finais = afd_minimizado.finais.difference({eq1})

                for (orig, letra) in list(afd_minimizado.transicoes):
                    if afd_minimizado.transicoes[(orig, letra)] == eq1:
                        del afd_minimizado.transicoes[(orig, letra)]
                        afd_minimizado.transicoes[(orig, letra)] = eq2

                for s in afd_minimizado.alfabeto:
                    if (eq1, s) in afd_minimizado.transicoes:
                        del afd_minimizado.transicoes[(eq1, s)]

            return afd_minimizado

        return None

    # Checa as transições de cada par de estados na tabela de comparações de estados
    def __checa_transicoes_estados(self, e1, e2, afd_minimizado, tabela_estados: dict):
        tabela_transicoes = dict()

        for s in afd_minimizado.alfabeto:
            tabela_transicoes[(e1, s)] = afd_minimizado.transicoes[(e1, s)]
            tabela_transicoes[(e2, s)] = afd_minimizado.transicoes[(e2, s)]

        # Comparando-se o resultado das transições
        for s in afd_minimizado.alfabeto:
            dest1 = tabela_transicoes[(e1, s)]
            dest2 = tabela_transicoes[(e2, s)]

            if (dest1, dest2) in tabela_estados:
                if tabela_estados[(dest1, dest2)]["res"] == CelulasTabela.NAO_EQUIVALENTE:
                    tabela_estados[(e1, e2)]["res"] = CelulasTabela.NAO_EQUIVALENTE

                    # Marcando-se como não equivalente os estados nas suas pendências
                    if len(tabela_estados[(e1, e2)]["marcas"]) > 0:
                        for tupla_estados in tabela_estados[(e1, e2)]["marcas"]:
                            tabela_estados[(tupla_estados[0], tupla_estados[1])]["res"] = CelulasTabela.NAO_EQUIVALENTE

                    return
                else:
                    tabela_estados[(dest1, dest2)]["marcas"].append((e1, e2))

            elif (dest2, dest1) in tabela_estados:
                if tabela_estados[(dest2, dest1)]["res"] == CelulasTabela.NAO_EQUIVALENTE:
                    tabela_estados[(e1, e2)]["res"] = CelulasTabela.NAO_EQUIVALENTE

                    # Marcando-se como não equivalente os estados nas suas pendências
                    if len(tabela_estados[(e1, e2)]["marcas"]) > 0:
                        for tupla_estados in tabela_estados[(e1, e2)]["marcas"]:
                            tabela_estados[(tupla_estados[0], tupla_estados[1])]["res"] = CelulasTabela.NAO_EQUIVALENTE
                    return
                else:
                    tabela_estados[(dest2, dest1)]["marcas"].append((e1, e2))

    # Método para remover os estados inacessíveis
    def __remover_estados_inacessiveis(self, estados_inacessiveis: set, afd):
        if len(estados_inacessiveis) > 0:
            afd.estados = afd.estados.difference(estados_inacessiveis)

            # Removendo-se os estados finais
            for estado in estados_inacessiveis:
                if estado in afd.finais:
                    afd.finais = afd.finais.difference({estado})

            # Removendo-se a transições destes estados inacessíveis
            for (orig, letra) in list(afd.transicoes):
                if orig in estados_inacessiveis:
                    del afd.transicoes[(orig, letra)]

    # Método para marcar estados trivialmente não equivalente
    # Estados finais sempre serão diferentes dos demais
    def __marca_trivialidade_estados(self, tabela_estados: dict, afd):
        for (q, p) in tabela_estados:
            if (q in afd.finais and p not in afd.finais) or (q not in afd.finais and p in afd.finais):
                tabela_estados[(q, p)]["res"] = CelulasTabela.NAO_EQUIVALENTE

    # Método para determinar se o AFD é completo ou não
    def __is_afd_completo(self, afd) -> bool:
        for s in afd.estados:
            for letra in afd.alfabeto:
                if not (s, letra) in afd.transicoes:
                    return False
        return True

    # Constrói a tabela de comparação de estados para o processo de minimização e equivalência de autômatos
    def __constroi_tabela_estados(self, afd) -> dict:
        tabela_estados = dict()

        for i in afd.estados:
            for j in afd.estados:
                if j < i:
                    # Pra cada célula, inclui sobre se os estados são equivalente ou não e suas marcas
                    tabela_estados[(i, j)] = {
                        "res": CelulasTabela.INDETERMINADO,
                        "marcas": list()
                    }

        return tabela_estados

    ######################################################################
    #
    # - Métodos para multiplicação de autômatos
    #
    ######################################################################

    # Método para multiplicação de 2 automatos
    def multiplica_automatos(self, af1, af2, op_conjunto: OperaceosConjuntos):

        novo_alfabeto = af1.alfabeto
        for s in af2.alfabeto:
            if s not in novo_alfabeto:
                novo_alfabeto += s

        automato_multiplicado = AFD(novo_alfabeto)

        # Criando-se os estados do autômato multiplicado
        for i in range(0, (len(af1.estados) * len(af2.estados))):
            automato_multiplicado.cria_estado(i)

        mapa_estados = self.__monta_mapeamento_estados(automato_multiplicado, af1, af2)
        tabela_transicoes_simultaneas = self.__monta_tabela_transicoes_simultaneas(af1, af2,
                                                                                   automato_multiplicado.alfabeto)

        # Setando o estado incial
        for (s1, s2) in mapa_estados:
            if s1 == af1.inicial and s2 == af2.inicial:
                automato_multiplicado.muda_estado_inicial(mapa_estados[(s1, s2)])

        # Inserindo as transições no automato multiplicado
        for ((s1, s2), letra) in tabela_transicoes_simultaneas:
            if (s1, s2) in mapa_estados:
                # Pegando-se o estado de origem de acordo com o mapeamento de estados
                estado_orig = mapa_estados[(s1, s2)]
                q, p = tabela_transicoes_simultaneas[((s1, s2), letra)]

                # Pegando-se o estado de destino pelas transições simultâneas calculadas dos 2 AFDs
                if (q, p) in mapa_estados:
                    estado_destino = mapa_estados[(q, p)]
                    automato_multiplicado.cria_transicao(estado_orig, estado_destino, letra)

        # Calculando os estados finais
        self.__calcula_estados_finais(automato_multiplicado, af1, af2, op_conjunto, mapa_estados)

        return automato_multiplicado

    # Faz um mapeamento de estados para o AFD multiplicado
    # Faz uma correspondência de um estado do AFD para cada par de estados dos 2 AFDs usados na multiplicação
    def __monta_mapeamento_estados(self, afd_multiplicado, af1, af2) -> dict:
        mapeamento_estados = dict()
        lista_estados = list(afd_multiplicado.estados)

        for s1 in af1.estados:
            for s2 in af2.estados:
                e = lista_estados.pop(0)
                mapeamento_estados[(s1, s2)] = e

        return mapeamento_estados

    # Cálculo de estados finais para operações de conjuntos entre multiplicação de 2 AFDs
    def __calcula_estados_finais(self, afd_mult, af1, af2, op_conjunto: OperaceosConjuntos, mapa_estados: dict):
        estados_finais = set()

        # Verificando-se casa cada caso de operações de conjuntos
        if op_conjunto == OperaceosConjuntos.UNIAO:
            for (s1, s2) in mapa_estados:
                if s1 in af1.finais or s2 in af2.finais:
                    estados_finais = estados_finais.union({mapa_estados[(s1, s2)]})

        elif op_conjunto == OperaceosConjuntos.INTERCESSAO:
            for (s1, s2) in mapa_estados:
                if s1 in af1.finais and s2 in af2.finais:
                    estados_finais = estados_finais.union({mapa_estados[(s1, s2)]})

        elif op_conjunto == OperaceosConjuntos.COMPLEMENTO:
            for (s1, s2) in mapa_estados:
                if s1 not in af1.finais and s2 not in af2.finais:
                    estados_finais = estados_finais.union({mapa_estados[(s1, s2)]})

        elif op_conjunto == OperaceosConjuntos.DIFERENCA:
            for (s1, s2) in mapa_estados:
                if s1 in af1.finais and s2 not in af2.finais:
                    estados_finais = estados_finais.union({mapa_estados[(s1, s2)]})

        # Mudando o estado final de acordo com a operação de conjuntos
        afd_mult.finais = afd_mult.finais.union(estados_finais)

    # Tabela de transições simultâneas para o processo de multiplicação de AFDs
    def __monta_tabela_transicoes_simultaneas(self, af1, af2, alfabeto: str) -> dict:
        trans_simultaneas = dict()

        for letra in alfabeto:
            for s1 in af1.estados:
                for s2 in af2.estados:
                    if (s1, letra) in af1.transicoes and (s2, letra) in af2.transicoes:
                        dest1 = af1.transicoes[(s1, letra)]
                        dest2 = af2.transicoes[(s2, letra)]
                        trans_simultaneas[((s1, s2), letra)] = (dest1, dest2)

        return trans_simultaneas

    # Função para transicionar o autómato (mover entre estados atrvés da string de entrada)
    def move(self, cadeia):
        for simbolo in cadeia:
            if not simbolo in self.alfabeto:
                self.__deu_erro = True
                break

            # Verificando as transições
            if (self.__estado_atual, simbolo) in self.transicoes.keys():
                novo_estado = self.transicoes[(self.__estado_atual, simbolo)]
                self.__estado_atual = novo_estado
            else:
                self.__deu_erro = True
                break

        # Após percorrer todas as transições, retorna o estado em que se chegou
        return self.__estado_atual

    def copiar_afd(self):
        return deepcopy(self)

    def __str__(self):
        # Retorna uma string descrevendo o autômato
        s = "AFD (E, A, T, i, F): \n"
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
            s += "({}, '{}') --> {}, ".format(e, a, d)

        s += ' } \n'
        s += '\ti = {} \n'.format(self.inicial)
        s += '\tF = { '
        for e in self.finais:
            s += '{}, '.format(str(e))

        s += ' }'
        return s
