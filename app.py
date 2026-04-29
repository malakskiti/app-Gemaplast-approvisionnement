import streamlit as st
import pandas as pd

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Gemaplast - Workflow Achat", layout="wide")

# 2. DESIGN PERSONNALISÉ (FORÇAGE DES COULEURS)
st.markdown("""
    <style>
    /* Force la couleur noire sur TOUS les titres h2 de la page de login */
    h2 {
        color: #E0E0E0 !important;
        font-family: 'Arial Black', sans-serif !important;
        text-align: center !important;
        padding-bottom: 20px !important;
    }

    /* Barre latérale (Bande noire à gauche) */
    section[data-testid="stSidebar"] {
        background-color: #1a1a1a !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Boutons rouges Gemaplast */
    .stButton>button { 
        background-color: #cc0000 !important; 
        color: white !important;
        border: none !important;
        font-weight: bold !important;
    }

    /* Carte de connexion grise très claire */
    .login-card {
        background-color: #f1f1f1;
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        margin-top: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. INITIALISATION
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["ID", "Produit", "Desc", "Qte", "Statut"])

# --- BARRE LATÉRALE ---
with st.sidebar:
    # --- LIEN IMAGE ICI (Ligne 55 environ) ---
    st.image("https://i.ibb.co/L6V8XkP/gemaplast-logo.jpg", use_container_width=True) 
    
    st.markdown("### À propos de l'App")
    st.markdown("<p style='color:white; font-size:14px; opacity:0.8;'>Digitalisation des Flux Gemaplast. Centralisation des approvisionnements.</p>", unsafe_allow_html=True)
    
    if st.session_state.authenticated:
        st.write(f"🟢 Connecté : **{st.session_state.user_role}**")
        if st.button("Déconnexion"):
            st.session_state.authenticated = False
            st.rerun()

# --- PAGE DE CONNEXION ---
if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='login-card'>", unsafe_allow_html=True)
        
        # TITRE : Ici on utilise <h2> pour que le style CSS du haut s'applique
        st.markdown("<h2>Connexion Sécurisée</h2>", unsafe_allow_html=True)
        
        email = st.text_input("Email Professionnel")
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
    # Interface après login
    st.title(f"Interface {st.session_state.user_role}")
    st.write("Bienvenue sur votre espace de travail Gemaplast.")
    # (Le reste de la logique magasinier/achat vient ici)
