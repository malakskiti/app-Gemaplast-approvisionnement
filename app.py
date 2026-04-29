import streamlit as st
import pandas as pd
from datetime import datetime

# Configuration de la page
st.set_page_config(page_title="App Flux Achat", layout="centered")

# --- SIMULATION BASE DE DONNÉES (Dans une vraie app, utilisez Google Sheets ou SQL) ---
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=[
        "ID", "Produit", "Description", "Photo", "Quantite", "Statut", "Fournisseur"
    ])

# --- AUTHENTIFICATION ---
st.sidebar.title("🔑 Connexion")
user_role = st.sidebar.selectbox("Choisissez votre rôle", 
    ["Magasinier", "Responsable Production", "Responsable Achat", "Directeur Général"])

st.title(f"Interface : {user_role}")
st.divider()

# --- LOGIQUE DES ÉTAPES ---

# ÉTAPE 1 : MAGASINIER
if user_role == "Magasinier":
    st.subheader("📦 Nouvelle Demande de Besoin")
    with st.form("form_magasinier"):
        nom_produit = st.text_input("Nom du produit")
        description = st.text_area("Description / Urgence")
        photo = st.camera_input("Prendre une photo du produit")
        quantite = st.number_input("Quantité initiale", min_value=1)
        
        if st.form_submit_button("Envoyer au Responsable Production"):
            new_id = len(st.session_state.db) + 1
            new_entry = {
                "ID": new_id, "Produit": nom_produit, "Description": description,
                "Photo": photo, "Quantite": quantite, "Statut": "Attente Production",
                "Fournisseur": "Non défini"
            }
            st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_entry])], ignore_index=True)
            st.success("Demande envoyée !")

# ÉTAPE 2 : RESPONSABLE PRODUCTION
elif user_role == "Responsable Production":
    st.subheader("⚙️ Vérification Technique & Calcul")
    items = st.session_state.db[st.session_state.db['Statut'] == "Attente Production"]
    
    for index, row in items.iterrows():
        with st.expander(f"Demande #{row['ID']} - {row['Produit']}"):
            st.write(f"Description: {row['Description']}")
            # Simulation calcul technique
            new_qte = st.number_input(f"Ajuster Quantité pour #{row['ID']}", value=int(row['Quantite']))
            if st.button(f"Valider Calcul #{row['ID']}"):
                st.session_state.db.at[index, 'Quantite'] = new_qte
                st.session_state.db.at[index, 'Statut'] = "Attente Achat"
                st.rerun()

# ÉTAPE 3 : RESPONSABLE ACHAT
elif user_role == "Responsable Achat":
    st.subheader("🛒 Audit Commercial")
    items = st.session_state.db[st.session_state.db['Statut'] == "Attente Achat"]
    
    for index, row in items.iterrows():
        with st.expander(f"Demande #{row['ID']} - {row['Produit']}"):
            st.write(f"Quantité validée : {row['Quantite']}")
            col1, col2 = st.columns(2)
            if col1.button(f"✅ Envoyer au DG #{row['ID']}"):
                st.session_state.db.at[index, 'Statut'] = "Attente DG"
                st.rerun()
            if col2.button(f"❌ Refuser #{row['ID']}"):
                st.session_state.db.at[index, 'Statut'] = "Attente Production"
                st.warning("Retourné à la production")
                st.rerun()

# ÉTAPE 4 & 5 : DIRECTION & FINALISATION
elif user_role == "Directeur Général":
    st.subheader("🏛️ Approbation Finale DG")
    items = st.session_state.db[st.session_state.db['Statut'] == "Attente DG"]
    
    for index, row in items.iterrows():
        st.info(f"Produit: {row['Produit']} | Quantité: {row['Quantite']}")
        if st.button(f"🖋️ Signature Officielle pour #{row['ID']}"):
            st.session_state.db.at[index, 'Statut'] = "Validé"
            st.session_state.db.at[index, 'Fournisseur'] = "Contact: fournisseur@exemple.com"
            st.success("Approuvé ! Notification envoyée aux achats.")

# Affichage du suivi pour tous (Tableau de bord)
st.divider()
st.subheader("📊 Suivi des demandes")
st.dataframe(st.session_state.db)
