import streamlit as st
import pandas as pd
from datetime import datetime
import pandas as pd
import streamlit as st

# Créer un bouton de téléchargement dans la barre latérale ou le menu
file = st.file_uploader("Charger la liste des produits (Excel)", type=["xlsx"])

if file is not None:
    df_produits = pd.read_excel(file)
    # On récupère la colonne 'Designation' (ou le nom de ta colonne)
    LISTE_PRODUITS = df_produits["Designation"].tolist()
else:
    # Liste par défaut si aucun fichier n'est chargé
    LISTE_PRODUITS = ["Veuillez charger un fichier Excel"]
# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Gemaplast - Workflow", layout="wide")

# 2. STYLE CSS PERSONNALISÉ
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp { background-color: #F8F9FA; }
    
    /* Logo Gemaplast */
    .logo-text {
        color: #CC0000;
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        font-style: italic;
        font-size: 35px;
    }
    /* 1. Forcer le texte saisi par l'utilisateur en noir */
    .stTextArea textarea {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }

    /* 2. Forcer le titre 'Description / Notes particulières' en noir */
    .stTextArea label p {
        color: #000000 !important;
    }

    /* 3. Bonus : Forcer aussi le texte dans la case Quantité (car elle est sombre sur ton image) */
    .stNumberInput input {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }
    /* 1. Mettre le bouton d'upload en blanc/gris clair avec texte noir */
    .stFileUploader section {
        background-color: #FFFFFF !important;
        border: 1px solid #E0E0E0 !important;
        color: black !important;
    }
    /* Pour la zone de texte (Description) */
.stTextArea textarea {
    color: #000000 !important; /* Texte tapé en noir */
    background-color: #FFFFFF !important; /* Fond bien blanc */
}

/* Pour le label (le titre au-dessus de la case) */
.stTextArea label p {
    color: #000000 !important; /* Titre en noir */
    font-weight: bold;
}
    /* Changer la couleur du texte d'aide (200MB, XLSX) en noir */
    .stFileUploader [data-testid="stMarkdownContainer"] p {
        color: black !important;
    }

    /* 2. Mettre la liste déroulante (Selectbox) en blanc avec texte noir */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: black !important;
        border: 1px solid #E0E0E0 !important;
    }

    /* Forcer la couleur noire pour le texte à l'intérieur de la liste */
    div[data-testid="stSelectbox"] label, div[data-testid="stSelectbox"] p {
        color: black !important;
    }
    /* Titre en rouge */
    .titre-rouge {
        color: #CC0000;
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        font-size: 28px;
    }

  .kpi-card {
        background-color: #FFFFFF !important; /* Gris un peu foncé */
        color: black !important; /* Texte en blanc pour le contraste */
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
    /* Style spécifique pour l'en-tête de l'expander (formulaire) */
    .st-emotion-cache-p6495m { 
        background-color: #262730 !important; 
        color: white !important;
        border-radius: 8px;
    }
.stTextInput>div>div>input, .stNumberInput>div>div>input, .stTextArea>div>div>textarea {
    background-color:#FFFFFF !important; /* Gris moyen */
    color: white !important;
    border: 1px solid #666 !important;
}
    /* Bouton envoyer et autres boutons en gris foncé */
    .stButton>button {
        background-color: #FF0000 !important;
        color: white !important;
        border: none !important;
    }

    /* Barre latérale (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E0E0E0;
    }
    .sidebar-desc {
        color: #CC0000;
        font-weight: bold;
        font-size: 15px;
        text-align: center;
        margin-top: 10px;
    }

    /* Carte de demande */
    .demand-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E0E0E0;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. INITIALISATION DES DONNÉES
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame([
        {"ID": "D001", "Produit": "Huile moteur 5W-30 (20L)", "Quantité": 10, "Date": "28/04/2026", "Statut": "En attente Production", "Description": "Stock faible", "Priorité": "Haute"}
    ])
if 'show_form' not in st.session_state:
    st.session_state.show_form = False

# 4. BARRE LATÉRALE (SIDEBAR NETTOYÉE)
with st.sidebar:
    st.markdown('<p class="logo-text" style="text-align:center;">GEMAPLAST</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-desc">Entreprise de fabrication de conduites en PVC et polyéthylène</p>', unsafe_allow_html=True)
    # Suppression des boutons Paramètres et Tableau de bord ici

# 5. EN-TÊTE PRINCIPAL
col_logo, col_titre, col_btn = st.columns([1, 3, 1.2])

with col_logo:
    st.markdown('<p class="logo-text">GEMAPLAST</p>', unsafe_allow_html=True)

with col_titre:
    st.markdown('<p class="titre-rouge">Mes Demandes d\'Approvisionnement</p>', unsafe_allow_html=True)

with col_btn:
    # Bouton Nouvelle Demande (en rouge pour attirer l'attention)
    if st.button("+ Nouvelle Demande", use_container_width=True, type="secondary"):
        st.session_state.show_form = not st.session_state.show_form

# 6. FORMULAIRE DE SAISIE (Gris foncé appliqué via CSS)
if st.session_state.show_form:
    with st.expander("Nouvelle saisie", expanded=True):
       with st.form("add_form"):
            # 1. Sélection du produit depuis ton Excel
            prod = st.selectbox("Sélectionner le Produit", LISTE_PRODUITS)
            
            # 2. Champ Quantité : l'utilisateur peut taper ou cliquer sur + / -
            # value=1 est la valeur par défaut au chargement
            qte_saisie = st.number_input("Quantité à commander", min_value=1, value=1, step=1)
            
            # 3. Description et Priorité
            desc = st.text_area("Description / Notes particulières")
            prio = st.selectbox("Priorité", ["Haute", "Moyenne", "Basse"]) 
            
            # Bouton de validation
            envoi = st.form_submit_button("Envoyer la demande")

            if envoi:
                new_data = {
                    "ID": f"D00{len(st.session_state.db)+1}",
                    "Produit": prod,
                    "Quantité": qte_saisie, # On utilise ici la variable qte_saisie
                    "Date": datetime.now().strftime("%d/%m/%Y"),
                    "Statut": "En attente Production",
                    "Description": desc,
                    "Priorité": prio
                }
                # (Ici ton code pour ajouter new_data à ton st.session_state.db)
                st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([new_data])], ignore_index=True)
                st.success("Demande enregistrée avec succès !")
                st.rerun()

# 7. INDICATEURS (KPI) EN GRIS FONCÉ
st.write("")
k1, k2, k3, k4 = st.columns(4)
total = len(st.session_state.db)

k1.markdown(f'<div class="kpi-card"><div>Total Demandes</div><div style="font-size:24px; font-weight:bold;">{total}</div></div>', unsafe_allow_html=True)
k2.markdown('<div class="kpi-card"><div>En Attente</div><div style="font-size:24px; font-weight:bold;">1</div></div>', unsafe_allow_html=True)
k3.markdown('<div class="kpi-card"><div>Approuvées</div><div style="font-size:24px; font-weight:bold;">0</div></div>', unsafe_allow_html=True)
k4.markdown('<div class="kpi-card"><div>Refusées</div><div style="font-size:24px; font-weight:bold;">0</div></div>', unsafe_allow_html=True)

st.divider()

# --- AFFICHAGE DES COMMANDES ---
for index, row in st.session_state.db.iterrows():
    # On utilise st.container pour bien isoler chaque commande
    with st.container():
        # Cette commande HTML va créer la carte blanche propre
        st.markdown(f"""
            <div style="background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #E0E0E0; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between;">
                    <span style="background-color: #FFF9C4; color: #FBC02D; padding: 2px 10px; border-radius: 10px; font-weight: bold; font-size: 12px;">
                        {row['Statut']}
                    </span>
                    <span style="color: #CC0000; font-weight: bold;">● {row['Priorité']}</span>
                </div>
                <div style="color: black; font-size: 20px; font-weight: bold; margin-top: 10px;">
                    {row['Produit']}
                </div>
                <div style="color: black; font-size: 14px; margin-top: 5px;">
                    <b>ID:</b> {row['ID']} | <b>Date:</b> {row['Date']} | <b>Quantité:</b> {row['Quantité']}
                </div>
            </div>
        """, unsafe_allow_html=True)
