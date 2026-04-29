import streamlit as st
import pandas as pd

# 1. Configuration du style "Mobile App"
st.set_page_config(page_title="Gemaplast Flow", layout="centered")

# CSS personnalisé pour un look "App Mobile" (Design épuré)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #004a99; color: white; font-weight: bold; }
    .card { background-color: white; padding: 20px; border-radius: 15px; border: 1px solid #e0e0e0; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .step-header { color: #004a99; font-weight: bold; border-left: 5px solid #004a99; padding-left: 15px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Gestion de la base de données temporaire
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["ID", "Produit", "Desc", "Qte", "Statut", "Fournisseur"])

# 3. Sidebar : Authentification par Rôle (Login)
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3063/3063822.png", width=100)
st.sidebar.title("Portail Authentifié")
user_role = st.sidebar.selectbox("Connexion en tant que :", 
    ["Magasinier", "Responsable Production", "Responsable Achat", "Directeur Général"])

# --- ÉTAPE 1 : MAGASINIER ---
if user_role == "Magasinier":
    st.markdown("<div class='step-header'><h3>📦 ÉTAPE 1 : SAISIE MAGASINIER</h3></div>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_index=True)
        nom = st.text_input("📦 Nom du Produit")
        desc = st.text_area("📝 Description & Urgence")
        photo = st.camera_input("📷 Photo du besoin")
        qte = st.number_input("🔢 Quantité souhaitée", min_value=1, value=1)
        if st.button("ENVOYER LA DEMANDE"):
            new_id = len(st.session_state.db) + 1
            entry = {"ID": new_id, "Produit": nom, "Desc": desc, "Qte": qte, "Statut": "Attente Prod", "Fournisseur": ""}
            st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([entry])], ignore_index=True)
            st.success("Notification envoyée à la Production !")
        st.markdown("</div>", unsafe_allow_html=True)

# --- ÉTAPE 2 : PRODUCTION ---
elif user_role == "Responsable Production":
    st.markdown("<div class='step-header'><h3>⚙️ ÉTAPE 2 : VÉRIFICATION TECHNIQUE</h3></div>", unsafe_allow_index=True)
    items = st.session_state.db[st.session_state.db['Statut'] == "Attente Prod"]
    if items.empty: st.info("Aucune demande en attente.")
    for idx, row in items.iterrows():
        with st.container():
            st.markdown(f"<div class='card'><b>Produit:</b> {row['Produit']}<br><i>{row['Desc']}</i>", unsafe_allow_index=True)
            new_qte = st.number_input(f"Ajuster Quantité (Calcul ratio)", value=int(row['Qte']), key=f"p_{idx}")
            if st.button(f"VALIDER LA LISTE #{row['ID']}", key=f"btn_{idx}"):
                st.session_state.db.at[idx, 'Qte'] = new_qte
                st.session_state.db.at[idx, 'Statut'] = "Attente Achat"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

# --- ÉTAPE 3 : ACHAT ---
elif user_role == "Responsable Achat":
    st.markdown("<div class='step-header'><h3>🛒 ÉTAPE 3 : AUDIT COMMERCIAL</h3></div>", unsafe_allow_index=True)
    items = st.session_state.db[st.session_state.db['Statut'] == "Attente Achat"]
    for idx, row in items.iterrows():
        with st.container():
            st.markdown(f"<div class='card'><b>Besoin:</b> {row['Produit']} | <b>Qte:</b> {row['Qte']}", unsafe_allow_index=True)
            col1, col2 = st.columns(2)
            if col1.button(f"✅ TRANSMETTRE AU DG", key=f"v_{idx}"):
                st.session_state.db.at[idx, 'Statut'] = "Attente DG"
                st.rerun()
            if col2.button(f"❌ REFUSER (RETOUR PROD)", key=f"r_{idx}"):
                st.session_state.db.at[idx, 'Statut'] = "Attente Prod"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

# --- ÉTAPE 4 : DIRECTION GÉNÉRALE ---
elif user_role == "Directeur Général":
    st.markdown("<div class='step-header'><h3>🏛️ ÉTAPE 4 : APPROBATION DG</h3></div>", unsafe_allow_index=True)
    items = st.session_state.db[st.session_state.db['Statut'] == "Attente DG"]
    for idx, row in items.iterrows():
        st.markdown(f"<div class='card'><b>INVESTISSEMENT :</b> {row['Produit']}<br>Quantité validée : {row['Qte']}", unsafe_allow_index=True)
        if st.button(f"🖋️ SIGNATURE OFFICIELLE", key=f"dg_{idx}"):
            st.session_state.db.at[idx, 'Statut'] = "VALIDÉ"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- ÉTAPE 5 : EXÉCUTION ACHAT (FOURNISSEURS) ---
if user_role == "Responsable Achat":
    st.divider()
    st.subheader("🏁 Commandes Validées (Prêtes à l'achat)")
    valid_items = st.session_state.db[st.session_state.db['Statut'] == "VALIDÉ"]
    for idx, row in valid_items.iterrows():
        st.success(f"Commande #{row['ID']} approuvée par DG")
        st.write("📞 **Fournisseur :** Contact disponible - 05 XX XX XX XX")
        st.button(f"📄 Générer Bon de Commande (PDF) #{row['ID']}")

# Tableau de bord global (Bas de page)
st.divider()
st.caption("Système de Digitalisation Gemaplast - Suivi en temps réel")
st.dataframe(st.session_state.db[["ID", "Produit", "Qte", "Statut"]])
