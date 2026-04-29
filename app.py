import streamlit as st
import pandas as pd

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Gemaplast - Workflow Achat", layout="wide", initial_sidebar_state="collapsed")

# 2. DESIGN PERSONNALISÉ (CSS pour corriger le style et le texte en rouge/italique)
st.markdown("""
    <style>
    /* ÉLIMINER TOUS LES ESPACES BLANCS EN HAUT */
    #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem !important;}
    header {visibility: hidden; height: 0px !important;}
    footer {visibility: hidden;}
    .main .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
    }
    
    /* STYLE POUR LE LOGO TEXTE GEMAPLAST EN ROUGE ET ITALIQUE */
    .gemaplast-logo-text {
        color: #CC0000 !important; /* Rouge */
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        font-style: italic; /* Italique */
        font-size: 50px;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 0px;
        letter-spacing: 2px;
    }

    /* FOND DE LA PAGE BLANC */
    .stApp {
        background-color: #FFFFFF !important;
    }

    /* BARRE LATÉRALE (DÉSACTIVÉE ICI POUR LA CONNEXION) */
    section[data-testid="stSidebar"] {
        background-color: #000000 !important;
    }
    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* TITRE DE CONNEXION NOIR */
    .login-header-text {
        color: #000000 !important;
        font-family: 'Arial Black', sans-serif !important;
        text-align: center !important;
        margin-top: -10px; /* Remonte un peu le titre */
        margin-bottom: 30px;
    }

    /* CARTE DE CONNEXION */
    .login-card {
        background-color: #f8f9fa;
        padding: 40px;
        border-radius: 15px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin-top: -20px; /* Remonte la carte */
    }

    /* BOUTONS ROUGES GEMAPLAST */
    .stButton>button { 
        background-color: #CC0000 !important; 
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        height: 48px !important;
        border: none !important;
    }
    .stButton>button:hover {
        background-color: #990000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. INITIALISATION DE LA SESSION
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["ID", "Produit", "Qte", "Statut"])

# --- PAGE DE CONNEXION ---
if not st.session_state.authenticated:
    
    # Étape 1: Afficher "GEMAPLAST" en rouge et italique tout en haut
    st.markdown("<p class='gemaplast-logo-text'>GEMAPLAST</p>", unsafe_allow_html=True)
    
    # Centrage de la carte de connexion
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        st.markdown("<div class='login-card'>", unsafe_allow_html=True)
        st.markdown("<h2 class='login-header-text'>Connexion Sécurisée</h2>", unsafe_allow_html=True)
        
        email = st.text_input("Identifiant Email")
        password = st.text_input("Code d'accès", type="password")
        
        users = {
            "magasinier@gemaplast.ma": {"code": "1234", "role": "Magasinier"},
            "production@gemaplast.ma": {"code": "2222", "role": "Responsable Production"},
            "achat@gemaplast.ma": {"code": "3333", "role": "Responsable Achat"},
            "dg@gemaplast.ma": {"code": "4444", "role": "Directeur Général"}
        }

        if st.button("ACCÉDER AU PORTAIL"):
            if email in users and users[email]["code"] == password:
                st.session_state.authenticated = True
                st.session_state.user_role = users[email]["role"]
                st.rerun()
            else:
                st.error("Email ou code incorrect.")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # Interface après connexion (le reste de la logique pour les différents rôles vient ici)
    st.title(f"Espace {st.session_state.user_role}")
    st.write("Bienvenue sur la plateforme Gemaplast.")
