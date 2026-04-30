import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURATION
st.set_page_config(page_title="Gemaplast - Workflow", layout="wide")

# (Le style CSS reste le même que précédemment)
st.markdown("""
    <style>
    header {visibility: hidden;}
    .gemaplast-logo { color: #CC0000; font-weight: bold; font-style: italic; font-size: 40px; }
    .stApp { background-color: #F8F9FA; }
    .kpi-card { background-color: white; padding: 20px; border-radius: 15px; border: 1px solid #E0E0E0; text-align: center; }
    .kpi-value { font-size: 24px; font-weight: bold; }
    .demand-card { background-color: white; padding: 25px; border-radius: 15px; border: 1px solid #E0E0E0; margin-bottom: 20px; }
    .status-badge { background-color: #FFF9C4; color: #FBC02D; padding: 5px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. INITIALISATION DES ÉTATS
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["ID", "Produit", "Quantité", "Date", "Statut", "Description", "Priorité"])
if 'show_form' not in st.session_state:
    st.session_state.show_form = False

# 3. CONNEXION (Simplifiée pour l'exemple)
if not st.session_state.authenticated:
    st.title("Connexion Gemaplast")
    user = st.text_input("Email")
    pwd = st.text_input("Pass", type="password")
    if st.button("Se connecter"):
        if pwd == "1111": # Test rapide pour Magasinier
            st.session_state.authenticated = True
            st.session_state.user_role = "Magasinier"
            st.rerun()
else:
    # --- INTERFACE MAGASINIER ---
    if st.session_state.user_role == "Magasinier":
        
        # En-tête avec bouton fonctionnel
        head1, head2 = st.columns([3, 1])
        with head1:
            st.markdown("<h1>Mes Demandes d'Approvisionnement</h1>", unsafe_allow_html=True)
        with head2:
            # Cliquer ici bascule l'affichage du formulaire
            if st.button("+ Nouvelle Demande", type="primary", use_container_width=True):
                st.session_state.show_form = not st.session_state.show_form

        # --- FORMULAIRE DE SAISIE (Apparaît si on clique sur le bouton) ---
        if st.session_state.show_form:
            with st.expander("📝 Remplir la nouvelle demande", expanded=True):
                with st.form("new_demand_form"):
                    col_f1, col_f2 = st.columns(2)
                    with col_f1:
                        prod = st.text_input("Nom du produit", placeholder="ex: Huile moteur 5W-30")
                        qte = st.number_input("Quantité", min_value=1)
                    with col_f2:
                        prio = st.selectbox("Priorité", ["Basse", "Moyenne", "Haute"])
                        desc = st.text_area("Description / Motif", placeholder="Besoin urgent...")
                    
                    if st.form_submit_button("Confirmer et Envoyer"):
                        new_id = f"D{len(st.session_state.db) + 1:03d}"
                        new_data = {
                            "ID": new_id,
                            "Produit": prod,
                            "Quantité": qte,
                            "Date": datetime.now().strftime("%d/%m/%Y"),
                            "Statut": "En attente Production",
                            "Description": desc,
                            "Priorité": prio
                        }
                        st.session_state.db = pd.concat([pd.DataFrame([new_data]), st.session_state.db], ignore_index=True)
                        st.session_state.show_form = False # Ferme le formulaire après envoi
                        st.success(f"Demande {new_id} envoyée !")
                        st.rerun()

        # --- INDICATEURS (KPIs) ---
        st.write("")
        k1, k2, k3, k4 = st.columns(4)
        k1.markdown(f"<div class='kpi-card'><div style='color:#666'>Total</div><div class='kpi-value'>{len(st.session_state.db)}</div></div>", unsafe_allow_html=True)
        # ... (ajoute les autres KPI ici)

        st.divider()

        # --- AFFICHAGE DES CARTES (LISTE) ---
        if st.session_state.db.empty:
            st.info("Aucune demande pour le moment. Cliquez sur '+ Nouvelle Demande'.")
        else:
            for index, row in st.session_state.db.iterrows():
                st.markdown(f"""
                <div class="demand-card">
                    <div style="display: flex; justify-content: space-between;">
                        <span class="status-badge">⌛ {row['Statut']}</span>
                        <span style="color: #CC0000; font-weight: bold;">● {row['Priorité']}</span>
                    </div>
                    <h3 style="margin: 10px 0;">{row['Produit']} (ID: {row['ID']})</h3>
                    <p><b>Quantité:</b> {row['Quantité']} | <b>Date:</b> {row['Date']}</p>
                    <p style="color: #666; font-size: 14px;">{row['Description']}</p>
                </div>
                """, unsafe_allow_html=True)
