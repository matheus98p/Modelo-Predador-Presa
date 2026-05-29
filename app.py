import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.integrate import solve_ivp

st.set_page_config(layout="wide")

st.title("Modelo Presa-Predador de Lotka-Volterra")

# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.header("Parâmetros")

alpha = st.sidebar.slider(
    "Crescimento das presas",
    0.1,
    2.0,
    1.0
)

beta = st.sidebar.slider(
    "Taxa de predação",
    0.01,
    1.0,
    0.1
)

delta = st.sidebar.slider(
    "Eficiência predatória",
    0.01,
    1.0,
    0.075
)

gamma = st.sidebar.slider(
    "Mortalidade dos predadores",
    0.1,
    2.0,
    1.5
)

presas0 = st.sidebar.slider(
    "Presas iniciais",
    1,
    100,
    40
)

predadores0 = st.sidebar.slider(
    "Predadores iniciais",
    1,
    100,
    9
)

tempo = st.sidebar.slider(
    "Tempo de simulação",
    10,
    100,
    40
)

# -----------------------------
# MODELO
# -----------------------------

def lotka_volterra(t, z):

    x, y = z

    dxdt = alpha*x - beta*x*y
    dydt = delta*x*y - gamma*y

    return [dxdt, dydt]

# -----------------------------
# SOLUÇÃO NUMÉRICA
# -----------------------------

t_eval = np.linspace(0, tempo, 1000)

sol = solve_ivp(
    lotka_volterra,
    [0, tempo],
    [presas0, predadores0],
    t_eval=t_eval
)

presas = sol.y[0]
predadores = sol.y[1]

# -----------------------------
# GRÁFICOS
# -----------------------------

col1, col2 = st.columns(2)

# ---------------------------------
# POPULAÇÕES NO TEMPO
# ---------------------------------

with col1:

    fig1 = go.Figure()

    fig1.add_trace(
        go.Scatter(
            x=t_eval,
            y=presas,
            mode="lines",
            name="Presas"
        )
    )

    fig1.add_trace(
        go.Scatter(
            x=t_eval,
            y=predadores,
            mode="lines",
            name="Predadores"
        )
    )

    fig1.update_layout(
        title="Populações ao longo do tempo",
        xaxis_title="Tempo",
        yaxis_title="População"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

# ---------------------------------
# PLANO DE FASE
# ---------------------------------

with col2:

    fig2 = go.Figure()

    fig2.add_trace(
        go.Scatter(
            x=presas,
            y=predadores,
            mode="lines",
            name="Trajetória"
        )
    )

    fig2.update_layout(
        title="Plano de fase",
        xaxis_title="Presas",
        yaxis_title="Predadores"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# -----------------------------
# EQUAÇÕES
# -----------------------------

st.subheader("Equações do modelo")

st.latex(r"""
\frac{dx}{dt} = \alpha x - \beta xy
""")

st.latex(r"""
\frac{dy}{dt} = \delta xy - \gamma y
""")