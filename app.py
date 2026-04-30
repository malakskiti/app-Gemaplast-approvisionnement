import streamlit as st
import pandas as pd

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Gemaplast - Workflow Achat", layout="wide")

# 2. DESIGN PERSONNALISÉ (CSS)
st.markdown("""
    <style>
    /* Nettoyage du haut de page */
    #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem !important;}
    header {visibility: hidden; height: 0px !important;}
    footer {visibility: hidden;}
    .main .block-container { padding-top: 0rem !important; padding-bottom: 0rem !important; }
    
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

    /* BARRE LATÉRALE NOIRE RÉACTIVÉE */
    section[data-testid="stSidebar"] { 
        background-color: #000000 !important; 
        min-width: 250px !important;
    }
    section[data-testid="stSidebar"] * { color: white !important; }

    /* ZONE BLANCHE DE L'OPÉRATION */
    .prod-card {
       background-color: #f8f9fa;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        color: #000000 !important;
    }
    
    /* TEXTE EN NOIR DANS LA ZONE BLANCHE */
    .prod-card p, .prod-card b, .prod-card span, .prod-card h4 {
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
    st.session_state.db = pd.DataFrame(columns=["ID", "Produit", "Quantité", "Unité", "Statut"])

# --- PAGE DE CONNEXION ---
if not st.session_state.authenticated:
    st.markdown("<p class='gemaplast-logo-text'>GEMAPLAST</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        st.markdown("<div style='background-color:#f8f9fa; padding:40px; border-radius:15px; border:1px solid #e0e0e0;'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color:black; text-align:center;'>Connexion Sécurisée</h2>", unsafe_allow_html=True)
        email = st.text_input("Identifiant Email")
        password = st.text_input("Code d'accès", type="password")
        if st.button("ACCÉDER AU PORTAIL"):
            if password == "2222":
                st.session_state.authenticated = True
                st.session_state.user_role = "Responsable Production"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # --- BARRE LATÉRALE ---
    with st.sidebar:
        st.markdown("<h2 style='color:white; font-style:italic;'>GEMAPLAST</h2>", unsafe_allow_html=True)
        st.write(f"Utilisateur : **{st.session_state.user_role}**")
        if st.button("Déconnexion"):
            st.session_state.authenticated = False
            st.rerun()

    # --- CALCULATEUR (X + Y = Z) ---
    st.markdown("<h3 style='color: #000000;'>🧮 Calculateur de Contrôle</h3>", unsafe_allow_html=True)
    c_x, c_y, c_z = st.columns(3)
    with c_x: val_x = st.number_input("Valeur x", value=0.0, key="x_val")
    with c_y: val_y = st.number_input("Valeur y", value=0.0, key="y_val")
    with c_z: 
        val_z = val_x + val_y
        st.metric("Total calculé (z)", f"{val_z}")

    st.divider()

    # --- ESPACE RESPONSABLE PRODUCTION ---
    if st.session_state.user_role == "Responsable Production":
        st.markdown("<h2 style='color: #CC0000;'>Espace Responsable Production</h2>", unsafe_allow_html=True)
        
        # Demandes en attente
        demandes = st.session_state.db[st.session_state.db['Statut'] == "Attente Production"]
        
        if demandes.empty:
            st.info("Aucune opération en attente de validation.")
        else:
            for index, row in demandes.iterrows():
                # AFFICHAGE DU RÉSULTAT DU CALCUL EN NOIR DANS LA ZONE BLANCHE
                st.markdown(f"""
                <div class='prod-card'>
                    <h4>Détails de l'opération : Demande #{row['ID']}</h4>
                    <p><b>Produit :</b> {row['Produit']}</p>
                    <p><b>Quantité demandée par Magasin :</b> {row['Quantité']} {row['Unité']}</p>
                    <hr style='border: 0.5px solid #e0e0e0;'>
                    <p style='font-size: 20px;'><b>Résultat de votre calcul : <span style='color:black;'>{val_z}</span></b></p>
                </div>
                """, unsafe_allow_html=True)
                
                c1, c2, _ = st.columns([1, 1, 4])
                if c1.button(f"Approuver #{row['ID']}", key=f"app_{row['ID']}"):
                    st.session_state.db.at[index, 'Statut'] = "Approuvé par Prod"
                    st.rerun()
                if c2.button(f"Rejeter #{row['ID']}", key=f"rej_{row['ID']}"):
                    st.session_state.db.at[index, 'Statut'] = "Rejeté par Prod"
                    st.rerun()

    # TABLEAU DE SUIVI GÉNÉRAL
    st.divider()
    st.subheader("📊 Historique et Suivi des flux")
    st.dataframe(st.session_state.db, use_container_width=True)
