import pandas as pd

# Importando o relatório de vendas
vendas = pd.read_csv("https://raw.githubusercontent.com/alura-cursos/dataviz-graficos/master/dados/relatorio_vendas.csv")
vendas["data_pedido"] = pd.to_datetime(vendas["data_pedido"], format="%Y-%m-%d")
vendas["data_envio"] = pd.to_datetime(vendas["data_envio"], format="%Y-%m-%d")

print(vendas)

vendas.info()

#Qual o total de vendas por ano? E qual ano performou melhor em nossa base de dados?

#Criando um df com os dados desejados
df_vendas_ano = vendas.copy()
df_vendas_ano = df_vendas_ano[["data_pedido","vendas"]]

#Gerando uma coluna que representa somente os anos a partir da coluna data pedido
df_vendas_ano["ano"] = df_vendas_ano.data_pedido.dt.year
df_vendas_ano.drop(labels = "data_pedido", axis=1, inplace=True)

#Agrupando os dados por ano 
df_vendas_ano = df_vendas_ano.groupby("ano").aggregate("sum")

print(df_vendas_ano)


#Importando as bibliotecas
import matplotlib.pyplot as plt
import seaborn as sns

def grafico_vendas(cores: list= "Blues"):
    #Área do gráfico e tema da visualização
    fig, ax = plt.subplots(figsize=(10,4))
    sns.set_theme(style="white")

    #Gerando o gráfico de colunas
    ax = sns.barplot(data = df_vendas_ano, x= df_vendas_ano.index, y="vendas", palette= cores)

    #Personalizando o gráfico
    CINZA1="#4F4F4F"
    CINZA2="#A9A9A9"

    ax.set_title("Vendas das lojas de departamentos de\n2016 a 2019", loc="left", fontsize=18, color= CINZA1)
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.xaxis.set_tick_params(labelsize=14, labelcolor= CINZA2)
    sns.despine(left=True, bottom=True)

    #Escrevendo os valores de cada barra no gráfico
    ax.set_yticklabels([])
    for i, valor in enumerate(df_vendas_ano["vendas"]):
        qtd = f'R$ {valor:,.0f}'.replace(",",".")
        offset = 1e5
        ax.text(i, valor + offset, qtd, color= CINZA2, fontsize= 12, ha="center", va="center")

    #Retornar o eixo
    return ax


#Definindo as cores do gráfico
AZUL2="#1474a8"
AZUL5="#70a2bf"

cores=[]
for ano in df_vendas_ano.index:
    if df_vendas_ano.loc[ano,"vendas"] == df_vendas_ano.vendas.max():
        cores.append(AZUL2)
    else:
        cores.append(AZUL5)

#Chamando a função
ax= grafico_vendas(cores)


# Anotando uma conclusão no gráfico
ax.text(3.5, 1.5e6,
         'Em $\\bf{2019}$, as vendas\n'
         'nas lojas subiram\n'
         'aproximadamente $\\bf{22,3}$%\n'
         'em relação ao ano de 2018.',
         fontsize=14, linespacing=1.45, color=AZUL2)


#Exibir gráfico
plt.show()