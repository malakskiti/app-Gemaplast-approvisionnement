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

    .login-card, .prod-card {
        background-color: #f8f9fa;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    .stButton>button { 
        background-color: #CC0000 !important; 
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        height: 40px !important;
        border: none !important;
    }
    
    /* Style spécifique pour les boutons de validation */
    .btn-approve > div > button { background-color: #28a745 !important; }
    .btn-reject > div > button { background-color: #dc3545 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. INITIALISATION DE LA SESSION
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'db' not in st.session_state:
    # Simulation de quelques données pour tester
    st.session_state.db = pd.DataFrame([
        {"ID": 1, "Produit": "PVC", "Quantité": 50, "Unité": "Plaque", "Statut": "Attente Production"},
        {"ID": 2, "Produit": "Huile moteur", "Quantité": 10, "Unité": "Litre", "Statut": "Attente Production"}
    ])

# --- LOGIQUE D'AFFICHAGE ---

if not st.session_state.authenticated:
    st.markdown("<p class='gemaplast-logo-text'>GEMAPLAST</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        st.markdown("<div class='login-card'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color:black; text-align:center;'>Connexion Sécurisée</h2>", unsafe_allow_html=True)
        
        email = st.text_input("Identifiant Email")
        password = st.text_input("Code d'accès", type="password")
        
        users = {
            "magasinier@gemaplast.ma": {"code": "1234", "role": "Magasinier"},
            "production@gemaplast.ma": {"code": "2222", "role": "Responsable Production"},
            "achat@gemaplast.ma": {"code": "3333", "role": "Responsable Achat"},
            "dg@gemaplast.ma": {"code": "4444", "role": "Directeur Général"}
        }

        if st.button("ACCÉDER AU PORTAIL"):
            if email in users and users[email]["code"] == password:
                st.session_state.authenticated = True
                st.session_state.user_role = users[email]["role"]
                st.rerun()
            else:
                st.error("Email ou code incorrect.")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    with st.sidebar:
        st.markdown("<h2 style='color:white; font-style:italic;'>GEMAPLAST</h2>", unsafe_allow_html=True)
        st.write(f"Connecté : **{st.session_state.user_role}**")
        if st.button("Déconnexion"):
            st.session_state.authenticated = False
            st.rerun()

    # --- ESPACE RESPONSABLE PRODUCTION ---
    if st.session_state.user_role == "Responsable Production":
        st.markdown("<h2 style='color: #CC0000;'>Espace Responsable Production</h2>", unsafe_allow_html=True)
        
        # Filtrer les demandes en attente de production
        demandes_a_valider = st.session_state.db[st.session_state.db['Statut'] == "Attente Production"]
        
        if demandes_a_valider.empty:
            st.success("Aucune demande en attente de validation.")
        else:
            for index, row in demandes_a_valider.iterrows():
                with st.container():
                    st.markdown(f"""
                    <div class='prod-card'>
                        <h4 style='margin-top:0;'>Demande #{row['ID']} - {row['Produit']}</h4>
                        <p><b>Quantité :</b> {row['Quantité']} {row['Unité']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    c1, c2, _ = st.columns([1, 1, 4])
                    with c1:
                        if st.button(f"Approuver #{row['ID']}", key=f"app_{row['ID']}"):
                            st.session_state.db.at[index, 'Statut'] = "Approuvé par Production"
                            st.rerun()
                    with c2:
                        if st.button(f"Rejeter #{row['ID']}", key=f"rej_{row['ID']}"):
                            st.session_state.db.at[index, 'Statut'] = "Rejeté par Production"
                            st.rerun()

    # --- ESPACE MAGASINIER (Rappel du code précédent) ---
    elif st.session_state.user_role == "Magasinier":
        st.markdown("<h2 style='color: #CC0000;'>Espace Magasinier</h2>", unsafe_allow_html=True)
        # ... (votre code magasinier avec la liste déroulante reste ici)

    st.divider()
    st.subheader("📊 État global du stock et des flux")
    st.dataframe(st.session_state.db, use_container_width=True)
