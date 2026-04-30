import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Gemaplast - Workflow", layout="wide")

# 2. STYLE CSS PERSONNALISÉ
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp { background-color: #F8F9FA; }
    
    /* Style du Logo Gemaplast en haut */
    .logo-text {
        color: #CC0000;
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        font-style: italic;
        font-size: 35px;
    }
    
    /* Titre en rouge */
    .titre-rouge {
        color: #CC0000;
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        font-size: 30px;
    }

    /* Cases KPI en GRIS FONCÉ */
    .kpi-card {
        background-color: #262730; /* Gris foncé */
        color: white !important;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        border: 1px solid #444;
    }
    .kpi-value { font-size: 24px; font-weight: bold; color: white; }
    .kpi-label { font-size: 14px; color: #BBB; }

    /* Barre latérale (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E0E0E0;
    }
    .sidebar-desc {
        color: #CC0000;
        font-weight: bold;
        font-size: 16px;
        text-align: center;
        margin-top: 20px;
    }

    /* Carte de demande */
    .demand-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #E0E0E0;
        margin-bottom: 20px;
    }
    .status-badge {
        background-color: #FFF9C4;
        color: #FBC02D;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. INITIALISATION DES DONNÉES
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([
        {"ID": "D001", "Produit": "Huile moteur 5W-30 (20L)", "Quantité": 10, "Date": "28/04/2026", "Statut": "En attente Production", "Description": "Stock faible", "Priorité": "Haute"}
    ])
if 'show_form' not in st.session_state:
    st.session_state.show_form = False

# 4. BARRE LATÉRALE (SIDEBAR)
with st.sidebar:
    st.markdown('<p class="logo-text" style="text-align:center;">GEMAPLAST</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-desc">Entreprise de fabrication de conduites en PVC et polyéthylène</p>', unsafe_allow_html=True)
    st.divider()
    st.write("Menu")
    st.button("Tableau de bord", use_container_width=True)
    st.button("Paramètres", use_container_width=True)

# 5. EN-TÊTE PRINCIPAL
col_logo, col_titre, col_btn = st.columns([1, 3, 1.2])

with col_logo:
    st.markdown('<p class="logo-text">GEMAPLAST</p>', unsafe_allow_html=True)

with col_titre:
    st.markdown('<p class="titre-rouge">Mes Demandes d\'Approvisionnement</p>', unsafe_allow_html=True)

with col_btn:
    if st.button("+ Nouvelle Demande", type="primary", use_container_width=True):
        st.session_state.show_form = not st.session_state.show_form

# 6. FORMULAIRE DE SAISIE
if st.session_state.show_form:
    with st.expander("📝 Nouvelle saisie", expanded=True):
        with st.form("add_form"):
            prod = st.text_input("Produit")
            qte = st.number_input("Quantité", min_value=1)
            desc = st.text_area("Description")
            if st.form_submit_button("Envoyer la demande"):
                new_data = {
                    "ID": f"D00{len(st.session_state.db)+1}",
                    "Produit": prod,
                    "Quantité": qte,
                    "Date": datetime.now().strftime("%d/%m/%Y"),
                    "Statut": "En attente Production",
                    "Description": desc,
                    "Priorité": "Moyenne"
                }
                st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_data])], ignore_index=True)
                st.session_state.show_form = False
                st.rerun()

# 7. INDICATEURS (KPI) EN GRIS FONCÉ
st.write("")
k1, k2, k3, k4 = st.columns(4)
total = len(st.session_state.db)

k1.markdown(f'<div class="kpi-card"><div class="kpi-label">Total Demandes</div><div class="kpi-value">{total}</div></div>', unsafe_allow_html=True)
k2.markdown('<div class="kpi-card"><div class="kpi-label">En Attente</div><div class="kpi-value">1</div></div>', unsafe_allow_html=True)
k3.markdown('<div class="kpi-card"><div class="kpi-label">Approuvées</div><div class="kpi-value">0</div></div>', unsafe_allow_html=True)
k4.markdown('<div class="kpi-card"><div class="kpi-label">Refusées</div><div class="kpi-value">0</div></div>', unsafe_allow_html=True)

st.divider()

# 8. AFFICHAGE DES DEMANDES
for index, row in st.session_state.db.iterrows():
    st.markdown(f"""
    <div class="demand-card">
        <div style="display: flex; justify-content: space-between;">
            <span class="status-badge">⌛ {row['Statut']}</span>
            <span style="color: #CC0000; font-weight: bold;">● {row['Priorité']}</span>
        </div>
        <h3 style="margin: 10px 0;">{row['Produit']}</h3>
        <p style="font-size: 14px; color: #666;">
            <b>ID:</b> {row['ID']} | <b>Date:</b> {row['Date']} | <b>Quantité:</b> {row['Quantité']}
        </p>
        <p style="font-size: 14px; border-top: 1px solid #EEE; padding-top: 10px;">{row['Description']}</p>
    </div>
    """, unsafe_allow_html=True)
