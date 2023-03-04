import pandas as pd 
import os
from flask import Flask

# Carregando os dados...
df = pd.read_excel("vendas_api_flask.xlsx")

# cria o site para API
app=Flask(__name__)

# decorator diz em qual link a função vai rodar
@app.route("/")
def calcula_faturamento():
    faturamento=float(df["Valor Final"].sum())    
    return {"Faturamento":faturamento}

# decorator diz em qual link a função vai rodar
@app.route("/vendas/produtos")
def calcula_faturamento_por_produto():
    faturamento_por_produto=df[["Valor Final","Produto"]].groupby("Produto").sum().sort_values("Produto",ascending=True).reset_index()
    return faturamento_por_produto.to_dict()

# decorator diz em qual link a função vai rodar
@app.route("/vendas/produtos/<produto>")
def faturamento_produto_especifico(produto):
    faturamento_produto_especifico = df[["Produto","Valor Final"]].groupby("Produto").sum()
    if produto in faturamento_produto_especifico.index:
        venda_produto = faturamento_produto_especifico.loc[produto]
        produto_especifico = venda_produto.to_dict()
        return produto_especifico
    else:
        return {produto:" produto não encontrado"}
if __name__=="__main__":   
    port= int(os.environ.get('PORT',5000))   
    app.run(host='0.0.0.0',port=port)   
