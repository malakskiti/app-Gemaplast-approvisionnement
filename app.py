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
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. INITIALISATION DE LA SESSION
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["ID", "Produit", "Quantité", "Unité", "Statut"])

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

    if st.session_state.user_role == "Magasinier":
        st.markdown("<h2 style='color: #CC0000;'>Espace Magasinier</h2>", unsafe_allow_html=True)
        
        with st.expander("➕ Créer une nouvelle demande", expanded=True):
            # Données issues de votre fichier
            articles = {
                "Huile moteur": "Litre",
                "Courroie": "Pièce",
                "PVC": "Plaque",
                "Acier": "Pièce",
                "Câble électrique": "Mètre",
                "Roulement": "Pièce"
            }
            
            liste_produits = ["--- Choisir un article ---"] + list(articles.keys())
            
            produit_choisi = st.selectbox("Sélectionnez l'article", options=liste_produits)
            
            # Affichage de l'unité si un produit est sélectionné
            unite = ""
            if produit_choisi != "--- Choisir un article ---":
                unite = articles[produit_choisi]
                st.write(f"Unité de mesure : **{unite}**")
            
            qte = st.number_input("Entrez la quantité", min_value=1, step=1)
            
            if st.button("Envoyer la demande"):
                if produit_choisi == "--- Choisir un article ---":
                    st.error("Veuillez sélectionner un article dans la liste.")
                else:
                    new_id = len(st.session_state.db) + 1
                    new_entry = {
                        "ID": new_id, 
                        "Produit": produit_choisi, 
                        "Quantité": qte, 
                        "Unité": unite,
                        "Statut": "Attente Production"
                    }
                    st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_entry])], ignore_index=True)
                    st.success(f"Demande de {qte} {unite}(s) pour {produit_choisi} enregistrée !")

    st.divider()
    st.subheader("📊 Suivi des demandes")
    st.dataframe(st.session_state.db, use_container_width=True)
