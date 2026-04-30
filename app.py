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
    
    /* Logo Gemaplast en Rouge */
    .gemaplast-logo-text {
        color: #CC0000 !important;
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        font-style: italic;
        font-size: 50px;
        text-align: center;
        margin-top: 10px;
    }

    .stApp { background-color: #FFFFFF !important; }

    /* Barre latérale noire */
    section[data-testid="stSidebar"] { background-color: #000000 !important; }
    section[data-testid="stSidebar"] * { color: white !important; }

    /* Boîte de résultat du calcul */
    .result-box {
        background-color: #262730;
        color: #FFFFFF !important;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        border: 2px solid #CC0000;
    }

    /* Carte blanche pour les opérations */
    .prod-card {
        background-color: #f8f9fa;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        color: #000000 !important;
    }

    .stButton>button { 
        background-color: #CC0000 !important; 
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. INITIALISATION
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'db' not in st.session_state:
    # On ajoute une ligne d'exemple pour tester l'affichage
    st.session_state.db = pd.DataFrame([
        {"ID": 1, "Produit": "Huile moteur 5W-30", "Quantité": 20, "Unité": "Litre", "Statut": "Attente Production"}
    ])

# --- LOGIQUE ---
if not st.session_state.authenticated:
    st.markdown("<p class='gemaplast-logo-text'>GEMAPLAST</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        st.markdown("<h2 style='color:black; text-align:center;'>Connexion</h2>", unsafe_allow_html=True)
        password = st.text_input("Code d'accès", type="password")
        if st.button("ACCÉDER"):
            if password == "2222":
                st.session_state.authenticated = True
                st.session_state.user_role = "Responsable Production"
                st.rerun()
else:
    # SIDEBAR
    with st.sidebar:
        st.markdown("<h2 style='color:white; font-style:italic;'>GEMAPLAST</h2>", unsafe_allow_html=True)
        st.write(f"Rôle : **{st.session_state.user_role}**")
        if st.button("Déconnexion"):
            st.session_state.authenticated = False
            st.rerun()

    # SECTION CALCULATEUR AMÉLIORÉE
    st.markdown("### 🧮 Calculateur de Contrôle (x + y = z)")
    col_input1, col_input2, col_res = st.columns([1, 1, 1.5])
    
    with col_input1:
        x = st.number_input("Valeur x", value=0.0)
    with col_input2:
        y = st.number_input("Valeur y", value=0.0)
    with col_res:
        z = x + y
        st.markdown(f"""
            <div class='result-box'>
                <span style='font-size:14px; opacity:0.8;'>RÉSULTAT TOTAL (Z)</span><br>
                <span style='font-size:32px; font-weight:bold;'>{z}</span>
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ESPACE PRODUCTION
    if st.session_state.user_role == "Responsable Production":
        st.markdown("<h2 style='color: #CC0000;'>Espace Responsable Production</h2>", unsafe_allow_html=True)
        
        demandes = st.session_state.db[st.session_state.db['Statut'] == "Attente Production"]
        
        if demandes.empty:
            st.info("Aucune opération en attente.")
        else:
            for index, row in demandes.iterrows():
                st.markdown(f"""
                <div class='prod-card'>
                    <h4 style='color:black;'>Demande #{row['ID']} - {row['Produit']}</h4>
                    <p style='color:black;'>Quantité : <b>{row['Quantité']} {row['Unité']}</b></p>
                    <p style='color:black; font-size:18px;'>Valeur calculée actuelle : <b style='color:#CC0000;'>{z}</b></p>
                </div>
                """, unsafe_allow_html=True)
                
                c1, c2, _ = st.columns([1, 1, 4])
                if c1.button(f"Approuver #{row['ID']}", key=f"a{index}"):
                    st.session_state.db.at[index, 'Statut'] = "Approuvé"
                    st.rerun()
                if c2.button(f"Rejeter #{row['ID']}", key=f"r{index}"):
                    st.session_state.db.at[index, 'Statut'] = "Rejeté"
                    st.rerun()

    # SUIVI
    st.divider()
    st.subheader("📊 Suivi des flux")
    st.dataframe(st.session_state.db, use_container_width=True)
