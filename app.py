import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURATION
st.set_page_config(page_title="Gemaplast - Workflow", layout="wide")

# 2. STYLE CSS
st.markdown("""
    <style>
    header {visibility: hidden;}
    .stApp { background-color: #F8F9FA; }
    
    /* Style du Logo Gemaplast */
    .logo-text {
        color: #CC0000;
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        font-style: italic;
        font-size: 35px;
        line-height: 1;
    }
    
    /* Style du Titre Rouge */
    .titre-rouge {
        color: #CC0000;
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        font-size: 30px;
        margin-left: -20px; /* Rapproche le titre du logo */
    }

    /* Cartes et Badges */
    .kpi-card { background-color: white; padding: 20px; border-radius: 15px; border: 1px solid #E0E0E0; text-align: center; }
    .demand-card { background-color: white; padding: 25px; border-radius: 15px; border: 1px solid #E0E0E0; margin-bottom: 20px; box-shadow: 2px 4px 10px rgba(0,0,0,0.05); }
    .status-badge { background-color: #FFF9C4; color: #FBC02D; padding: 5px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. INITIALISATION (SI VIDE)
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([
        {"ID": "D001", "Produit": "Huile moteur 5W-30 (20L)", "Quantité": 10, "Date": "28/04/2026", "Statut": "En attente Production", "Description": "Stock faible", "Priorité": "Haute"}
    ])
if 'show_form' not in st.session_state:
    st.session_state.show_form = False

# --- HAUT DE PAGE : LOGO ET TITRE ---
col_logo, col_titre, col_btn = st.columns([1, 3, 1])

with col_logo:
    # Insertion du logo à gauche
    st.markdown('<p class="logo-text">GEMAPLAST</p>', unsafe_allow_html=True)

with col_titre:
    # Titre en rouge
    st.markdown('<p class="titre-rouge">Mes Demandes d\'Approvisionnement</p>', unsafe_allow_html=True)

with col_btn:
    # Bouton nouvelle demande
    if st.button("+ Nouvelle Demande", type="primary", use_container_width=True):
        st.session_state.show_form = not st.session_state.show_form

st.write("Créez et suivez vos demandes de produits")

# --- FORMULAIRE (Optionnel) ---
if st.session_state.show_form:
    with st.expander("Saisir une nouvelle demande", expanded=True):
        with st.form("form_add"):
            p = st.text_input("Produit")
            q = st.number_input("Quantité", min_value=1)
            submit = st.form_submit_button("Envoyer")
            if submit:
                # Logique d'ajout ici...
                st.success("Demande envoyée")
                st.session_state.show_form = False
                st.rerun()

# --- INDICATEURS ---
st.write("")
k1, k2, k3, k4 = st.columns(4)
k1.markdown(f"<div class='kpi-card'><div style='color:#666'>Total</div><div style='font-size:24px; font-weight:bold;'>{len(st.session_state.db)}</div></div>", unsafe_allow_html=True)
k2.markdown("<div class='kpi-card'><div style='color:#666'>En Attente</div><div style='font-size:24px; font-weight:bold;'>1</div></div>", unsafe_allow_html=True)
k3.markdown("<div class='kpi-card'><div style='color:#666'>Approuvées</div><div style='font-size:24px; font-weight:bold;'>0</div></div>", unsafe_allow_html=True)
k4.markdown("<div class='kpi-card'><div style='color:#666'>Refusées</div><div style='font-size:24px; font-weight:bold;'>0</div></div>", unsafe_allow_html=True)

st.divider()

# --- LISTE DES CARTES ---
for index, row in st.session_state.db.iterrows():
    st.markdown(f"""
    <div class="demand-card">
        <div style="display: flex; justify-content: space-between;">
            <span class="status-badge">{row['Statut']}</span>
            <span style="color: #CC0000; font-weight: bold;">● {row['Priorité']}</span>
        </div>
        <h3 style="margin: 10px 0; color: #333;">{row['Produit']}</h3>
        <p style="font-size: 14px; color: #555;"><b>ID:</b> {row['ID']} | <b>Date:</b> {row['Date']} | <b>Quantité:</b> {row['Quantité']}</p>
        <p style="font-style: italic; color: #888;">{row['Description']}</p>
    </div>
    """, unsafe_allow_html=True)
