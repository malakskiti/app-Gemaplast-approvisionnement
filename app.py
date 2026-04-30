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
        margin-bottom: 20px;
    }

    .stApp { background-color: #FFFFFF !important; }

    /* Barre latérale noire */
    section[data-testid="stSidebar"] { background-color: #000000 !important; }
    section[data-testid="stSidebar"] * { color: white !important; }

    /* TABLEAU (SUIVI DES FLUX) EN ROUGE ET NOIR */
    thead tr th {
        background-color: #CC0000 !important;
        color: #000000 !important;
        font-weight: bold !important;
    }
    
    [data-testid="stDataFrame"] {
        border: 2px solid #CC0000;
        border-radius: 10px;
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
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        margin-bottom: 20px;
    }
    
    .prod-card * { color: #000000 !important; }

    .stButton>button { 
        background-color: #CC0000 !important; 
        color: white !important;
        border-radius: 8px !important;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. INITIALISATION
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["ID", "Produit", "Quantité", "Unité", "Statut"])

# --- AFFICHAGE DU LOGO TOUT LE TEMPS ---
st.markdown("<p class='gemaplast-logo-text'>GEMAPLAST</p>", unsafe_allow_html=True)

# --- LOGIQUE DE CONNEXION ---
if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<h2 style='color:black; text-align:center;'>Connexion Sécurisée</h2>", unsafe_allow_html=True)
        # Rétablissement du champ Email
        user_email = st.text_input("Identifiant Email", placeholder="exemple@gemaplast.ma")
        password = st.text_input("Code d'accès", type="password")
        
        if st.button("ACCÉDER"):
            if password == "2222": # Vous pouvez ajouter une vérification d'email ici
                st.session_state.authenticated = True
                st.session_state.user_role = "Responsable Production"
                st.session_state.user_email = user_email
                st.rerun()
            else:
                st.error("Code d'accès incorrect")

else:
    # LA SIDEBAR APPARAÎT ICI APRÈS CONNEXION
    with st.sidebar:
        st.markdown("<h2 style='color:white; font-style:italic;'>GEMAPLAST</h2>", unsafe_allow_html=True)
        st.write(f"Connecté : **{st.session_state.user_email}**")
        st.write(f"Rôle : **{st.session_state.user_role}**")
        if st.button("Se déconnecter"):
            st.session_state.authenticated = False
            st.rerun()

  # --- CONTENU RESPONSABLE PRODUCTION ---
    # 1. Le titre en rouge (bien aligné)
    st.markdown("<h3 style='color: #CC0000;'>🧮 Calculateur de Contrôle</h3>", unsafe_allow_html=True)
    
    # 2. Les colonnes (alignées exactement sous le 's' de st.markdown)
    c1, c2, c3 = st.columns([1, 1, 1])
    
    with c1: 
        x = st.number_input("Valeur x", value=0.0)
    with c2: 
        y = st.number_input("Valeur y", value=0.0)
    with c3:
        z = x + y
        st.markdown(f"<div class='result-box'>TOTAL (Z) : <b>{z}</b></div>", unsafe_allow_html=True)
        z = x + y
        st.markdown(f"<div class='result-box'>TOTAL (Z) : <b>{z}</b></div>", unsafe_allow_html=True)

    st.divider()

    if st.session_state.user_role == "Responsable Production":
        st.markdown("<h2 style='color: #CC0000;'>Opérations en attente</h2>", unsafe_allow_html=True)
        demandes = st.session_state.db[st.session_state.db['Statut'] == "Attente Production"]
        
        if demandes.empty:
            st.info("Aucune commande à valider pour le moment.")
        else:
            for index, row in demandes.iterrows():
                st.markdown(f"""
                <div class='prod-card'>
                    <h4>Demande #{row['ID']} - {row['Produit']}</h4>
                    <p>Quantité : <b>{row['Quantité']} {row['Unité']}</b></p>
                    <p>Calcul actuel : <b style='color:#CC0000;'>{z}</b></p>
                </div>
                """, unsafe_allow_html=True)
                
                col_b1, col_b2, _ = st.columns([1, 1, 3])
                if col_b1.button(f"Valider #{row['ID']}", key=f"v{index}"):
                    st.session_state.db.at[index, 'Statut'] = "Validé"
                    st.rerun()
                if col_b2.button(f"Refuser #{row['ID']}", key=f"r{index}"):
                    st.session_state.db.at[index, 'Statut'] = "Refusé"
                    st.rerun()

    # TABLEAU AVEC EN-TÊTE ROUGE
    st.divider()
    st.subheader("📊 Historique des flux")
    st.dataframe(st.session_state.db, use_container_width=True)
