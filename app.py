import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gemaplast - Workflow Achat", layout="wide")

st.markdown("""
    <style>
    #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .main .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
    }

    .stApp {
        background-color: #FFFFFF !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #000000 !important;
        min-width: 320px !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0rem;
        padding-top: 0rem;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    h2 {
        color: #000000 !important;
        font-family: 'Arial Black', sans-serif !important;
        text-align: center !important;
    }

    .login-card {
        background-color: #f8f9fa;
        padding: 40px;
        border-radius: 15px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin-top: 20px;
    }

    .stButton>button { 
        background-color: #CC0000 !important; 
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        height: 48px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. INITIALISATION DES DONNÉES
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["ID", "Produit", "Qte", "Statut"])

# --- BARRE LATÉRALE ---
with st.sidebar:
    # LIGNE 61 : TON IMAGE ICI
    st.image("https://i.ibb.co/L6V8XkP/gemaplast-logo.jpg", use_container_width=True) 
    st.markdown("<br><h3 style='border-bottom: 2px solid #CC0000; padding-bottom:10px;'>PLATEFORME FLUX</h3>", unsafe_allow_html=True)
    st.markdown("""
    <p style='color: #d1d1d1; font-size: 14px; line-height: 1.5;'>
    <b>Digitalisation Gemaplast</b><br>
    Gestion centralisée des approvisionnements :<br>
    • Saisie Magasinier<br>
    • Validation Production<br>
    • Audit Achat<br>
    • Approbation Direction
    </p>
    """, unsafe_allow_html=True)
    
    if st.session_state.authenticated:
        st.divider()
        st.write(f"👤 Connecté : **{st.session_state.user_role}**")
        if st.button("Se déconnecter"):
            st.session_state.authenticated = False
            st.rerun()

# --- LOGIQUE D'AFFICHAGE ---
if not st.session_state.authenticated:
    # Centrage de la carte de connexion
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<div class='login-card'>", unsafe_allow_html=True)
        st.markdown("<h2>Connexion Sécurisée</h2>", unsafe_allow_html=True)
        
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
    # Contenu après connexion (exemple Magasinier)
    st.title(f"Espace {st.session_state.user_role}")
    st.info("Sélectionnez une action dans le menu ou gérez les flux ci-dessous.")
    
    if st.session_state.user_role == "Magasinier":
        with st.expander("➕ Créer une nouvelle demande", expanded=True):
            prod = st.text_input("Nom du produit / Matière")
            qte = st.number_input("Quantité", min_value=1)
            if st.button("Envoyer la demande"):
                new_id = len(st.session_state.db) + 1
                new_entry = {"ID": new_id, "Produit": prod, "Qte": qte, "Statut": "Attente Production"}
                st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_entry])], ignore_index=True)
                st.success("Demande enregistrée !")

    # Affichage du tableau de bord pour le suivi
    st.divider()
    st.subheader("📊 État du Flux de Validation")
    st.dataframe(st.session_state.db, use_container_width=True)
