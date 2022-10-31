from src.automatos.AFD import AFD
from src.automatos.AFN import AFN
from src.utils.arquivo_util import ManipularArquivo
from src.utils.enum_operacoes_conjuntos import OperaceosConjuntos
import os


def __casos_teste_afd():
    opcao = 0

    afd = AFD("ab")
    for i in range(1, 5):
        afd.cria_estado(i)
    afd.muda_estado_inicial(1)
    afd.muda_estado_final(4, True)

    afd.cria_transicao(1, 2, "a")
    afd.cria_transicao(2, 1, "a")
    afd.cria_transicao(3, 4, "a")
    afd.cria_transicao(4, 3, "a")
    afd.cria_transicao(1, 3, "b")
    afd.cria_transicao(3, 1, "b")
    afd.cria_transicao(2, 4, "b")
    afd.cria_transicao(4, 2, "b")

    while True:
        print("Escolha uma das opções abaixo para se trabalhar com um AFD:\n"
              "0 - Voltar ao menu principal\n"
              "1 - Testar cadeias em um AFD\n"
              "2 - Importar um xml para um AFD\n"
              "3 - Exportar um AFD para xml\n")
        opcao = int(input("Digite a sua opção: -> "))

        if opcao == 0:
            break

        elif opcao == 1:
            print("\n\n{}\n\n".format(afd))
            cadeia = input("Digite a cadeia que deseja testar -> ").strip()
            afd.limpa_afd()
            parada = afd.move(cadeia)

            if not afd.deu_erro() and afd.estado_final(parada):
                print("Aceita a cadeia '{}'\n".format(cadeia))
            else:
                print("Não aceita a cadeia '{}'\n".format(cadeia))

        elif opcao == 2:
            arquivo = input("Digite o nome do arquivo que deseja importar -> ").strip()
            arq = ManipularArquivo()
            af = arq.xml_para_afd(arquivo, arq.extrair_alfabeto_do_xml(arquivo))

            if af is not None:
                print("AFD importado:\n {}\n\n".format(af))
                testar_afd = int(input("Deseja testar uma cadeia no AFD importado?\n1 - Sim\n"
                                       "2 - Não\n-> "))
                if testar_afd == 1:
                    cadeia = input("Digite a cadeia que deseja testar -> ").strip()
                    af.limpa_afd()
                    parada = af.move(cadeia)
                    if not af.deu_erro() and af.estado_final(parada):
                        print("Aceita a cadeia '{}'\n".format(cadeia))
                    else:
                        print("Não aceita a cadeia '{}'\n".format(cadeia))
            else:
                print("Insira um arquivo de um AFD válido!\n\n")

        elif opcao == 3:
            arquivo = input("Digite o nome do arquivo para o qual ele será exportado -> ").strip()
            arq = ManipularArquivo()
            arq.afd_para_xml(arquivo, afd)

            print("Arquivo exportado com sucesso.\n\n")


def __casos_teste_afn():
    opcao = 0

    afn = AFN("01")
    for i in range(1, 5):
        afn.cria_estado(i)

    afn.muda_estado_inicial(1)
    afn.muda_estado_final(4, True)

    afn.cria_transicao(1, 1, "0")
    afn.cria_transicao(1, 1, "1")
    afn.cria_transicao(1, 2, "1")
    afn.cria_transicao(2, 3, "0")
    afn.cria_transicao(2, 3, "1")
    afn.cria_transicao(3, 4, "0")
    afn.cria_transicao(3, 4, "1")

    while True:
        print("Escolha uma das opções abaixo para se trabalhar com um AFN:\n"
              "0 - Voltar ao menu principal\n"
              "1 - Testar cadeias em um AFN\n"
              "2 - Importar um xml para um AFN\n"
              "3 - Exportar um AFN para xml\n")
        opcao = int(input("Digite a sua opção: -> "))

        if opcao == 0:
            break
        elif opcao == 1:
            print("\n\n{}\n\n".format(afn))
            cadeia = input("Digite a cadeia que deseja testar -> ").strip()
            afn.limpa_afn()
            parada = afn.move(cadeia)

            if parada:
                print("Aceita a cadeia '{}'\n".format(cadeia))
            else:
                print("Não aceita a cadeia '{}'\n".format(cadeia))
        elif opcao == 2:
            arquivo = input("Digite o nome do arquivo que deseja importar -> ").strip()
            arq = ManipularArquivo()
            af = arq.xml_para_afn(arquivo, arq.extrair_alfabeto_do_xml(arquivo))

            print("AFN importado:\n {}\n\n".format(af))
            testar_afn = int(input("Deseja testar uma cadeia no AFN importado?\n1 - Sim\n"
                                   "2 - Não\n-> "))

            if testar_afn == 1:
                cadeia = input("Digite a cadeia que deseja testar -> ").strip()
                af.limpa_afn()
                parada = af.move(cadeia)
                if parada:
                    print("Aceita a cadeia '{}'\n".format(cadeia))
                else:
                    print("Não aceita a cadeia '{}'\n".format(cadeia))

        elif opcao == 3:
            arquivo = input("Digite o nome do arquivo para o qual ele será exportado -> ").strip()
            arq = ManipularArquivo()
            arq.afn_para_xml(arquivo, afn)

            print("Arquivo exportado com sucesso.\n\n")

    pass


def __casos_teste_minimiza_afds():
    # #-- PRIMEIRO AUTOMATO --#
    af1 = AFD("ab")
    for i in range(0, 6):
        af1.cria_estado(i)

    af1.muda_estado_inicial(0)
    af1.muda_estado_final(0, True)
    af1.muda_estado_final(4, True)
    af1.muda_estado_final(5, True)

    af1.cria_transicao(0, 1, "b")
    af1.cria_transicao(0, 2, "a")
    af1.cria_transicao(1, 1, "a")
    af1.cria_transicao(1, 0, "b")
    af1.cria_transicao(2, 4, "a")
    af1.cria_transicao(2, 5, "b")
    af1.cria_transicao(3, 5, "a")
    af1.cria_transicao(3, 4, "b")
    af1.cria_transicao(4, 3, "a")
    af1.cria_transicao(4, 2, "b")
    af1.cria_transicao(5, 2, "a")
    af1.cria_transicao(5, 3, "b")

    afmin1 = af1.minimiza_afd()
    print("1° AUTOMATO:\nORIGINAL:{}\n\nMINIMIZADO:{}".format(af1, afmin1))

    # #-- SEGUNDO AUTOMATO --#
    af2 = AFD("ab")
    for i in range(1, 7):
        af2.cria_estado(i)
    af2.muda_estado_inicial(1)
    af2.muda_estado_final(1, True)
    af2.muda_estado_final(2, True)
    af2.muda_estado_final(3, True)
    af2.muda_estado_final(4, True)
    af2.muda_estado_final(5, True)

    af2.cria_transicao(1, 6, "a")
    af2.cria_transicao(1, 4, "b")
    af2.cria_transicao(2, 1, "a")
    af2.cria_transicao(2, 3, "b")
    af2.cria_transicao(3, 3, "a")
    af2.cria_transicao(3, 5, "b")
    af2.cria_transicao(4, 6, "a")
    af2.cria_transicao(4, 5, "b")
    af2.cria_transicao(5, 6, "a")
    af2.cria_transicao(5, 5, "b")
    af2.cria_transicao(6, 2, "a")
    af2.cria_transicao(6, 3, "b")

    afmin2 = af2.minimiza_afd()
    print("2° AUTOMATO:\nORIGINAL:{}\n\nMINIMIZADO:{}".format(af2, afmin2))

    # #-- TERCEIRO AUTOMATO --#
    af3 = AFD("01")
    for i in range(0, 7):
        af3.cria_estado(i)

    af3.muda_estado_inicial(0)
    af3.muda_estado_final(5, True)
    af3.muda_estado_final(6, True)

    af3.cria_transicao(0, 1, "0")
    af3.cria_transicao(0, 3, "1")
    af3.cria_transicao(1, 5, "0")
    af3.cria_transicao(1, 4, "1")
    af3.cria_transicao(2, 0, "0")
    af3.cria_transicao(2, 4, "1")
    af3.cria_transicao(3, 6, "0")
    af3.cria_transicao(3, 4, "1")
    af3.cria_transicao(4, 4, "0")
    af3.cria_transicao(4, 4, "1")
    af3.cria_transicao(5, 5, "0")
    af3.cria_transicao(5, 5, "1")
    af3.cria_transicao(6, 6, "0")
    af3.cria_transicao(6, 6, "1")

    afmin3 = af3.minimiza_afd()
    print("3° AUTOMATO:\nORIGINAL:{}\n\nMINIMIZADO:{}".format(af3, afmin3))


def __casos_teste_multiplica_afd():
    op_conjunto = None
    opcao_op = int(input("Digite uma das opções abaixo para a operação de conjuntos:\n"
                         "1 - União\n"
                         "2 - Intercessão\n"
                         "3 - Diferença\n"
                         "4 - Complemento\n"
                         "-> "))

    if opcao_op == 1:
        op_conjunto = OperaceosConjuntos.UNIAO
    elif opcao_op == 2:
        op_conjunto = OperaceosConjuntos.INTERCESSAO
    elif opcao_op == 3:
        op_conjunto = OperaceosConjuntos.DIFERENCA
    elif opcao_op == 4:
        op_conjunto = OperaceosConjuntos.COMPLEMENTO

    # #-- PRIMEIRO AUTOMATO --#
    af1 = AFD("ab")
    for i in range(1, 4):
        af1.cria_estado(i)
    af1.muda_estado_inicial(1)
    af1.muda_estado_final(2, True)

    af1.cria_transicao(1, 3, "a")
    af1.cria_transicao(1, 2, "b")
    af1.cria_transicao(2, 1, "a")
    af1.cria_transicao(2, 2, "b")
    af1.cria_transicao(3, 3, "a")
    af1.cria_transicao(3, 2, "b")

    af2 = AFD("ab")
    for i in range(4, 6):
        af2.cria_estado(i)
    af2.muda_estado_inicial(4)
    af2.muda_estado_final(5, True)

    af2.cria_transicao(4, 5, "a")
    af2.cria_transicao(4, 4, "b")
    af2.cria_transicao(5, 4, "a")
    af2.cria_transicao(5, 5, "b")

    af_multiplicado1 = af1.multiplica_automatos(af1, af2, op_conjunto)
    print("1° AUTOMATO:\nAFD1:\n{}\n\nAFD2:\n{}\n\nMULTIPLICADO:\n{}\n\n".format(af1, af2, af_multiplicado1))

    # #-- SEGUNDO AUTOMATO --#
    af3 = AFD("ab")
    for i in range(0, 4):
        af3.cria_estado(i)

    af3.muda_estado_inicial(0)
    af3.muda_estado_final(0, True)
    af3.muda_estado_final(1, True)
    af3.muda_estado_final(2, True)

    af3.cria_transicao(0, 0, "a")
    af3.cria_transicao(0, 1, "b")
    af3.cria_transicao(1, 2, "a")
    af3.cria_transicao(1, 1, "b")
    af3.cria_transicao(2, 0, "a")
    af3.cria_transicao(2, 3, "b")
    af3.cria_transicao(3, 3, "a")
    af3.cria_transicao(3, 3, "b")

    af4 = AFD("ab")
    for i in range(4, 6):
        af4.cria_estado(i)

    af4.muda_estado_inicial(4)
    af4.muda_estado_final(4, True)

    af4.cria_transicao(4, 5, "a")
    af4.cria_transicao(4, 4, "b")
    af4.cria_transicao(5, 4, "a")
    af4.cria_transicao(5, 5, "b")

    af_multiplicado2 = af1.multiplica_automatos(af3, af4, op_conjunto)
    print("2° AUTOMATO:\nAFD1:\n{}\n\nAFD2:\n{}\n\nMULTIPLICADO:\n{}\n\n".format(af3, af4, af_multiplicado2))

    # #-- TERCEIRO AUTOMATO --#
    af5 = AFD("ab")
    for i in range(1, 6):
        af5.cria_estado(i)
    af5.muda_estado_inicial(1)
    af5.muda_estado_final(4, True)

    af5.cria_transicao(1, 2, "a")
    af5.cria_transicao(1, 1, "b")
    af5.cria_transicao(2, 3, "a")
    af5.cria_transicao(2, 5, "b")
    af5.cria_transicao(3, 4, "a")
    af5.cria_transicao(3, 5, "b")
    af5.cria_transicao(4, 4, "a")
    af5.cria_transicao(4, 4, "b")
    af5.cria_transicao(5, 2, "a")
    af5.cria_transicao(5, 5, "b")

    af6 = AFD("ab")
    for i in range(6, 11):
        af6.cria_estado(i)
    af6.muda_estado_inicial(6)
    af6.muda_estado_final(9, True)

    af6.cria_transicao(6, 6, "a")
    af6.cria_transicao(6, 7, "b")
    af6.cria_transicao(7, 10, "a")
    af6.cria_transicao(7, 8, "b")
    af6.cria_transicao(8, 10, "a")
    af6.cria_transicao(8, 9, "b")
    af6.cria_transicao(9, 9, "a")
    af6.cria_transicao(9, 9, "b")
    af6.cria_transicao(10, 10, "a")
    af6.cria_transicao(10, 7, "b")

    af3_multiplicado = af5.multiplica_automatos(af5, af6, op_conjunto)
    print("3° AUTOMATO:\nAFD1:\n{}\n\nAFD2:\n{}\n\nMULTIPLICADO:\n{}\n\n".format(af5, af6, af3_multiplicado))


def __casos_teste_equivalencia_automatos():
    # #-- PRIMEIRO AUTOMATO --#
    af1 = AFD("ab")
    for i in range(1, 4):
        af1.cria_estado(i)

    af1.muda_estado_inicial(1)
    af1.muda_estado_final(2, True)

    af1.cria_transicao(1, 3, "a")
    af1.cria_transicao(1, 2, "b")
    af1.cria_transicao(2, 1, "a")
    af1.cria_transicao(2, 2, "b")
    af1.cria_transicao(3, 3, "a")
    af1.cria_transicao(3, 2, "b")

    af2 = AFD("ab")
    for i in range(4, 6):
        af2.cria_estado(i)

    af2.muda_estado_inicial(4)
    af2.muda_estado_final(5, True)

    af2.cria_transicao(4, 5, "a")
    af2.cria_transicao(4, 4, "b")
    af2.cria_transicao(5, 4, "a")
    af2.cria_transicao(5, 5, "b")

    print("\nAFD1:\n{}\n\nAFD2:\n{}\n\n".format(af1, af2))
    if af1.is_afds_equivalentes(af1, af2):
        print("Automatos equivalentes\n\n")
    else:
        print("Automatos não são equivalentes\n\n")

    # #-- SEGUNDO AUTOMATO --#
    af3 = AFD("a")
    af3.cria_estado(0)
    af3.muda_estado_final(0, True)
    af3.muda_estado_inicial(0)
    af3.cria_transicao(0, 0, "a")

    af4 = AFD("a")
    for i in range(1, 3):
        af4.cria_estado(i)
    af4.muda_estado_inicial(1)
    af4.muda_estado_final(1, True)
    af4.muda_estado_final(2, True)

    af4.cria_transicao(1, 2, "a")
    af4.cria_transicao(2, 1, "a")

    print("\nAFD1:\n{}\n\nAFD2:\n{}\n\n".format(af3, af4))
    if af3.is_afds_equivalentes(af3, af4):
        print("Automatos equivalentes\n\n")
    else:
        print("Automatos não são equivalentes\n\n")

    # #-- SEGUNDO AUTOMATO --#
    af5 = AFD("ab")
    for i in range(1, 7):
        af5.cria_estado(i)
    af5.muda_estado_inicial(0)
    af5.muda_estado_final(4, True)
    af5.muda_estado_final(5, True)
    af5.muda_estado_final(0, True)

    af5.cria_transicao(0, 1, "b")
    af5.cria_transicao(0, 2, "a")
    af5.cria_transicao(1, 1, "a")
    af5.cria_transicao(1, 0, "b")
    af5.cria_transicao(2, 4, "a")
    af5.cria_transicao(2, 5, "b")
    af5.cria_transicao(3, 5, "a")
    af5.cria_transicao(3, 4, "b")
    af5.cria_transicao(4, 3, "a")
    af5.cria_transicao(4, 2, "b")
    af5.cria_transicao(5, 2, "a")
    af5.cria_transicao(5, 3, "b")

    af6 = AFD("ab")
    for i in range(7, 12):
        af6.cria_estado(i)
    af6.muda_estado_inicial(7)
    af6.muda_estado_final(8, True)
    af6.muda_estado_final(9, True)

    af6.cria_transicao(7, 8, "a")
    af6.cria_transicao(7, 9, "b")
    af6.cria_transicao(8, 8, "a")
    af6.cria_transicao(8, 10, "b")
    af6.cria_transicao(9, 11, "a")
    af6.cria_transicao(9, 9, "b")
    af6.cria_transicao(10, 8, "a")
    af6.cria_transicao(10, 10, "b")
    af6.cria_transicao(11, 11, "a")
    af6.cria_transicao(11, 9, "b")

    print("\nAFD1:\n{}\n\nAFD2:\n{}\n\n".format(af5, af6))
    if af5.is_afds_equivalentes(af5, af6):
        print("Automatos equivalentes\n\n")
    else:
        print("Automatos não são equivalentes\n\n")


def __casos_teste_conversao_afn_lambda_para_afn():
    # #-- PRIMEIRO AUTOMATO --#
    afn_lambda1 = AFN("ab")
    for i in range(0, 5):
        afn_lambda1.cria_estado(i)
    afn_lambda1.muda_estado_inicial(0)
    afn_lambda1.muda_estado_final(1, True)
    afn_lambda1.muda_estado_final(4, True)

    afn_lambda1.cria_transicao(0, 1, "")
    afn_lambda1.cria_transicao(0, 2, "")
    afn_lambda1.cria_transicao(1, 3, "a")
    afn_lambda1.cria_transicao(2, 1, "a")
    afn_lambda1.cria_transicao(2, 4, "b")
    afn_lambda1.cria_transicao(2, 3, "")
    afn_lambda1.cria_transicao(3, 1, "a")
    afn_lambda1.cria_transicao(3, 1, "b")
    afn_lambda1.cria_transicao(3, 2, "b")
    afn_lambda1.cria_transicao(4, 4, "a")
    afn_lambda1.cria_transicao(4, 2, "b")

    afn1 = afn_lambda1.converte_afn_lambda_para_afn(afn_lambda1)
    print("1° AUTOMATO:\nORIGINAL:{}\n\nSEM TRANSIÇÕES VAZIAS:{}\n\n".format(afn_lambda1, afn1))

    # #-- SEGUNDO AUTOMATO --#
    afn_lambda2 = AFN("abc")
    for i in range(1, 5):
        afn_lambda2.cria_estado(i)
    afn_lambda2.muda_estado_inicial(1)
    afn_lambda2.muda_estado_final(4, True)

    afn_lambda2.cria_transicao(1, 2, "")
    afn_lambda2.cria_transicao(1, 3, "a")
    afn_lambda2.cria_transicao(2, 2, "a")
    afn_lambda2.cria_transicao(2, 4, "b")
    afn_lambda2.cria_transicao(3, 3, "b")
    afn_lambda2.cria_transicao(3, 4, "")
    afn_lambda2.cria_transicao(4, 4, "c")

    afn2 = afn_lambda2.converte_afn_lambda_para_afn(afn_lambda2)
    print("2° AUTOMATO:\nORIGINAL:{}\n\nSEM TRANSIÇÕES VAZIAS:{}\n\n".format(afn_lambda2, afn2))

    # #-- TERCEIRO AUTOMATO --#
    afn_lambda3 = AFN("ab")
    for i in range(0, 6):
        afn_lambda3.cria_estado(i)

    afn_lambda3.muda_estado_inicial(0)
    afn_lambda3.muda_estado_final(5, True)

    afn_lambda3.cria_transicao(0, 1, "")
    afn_lambda3.cria_transicao(0, 2, "")
    afn_lambda3.cria_transicao(0, 3, "")
    afn_lambda3.cria_transicao(1, 3, "a")
    afn_lambda3.cria_transicao(2, 3, "b")
    afn_lambda3.cria_transicao(3, 2, "a")
    afn_lambda3.cria_transicao(3, 4, "b")
    afn_lambda3.cria_transicao(4, 4, "a")
    afn_lambda3.cria_transicao(4, 5, "")

    afn3 = afn_lambda3.converte_afn_lambda_para_afn(afn_lambda3)
    print("3° AUTOMATO:\nORIGINAL:{}\n\nSEM TRANSIÇÕES VAZIAS:{}\n\n".format(afn_lambda3, afn3))


def __casos_teste_conversao_afn_afd():
    # #-- PRIMEIRO AUTOMATO --#
    afn1 = AFN("01")
    for i in range(0, 3):
        afn1.cria_estado(i)
    afn1.muda_estado_inicial(0)
    afn1.muda_estado_final(2, True)

    afn1.cria_transicao(0, 0, "0")
    afn1.cria_transicao(0, 1, "0")
    afn1.cria_transicao(0, 0, "1")
    afn1.cria_transicao(1, 2, "1")

    afd1 = afn1.converte_afn_para_afd(afn1)
    print("1° AUTOMATO:\nORIGINAL:{}\n\nAFD CONVERTIDO:{}\n\n".format(afn1, afd1))

    # #-- SEGUNDO AUTOMATO --#
    afn2 = AFN("ab")
    for i in range(0, 5):
        afn2.cria_estado(i)
    afn2.muda_estado_inicial(0)
    afn2.muda_estado_final(1, True)
    afn2.muda_estado_final(4, True)

    afn2.cria_transicao(0, 1, "a")
    afn2.cria_transicao(0, 3, "a")
    afn2.cria_transicao(0, 3, "b")
    afn2.cria_transicao(0, 4, "b")
    afn2.cria_transicao(0, 2, "b")
    afn2.cria_transicao(1, 3, "a")
    afn2.cria_transicao(2, 1, "a")
    afn2.cria_transicao(2, 1, "b")
    afn2.cria_transicao(3, 3, "b")
    afn2.cria_transicao(3, 1, "a")
    afn2.cria_transicao(3, 2, "b")
    afn2.cria_transicao(4, 4, "a")
    afn2.cria_transicao(4, 3, "b")
    afn2.cria_transicao(4, 2, "b")

    afd2 = afn2.converte_afn_para_afd(afn2)
    print("2° AUTOMATO:\nORIGINAL:{}\n\nAFD CONVERTIDO:{}\n\n".format(afn2, afd2))

    # #-- TERCEIRO AUTOMATO --#
    afn3 = AFN("ab")
    for i in range(1, 4):
        afn3.cria_estado(i)
    afn3.muda_estado_final(3, True)
    afn3.muda_estado_inicial(1)
    afn3.muda_estado_inicial(2)
    afn3.muda_estado_inicial(3)

    afn3.cria_transicao(1, 3, "a")
    afn3.cria_transicao(2, 3, "b")
    afn3.cria_transicao(3, 2, "a")

    afd3 = afn3.converte_afn_para_afd(afn3)
    print("3° AUTOMATO:\nORIGINAL:{}\n\nAFD CONVERTIDO:{}\n\n".format(afn3, afd3))


if __name__ == '__main__':
    escolha_menu = -1

    while escolha_menu != 0:
        print("## -- TRABALHO LFA - MANIPULAÇÃO DE AUTOMATOS -- ##\nDigite um dos números correspondentes a uma"
              " das opções abaixo:\n\n"
              "0 - Sair\n"
              "1 - Testar um AFD.\n"
              "2 - Testar um AFN.\n"
              "3 - Testar multiplicação de autômatos.\n"
              "4 - Testar minimização de autômatos.\n"
              "5 - Testar equivalência de autômatos.\n"
              "6 - Testar conversão de AFN-λ para AFN.\n"
              "7 - Testar conversão de AFN para AFD.")
        escolha_menu = int(input("Digite a sua opção: -> "))

        if escolha_menu == 0:
            break
        elif escolha_menu == 1:
            __casos_teste_afd()
        elif escolha_menu == 2:
            __casos_teste_afn()
        elif escolha_menu == 3:
            __casos_teste_multiplica_afd()
        elif escolha_menu == 4:
            __casos_teste_minimiza_afds()
        elif escolha_menu == 5:
            __casos_teste_equivalencia_automatos()
        elif escolha_menu == 6:
            __casos_teste_conversao_afn_lambda_para_afn()
        elif escolha_menu == 7:
            __casos_teste_conversao_afn_afd()
