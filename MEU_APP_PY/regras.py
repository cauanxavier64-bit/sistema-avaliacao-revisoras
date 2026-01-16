from datetime import date
import pandas as pd
import os
from db import conectar


def cadastrar_revisora(nome):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            "INSERT INTO revisoras (nome, ativa) VALUES (?, 1)",
            (nome,)
        )
        conexao.commit()
        return True
    except Exception:
        return False
    finally:
        conexao.close()


def listar_revisoras():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT id, nome, ativa FROM revisoras ORDER BY nome")
    dados = cursor.fetchall()

    conexao.close()
    return dados


def alterar_status_revisora(revisora_id, ativa):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "UPDATE revisoras SET ativa = ? WHERE id = ?",
        (ativa, revisora_id)
    )

    conexao.commit()
    conexao.close()


def avaliar_revisora(nome, placa):
    pontos_por_placa = {
        "verde": 2,
        "amarela": 1,
        "vermelha": 0
    }

    placa = placa.lower()

    if placa not in pontos_por_placa:
        return False, "Placa inválida"

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT id FROM revisoras WHERE nome = ? AND ativa = 1",
        (nome,)
    )

    revisora = cursor.fetchone()

    if not revisora:
        conexao.close()
        return False, "Revisora não encontrada ou inativa"

    cursor.execute("""
        INSERT INTO avaliacoes (revisora_id, placa, pontos, data_avaliacao)
        VALUES (?, ?, ?, ?)
    """, (revisora[0], placa, pontos_por_placa[placa], date.today().isoformat()))

    conexao.commit()
    conexao.close()

    return True, "Avaliação registrada com sucesso"


def ranking_mensal(mes, ano):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT r.nome, SUM(a.pontos) AS total_pontos
        FROM avaliacoes a
        JOIN revisoras r ON a.revisora_id = r.id
        WHERE strftime('%m', a.data_avaliacao) = ?
          AND strftime('%Y', a.data_avaliacao) = ?
        GROUP BY r.nome
        ORDER BY total_pontos DESC
        LIMIT 3
    """, (f"{mes:02d}", str(ano)))

    ranking = cursor.fetchall()
    conexao.close()

    return ranking


def relatorio_mensal(mes, ano):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT 
            r.nome,
            COUNT(a.id) AS total_avaliacoes,
            SUM(CASE WHEN a.placa = 'verde' THEN 1 ELSE 0 END) AS verdes,
            SUM(CASE WHEN a.placa = 'amarela' THEN 1 ELSE 0 END) AS amarelas,
            SUM(CASE WHEN a.placa = 'vermelha' THEN 1 ELSE 0 END) AS vermelhas,
            SUM(a.pontos) AS total_pontos
        FROM avaliacoes a
        JOIN revisoras r ON r.id = a.revisora_id
        WHERE strftime('%m', a.data_avaliacao) = ?
          AND strftime('%Y', a.data_avaliacao) = ?
        GROUP BY r.nome
        ORDER BY total_pontos DESC
    """, (f"{mes:02d}", str(ano)))

    dados = cursor.fetchall()
    conexao.close()

    return dados


def ranking_geral(mes, ano):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT r.nome, SUM(a.pontos) AS total_pontos
        FROM avaliacoes a
        JOIN revisoras r ON a.revisora_id = r.id
        WHERE strftime('%m', a.data_avaliacao) = ?
          AND strftime('%Y', a.data_avaliacao) = ?
        GROUP BY r.nome
        ORDER BY total_pontos DESC
    """, (f"{mes:02d}", str(ano)))

    ranking = cursor.fetchall()
    conexao.close()

    return ranking


def exportar_ranking_geral_excel(mes, ano):
    conexao = conectar()

    query = """
        SELECT 
            r.nome AS Revisora,
            SUM(a.pontos) AS Pontos
        FROM avaliacoes a
        JOIN revisoras r ON a.revisora_id = r.id
        WHERE strftime('%m', a.data_avaliacao) = ?
          AND strftime('%Y', a.data_avaliacao) = ?
        GROUP BY r.nome
        ORDER BY Pontos DESC
    """

    df = pd.read_sql_query(
        query,
        conexao,
        params=(f"{mes:02d}", str(ano))
    )

    conexao.close()

    if df.empty:
        return False, "Nenhum dado para exportar."

    # 📁 Pasta de exportação
    pasta = "exports"
    os.makedirs(pasta, exist_ok=True)

    nome_arquivo = f"ranking_geral_{mes:02d}_{ano}.xlsx"
    caminho = os.path.join(pasta, nome_arquivo)

    df.to_excel(caminho, index=False)

    return True, f"Arquivo salvo em: {caminho}"


def exportar_relatorio_mensal_excel(mes, ano):
    conexao = conectar()

    query = """
        SELECT 
            r.nome AS Revisora,
            COUNT(a.id) AS Avaliacoes,
            SUM(CASE WHEN a.placa = 'verde' THEN 1 ELSE 0 END) AS Verdes,
            SUM(CASE WHEN a.placa = 'amarela' THEN 1 ELSE 0 END) AS Amarelas,
            SUM(CASE WHEN a.placa = 'vermelha' THEN 1 ELSE 0 END) AS Vermelhas,
            SUM(a.pontos) AS Pontos
        FROM avaliacoes a
        JOIN revisoras r ON r.id = a.revisora_id
        WHERE strftime('%m', a.data_avaliacao) = ?
          AND strftime('%Y', a.data_avaliacao) = ?
        GROUP BY r.nome
        ORDER BY Pontos DESC
    """

    df = pd.read_sql_query(
        query,
        conexao,
        params=(f"{mes:02d}", str(ano))
    )

    conexao.close()

    if df.empty:
        return False, "Nenhum dado para exportar."

    # 📁 Pasta de exportação
    pasta = "exports"
    os.makedirs(pasta, exist_ok=True)

    nome_arquivo = f"relatorio_mensal_{mes:02d}_{ano}.xlsx"
    caminho = os.path.join(pasta, nome_arquivo)

    df.to_excel(caminho, index=False)

    return True, f"Arquivo salvo em: {caminho}"


def listar_revisoras_ativas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome
        FROM revisoras
        WHERE ativa = 1
        ORDER BY nome
    """)
    revisoras = cursor.fetchall()
    conexao.close()

    return revisoras


def avaliar_revisora_por_id(revisora_id, placa):
    pontos_por_placa = {
        "verde": 2,
        "amarela": 1,
        "vermelha": 0
    }

    placa = placa.lower()

    if placa not in pontos_por_placa:
        return False, "Placa inválida."

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO avaliacoes (revisora_id, placa, pontos, data_avaliacao)
        VALUES (?, ?, ?, date('now'))
    """, (revisora_id, placa, pontos_por_placa[placa]))

    conexao.commit()
    conexao.close()

    return True, f"Avaliação registrada: {placa} ({pontos_por_placa[placa]} ponto(s)) ✅"


def historico_revisora(revisora_id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT 
            a.data_avaliacao,
            a.placa,
            a.pontos
        FROM avaliacoes a
        WHERE a.revisora_id = ?
        ORDER BY a.data_avaliacao DESC
    """, (revisora_id,))

    dados = cursor.fetchall()
    conexao.close()
    return dados
