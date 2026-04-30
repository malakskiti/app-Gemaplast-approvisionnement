import streamlit as st
import pandas as pd

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Gemaplast - Workflow Achat", layout="wide")

# 2. DESIGN PERSONNALISÉ (CSS)
st.markdown("""
    <style>
    #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem !important;}
    header {visibility: hidden; height: 0px !important;}
    footer {visibility: hidden;}
    
    .gemaplast-logo-text {
        color: #CC0000 !important;
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        font-style: italic;
        font-size: 50px;
        text-align: center;
        margin-top: 20px;
    }

    .stApp { background-color: #FFFFFF !important; }

    section[data-testid="stSidebar"] { background-color: #000000 !important; }
    section[data-testid="stSidebar"] * { color: white !important; }

    /* TABLEAU EN-TÊTE ROUGE ET TEXTE NOIR */
    thead tr th {
        background-color: #CC0000 !important;
        color: #000000 !important;
        font-weight: bold !important;
    }
    
    .result-box {
        background-color: #262730;
        color: #FFFFFF !important;
        padding: 8px;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #CC0000;
        margin-top: 28px;
    }

    .prod-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        margin-bottom: 15px;
    }
    .prod-card * { color: #000000 !important; }

    .stButton>button { 
        background-color: #CC0000 !important; 
        color: white !important;
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. INITIALISATION
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["ID", "Produit", "Quantité", "Unité", "Statut"])

# Dictionnaire des accès
USERS_DB = {
    "magasinier@gemaplast.ma": {"code": "1111", "role": "Magasinier"},
    "production@gemaplast.ma": {"code": "2222", "role": "Responsable Production"},
    "achat@gemaplast.ma": {"code": "3333", "role": "Responsable Achat"},
    "dg@gemaplast.ma": {"code": "4444", "role": "Directeur Général"}
}

st.markdown("<p class='gemaplast-logo-text'>GEMAPLAST</p>", unsafe_allow_html=True)

# 4. LOGIQUE DE CONNEXION
if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<h2 style='text-align:center; color:black;'>Connexion Sécurisée</h2>", unsafe_allow_html=True)
        email = st.text_input("Identifiant Email")
        password = st.text_input("Code d'accès", type="password")
        
       if st.button("ACCÉDER AU PORTAIL"):
    # On force la mise en minuscule de l'email pour éviter les erreurs de frappe
    clean_email = email.strip().lower() 
    
    if clean_email in USERS_DB and USERS_DB[clean_email]["code"] == password:
        st.session_state.authenticated = True
        st.session_state.user_role = USERS_DB[clean_email]["role"]
        st.session_state.user_email = clean_email
        st.rerun()
    # Ajoute ce bloc pour voir ce que le code reçoit vraiment (utile pour débugger)
    else:
        st.error(f"Email reçu: '{email}' | Code reçu: '{password}'")
else:
    # SIDEBAR
    with st.sidebar:
        st.markdown("<h2 style='color:white; font-style:italic;'>GEMAPLAST</h2>", unsafe_allow_html=True)
        st.write(f"Rôle : **{st.session_state.user_role}**")
        if st.button("Déconnexion"):
            st.session_state.authenticated = False
            st.rerun()

    # --- PARTIE CALCULATEUR (Visible par tous ou seulement Production selon ton choix) ---
    st.markdown("<h3 style='color: #CC0000;'>🧮 Calculateur de Contrôle</h3>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1: x = st.number_input("Valeur x", value=0.0)
    with c2: y = st.number_input("Valeur y", value=0.0)
    with c3:
        z = x + y
        st.markdown(f"<div class='result-box'>TOTAL (Z) : <b>{z}</b></div>", unsafe_allow_html=True)

    st.divider()

    # --- INTERFACE SELON LE RÔLE ---
    
    # MAGASINIER
    if st.session_state.user_role == "Magasinier":
        st.subheader("Nouvelle Demande d'Approvisionnement")
        with st.form("demande_form"):
            prod = st.selectbox("Produit", ["Huile moteur", "PVC", "Acier", "Courroie"])
            qte = st.number_input("Quantité", min_value=1)
            if st.form_submit_button("Envoyer la demande"):
                new_id = len(st.session_state.db) + 1
                new_row = {"ID": new_id, "Produit": prod, "Quantité": qte, "Unité": "Unité", "Statut": "Attente Production"}
                st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_row])], ignore_index=True)
                st.success("Demande envoyée !")

    # PRODUCTION
    elif st.session_state.user_role == "Responsable Production":
        st.markdown("<h2 style='color: #CC0000;'>Validation Production</h2>", unsafe_allow_html=True)
        demandes = st.session_state.db[st.session_state.db['Statut'] == "Attente Production"]
        if demandes.empty:
            st.info("Aucune commande en attente.")
        else:
            for index, row in demandes.iterrows():
                st.markdown(f"""
                <div class='prod-card'>
                    <h4>Demande #{row['ID']} - {row['Produit']}</h4>
                    <p>Quantité : <b>{row['Quantité']}</b> | Calcul : <b style='color:#CC0000;'>{z}</b></p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Approuver #{row['ID']}", key=f"app_{index}"):
                    st.session_state.db.at[index, 'Statut'] = "Approuvé Prod"
                    st.rerun()

    # --- TABLEAU DE SUIVI (EN BAS POUR TOUT LE MONDE) ---
    st.divider()
    st.subheader("📊 Suivi des flux")
    st.dataframe(st.session_state.db, use_container_width=True)
