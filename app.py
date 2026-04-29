import streamlit as st
import pandas as pd

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Gemaplast - Workflow Achat", layout="wide")

# 2. DESIGN PERSONNALISÉ (Noir, Rouge, Blanc, Gris)
st.markdown("""
    <style>
    /* Fond de l'application */
    .stApp { background-color: #ffffff; }
    
    /* Barre latérale personnalisée */
    section[data-testid="stSidebar"] {
        background-color: #1a1a1a !important;
        color: white !important;
        min-width: 350px !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    .sidebar-desc {
        font-size: 14px;
        color: #d1d1d1;
        line-height: 1.6;
        padding: 10px;
        border-left: 3px solid #cc0000;
        margin-top: 20px;
    }

    /* Boutons rouges */
    .stButton>button { 
        width: 100%; 
        border-radius: 5px; 
        background-color: #cc0000; 
        color: white; 
        border: none;
        font-weight: bold;
        height: 45px;
    }
    .stButton>button:hover { background-color: #990000; border: none; }
    
    /* Carte de connexion */
    .login-card {
        background-color: #f8f9fa;
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        margin-top: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. INITIALISATION
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame(columns=["ID", "Produit", "Desc", "Qte", "Statut"])

# --- BARRE LATÉRALE (Toujours visible) ---
with st.sidebar:
    # Insertion du Logo (Utilisation de l'image Gemaplast)
    st.image("https://i.ibb.co/L6V8XkP/gemaplast-logo.jpg", use_container_width=True) 
    
    st.markdown("### À propos de l'App")
    st.markdown("""
    <div class='sidebar-desc'>
    <b>Digitalisation des Flux Gemaplast</b><br><br>
    Cette plateforme centralise les demandes d'approvisionnement, de la saisie terrain par le magasinier jusqu'à l'approbation finale de la Direction Générale.
    <br><br>
    Optimisé pour la fabrication et commercialisation de tuyaux en plastique.
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.authenticated:
        st.write(f"🟢 Connecté : **{st.session_state.user_role}**")
        if st.button("Déconnexion"):
            st.session_state.authenticated = False
            st.rerun()

# --- LOGIQUE D'AFFICHAGE ---

if not st.session_state.authenticated:
    # Zone de connexion au centre
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='login-card'>", unsafe_allow_html=True)
        st.header("Connexion Sécurisée")
        email = st.text_input("Email Professionnel")
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
    # Contenu après login
    st.title(f"Interface {st.session_state.user_role}")
    
    if st.session_state.user_role == "Magasinier":
        st.subheader("📦 Nouveau besoin")
        with st.expander("Ouvrir le formulaire de saisie", expanded=True):
            nom = st.text_input("Produit")
            qte = st.number_input("Quantité", min_value=1)
            desc = st.text_area("Notes techniques")
            if st.button("Soumettre"):
                new_entry = {"ID": len(st.session_state.db)+1, "Produit": nom, "Desc": desc, "Qte": qte, "Statut": "Attente Production"}
                st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_entry])], ignore_index=True)
                st.success("Demande envoyée !")

    # Affichage du tableau pour tous les connectés
    st.divider()
    st.markdown("### 📊 État du Flux de Validation")
    st.table(st.session_state.db)
