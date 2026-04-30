import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Gemaplast - Workflow", layout="wide")

# 2. STYLE CSS AVANCÉ (Inspiré de l'image)
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .gemaplast-logo {
        color: #CC0000 !important;
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        font-style: italic;
        font-size: 40px;
        text-align: left;
        margin-bottom: 10px;
    }
    .stApp { background-color: #F8F9FA; }
    
    /* Cartes d'indicateurs (KPIs) */
    .kpi-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #E0E0E0;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    .kpi-value { font-size: 24px; font-weight: bold; color: #333; }
    .kpi-label { font-size: 14px; color: #666; }

    /* Carte de Demande (Style de l'image) */
    .demand-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #E0E0E0;
        margin-bottom: 20px;
        box-shadow: 2px 4px 10px rgba(0,0,0,0.05);
    }
    .status-badge {
        background-color: #FFF9C4;
        color: #FBC02D;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
    }
    .priority-dot {
        height: 10px;
        width: 10px;
        background-color: #FF5252;
        border-radius: 50%;
        display: inline-block;
        margin-right: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. INITIALISATION DES DONNÉES
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'db' not in st.session_state:
    # On ajoute des colonnes pour correspondre à la nouvelle interface
    st.session_state.db = pd.DataFrame([
        {"ID": "D001", "Produit": "Huile moteur 5W-30 (20L)", "Quantité": 10, "Date": "28/04/2026", "Statut": "En attente Production", "Description": "Stock faible, besoin urgent pour maintenance hebdomadaire", "Priorité": "Haute"}
    ])

USERS_DB = {
    "magasinier@gemaplast.ma": {"code": "1111", "role": "Magasinier"},
    "production@gemaplast.ma": {"code": "2222", "role": "Responsable Production"}
}

# 4. LOGIQUE DE CONNEXION
if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<p class='gemaplast-logo' style='text-align:center;'>GEMAPLAST</p>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center; color:black;'>Connexion Sécurisée</h2>", unsafe_allow_html=True)
        email_input = st.text_input("Identifiant Email").strip().lower()
        pass_input = st.text_input("Code d'accès", type="password")
        if st.button("ACCÉDER AU PORTAIL"):
            if email_input in USERS_DB and USERS_DB[email_input]["code"] == pass_input:
                st.session_state.authenticated = True
                st.session_state.user_role = USERS_DB[email_input]["role"]
                st.rerun()
            else:
                st.error("Identifiants incorrects.")

# 5. LOGIQUE APRÈS CONNEXION
else:
    with st.sidebar:
        st.markdown("<h2 style='color:white; font-style:italic;'>GEMAPLAST</h2>", unsafe_allow_html=True)
        st.write(f"Rôle : **{st.session_state.user_role}**")
        if st.button("Déconnexion"):
            st.session_state.authenticated = False
            st.rerun()

    # --- INTERFACE MAGASINIER (DASHBOARD) ---
    if st.session_state.user_role == "Magasinier":
        # En-tête
        head1, head2 = st.columns([3, 1])
        with head1:
            st.markdown("<h1 style='margin-bottom:0;'>Mes Demandes d'Approvisionnement</h1>", unsafe_allow_html=True)
            st.write("Créez et suivez vos demandes de produits")
        with head2:
            if st.button("+ Nouvelle Demande", use_container_width=True):
                st.session_state.show_form = True # Optionnel pour ouvrir un modal

        # Indicateurs (KPIs)
        st.write("")
        k1, k2, k3, k4 = st.columns(4)
        total = len(st.session_state.db)
        attente = len(st.session_state.db[st.session_state.db['Statut'].str.contains("attente")])
        
        k1.markdown(f"<div class='kpi-card'><div class='kpi-label'>Total Demandes</div><div class='kpi-value'>{total}</div></div>", unsafe_allow_html=True)
        k2.markdown(f"<div class='kpi-card'><div class='kpi-label'>En Attente</div><div class='kpi-value'>{attente}</div></div>", unsafe_allow_html=True)
        k3.markdown(f"<div class='kpi-card'><div class='kpi-label'>Approuvées</div><div class='kpi-value'>0</div></div>", unsafe_allow_html=True)
        k4.markdown(f"<div class='kpi-card'><div class='kpi-label'>Refusées</div><div class='kpi-value'>0</div></div>", unsafe_allow_html=True)

        st.write("---")

        # Liste des demandes (Style Carte)
        for index, row in st.session_state.db.iterrows():
            st.markdown(f"""
            <div class="demand-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="color: #888; font-size: 12px;">{row['ID']}</span>
                        <span class="status-badge">⌛ {row['Statut']}</span>
                    </div>
                    <div>
                        <span class="priority-dot"></span> <span style="color: #CC0000; font-weight: bold; font-size: 14px;">{row['Priorité']}</span>
                    </div>
                </div>
                <h3 style="margin: 10px 0;">{row['Produit']}</h3>
                <div style="display: flex; gap: 50px;">
                    <div>
                        <div style="color: #888; font-size: 12px;">Quantité demandée</div>
                        <div style="font-weight: bold;">{row['Quantité']}</div>
                    </div>
                    <div>
                        <div style="color: #888; font-size: 12px;">Date de création</div>
                        <div style="font-weight: bold;">{row['Date']}</div>
                    </div>
                </div>
                <div style="margin-top: 15px;">
                    <div style="color: #888; font-size: 12px;">Description</div>
                    <div style="font-size: 14px;">{row['Description']}</div>
                </div>
                <hr style="margin: 20px 0; border: 0; border-top: 1px solid #EEE;">
                <div style="font-size: 14px; font-weight: bold; color: #333;">Historique</div>
                <div style="color: #4A90E2; font-size: 13px; margin-top: 5px;">● Création de la demande</div>
                <div style="color: #888; font-size: 12px; margin-left: 15px;">Jean Dubois - {row['Date']}</div>
            </div>
            """, unsafe_allow_html=True)

    # --- INTERFACE PRODUCTION ---
    elif st.session_state.user_role == "Responsable Production":
        st.markdown("<h3 style='color: #CC0000;'>Calculateur de Contrôle</h3>", unsafe_allow_html=True)
        # ... (reste du code calculateur précédent)
