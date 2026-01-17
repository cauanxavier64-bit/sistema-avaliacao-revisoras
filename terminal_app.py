from regras import (
    cadastrar_revisora,
    listar_revisoras,
    listar_revisoras_ativas,
    alterar_status_revisora,
    avaliar_revisora_por_id,
    ranking_mensal,
    ranking_geral,
    relatorio_mensal,
    exportar_ranking_geral_excel,
    exportar_relatorio_mensal_excel,
    historico_revisora
)

from db import criar_tabelas

criar_tabelas()


# ===== MENUS =====
def menu_principal():
    print("\n=== MENU PRINCIPAL ===")
    print("1 - Gerenciar revisoras")
    print("2 - Avaliar revisora")
    print("3 - Ranking mensal (Top 3)")
    print("4 - Relatório mensal")
    print("5 - Ranking geral (mensal)")
    print("6 - Exportar ranking geral para Excel")
    print("7 - Exportar relatório mensal para Excel")
    print("8 - Histórico de uma revisora")
    print("0 - Sair")


def menu_revisoras():
    print("\n=== GERENCIAR REVISORAS ===")
    print("1 - Cadastrar revisora")
    print("2 - Listar revisoras")
    print("3 - Ativar revisora")
    print("4 - Inativar revisora")
    print("0 - Voltar")


# ===== LOOP PRINCIPAL =====
while True:
    menu_principal()
    opcao = input("Escolha uma opção: ")

    # ===== GERENCIAR REVISORAS =====
    if opcao == "1":
        while True:
            menu_revisoras()
            sub = input("Escolha uma opção: ")

            if sub == "1":
                nome = input("Nome da revisora: ")
                print("Sucesso!" if cadastrar_revisora(nome) else "Nome já cadastrado.")

            elif sub == "2":
                for nome, ativa in listar_revisoras():
                    print(f"- {nome} | {'Ativa' if ativa else 'Inativa'}")

            elif sub == "3":
                alterar_status_revisora(input("Nome: "), 1)
                print("Revisora ativada.")

            elif sub == "4":
                alterar_status_revisora(input("Nome: "), 0)
                print("Revisora inativada.")

            elif sub == "0":
                break

            else:
                print("Opção inválida.")

    # ===== AVALIAR REVISORA =====
    elif opcao == "2":
        revisoras = listar_revisoras_ativas()

        if not revisoras:
            print("Nenhuma revisora ativa cadastrada.")
            continue

        print("\n=== AVALIAR REVISORA ===")
        for i, revisora in enumerate(revisoras, start=1):
            print(f"{i} - {revisora[1]}")

        try:
            escolha = int(input("Escolha o número da revisora: "))
            revisora_id = revisoras[escolha - 1][0]
            nome_revisora = revisoras[escolha - 1][1]
        except (ValueError, IndexError):
            print("Opção inválida.")
            continue

        placa = input("Placa (verde / amarela / vermelha): ").lower()
        confirma = input(
            f"Confirma avaliação para {nome_revisora} com placa {placa}? (s/n): "
        ).lower()

        if confirma != "s":
            print("Avaliação cancelada.")
            continue

        sucesso, msg = avaliar_revisora_por_id(revisora_id, placa)
        print(msg)

    # ===== RANKING MENSAL =====
    elif opcao == "3":
        mes = int(input("Digite o mês (1-12): "))
        ano = int(input("Digite o ano (ex: 2026): "))

        ranking = ranking_mensal(mes, ano)

        if not ranking:
            print("Nenhuma avaliação encontrada.")
        else:
            print(f"\n=== TOP 3 - {mes:02d}/{ano} ===")
            medalhas = ["🥇", "🥈", "🥉"]
            for i, (nome, pontos) in enumerate(ranking):
                print(f"{medalhas[i]} {nome} - {pontos} pontos")

    # ===== RELATÓRIO MENSAL =====
    elif opcao == "4":
        mes = int(input("Digite o mês (1-12): "))
        ano = int(input("Digite o ano (ex: 2026): "))

        relatorio = relatorio_mensal(mes, ano)

        if not relatorio:
            print("Nenhum dado encontrado.")
        else:
            print(f"\n=== RELATÓRIO {mes:02d}/{ano} ===")
            for nome, total, verdes, amarelas, vermelhas, pontos in relatorio:
                print(f"\nRevisora: {nome}")
                print(f"- Avaliações: {total}")
                print(f"- Verdes: {verdes}")
                print(f"- Amarelas: {amarelas}")
                print(f"- Vermelhas: {vermelhas}")
                print(f"- Total de pontos: {pontos}")

    # ===== RANKING GERAL =====
    elif opcao == "5":
        mes = int(input("Digite o mês (1-12): "))
        ano = int(input("Digite o ano (ex: 2026): "))

        ranking = ranking_geral(mes, ano)

        for i, (nome, pontos) in enumerate(ranking, start=1):
            print(f"{i}º {nome} - {pontos} pontos")

    # ===== EXPORTAÇÕES =====
    elif opcao == "6":
        mes = int(input("Mês: "))
        ano = int(input("Ano: "))
        print(exportar_ranking_geral_excel(mes, ano)[1])

    elif opcao == "7":
        mes = int(input("Mês: "))
        ano = int(input("Ano: "))
        print(exportar_relatorio_mensal_excel(mes, ano)[1])

    # ===== HISTÓRICO =====
    elif opcao == "8":
        revisoras = listar_revisoras_ativas()

        print("\n=== HISTÓRICO DE REVISORA ===")
        for i, r in enumerate(revisoras, start=1):
            print(f"{i} - {r[1]}")

        try:
            escolha = int(input("Escolha: "))
            revisora_id = revisoras[escolha - 1][0]
            nome = revisoras[escolha - 1][1]
        except:
            print("Opção inválida.")
            continue

        historico = historico_revisora(revisora_id)

        print(f"\n=== HISTÓRICO - {nome} ===")
        for data, placa, pontos in historico:
            print(f"{data} | {placa} | {pontos} ponto(s)")

    # ===== SAIR =====
    elif opcao == "0":
        print("Saindo do sistema...")
        break

    else:
        print("Opção inválida.")