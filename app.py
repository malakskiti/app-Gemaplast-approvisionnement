import streamlit as st
import pandas as pd

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Gemaplast - Workflow", layout="wide")

# 2. STYLE CSS (Design Gemaplast)
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .gemaplast-logo {
        color: #CC0000 !important;
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        font-style: italic;
        font-size: 50px;
        text-align: center;
        margin-bottom: 20px;
    }
    .stApp { background-color: #FFFFFF; }
    section[data-testid="stSidebar"] { background-color: #000000 !important; }
    section[data-testid="stSidebar"] * { color: white !important; }
    .result-box {
        background-color: #262730;
        color: #FFFFFF !important;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #CC0000;
    }
    /* En-tête du tableau en rouge */
    thead tr th {
        background-color: #CC0000 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. INITIALISATION DES DONNÉES
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["ID", "Produit", "Quantité", "Unité", "Statut"])

# Dictionnaire des utilisateurs
USERS_DB = {
    "magasinier@gemaplast.ma": {"code": "1111", "role": "Magasinier"},
    "production@gemaplast.ma": {"code": "2222", "role": "Responsable Production"},
    "achat@gemaplast.ma": {"code": "3333", "role": "Responsable Achat"},
    "dg@gemaplast.ma": {"code": "4444", "role": "Directeur Général"}
}

st.markdown("<p class='gemaplast-logo'>GEMAPLAST</p>", unsafe_allow_html=True)

# 4. LOGIQUE DE CONNEXION
if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<h2 style='text-align:center; color:black;'>Connexion Sécurisée</h2>", unsafe_allow_html=True)
        email_input = st.text_input("Identifiant Email").strip().lower()
        pass_input = st.text_input("Code d'accès", type="password")
        
        if st.button("ACCÉDER AU PORTAIL"):
            if email_input in USERS_DB and USERS_DB[email_input]["code"] == pass_input:
                st.session_state.authenticated = True
                st.session_state.user_role = USERS_DB[email_input]["role"]
                st.rerun()
            else:
                st.error("Identifiants incorrects. Vérifiez l'email et le code.")

# 5. LOGIQUE APRÈS CONNEXION
else:
    # --- Barre Latérale ---
    with st.sidebar:
        st.markdown("<h2 style='font-style:italic;'>GEMAPLAST</h2>", unsafe_allow_html=True)
        st.write(f"Utilisateur : **{st.session_state.user_role}**")
        if st.button("Déconnexion"):
            st.session_state.authenticated = False
            st.rerun()

    # --- Interface PRODUCTION (Calculateur) ---
    if st.session_state.user_role == "Responsable Production":
        st.markdown("<h3 style='color: #CC0000;'>Calculateur de Contrôle</h3>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 1, 1])
        with c1: 
            val_x = st.number_input("Valeur x", value=0.0, key="x_prod")
        with c2: 
            val_y = st.number_input("Valeur y", value=0.0, key="y_prod")
        with c3:
            z = val_x + val_y
            st.markdown(f"<div class='result-box'>TOTAL (Z) : <br><b>{z}</b></div>", unsafe_allow_html=True)
        st.divider()

    # --- Interface MAGASINIER (Formulaire rouge) ---
    if st.session_state.user_role == "Magasinier":
        st.markdown("<h3 style='color: #CC0000;'>Nouvelle Demande d'Approvisionnement</h3>", unsafe_allow_html=True)
        with st.form("form_magasinier"):
            produit = st.selectbox("Article", ["PVC", "Huile moteur", "Acier", "Courroie"])
            quantite = st.number_input("Quantité", min_value=1)
            submit = st.form_submit_button("Envoyer la demande")
            
            if submit:
                new_id = len(st.session_state.db) + 1
                new_row = {"ID": new_id, "Produit": produit, "Quantité": quantite, "Unité": "PCS", "Statut": "Attente Production"}
                st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_row])], ignore_index=True)
                st.success("Demande enregistrée")
                st.rerun()

    # --- SUIVI DES FLUX (Bas de page pour tous) ---
    st.subheader("Suivi général des flux")
    st.dataframe(st.session_state.db, use_container_width=True)
