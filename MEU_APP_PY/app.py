from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from db import criar_tabelas
from regras import (
    listar_revisoras,
    cadastrar_revisora,
    listar_revisoras_ativas,
    avaliar_revisora_por_id,
    ranking_geral,
    relatorio_mensal,
    exportar_relatorio_mensal_excel,
    alterar_status_revisora,
    historico_revisora
)
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "qualidade_2026"

criar_tabelas()


@app.route("/")
def index():
    return render_template("index.html", datetime=datetime)


@app.route("/revisoras")
def revisoras():
    dados = listar_revisoras()
    return render_template("revisoras.html", revisoras=dados, datetime=datetime)


@app.route("/ranking")
def ranking():
    hoje = datetime.today()
    mes = hoje.month
    ano = hoje.year

    dados = ranking_geral(mes, ano)
    return render_template("ranking.html", ranking=dados, mes=mes, ano=ano, datetime=datetime)


@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        nome = request.form["nome"]
        cadastrar_revisora(nome)
        return redirect(url_for("revisoras"))

    return render_template("cadastrar.html", datetime=datetime)


@app.route("/avaliar", methods=["GET", "POST"])
def avaliar():
    revisoras = listar_revisoras_ativas()

    if request.method == "POST":
        revisora_id = request.form["revisora_id"]
        placa = request.form["placa"]

        sucesso, mensagem = avaliar_revisora_por_id(revisora_id, placa)

        flash(mensagem)

        # 👇 VOLTA PARA O MENU
        return redirect(url_for("index"))

    return render_template("avaliar.html", revisoras=revisoras, datetime=datetime)


@app.route("/relatorio", methods=["GET", "POST"])
def relatorio():
    hoje = datetime.today()
    mes = hoje.month
    ano = hoje.year

    dados = relatorio_mensal(mes, ano)
    return render_template("relatorio.html", dados=dados, mes=mes, ano=ano, datetime=datetime)


@app.route("/exportar_relatorio")
def exportar_relatorio():
    hoje = datetime.today()
    mes = hoje.month
    ano = hoje.year

    sucesso, mensagem = exportar_relatorio_mensal_excel(mes, ano)

    if not sucesso:
        return redirect(url_for("relatorio"))

    nome_arquivo = f"relatorio_mensal_{mes:02d}_{ano}.xlsx"
    caminho = os.path.join("exports", nome_arquivo)

    return send_file(caminho, as_attachment=True)


@app.route("/gerenciar_revisoras", methods=["GET", "POST"])
def gerenciar_revisoras():
    # Cadastro
    if request.method == "POST":
        nome = request.form.get("nome")
        if nome:
            cadastrar_revisora(nome)
        return redirect(url_for("gerenciar_revisoras"))

    dados = listar_revisoras()
    return render_template("gerenciar_revisoras.html", revisoras=dados, datetime=datetime)


@app.route("/alterar_status/<int:revisora_id>/<int:status>")
def alterar_status(revisora_id, status):
    alterar_status_revisora(revisora_id, status)
    return redirect(url_for("gerenciar_revisoras"))


@app.route("/historico/<int:revisora_id>")
def historico(revisora_id):
    dados = historico_revisora(revisora_id)
    return render_template("historico.html", dados=dados, revisora_id=revisora_id, datetime=datetime)


if __name__ == "__main__":
    app.run(debug=True)
