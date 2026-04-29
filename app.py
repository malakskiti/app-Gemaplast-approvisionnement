import streamlit as st
import pandas as pd

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Gemaplast - Flux Achat", layout="centered")

# 2. DESIGN PERSONNALISÉ (Noir, Rouge, Blanc, Gris)
st.markdown("""
    <style>
    /* Fond de l'application */
    .stApp { background-color: #f4f4f4; }
    
    /* En-tête et Titres */
    h1, h2, h3 { color: #1a1a1a !important; font-family: 'Arial', sans-serif; }
    
    /* Boutons */
    .stButton>button { 
        width: 100%; 
        border-radius: 5px; 
        background-color: #cc0000; /* Rouge */
        color: white; 
        border: none;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #1a1a1a; color: white; border: 1px solid #cc0000; }
    
    /* Cartes blanches pour le contenu */
    .card { 
        background-color: #ffffff; 
        padding: 25px; 
        border-radius: 10px; 
        border-left: 8px solid #cc0000; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    /* Barre latérale (Noir) */
    [data-testid="stSidebar"] { background-color: #1a1a1a; color: white; }
    [data-testid="stSidebar"] * { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. INITIALISATION DE LA SESSION
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["ID", "Produit", "Desc", "Qte", "Statut", "Fournisseur"])

# --- PAGE DE CONNEXION ---
def login_page():
    st.image("https://via.placeholder.com/150/1a1a1a/cc0000?text=GEMAPLAST", width=120) # Remplace par ton logo réel
    st.title("🔴 GEMAPLAST")
    st.subheader("Système de Gestion des Flux")
    
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        email = st.text_input("Identifiant (Email)")
        password = st.text_input("Code d'accès", type="password")
        
        # Simulation de base de données utilisateurs
        users = {
            "magasinier@gemaplast.ma": {"code": "1234", "role": "Magasinier"},
            "production@gemaplast.ma": {"code": "2222", "role": "Responsable Production"},
            "achat@gemaplast.ma": {"code": "3333", "role": "Responsable Achat"},
            "dg@gemaplast.ma": {"code": "4444", "role": "Directeur Général"}
        }

        if st.button("SE CONNECTER"):
            if email in users and users[email]["code"] == password:
                st.session_state.authenticated = True
                st.session_state.user_role = users[email]["role"]
                st.rerun()
            else:
                st.error("Identifiants incorrects. Veuillez réessayer.")
        st.markdown("</div>", unsafe_allow_html=True)

# --- LOGIQUE APRÈS CONNEXION ---
if not st.session_state.authenticated:
    login_page()
else:
    # Sidebar de déconnexion
    st.sidebar.write(f"Utilisateur : **{st.session_state.user_role}**")
    if st.sidebar.button("Se déconnecter"):
        st.session_state.authenticated = False
        st.rerun()

    # --- INTERFACES SELON LE RÔLE ---
    
    # 1. MAGASINIER
    if st.session_state.user_role == "Magasinier":
        st.header("📦 Espace Magasin")
        with st.container():
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            nom = st.text_input("Nom du Produit")
            desc = st.text_area("Description technique")
            qte = st.number_input("Quantité nécessaire", min_value=1)
            if st.button("ENVOYER POUR VALIDATION"):
                new_id = len(st.session_state.db) + 1
                entry = {"ID": new_id, "Produit": nom, "Desc": desc, "Qte": qte, "Statut": "Attente Production", "Fournisseur": ""}
                st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([entry])], ignore_index=True)
                st.success("Demande transmise au Responsable Production.")
            st.markdown("</div>", unsafe_allow_html=True)

    # 2. PRODUCTION
    elif st.session_state.user_role == "Responsable Production":
        st.header("⚙️ Vérification Production")
        items = st.session_state.db[st.session_state.db['Statut'] == "Attente Production"]
        if items.empty: st.info("Aucune demande en attente de calcul.")
        for idx, row in items.iterrows():
            st.markdown(f"<div class='card'><b>Demande #{row['ID']}</b> : {row['Produit']}<br>{row['Desc']}</div>", unsafe_allow_html=True)
            new_qte = st.number_input(f"Ajuster Quantité #{row['ID']}", value=int(row['Qte']), key=f"q_{idx}")
            if st.button(f"VALIDER LE CALCUL #{row['ID']}"):
                st.session_state.db.at[idx, 'Qte'] = new_qte
                st.session_state.db.at[idx, 'Statut'] = "Attente Achat"
                st.rerun()

    # 3. ACHAT
    elif st.session_state.user_role == "Responsable Achat":
        st.header("🛒 Audit Achats")
        items = st.session_state.db[st.session_state.db['Statut'] == "Attente Achat"]
        for idx, row in items.iterrows():
            st.markdown(f"<div class='card'><b>{row['Produit']}</b> (Qte: {row['Qte']})</div>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            if c1.button(f"✅ Transmettre au DG", key=f"dgv_{idx}"):
                st.session_state.db.at[idx, 'Statut'] = "Attente DG"
                st.rerun()
            if c2.button(f"❌ Refuser", key=f"ref_{idx}"):
                st.session_state.db.at[idx, 'Statut'] = "Attente Production"
                st.rerun()

    # 4. DIRECTEUR GÉNÉRAL
    elif st.session_state.user_role == "Directeur Général":
        st.header("🏛️ Approbation Direction")
        items = st.session_state.db[st.session_state.db['Statut'] == "Attente DG"]
        for idx, row in items.iterrows():
            st.markdown(f"<div class='card'><b>CONFIRMATION OFFICIELLE :</b> {row['Produit']}</div>", unsafe_allow_html=True)
            if st.button(f"✍️ SIGNER ET VALIDER #{row['ID']}"):
                st.session_state.db.at[idx, 'Statut'] = "COMMANDE VALIDÉE"
                st.rerun()

    # Bas de page : Tableau de bord pour tous
    st.divider()
    st.subheader("📊 État des flux")
    st.table(st.session_state.db[["ID", "Produit", "Qte", "Statut"]])
