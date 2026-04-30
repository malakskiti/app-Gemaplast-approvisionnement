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
    .main .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
    }
    
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

    section[data-testid="stSidebar"] { background-color: #000000 !important; }
    section[data-testid="stSidebar"] * { color: white !important; }

    /* STYLE DE LA CARTE BLANCHE (OPÉRATION) */
    .prod-card {
        background-color: #f8f9fa;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        color: #000000 !important; /* Texte en noir */
    }

    .stButton>button { 
        background-color: #CC0000 !important; 
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        height: 40px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. INITIALISATION
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["ID", "Produit", "Quantité", "Unité", "Statut"])

# --- CONNEXION ---
if not st.session_state.authenticated:
    st.markdown("<p class='gemaplast-logo-text'>GEMAPLAST</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        st.markdown("<div style='background-color:#f8f9fa; padding:40px; border-radius:15px; border:1px solid #e0e0e0;'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color:black; text-align:center;'>Connexion Sécurisée</h2>", unsafe_allow_html=True)
        email = st.text_input("Identifiant Email")
        password = st.text_input("Code d'accès", type="password")
        if st.button("ACCÉDER AU PORTAIL"):
            if password == "2222": # Test rapide pour Responsable Prod
                st.session_state.authenticated = True
                st.session_state.user_role = "Responsable Production"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # --- CALCULATEUR (X + Y = Z) ---
    st.markdown("<h3 style='color: #000000;'>🧮 Calculateur Rapide</h3>", unsafe_allow_html=True)
    c_x, c_y, c_z = st.columns(3)
    with c_x: val_x = st.number_input("Valeur x", value=0.0, key="x")
    with c_y: val_y = st.number_input("Valeur y", value=0.0, key="y")
    with c_z: 
        val_z = val_x + val_y
        st.metric("Résultat z", f"{val_z}")

    st.divider()

    # --- ESPACE RESPONSABLE PRODUCTION ---
    if st.session_state.user_role == "Responsable Production":
        st.markdown("<h2 style='color: #CC0000;'>Espace Responsable Production</h2>", unsafe_allow_html=True)
        
        demandes = st.session_state.db[st.session_state.db['Statut'] == "Attente Production"]
        
        if demandes.empty:
            st.info("Aucune opération en attente.")
        else:
            for index, row in demandes.iterrows():
                # PARTIE BLANCHE AVEC LE RÉSULTAT DU CALCUL
                st.markdown(f"""
                <div class='prod-card'>
                    <h4 style='color:black;'>Opération : Demande #{row['ID']}</h4>
                    <p style='color:black;'><b>Produit :</b> {row['Produit']}</p>
                    <p style='color:black;'><b>Quantité demandée :</b> {row['Quantité']} {row['Unité']}</p>
                    <hr>
                    <p style='color:black; font-size:18px;'><b>➡️ Résultat de votre calcul (z) : <span style='color:#CC0000;'>{val_z}</span></b></p>
                </div>
                """, unsafe_allow_html=True)
                
                c1, c2, _ = st.columns([1, 1, 4])
                if c1.button(f"Approuver #{row['ID']}", key=f"a{row['ID']}"):
                    st.session_state.db.at[index, 'Statut'] = "Approuvé par Prod"
                    st.rerun()
                if c2.button(f"Rejeter #{row['ID']}", key=f"r{row['ID']}"):
                    st.session_state.db.at[index, 'Statut'] = "Rejeté par Prod"
                    st.rerun()

    # TABLEAU DE SUIVI
    st.divider()
    st.subheader("📊 Suivi des flux")
    st.dataframe(st.session_state.db, use_container_width=True)
