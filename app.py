import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(
    page_title="Modelo Presa-Predador",
    layout="wide"
)

st.title("Modelo Presa-Predador")
st.write("Simulação discreta inspirada no modelo de Lotka-Volterra")

# -------------------------
# BARRA LATERAL
# -------------------------

st.sidebar.header("Parâmetros")

presas = st.sidebar.slider(
    "Presas iniciais",
    1,
    100,
    40
)

predadores = st.sidebar.slider(
    "Predadores iniciais",
    1,
    100,
    9
)

r = st.sidebar.slider(
    "Taxa de crescimento das presas",
    0.0,
    1.0,
    0.1
)

a = st.sidebar.slider(
    "Taxa de predação",
    0.0,
    0.1,
    0.02
)

b = st.sidebar.slider(
    "Eficiência dos predadores",
    0.0,
    0.1,
    0.01
)

m = st.sidebar.slider(
    "Mortalidade dos predadores",
    0.0,
    1.0,
    0.1
)

passos = st.sidebar.slider(
    "Número de passos",
    10,
    300,
    100
)

# -------------------------
# SIMULAÇÃO
# -------------------------

lista_presas = [presas]
lista_predadores = [predadores]

presas_atual = presas
predadores_atual = predadores

for tempo in range(passos):

    novas_presas = (
        presas_atual
        + r*presas_atual
        - a*presas_atual*predadores_atual
    )

    novos_predadores = (
        predadores_atual
        + b*presas_atual*predadores_atual
        - m*predadores_atual
    )

    presas_atual = max(novas_presas, 0)
    predadores_atual = max(novos_predadores, 0)

    lista_presas.append(presas_atual)
    lista_predadores.append(predadores_atual)

# -------------------------
# MÉTRICAS
# -------------------------

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Presas finais",
        round(lista_presas[-1],2)
    )

with col2:
    st.metric(
        "Predadores finais",
        round(lista_predadores[-1],2)
    )

# -------------------------
# INTERPRETAÇÃO
# -------------------------

st.subheader("Interpretação")

if lista_presas[-1] < 1:
    st.warning("As presas foram praticamente extintas.")

elif lista_predadores[-1] < 1:
    st.warning("Os predadores foram praticamente extintos.")

else:
    st.success("As espécies coexistem ao final da simulação.")

# -------------------------
# GRÁFICO TEMPORAL
# -------------------------

st.subheader("Evolução temporal")

fig, ax = plt.subplots(figsize=(10,5))

ax.plot(lista_presas)

ax.plot(lista_predadores)

ax.set_xlabel("Tempo")

ax.set_ylabel("População")

ax.legend(["Presas", "Predadores"])

ax.grid()

st.pyplot(fig)

# -------------------------
# PLANO DE FASE
# -------------------------

st.subheader("Plano de fase")

fig, ax = plt.subplots(figsize=(7,7))

ax.plot(
    lista_presas,
    lista_predadores,
    linewidth=2
)

ax.scatter(
    lista_presas[0],
    lista_predadores[0],
    s=100,
    label="Início"
)

ax.scatter(
    lista_presas[-1],
    lista_predadores[-1],
    s=100,
    label="Fim"
)

ax.set_xlabel("Presas")
ax.set_ylabel("Predadores")
ax.set_title("Plano de fase")
ax.grid()
ax.legend()

st.pyplot(fig)

# -------------------------
# TABELA
# -------------------------

st.subheader("Tabela de dados")

dados = pd.DataFrame({
    "Tempo": range(len(lista_presas)),
    "Presas": lista_presas,
    "Predadores": lista_predadores
})

st.dataframe(dados)
