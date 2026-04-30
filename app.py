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
    
    /* Logo Gemaplast */
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
        font-size: 28px;
    }

   /* Cases KPI et En-tête Nouvelle saisie */
.kpi-card, .st-emotion-cache-p6495m {
    background-color: ##E3B3A1 !important; /* On remplace #262730 par #454754 */
    color: white !important;
}
    /* Style spécifique pour l'en-tête de l'expander (formulaire) */
    .st-emotion-cache-p6495m { 
        background-color: #262730 !important; 
        color: white !important;
        border-radius: 8px;
    }
.stTextInput>div>div>input, .stNumberInput>div>div>input, .stTextArea>div>div>textarea {
    background-color:#FFFFFF !important; /* Gris moyen */
    color: white !important;
    border: 1px solid #666 !important;
}
    /* Bouton envoyer et autres boutons en gris foncé */
    .stButton>button {
        background-color: #FF0000 !important;
        color: white !important;
        border: none !important;
    }

    /* Barre latérale (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E0E0E0;
    }
    .sidebar-desc {
        color: #CC0000;
        font-weight: bold;
        font-size: 15px;
        text-align: center;
        margin-top: 10px;
    }

    /* Carte de demande */
    .demand-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E0E0E0;
        margin-bottom: 15px;
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

# 4. BARRE LATÉRALE (SIDEBAR NETTOYÉE)
with st.sidebar:
    st.markdown('<p class="logo-text" style="text-align:center;">GEMAPLAST</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-desc">Entreprise de fabrication de conduites en PVC et polyéthylène</p>', unsafe_allow_html=True)
    # Suppression des boutons Paramètres et Tableau de bord ici

# 5. EN-TÊTE PRINCIPAL
col_logo, col_titre, col_btn = st.columns([1, 3, 1.2])

with col_logo:
    st.markdown('<p class="logo-text">GEMAPLAST</p>', unsafe_allow_html=True)

with col_titre:
    st.markdown('<p class="titre-rouge">Mes Demandes d\'Approvisionnement</p>', unsafe_allow_html=True)

with col_btn:
    # Bouton Nouvelle Demande (en rouge pour attirer l'attention)
    if st.button("+ Nouvelle Demande", use_container_width=True, type="secondary"):
        st.session_state.show_form = not st.session_state.show_form

# 6. FORMULAIRE DE SAISIE (Gris foncé appliqué via CSS)
if st.session_state.show_form:
    with st.expander("Nouvelle saisie", expanded=True):
        with st.form("add_form"):
            prod = st.text_input("Produit")
            qte = st.number_input("Quantité", min_value=1)
            desc = st.text_area("Description")
            submit = st.form_submit_button("Envoyer la demande")
            if submit:
                new_data = {
                    "ID": f"D00{len(st.session_state.db)+1}",
                    "Produit": prod, "Quantité": qte, 
                    "Date": datetime.now().strftime("%d/%m/%Y"),
                    "Statut": "En attente Production", "Description": desc, "Priorité": "Moyenne"
                }
                st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_data])], ignore_index=True)
                st.session_state.show_form = False
                st.rerun()

# 7. INDICATEURS (KPI) EN GRIS FONCÉ
st.write("")
k1, k2, k3, k4 = st.columns(4)
total = len(st.session_state.db)

k1.markdown(f'<div class="kpi-card"><div>Total Demandes</div><div style="font-size:24px; font-weight:bold;">{total}</div></div>', unsafe_allow_html=True)
k2.markdown('<div class="kpi-card"><div>En Attente</div><div style="font-size:24px; font-weight:bold;">1</div></div>', unsafe_allow_html=True)
k3.markdown('<div class="kpi-card"><div>Approuvées</div><div style="font-size:24px; font-weight:bold;">0</div></div>', unsafe_allow_html=True)
k4.markdown('<div class="kpi-card"><div>Refusées</div><div style="font-size:24px; font-weight:bold;">0</div></div>', unsafe_allow_html=True)

st.divider()

# 8. AFFICHAGE DES DEMANDES
for index, row in st.session_state.db.iterrows():
    st.markdown(f"""
    <div class="demand-card">
        <div style="display: flex; justify-content: space-between;">
            <span style="background:#FFF9C4; color:#FBC02D; padding:5px 12px; border-radius:20px; font-size:12px; font-weight:bold;">{row['Statut']}</span>
            <span style="color: #CC0000; font-weight: bold;">● {row['Priorité']}</span>
        </div>
        <h3 style="margin: 10px 0;">{row['Produit']}</h3>
        <p style="font-size: 14px; color: #666;">
            <b>ID:</b> {row['ID']} | <b>Date:</b> {row['Date']} | <b>Quantité:</b> {row['Quantité']}
        </p>
    </div>
    """, unsafe_allow_html=True)
