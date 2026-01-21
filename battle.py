import streamlit as st
import random
import qrcode
from io import BytesIO

# 1. Configuración de página
st.set_page_config(page_title="Technovation Battle", layout="wide", initial_sidebar_state="expanded")

# 2. Inyección de estilos (Tu versión original con el alto al 15%)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    /* Fondo y Fuente Global */
    .stApp {
        background-color: #181c26;
        background-image: radial-gradient(circle at 2px 2px, rgba(255,255,255,0.05) 1px, transparent 0);
        background-size: 24px 24px;
        font-family: 'Space Grotesk', sans-serif;
    }

    /* Contenedor Principal */
    [data-testid="stAppViewBlockContainer"] {
        max-width: 1000px !important;
        padding-top: 2rem !important;
    }

    /* Ocultar elementos de Streamlit */
    # header, footer {visibility: hidden;}
    
    /* Header Glassmorphism */
    .glass-header {
        background: rgba(24, 28, 38, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1.5rem;
        padding: 1.5rem;
        text-align: center;
        margin-bottom: 2rem;
    }

    /* BOTONES CON ALTO AL 15% DE LA PANTALLA */
    div.stButton > button {
        width: 100% !important;
        height: 15vh !important; /* Ajuste solicitado */
        min-height: 15vh !important;
        background-color: #272D3A !important;
        color: white !important;
        border-radius: 1.5rem !important;
        padding: 1rem !important;
        transition: all 0.3s ease-in-out !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        gap: 0.5rem !important;
    }

    /* Efectos de color originales */
    div[data-testid="column"]:nth-of-type(1) div.stButton > button {
        border: 2px solid #00bdc7 !important;
        box-shadow: 0 0 20px rgba(0, 189, 199, 0.2) !important;
    }

    div[data-testid="column"]:nth-of-type(3) div.stButton > button:hover {
        border: 2px solid #EE40DA !important;
        box-shadow: 0 0 20px rgba(238, 64, 218, 0.3) !important;
    }

    /* Estilo del VS centrado al alto del botón */
    .vs-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 15vh;
    }
    .vs-circle {
        width: 50px;
        height: 50px;
        background: #181c26;
        border: 4px solid #EE40DA;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #EE40DA;
        font-weight: 900;
        font-style: italic;
        font-size: 1.2rem;
        box-shadow: 0 0 15px #EE40DA;
    }

    .stProgress > div > div > div > div {
        background-color: #00bdc7 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- LÓGICA DE DATOS ---
if 'competidores' not in st.session_state:
    PROBLEMAS = [
        {"nombre": "ODS#12 Consumo Responsable", "desc": "Contaminación por desecho masivo de textiles y microplásticos."},
        {"nombre": "ODS#16 Paz e Instituciones", "desc": "Engaños online y grooming: adultos contactando menores en redes."},
        {"nombre": "ODS#5 Igualdad de Género", "desc": "Pobreza menstrual: falta de acceso a productos de higiene básica."},
        {"nombre": "ODS#6 Agua y Saneamiento", "desc": "Acceso limitado a agua potable en comunidades vulnerables."},
        {"nombre": "ODS#9 Industria e Innovación", "desc": "Brecha digital: falta de conectividad e internet en zonas rurales."},
        {"nombre": "ODS#3 Salud y Bienestar", "desc": "Crisis de Salud Mental: aumento de ansiedad y depresión en jóvenes."},
        {"nombre": "ODS#10 Reducción de Desigualdades", "desc": "Ciberestafas y vulnerabilidad digital en adultos mayores."},
        {"nombre": "ODS#13 Acción por el Clima", "desc": "Moda Rápida: alto impacto ambiental por emisiones y uso de agua."}
    ]
    random.shuffle(PROBLEMAS)
    st.session_state.competidores = PROBLEMAS
    st.session_state.ganadores_ronda_actual = []
    st.session_state.indice_duelo = 0
    st.session_state.ronda_nombre = "Octavos de final"

CRITERIOS = {
    "Octavos de final": {"t": "Impacto", "p": "¿Cuál es más urgente?"},
    "Cuartos de final": {"t": "Viabilidad", "p": "¿Cuál es más fácil?"},
    "Semifinal": {"t": "Usuario", "p": "¿Quién tiene usuarios claros?"},
    "Gran final": {"t": "Pasión", "p": "¿Cuál les motiva más?"}
}

def elegir_ganador(elegido):
    st.session_state.ganadores_ronda_actual.append(elegido)
    st.session_state.indice_duelo += 2
    if st.session_state.indice_duelo >= len(st.session_state.competidores):
        if len(st.session_state.ganadores_ronda_actual) == 1:
            st.session_state.ronda_nombre = "¡Ganador!"
        else:
            st.session_state.competidores = st.session_state.ganadores_ronda_actual
            st.session_state.ganadores_ronda_actual = []
            st.session_state.indice_duelo = 0
            etapas = {8: "Cuartos de final", 4: "Semifinal", 2: "Gran final"}
            st.session_state.ronda_nombre = etapas.get(len(st.session_state.competidores), "Final")

# --- UI RENDER ---
info = CRITERIOS.get(st.session_state.ronda_nombre, CRITERIOS["Octavos de final"])

# Sidebar para QR y Reinicio
with st.sidebar:
    st.markdown("### OPCIONES")
    if st.button("REINICIAR"):
        st.session_state.clear()
        st.rerun()
    st.divider()
    url = "https://tu-app.streamlit.app/"
    qr_img = qrcode.make(url)
    buf = BytesIO()
    qr_img.save(buf, format="PNG")
    st.image(buf.getvalue(), caption="¡Invita a otros!")

# Header
st.markdown(f"""
    <div class="glass-header">
        <p style="color:#00bdc7; font-size:12px; text-transform:uppercase; letter-spacing:0.3em; margin-bottom:5px;">Tournament</p>
        <h1 style="color:white; margin:0; font-size:1.5rem;">{st.session_state.ronda_nombre}: {info['t']}</h1>
        <p style="color:#9ababc; margin-top:5px; font-size:0.9rem;">{info['p']}</p>
    </div>
""", unsafe_allow_html=True)

if st.session_state.ronda_nombre == "¡Ganador!":
    ganador = st.session_state.ganadores_ronda_actual[0]
    st.balloons()
    st.markdown(f"<div class='glass-header'><h2 style='color:#00bdc7'>GANADOR</h2><h1 style='color:white'>{ganador['nombre']}</h1></div>", unsafe_allow_html=True)
else:
    i = st.session_state.indice_duelo
    p1, p2 = st.session_state.competidores[i], st.session_state.competidores[i+1]
    
    st.markdown(f'<p style="text-align:center; color:#00bdc7; font-weight:bold; font-size:12px; margin-bottom:10px;">BATTLE {int(i/2)+1} OF {int(len(st.session_state.competidores)/2)}</p>', unsafe_allow_html=True)

    col1, col_v, col2 = st.columns([10, 2, 10])
    
    with col1:
        if st.button(f"{p1['nombre']}\n\n{p1['desc']}", key=f"btn_{i}"):
            elegir_ganador(p1)
            st.rerun()

    with col_v:
        st.markdown('<div class="vs-container"><div class="vs-circle">VS</div></div>', unsafe_allow_html=True)

    with col2:
        if st.button(f"{p2['nombre']}\n\n{p2['desc']}", key=f"btn_{i+1}"):
            elegir_ganador(p2)
            st.rerun()

    # Progreso inferior
    st.markdown("<br>", unsafe_allow_html=True)
    progreso = (int(i/2) + 1) / (len(st.session_state.competidores)/2)
    st.progress(progreso)
    st.markdown(f'<p style="text-align:right; color:#00bdc7; font-size:12px; font-weight:bold;">{int(progreso*100)}% COMPLETADO</p>', unsafe_allow_html=True)
