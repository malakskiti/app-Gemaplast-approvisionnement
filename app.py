import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURATION (TOUJOURS EN PREMIER)
st.set_page_config(page_title="Gemaplast - Workflow", layout="wide")

# --- 2. INITIALISATION DE L'ACCÈS ---
if 'authentifie' not in st.session_state:
    st.session_state.authentifie = False

# --- 3. PAGE DE LOGIN ---
if not st.session_state.authentifie:
    st.title("Authentification Gemaplast")
    user = st.text_input("Username")
    code = st.text_input("Code / Mot de passe", type="password")
    
    if st.button("Se connecter"):
        if user == "admin" and code == "1234":
            st.session_state.authentifie = True
            st.rerun()
        else:
            st.error("Identifiants incorrects")

# --- 4. TON APPLICATION (SI CONNECTÉ) ---
else:
    # --- TOUT LE CODE CI-DESSOUS EST DÉCALÉ (INDENTÉ) ---

    # Chargement du fichier Excel
    file = st.sidebar.file_uploader("Charger la liste des produits (Excel)", type=["xlsx"])
    if file is not None:
        df_produits = pd.read_excel(file)
        LISTE_PRODUITS = df_produits["Designation"].tolist()
    else:
        LISTE_PRODUITS = ["Veuillez charger un fichier Excel"]

    # STYLE CSS
    st.markdown("""
        <style>
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .stApp { background-color: #F8F9FA; }
        .logo-text { color: #CC0000; font-family: 'Arial', sans-serif; font-weight: bold; font-style: italic; font-size: 35px; }
        
        /* Forcer l'écriture en noir partout */
        input, textarea, [data-baseweb="select"] > div { 
            color: #000000 !important; 
            background-color: #FFFFFF !important; 
            -webkit-text-fill-color: #000000 !important;
        }
        
        .stTextArea label p, .stNumberInput label p, .stSelectbox label p { color: #000000 !important; font-weight: bold; }
        
        .kpi-card { background-color: #FFFFFF !important; color: black !important; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #E0E0E0; }
        .titre-rouge { color: #CC0000; font-family: 'Arial', sans-serif; font-weight: bold; font-size: 28px; }
        
        /* Style Sidebar */
        [data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #E0E0E0; }
        .sidebar-desc { color: #CC0000; font-weight: bold; font-size: 15px; text-align: center; }
        </style>
        """, unsafe_allow_html=True)

    # INITIALISATION DES DONNÉES
    if 'db' not in st.session_state:
        st.session_state.db = pd.DataFrame([
            {"ID": "D001", "Produit": "Huile moteur 5W-30 (20L)", "Quantité": 10, "Date": "28/04/2026", "Statut": "En attente Production", "Description": "Stock faible", "Priorité": "Haute"}
        ])
    if 'show_form' not in st.session_state:
        st.session_state.show_form = False

    # SIDEBAR
    with st.sidebar:
        st.markdown('<p class="logo-text" style="text-align:center;">GEMAPLAST</p>', unsafe_allow_html=True)
        st.markdown('<p class="sidebar-desc">Entreprise de fabrication de conduites en PVC et polyéthylène</p>', unsafe_allow_html=True)
        st.markdown("---")
        if st.button("🔓 Déconnexion", use_container_width=True):
            st.session_state.authentifie = False
            st.rerun()

    # EN-TÊTE
    col_logo, col_titre, col_btn = st.columns([1, 3, 1.2])
    with col_logo: st.markdown('<p class="logo-text">GEMAPLAST</p>', unsafe_allow_html=True)
    with col_titre: st.markdown('<p class="titre-rouge">Mes Demandes d\'Approvisionnement</p>', unsafe_allow_html=True)
    with col_btn:
        if st.button("+ Nouvelle Demande", use_container_width=True):
            st.session_state.show_form = not st.session_state.show_form

    # FORMULAIRE
    if st.session_state.show_form:
        with st.expander("Nouvelle saisie", expanded=True):
            with st.form("add_form"):
                prod = st.selectbox("Sélectionner le Produit", LISTE_PRODUITS)
                qte_saisie = st.number_input("Quantité à commander", min_value=1, value=1)
                desc = st.text_area("Description / Notes particulières")
                prio = st.selectbox("Priorité", ["Haute", "Moyenne", "Basse"]) 
                if st.form_submit_button("Envoyer la demande"):
                    new_data = {
                        "ID": f"D00{len(st.session_state.db)+1}",
                        "Produit": prod,
                        "Quantité": qte_saisie,
                        "Date": datetime.now().strftime("%d/%m/%Y"),
                        "Statut": "En attente Production",
                        "Description": desc,
                        "Priorité": prio
                    }
                    st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_data])], ignore_index=True)
                    st.success("Demande enregistrée !")
                    st.rerun()

    # KPI
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(f'<div class="kpi-card">Total Demandes<br><b>{len(st.session_state.db)}</b></div>', unsafe_allow_html=True)
    k2.markdown('<div class="kpi-card">En Attente<br><b>1</b></div>', unsafe_allow_html=True)
    k3.markdown('<div class="kpi-card">Approuvées<br><b>0</b></div>', unsafe_allow_html=True)
    k4.markdown('<div class="kpi-card">Refusées<br><b>0</b></div>', unsafe_allow_html=True)

    st.divider()

    # AFFICHAGE DES CARTES
    for index, row in st.session_state.db.iterrows():
        st.markdown(f"""
            <div style="background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #E0E0E0; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between;">
                    <span style="background-color: #FFF9C4; color: #FBC02D; padding: 2px 10px; border-radius: 10px; font-weight: bold; font-size: 12px;">{row['Statut']}</span>
                    <span style="color: #CC0000; font-weight: bold;">● {row['Priorité']}</span>
                </div>
                <div style="color: black; font-size: 18px; font-weight: bold; margin-top: 10px;">{row['Produit']}</div>
                <div style="color: #666; font-size: 14px;">ID: {row['ID']} | Date: {row['Date']} | Qté: {row['Quantité']}</div>
            </div>
        """, unsafe_allow_html=True)
