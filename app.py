import streamlit as st
import pandas as pd
import json
import urllib.request
from datetime import datetime

st.set_page_config(
    page_title="Département Génie Civil - Répartition des Charges",
    page_icon="🏗️",
    layout="wide"
)

# Style CSS institutionnel
st.markdown("""
<style>
    .main-title { font-size: 26px; font-weight: 800; color: #1e3a8a; margin-bottom: 2px; }
    .sub-title { font-size: 14px; color: #64748b; margin-bottom: 18px; }
    .nudge-card { 
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border-left: 5px solid #2563eb;
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    .badge-closed { background-color: #fee2e2; color: #991b1b; padding: 2px 8px; border-radius: 6px; font-size: 11px; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 1. BASE DE DONNÉES COMPLÈTE DU DÉPARTEMENT (12 PARCOURS)
# -------------------------------------------------------------
@st.cache_data
def get_master_modules():
    return pd.DataFrame([
        # =========================================================
        # 1ÈRE ANNÉE INGÉNIEUR - S1 (ST) - (2 Groupes)
        # =========================================================
        {"ID": "ING1-S1-C01", "Code": "IST 1.1", "Parcours": "1ère Ingénieur", "Matière": "Analyse 1", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING1-S1-C02", "Code": "IST 1.2", "Parcours": "1ère Ingénieur", "Matière": "Algèbre 1", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING1-S1-C03", "Code": "IST 1.3", "Parcours": "1ère Ingénieur", "Matière": "Probabilités et Statistiques", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING1-S1-C04", "Code": "IST 1.4", "Parcours": "1ère Ingénieur", "Matière": "Structure de la Matière (Chimie)", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING1-S1-C05", "Code": "IST 1.5", "Parcours": "1ère Ingénieur", "Matière": "Éléments de Mécanique (Physique 1)", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING1-S1-TD01", "Code": "IST 1.1", "Parcours": "1ère Ingénieur", "Matière": "Analyse 1", "Type": "TD", "Groupe": "Groupe 1", "Volume_Hebdo": 3.0, "Is_New": False},
        {"ID": "ING1-S1-TD02", "Code": "IST 1.1", "Parcours": "1ère Ingénieur", "Matière": "Analyse 1", "Type": "TD", "Groupe": "Groupe 2", "Volume_Hebdo": 3.0, "Is_New": False},
        {"ID": "ING1-S1-TD03", "Code": "IST 1.2", "Parcours": "1ère Ingénieur", "Matière": "Algèbre 1", "Type": "TD", "Groupe": "Groupe 1", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING1-S1-TD04", "Code": "IST 1.2", "Parcours": "1ère Ingénieur", "Matière": "Algèbre 1", "Type": "TD", "Groupe": "Groupe 2", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING1-S1-TD05", "Code": "IST 1.3", "Parcours": "1ère Ingénieur", "Matière": "Probabilités et Statistiques", "Type": "TD", "Groupe": "Groupe 1", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING1-S1-TD06", "Code": "IST 1.3", "Parcours": "1ère Ingénieur", "Matière": "Probabilités et Statistiques", "Type": "TD", "Groupe": "Groupe 2", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING1-S1-TD07", "Code": "IST 1.4", "Parcours": "1ère Ingénieur", "Matière": "Structure de la Matière (Chimie)", "Type": "TD", "Groupe": "Groupe 1", "Volume_Hebdo": 3.0, "Is_New": False},
        {"ID": "ING1-S1-TD08", "Code": "IST 1.4", "Parcours": "1ère Ingénieur", "Matière": "Structure de la Matière (Chimie)", "Type": "TD", "Groupe": "Groupe 2", "Volume_Hebdo": 3.0, "Is_New": False},
        {"ID": "ING1-S1-TD09", "Code": "IST 1.5", "Parcours": "1ère Ingénieur", "Matière": "Éléments de Mécanique (Physique 1)", "Type": "TD", "Groupe": "Groupe 1", "Volume_Hebdo": 3.0, "Is_New": False},
        {"ID": "ING1-S1-TD10", "Code": "IST 1.5", "Parcours": "1ère Ingénieur", "Matière": "Éléments de Mécanique (Physique 1)", "Type": "TD", "Groupe": "Groupe 2", "Volume_Hebdo": 3.0, "Is_New": False},
        {"ID": "ING1-S1-TP01", "Code": "IST 1.4", "Parcours": "1ère Ingénieur", "Matière": "Structure de la Matière (TP)", "Type": "TP", "Groupe": "Groupe 1", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING1-S1-TP02", "Code": "IST 1.4", "Parcours": "1ère Ingénieur", "Matière": "Structure de la Matière (TP)", "Type": "TP", "Groupe": "Groupe 2", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING1-S1-TP03", "Code": "IST 1.5", "Parcours": "1ère Ingénieur", "Matière": "Éléments de Mécanique (TP)", "Type": "TP", "Groupe": "Groupe 1", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING1-S1-TP04", "Code": "IST 1.5", "Parcours": "1ère Ingénieur", "Matière": "Éléments de Mécanique (TP)", "Type": "TP", "Groupe": "Groupe 2", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING1-S1-TP05", "Code": "IST 1.6", "Parcours": "1ère Ingénieur", "Matière": "Structure des Ordinateurs et Applications", "Type": "TP", "Groupe": "Groupe 1", "Volume_Hebdo": 3.0, "Is_New": False},
        {"ID": "ING1-S1-TP06", "Code": "IST 1.6", "Parcours": "1ère Ingénieur", "Matière": "Structure des Ordinateurs et Applications", "Type": "TP", "Groupe": "Groupe 2", "Volume_Hebdo": 3.0, "Is_New": False},
        {"ID": "ING1-S1-NEW01", "Code": "IST 1.8", "Parcours": "1ère Ingénieur", "Matière": "Dimension Éthique et Déontologique", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": True},
        {"ID": "ING1-S1-NEW02", "Code": "IST 1.9", "Parcours": "1ère Ingénieur", "Matière": "Histoire de l'Algérie", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": True},

        # =========================================================
        # 2ÈME ANNÉE INGÉNIEUR - S1 (IGC 3) - (1 Seul Groupe)
        # =========================================================
        {"ID": "ING2-S1-C01", "Code": "IGC3.1", "Parcours": "2ème Ingénieur", "Matière": "Mathématiques appliquées", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING2-S1-TD01", "Code": "IGC3.1", "Parcours": "2ème Ingénieur", "Matière": "Mathématiques appliquées", "Type": "TD", "Groupe": "Groupe Unique", "Volume_Hebdo": 3.0, "Is_New": False},
        {"ID": "ING2-S1-C02", "Code": "IGC3.2", "Parcours": "2ème Ingénieur", "Matière": "Ondes et vibrations", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING2-S1-TD02", "Code": "IGC3.2", "Parcours": "2ème Ingénieur", "Matière": "Ondes et vibrations", "Type": "TD", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING2-S1-TP01", "Code": "IGC3.2", "Parcours": "2ème Ingénieur", "Matière": "Ondes et vibrations", "Type": "TP", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING2-S1-C03", "Code": "IGC3.3", "Parcours": "2ème Ingénieur", "Matière": "Résistance des matériaux 1 (RDM 1)", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING2-S1-TD03", "Code": "IGC3.3", "Parcours": "2ème Ingénieur", "Matière": "Résistance des matériaux 1 (RDM 1)", "Type": "TD", "Groupe": "Groupe Unique", "Volume_Hebdo": 3.0, "Is_New": False},
        {"ID": "ING2-S1-C04", "Code": "IGC3.4", "Parcours": "2ème Ingénieur", "Matière": "Matériaux de construction 1 (MDC 1)", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING2-S1-TP02", "Code": "IGC3.4", "Parcours": "2ème Ingénieur", "Matière": "Matériaux de construction 1 (MDC 1)", "Type": "TP", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING2-S1-C05", "Code": "IGC3.5", "Parcours": "2ème Ingénieur", "Matière": "Mécanique des fluides (MDF)", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING2-S1-TD04", "Code": "IGC3.5", "Parcours": "2ème Ingénieur", "Matière": "Mécanique des fluides (MDF)", "Type": "TD", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING2-S1-TP03", "Code": "IGC3.5", "Parcours": "2ème Ingénieur", "Matière": "Mécanique des fluides (MDF)", "Type": "TP", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING2-S1-C06", "Code": "IGC3.6", "Parcours": "2ème Ingénieur", "Matière": "Informatique 3", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING2-S1-TP04", "Code": "IGC3.6", "Parcours": "2ème Ingénieur", "Matière": "Informatique 3", "Type": "TP", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING2-S1-C07", "Code": "IGC3.7", "Parcours": "2ème Ingénieur", "Matière": "Procédés généraux de construction (PGC)", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING2-S1-C08", "Code": "IGC3.8", "Parcours": "2ème Ingénieur", "Matière": "Géologie", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING2-S1-TD05", "Code": "IGC3.9", "Parcours": "2ème Ingénieur", "Matière": "Anglais technique", "Type": "TD", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},

        # =========================================================
        # 3ÈME ANNÉE INGÉNIEUR - S1 (SEG 5) - (1 Seul Groupe)
        # =========================================================
        {"ID": "ING3-S1-C01", "Code": "SEG 5.1", "Parcours": "3ème Ingénieur", "Matière": "Calcul Béton Armé 2", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING3-S1-TD01", "Code": "SEG 5.1", "Parcours": "3ème Ingénieur", "Matière": "Calcul Béton Armé 2", "Type": "TD", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING3-S1-C02", "Code": "SEG 5.2", "Parcours": "3ème Ingénieur", "Matière": "Mécanique des sols 2", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING3-S1-TD02", "Code": "SEG 5.2", "Parcours": "3ème Ingénieur", "Matière": "Mécanique des sols 2", "Type": "TD", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING3-S1-TP01", "Code": "SEG 5.2", "Parcours": "3ème Ingénieur", "Matière": "Mécanique des sols 2", "Type": "TP", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING3-S1-C03", "Code": "SEG 5.3", "Parcours": "3ème Ingénieur", "Matière": "Matériaux de Construction 2", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING3-S1-TP02", "Code": "SEG 5.3", "Parcours": "3ème Ingénieur", "Matière": "Matériaux de Construction 2", "Type": "TP", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING3-S1-C04", "Code": "SEG 5.4", "Parcours": "3ème Ingénieur", "Matière": "Résistance des Matériaux 3 (RDM 3)", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING3-S1-TD03", "Code": "SEG 5.4", "Parcours": "3ème Ingénieur", "Matière": "Résistance des Matériaux 3 (RDM 3)", "Type": "TD", "Groupe": "Groupe Unique", "Volume_Hebdo": 3.0, "Is_New": False},
        {"ID": "ING3-S1-C05", "Code": "SEG 5.5", "Parcours": "3ème Ingénieur", "Matière": "Charpente Métallique 2", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING3-S1-TD04", "Code": "SEG 5.5", "Parcours": "3ème Ingénieur", "Matière": "Charpente Métallique 2", "Type": "TD", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING3-S1-C06", "Code": "SEG 5.6", "Parcours": "3ème Ingénieur", "Matière": "Topographie 2", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING3-S1-TP03", "Code": "SEG 5.6", "Parcours": "3ème Ingénieur", "Matière": "Topographie 2", "Type": "TP", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING3-S1-TP04", "Code": "SEG 5.7", "Parcours": "3ème Ingénieur", "Matière": "Dessin du BTP", "Type": "TP", "Groupe": "Groupe Unique", "Volume_Hebdo": 3.0, "Is_New": False},
        {"ID": "ING3-S1-C07", "Code": "SEG 5.8", "Parcours": "3ème Ingénieur", "Matière": "Dessin Assisté par Ordinateur 2 (DAO 2)", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING3-S1-TP05", "Code": "SEG 5.8", "Parcours": "3ème Ingénieur", "Matière": "Dessin Assisté par Ordinateur 2 (DAO 2)", "Type": "TP", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "ING3-S1-TD05", "Code": "SEG 5.9", "Parcours": "3ème Ingénieur", "Matière": "Anglais technique de spécialité", "Type": "TD", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},

        # =========================================================
        # 4ÈME ANNÉE INGÉNIEUR - S1 (SEG 7) - NOUVELLE FORMATION
        # =========================================================
        {"ID": "ING4-S1-C01", "Code": "SEG 7.1", "Parcours": "4ème Ingénieur", "Matière": "Résistance des Matériaux 4 (RDM 4)", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": True},
        {"ID": "ING4-S1-TD01", "Code": "SEG 7.1", "Parcours": "4ème Ingénieur", "Matière": "Résistance des Matériaux 4 (RDM 4)", "Type": "TD", "Groupe": "Groupe Unique", "Volume_Hebdo": 3.0, "Is_New": True},
        {"ID": "ING4-S1-C02", "Code": "SEG 7.2", "Parcours": "4ème Ingénieur", "Matière": "Charpente Métallique 4 (Assemblages)", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": True},
        {"ID": "ING4-S1-TD02", "Code": "SEG 7.2", "Parcours": "4ème Ingénieur", "Matière": "Charpente Métallique 4 (Assemblages)", "Type": "TD", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": True},
        {"ID": "ING4-S1-C03", "Code": "SEG 7.3", "Parcours": "4ème Ingénieur", "Matière": "Calcul Béton Armé 3", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": True},
        {"ID": "ING4-S1-TD03", "Code": "SEG 7.3", "Parcours": "4ème Ingénieur", "Matière": "Calcul Béton Armé 3", "Type": "TD", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": True},
        {"ID": "ING4-S1-C04", "Code": "SEG 7.4", "Parcours": "4ème Ingénieur", "Matière": "Soutènements et Talus", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": True},
        {"ID": "ING4-S1-TD04", "Code": "SEG 7.4", "Parcours": "4ème Ingénieur", "Matière": "Soutènements et Talus", "Type": "TD", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": True},
        {"ID": "ING4-S1-C05", "Code": "SEG 7.5", "Parcours": "4ème Ingénieur", "Matière": "Dynamique des structures 1", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": True},
        {"ID": "ING4-S1-TD05", "Code": "SEG 7.5", "Parcours": "4ème Ingénieur", "Matière": "Dynamique des structures 1", "Type": "TD", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": True},
        {"ID": "ING4-S1-C06", "Code": "SEG 7.6", "Parcours": "4ème Ingénieur", "Matière": "Diagnostique et réparation des structures", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": True},
        {"ID": "ING4-S1-TP01", "Code": "SEG 7.6", "Parcours": "4ème Ingénieur", "Matière": "Diagnostique et réparation des structures", "Type": "TP", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": True},
        {"ID": "ING4-S1-C07", "Code": "SEG 7.7", "Parcours": "4ème Ingénieur", "Matière": "Projet en charpente Métallique", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": True},
        {"ID": "ING4-S1-TP02", "Code": "SEG 7.7", "Parcours": "4ème Ingénieur", "Matière": "Projet en charpente Métallique", "Type": "TP", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": True},
        {"ID": "ING4-S1-C08", "Code": "SEG 7.8", "Parcours": "4ème Ingénieur", "Matière": "Planification et gestion de projet de construction", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": True},
        {"ID": "ING4-S1-TP03", "Code": "SEG 7.8", "Parcours": "4ème Ingénieur", "Matière": "Planification et gestion de projet de construction", "Type": "TP", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": True},
        {"ID": "ING4-S1-NEW01", "Code": "SEG 7.9", "Parcours": "4ème Ingénieur", "Matière": "Programmation avancée en Python", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": True},
        {"ID": "ING4-S1-NEW02", "Code": "SEG 7.9", "Parcours": "4ème Ingénieur", "Matière": "Programmation avancée en Python", "Type": "TP", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": True},
        {"ID": "ING4-S1-NEW03", "Code": "SEG 7.10", "Parcours": "4ème Ingénieur", "Matière": "Respect des normes et des règles d'éthique et d'intégrité", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": True},

        # =========================================================
        # LICENCE 2ÈME ANNÉE - S1 (S3) - (3 Groupes)
        # =========================================================
        {"ID": "L2-S1-C01", "Code": "UEF 2.1.1", "Parcours": "L2 Génie Civil", "Matière": "Analyse 3", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L2-S1-TD01", "Code": "UEF 2.1.1", "Parcours": "L2 Génie Civil", "Matière": "Analyse 3", "Type": "TD", "Groupe": "Groupe 1", "Volume_Hebdo": 3.0, "Is_New": False},
        {"ID": "L2-S1-TD02", "Code": "UEF 2.1.1", "Parcours": "L2 Génie Civil", "Matière": "Analyse 3", "Type": "TD", "Groupe": "Groupe 2", "Volume_Hebdo": 3.0, "Is_New": False},
        {"ID": "L2-S1-TD03", "Code": "UEF 2.1.1", "Parcours": "L2 Génie Civil", "Matière": "Analyse 3", "Type": "TD", "Groupe": "Groupe 3", "Volume_Hebdo": 3.0, "Is_New": False},
        {"ID": "L2-S1-C02", "Code": "UEF 2.1.1", "Parcours": "L2 Génie Civil", "Matière": "Ondes et vibrations", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L2-S1-TD04", "Code": "UEF 2.1.1", "Parcours": "L2 Génie Civil", "Matière": "Ondes et vibrations", "Type": "TD", "Groupe": "Groupe 1", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L2-S1-TD05", "Code": "UEF 2.1.1", "Parcours": "L2 Génie Civil", "Matière": "Ondes et vibrations", "Type": "TD", "Groupe": "Groupe 2", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L2-S1-TD06", "Code": "UEF 2.1.1", "Parcours": "L2 Génie Civil", "Matière": "Ondes et vibrations", "Type": "TD", "Groupe": "Groupe 3", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L2-S1-C03", "Code": "UEF 2.1.2", "Parcours": "L2 Génie Civil", "Matière": "Mécanique des fluides", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L2-S1-TD07", "Code": "UEF 2.1.2", "Parcours": "L2 Génie Civil", "Matière": "Mécanique des fluides", "Type": "TD", "Groupe": "Groupe 1", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L2-S1-TD08", "Code": "UEF 2.1.2", "Parcours": "L2 Génie Civil", "Matière": "Mécanique des fluides", "Type": "TD", "Groupe": "Groupe 2", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L2-S1-TD09", "Code": "UEF 2.1.2", "Parcours": "L2 Génie Civil", "Matière": "Mécanique des fluides", "Type": "TD", "Groupe": "Groupe 3", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L2-S1-TP01", "Code": "UEF 2.1.2", "Parcours": "L2 Génie Civil", "Matière": "Mécanique des fluides (TP)", "Type": "TP", "Groupe": "Groupe 1", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L2-S1-TP02", "Code": "UEF 2.1.2", "Parcours": "L2 Génie Civil", "Matière": "Mécanique des fluides (TP)", "Type": "TP", "Groupe": "Groupe 2", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L2-S1-TP03", "Code": "UEF 2.1.2", "Parcours": "L2 Génie Civil", "Matière": "Mécanique des fluides (TP)", "Type": "TP", "Groupe": "Groupe 3", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L2-S1-C04", "Code": "UEF 2.1.2", "Parcours": "L2 Génie Civil", "Matière": "Mécanique rationnelle", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L2-S1-TD10", "Code": "UEF 2.1.2", "Parcours": "L2 Génie Civil", "Matière": "Mécanique rationnelle", "Type": "TD", "Groupe": "Groupe 1", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L2-S1-TD11", "Code": "UEF 2.1.2", "Parcours": "L2 Génie Civil", "Matière": "Mécanique rationnelle", "Type": "TD", "Groupe": "Groupe 2", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L2-S1-TD12", "Code": "UEF 2.1.2", "Parcours": "L2 Génie Civil", "Matière": "Mécanique rationnelle", "Type": "TD", "Groupe": "Groupe 3", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L2-S1-C05", "Code": "UEM 2.1", "Parcours": "L2 Génie Civil", "Matière": "Probabilités et statistiques", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L2-S1-TD13", "Code": "UEM 2.1", "Parcours": "L2 Génie Civil", "Matière": "Probabilités et statistiques", "Type": "TD", "Groupe": "Groupe 1", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L2-S1-TD14", "Code": "UEM 2.1", "Parcours": "L2 Génie Civil", "Matière": "Probabilités et statistiques", "Type": "TD", "Groupe": "Groupe 2", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L2-S1-TD15", "Code": "UEM 2.1", "Parcours": "L2 Génie Civil", "Matière": "Probabilités et statistiques", "Type": "TD", "Groupe": "Groupe 3", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L2-S1-C06", "Code": "UEM 2.1", "Parcours": "L2 Génie Civil", "Matière": "Programmation Python", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L2-S1-TP04", "Code": "UEM 2.1", "Parcours": "L2 Génie Civil", "Matière": "Programmation Python (TP)", "Type": "TP", "Groupe": "Groupe 1", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L2-S1-TP05", "Code": "UEM 2.1", "Parcours": "L2 Génie Civil", "Matière": "Programmation Python (TP)", "Type": "TP", "Groupe": "Groupe 2", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L2-S1-TP06", "Code": "UEM 2.1", "Parcours": "L2 Génie Civil", "Matière": "Programmation Python (TP)", "Type": "TP", "Groupe": "Groupe 3", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L2-S1-TP07", "Code": "UEM 2.1", "Parcours": "L2 Génie Civil", "Matière": "Dessin technique", "Type": "TP", "Groupe": "Groupe 1", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L2-S1-TP08", "Code": "UEM 2.1", "Parcours": "L2 Génie Civil", "Matière": "Dessin technique", "Type": "TP", "Groupe": "Groupe 2", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L2-S1-TP09", "Code": "UEM 2.1", "Parcours": "L2 Génie Civil", "Matière": "Dessin technique", "Type": "TP", "Groupe": "Groupe 3", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L2-S1-TP10", "Code": "UEM 2.1", "Parcours": "L2 Génie Civil", "Matière": "TP Ondes et vibrations", "Type": "TP", "Groupe": "Groupe 1", "Volume_Hebdo": 1.0, "Is_New": False},
        {"ID": "L2-S1-TP11", "Code": "UEM 2.1", "Parcours": "L2 Génie Civil", "Matière": "TP Ondes et vibrations", "Type": "TP", "Groupe": "Groupe 2", "Volume_Hebdo": 1.0, "Is_New": False},
        {"ID": "L2-S1-TP12", "Code": "UEM 2.1", "Parcours": "L2 Génie Civil", "Matière": "TP Ondes et vibrations", "Type": "TP", "Groupe": "Groupe 3", "Volume_Hebdo": 1.0, "Is_New": False},
        {"ID": "L2-S1-C07", "Code": "UED 2.1", "Parcours": "L2 Génie Civil", "Matière": "Métrologie", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},

        # =========================================================
        # LICENCE 3ÈME ANNÉE - S1 (S5) - (2 Groupes)
        # =========================================================
        {"ID": "L3-S1-C01", "Code": "UEF 3.1.1", "Parcours": "L3 Génie Civil", "Matière": "Résistance des Matériaux 2 (RDM 2)", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L3-S1-TD01", "Code": "UEF 3.1.1", "Parcours": "L3 Génie Civil", "Matière": "Résistance des Matériaux 2 (RDM 2)", "Type": "TD", "Groupe": "Groupe 1", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L3-S1-TD02", "Code": "UEF 3.1.1", "Parcours": "L3 Génie Civil", "Matière": "Résistance des Matériaux 2 (RDM 2)", "Type": "TD", "Groupe": "Groupe 2", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L3-S1-C02", "Code": "UEF 3.1.1", "Parcours": "L3 Génie Civil", "Matière": "Béton Armé 1 (BA 1)", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L3-S1-TD03", "Code": "UEF 3.1.1", "Parcours": "L3 Génie Civil", "Matière": "Béton Armé 1 (BA 1)", "Type": "TD", "Groupe": "Groupe 1", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L3-S1-TD04", "Code": "UEF 3.1.1", "Parcours": "L3 Génie Civil", "Matière": "Béton Armé 1 (BA 1)", "Type": "TD", "Groupe": "Groupe 2", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L3-S1-C03", "Code": "UEF 3.1.1", "Parcours": "L3 Génie Civil", "Matière": "Charpente Métallique (CM)", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L3-S1-TD05", "Code": "UEF 3.1.1", "Parcours": "L3 Génie Civil", "Matière": "Charpente Métallique (CM)", "Type": "TD", "Groupe": "Groupe 1", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L3-S1-TD06", "Code": "UEF 3.1.1", "Parcours": "L3 Génie Civil", "Matière": "Charpente Métallique (CM)", "Type": "TD", "Groupe": "Groupe 2", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L3-S1-C04", "Code": "UEF 3.1.2", "Parcours": "L3 Génie Civil", "Matière": "Mécanique des Sols 2 (MDS 2)", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L3-S1-TD07", "Code": "UEF 3.1.2", "Parcours": "L3 Génie Civil", "Matière": "Mécanique des Sols 2 (MDS 2)", "Type": "TD", "Groupe": "Groupe 1", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L3-S1-TD08", "Code": "UEF 3.1.2", "Parcours": "L3 Génie Civil", "Matière": "Mécanique des Sols 2 (MDS 2)", "Type": "TD", "Groupe": "Groupe 2", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L3-S1-C05", "Code": "UEF 3.1.2", "Parcours": "L3 Génie Civil", "Matière": "Matériaux de Construction 2 (MDC 2)", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L3-S1-C06", "Code": "UEM 3.1", "Parcours": "L3 Génie Civil", "Matière": "Topographie", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L3-S1-TP01", "Code": "UEM 3.1", "Parcours": "L3 Génie Civil", "Matière": "Topographie (TP)", "Type": "TP", "Groupe": "Groupe 1", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L3-S1-TP02", "Code": "UEM 3.1", "Parcours": "L3 Génie Civil", "Matière": "Topographie (TP)", "Type": "TP", "Groupe": "Groupe 2", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L3-S1-TP03", "Code": "UEM 3.1", "Parcours": "L3 Génie Civil", "Matière": "TP Mécanique des sols 2", "Type": "TP", "Groupe": "Groupe 1", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L3-S1-TP04", "Code": "UEM 3.1", "Parcours": "L3 Génie Civil", "Matière": "TP Mécanique des sols 2", "Type": "TP", "Groupe": "Groupe 2", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L3-S1-TP05", "Code": "UEM 3.1", "Parcours": "L3 Génie Civil", "Matière": "TP Matériaux de Construction 2", "Type": "TP", "Groupe": "Groupe 1", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L3-S1-TP06", "Code": "UEM 3.1", "Parcours": "L3 Génie Civil", "Matière": "TP Matériaux de Construction 2", "Type": "TP", "Groupe": "Groupe 2", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L3-S1-TP07", "Code": "UEM 3.1", "Parcours": "L3 Génie Civil", "Matière": "Dessin du BTP", "Type": "TP", "Groupe": "Groupe 1", "Volume_Hebdo": 2.5, "Is_New": False},
        {"ID": "L3-S1-TP08", "Code": "UEM 3.1", "Parcours": "L3 Génie Civil", "Matière": "Dessin du BTP", "Type": "TP", "Groupe": "Groupe 2", "Volume_Hebdo": 2.5, "Is_New": False},
        {"ID": "L3-S1-C07", "Code": "UED 3.1", "Parcours": "L3 Génie Civil", "Matière": "Hydraulique générale", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "L3-S1-C08", "Code": "UET 3.1", "Parcours": "L3 Génie Civil", "Matière": "Techniques et règles de construction", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},

        # =========================================================
        # MASTER 1 VOA - S1 (1 Seul Groupe)
        # =========================================================
        {"ID": "M1-VOA-C01", "Code": "UEF 1.1.1", "Parcours": "Master 1 VOA", "Matière": "Théorie de l'Élasticité", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M1-VOA-TD01", "Code": "UEF 1.1.1", "Parcours": "Master 1 VOA", "Matière": "Théorie de l'Élasticité", "Type": "TD", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M1-VOA-C02", "Code": "UEF 1.1.1", "Parcours": "Master 1 VOA", "Matière": "Dynamique des structures", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M1-VOA-TD02", "Code": "UEF 1.1.1", "Parcours": "Master 1 VOA", "Matière": "Dynamique des structures", "Type": "TD", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M1-VOA-C03", "Code": "UEF 1.1.2", "Parcours": "Master 1 VOA", "Matière": "Dimensionnement des Ponts", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 3.0, "Is_New": False},
        {"ID": "M1-VOA-TD03", "Code": "UEF 1.1.2", "Parcours": "Master 1 VOA", "Matière": "Dimensionnement des Ponts", "Type": "TD", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M1-VOA-C04", "Code": "UEF 1.1.2", "Parcours": "Master 1 VOA", "Matière": "Dimensionnement des Routes", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M1-VOA-TD04", "Code": "UEF 1.1.2", "Parcours": "Master 1 VOA", "Matière": "Dimensionnement des Routes", "Type": "TD", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M1-VOA-C05", "Code": "UEM 1.1", "Parcours": "Master 1 VOA", "Matière": "Projet Ouvrages en Béton Armé", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M1-VOA-TD05", "Code": "UEM 1.1", "Parcours": "Master 1 VOA", "Matière": "Projet Ouvrages en Béton Armé", "Type": "TD", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M1-VOA-TP01", "Code": "UEM 1.1", "Parcours": "Master 1 VOA", "Matière": "Projet Ouvrages en Béton Armé", "Type": "TP", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M1-VOA-C06", "Code": "UEM 1.1", "Parcours": "Master 1 VOA", "Matière": "Programmation Avancée Python", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M1-VOA-TP02", "Code": "UEM 1.1", "Parcours": "Master 1 VOA", "Matière": "Programmation Avancée Python (TP)", "Type": "TP", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M1-VOA-TP03", "Code": "UEM 1.1", "Parcours": "Master 1 VOA", "Matière": "TP Logiciels Appliqués aux Routes", "Type": "TP", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M1-VOA-C07", "Code": "UET 1.1", "Parcours": "Master 1 VOA", "Matière": "Code des marchés publics", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M1-VOA-NEW01", "Code": "UET 1.1", "Parcours": "Master 1 VOA", "Matière": "Respect des normes et des règles d'éthique et d'intégrité", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": True},

        # =========================================================
        # MASTER 2 VOA - S1 (1 Seul Groupe)
        # =========================================================
        {"ID": "M2-VOA-C01", "Code": "UEF 2.1.1", "Parcours": "Master 2 VOA", "Matière": "Conceptions avancées de ponts", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M2-VOA-TD01", "Code": "UEF 2.1.1", "Parcours": "Master 2 VOA", "Matière": "Conceptions avancées de ponts", "Type": "TD", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M2-VOA-C02", "Code": "UEF 2.1.1", "Parcours": "Master 2 VOA", "Matière": "Ouvrages souterrains", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M2-VOA-TD02", "Code": "UEF 2.1.1", "Parcours": "Master 2 VOA", "Matière": "Ouvrages souterrains", "Type": "TD", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M2-VOA-C03", "Code": "UEF 2.1.2", "Parcours": "Master 2 VOA", "Matière": "Chemins de fer", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M2-VOA-TD03", "Code": "UEF 2.1.2", "Parcours": "Master 2 VOA", "Matière": "Chemins de fer", "Type": "TD", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M2-VOA-C04", "Code": "UEF 2.1.2", "Parcours": "Master 2 VOA", "Matière": "Aérodromes", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M2-VOA-TD04", "Code": "UEF 2.1.2", "Parcours": "Master 2 VOA", "Matière": "Aérodromes", "Type": "TD", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M2-VOA-C05", "Code": "UEF 2.1.2", "Parcours": "Master 2 VOA", "Matière": "Pathologie et réhabilitation des OA", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M2-VOA-C06", "Code": "UEM 2.1", "Parcours": "Master 2 VOA", "Matière": "Géotechnique avancée", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M2-VOA-TP01", "Code": "UEM 2.1", "Parcours": "Master 2 VOA", "Matière": "Géotechnique avancée (TP)", "Type": "TP", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M2-VOA-TP02", "Code": "UEM 2.1", "Parcours": "Master 2 VOA", "Matière": "Modélisation numérique des Ponts", "Type": "TP", "Groupe": "Groupe Unique", "Volume_Hebdo": 2.5, "Is_New": False},
        {"ID": "M2-VOA-TP03", "Code": "UEM 2.1", "Parcours": "Master 2 VOA", "Matière": "Organisation et visites de chantiers", "Type": "TP", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M2-VOA-C07", "Code": "UET 2.1", "Parcours": "Master 2 VOA", "Matière": "Recherche documentaire et conception de mémoire", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M2-VOA-NEW01", "Code": "UET 2.1", "Parcours": "Master 2 VOA", "Matière": "Reverse Engineering", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": True},
        {"ID": "M2-VOA-NEW02", "Code": "UET 2.1", "Parcours": "Master 2 VOA", "Matière": "Reverse Engineering", "Type": "Atelier", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": True},

        # =========================================================
        # MASTER 1 STRUCTURES - S1 (1 Seul Groupe)
        # =========================================================
        {"ID": "M1-STR-C01", "Code": "UEF 1.1.1", "Parcours": "Master 1 Structures", "Matière": "Mécanique des structures", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M1-STR-TD01", "Code": "UEF 1.1.1", "Parcours": "Master 1 Structures", "Matière": "Mécanique des structures", "Type": "TD", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M1-STR-C02", "Code": "UEF 1.1.1", "Parcours": "Master 1 Structures", "Matière": "Dynamique des structures 1", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M1-STR-TD02", "Code": "UEF 1.1.1", "Parcours": "Master 1 Structures", "Matière": "Dynamique des structures 1", "Type": "TD", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M1-STR-C03", "Code": "UEF 1.1.2", "Parcours": "Master 1 Structures", "Matière": "Structures en béton armé 1", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M1-STR-TD03", "Code": "UEF 1.1.2", "Parcours": "Master 1 Structures", "Matière": "Structures en béton armé 1", "Type": "TD", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M1-STR-C04", "Code": "UEF 1.1.2", "Parcours": "Master 1 Structures", "Matière": "Structures métalliques", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 3.0, "Is_New": False},
        {"ID": "M1-STR-TD04", "Code": "UEF 1.1.2", "Parcours": "Master 1 Structures", "Matière": "Structures métalliques", "Type": "TD", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M1-STR-C05", "Code": "UEM 1.1", "Parcours": "Master 1 Structures", "Matière": "Programmation Avancée Python", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M1-STR-TP01", "Code": "UEM 1.1", "Parcours": "Master 1 Structures", "Matière": "Programmation Avancée Python (TP)", "Type": "TP", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M1-STR-TP02", "Code": "UEM 1.1", "Parcours": "Master 1 Structures", "Matière": "Méthodes expérimentales", "Type": "TP", "Groupe": "Groupe Unique", "Volume_Hebdo": 3.0, "Is_New": False},
        {"ID": "M1-STR-C06", "Code": "UEM 1.1", "Parcours": "Master 1 Structures", "Matière": "Matériaux innovants et durabilité", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M1-STR-TP03", "Code": "UEM 1.1", "Parcours": "Master 1 Structures", "Matière": "Matériaux innovants et durabilité (TP)", "Type": "TP", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M1-STR-C07", "Code": "UEM 1.1", "Parcours": "Master 1 Structures", "Matière": "Gestion de l'Incertitude et Risques en Ingénierie", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M1-STR-C08", "Code": "UED 1.1", "Parcours": "Master 1 Structures", "Matière": "Code des marchés publics", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M1-STR-NEW01", "Code": "UED 1.1", "Parcours": "Master 1 Structures", "Matière": "Respect des normes et des règles d'éthique et d'intégrité", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": True},

        # =========================================================
        # MASTER 2 STRUCTURES - S1 (1 Seul Groupe)
        # =========================================================
        {"ID": "M2-STR-C01", "Code": "UEF 2.1.1", "Parcours": "Master 2 Structures", "Matière": "Béton précontraint", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 3.0, "Is_New": False},
        {"ID": "M2-STR-TD01", "Code": "UEF 2.1.1", "Parcours": "Master 2 Structures", "Matière": "Béton précontraint", "Type": "TD", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M2-STR-C02", "Code": "UEF 2.1.1", "Parcours": "Master 2 Structures", "Matière": "Plasticité et endommagement", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M2-STR-TD02", "Code": "UEF 2.1.1", "Parcours": "Master 2 Structures", "Matière": "Plasticité et endommagement", "Type": "TD", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M2-STR-C03", "Code": "UEF 2.1.2", "Parcours": "Master 2 Structures", "Matière": "Génie parasismique", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M2-STR-TD03", "Code": "UEF 2.1.2", "Parcours": "Master 2 Structures", "Matière": "Génie parasismique", "Type": "TD", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M2-STR-C04", "Code": "UEF 2.1.2", "Parcours": "Master 2 Structures", "Matière": "Ovrages spéciaux", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M2-STR-TD04", "Code": "UEF 2.1.2", "Parcours": "Master 2 Structures", "Matière": "Ovrages spéciaux", "Type": "TD", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M2-STR-C05", "Code": "UEM 2.1", "Parcours": "Master 2 Structures", "Matière": "Projet structures en béton armé", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M2-STR-TP01", "Code": "UEM 2.1", "Parcours": "Master 2 Structures", "Matière": "Projet structures en béton armé", "Type": "TP", "Groupe": "Groupe Unique", "Volume_Hebdo": 3.0, "Is_New": False},
        {"ID": "M2-STR-TP02", "Code": "UEM 2.1", "Parcours": "Master 2 Structures", "Matière": "Modélisation des structures", "Type": "TP", "Groupe": "Groupe Unique", "Volume_Hebdo": 3.0, "Is_New": False},
        {"ID": "M2-STR-C06", "Code": "UET 2.1", "Parcours": "Master 2 Structures", "Matière": "Recherche documentaire et conception de mémoire", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M2-STR-NEW01", "Code": "UET 2.1", "Parcours": "Master 2 Structures", "Matière": "Reverse Engineering", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": True},
        {"ID": "M2-STR-NEW02", "Code": "UET 2.1", "Parcours": "Master 2 Structures", "Matière": "Reverse Engineering", "Type": "Atelier", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": True},

        # =========================================================
        # MASTER 1 RIB - S1 (1 Seul Groupe)
        # =========================================================
        {"ID": "M1-RIB-C01", "Code": "UEF 1.1.1", "Parcours": "Master 1 RIB", "Matière": "Pathologie des ouvrages (bâtiments et géotechniques)", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 3.0, "Is_New": False},
        {"ID": "M1-RIB-C02", "Code": "UEF 1.1.1", "Parcours": "Master 1 RIB", "Matière": "Eléments en béton armé", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M1-RIB-TD01", "Code": "UEF 1.1.1", "Parcours": "Master 1 RIB", "Matière": "Eléments en béton armé", "Type": "TD", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M1-RIB-C03", "Code": "UEF 1.1.2", "Parcours": "Master 1 RIB", "Matière": "Dynamique des Structures (DDS)", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M1-RIB-TD02", "Code": "UEF 1.1.2", "Parcours": "Master 1 RIB", "Matière": "Dynamique des Structures (DDS)", "Type": "TD", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M1-RIB-C04", "Code": "UEF 1.1.2", "Parcours": "Master 1 RIB", "Matière": "Elasticité", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M1-RIB-TD03", "Code": "UEF 1.1.2", "Parcours": "Master 1 RIB", "Matière": "Elasticité", "Type": "TD", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M1-RIB-C05", "Code": "UEM 1.1", "Parcours": "Master 1 RIB", "Matière": "Matériaux innovants", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M1-RIB-TP01", "Code": "UEM 1.1", "Parcours": "Master 1 RIB", "Matière": "Matériaux innovants (TP)", "Type": "TP", "Groupe": "Groupe Unique", "Volume_Hebdo": 3.0, "Is_New": False},
        {"ID": "M1-RIB-TP02", "Code": "UEM 1.1", "Parcours": "Master 1 RIB", "Matière": "Mini projet tuteuré 1", "Type": "TP", "Groupe": "Groupe Unique", "Volume_Hebdo": 2.5, "Is_New": False},
        {"ID": "M1-RIB-C06", "Code": "UEM 1.1", "Parcours": "Master 1 RIB", "Matière": "Programmation avancée en Python", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M1-RIB-TP03", "Code": "UEM 1.1", "Parcours": "Master 1 RIB", "Matière": "Programmation avancée en Python (TP)", "Type": "TP", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M1-RIB-NEW01", "Code": "UED 1.1", "Parcours": "Master 1 RIB", "Matière": "Respect des normes et des règles d'éthique et d'intégrité", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": True},
        {"ID": "M1-RIB-C07", "Code": "UED 1.1", "Parcours": "Master 1 RIB", "Matière": "Communication interpersonnelle", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},

        # =========================================================
        # MASTER 2 RIB - S1 (1 Seul Groupe)
        # =========================================================
        {"ID": "M2-RIB-C01", "Code": "UEF 2.1.1", "Parcours": "Master 2 RIB", "Matière": "Réhabilitation du bâtiment", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M2-RIB-TD01", "Code": "UEF 2.1.1", "Parcours": "Master 2 RIB", "Matière": "Réhabilitation du bâtiment", "Type": "TD", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M2-RIB-C02", "Code": "UEF 2.1.1", "Parcours": "Master 2 RIB", "Matière": "Durabilité des bétons", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M2-RIB-TP01", "Code": "UEM 2.1", "Parcours": "Master 2 RIB", "Matière": "Mini projet tuteuré 3 : atelier", "Type": "TP", "Groupe": "Groupe Unique", "Volume_Hebdo": 2.5, "Is_New": False},
        {"ID": "M2-RIB-C03", "Code": "UEM 2.1", "Parcours": "Master 2 RIB", "Matière": "Building information modeling (BIM)", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.0, "Is_New": False},
        {"ID": "M2-RIB-TP02", "Code": "UEM 2.1", "Parcours": "Master 2 RIB", "Matière": "Building information modeling (BIM) (TP)", "Type": "TP", "Groupe": "Groupe Unique", "Volume_Hebdo": 2.0, "Is_New": False},
        {"ID": "M2-RIB-C04", "Code": "UEM 2.1", "Parcours": "Master 2 RIB", "Matière": "Intelligence artificielle 2", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M2-RIB-TP03", "Code": "UEM 2.1", "Parcours": "Master 2 RIB", "Matière": "Intelligence artificielle 2 (TP)", "Type": "TP", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M2-RIB-TP04", "Code": "UEM 2.1", "Parcours": "Master 2 RIB", "Matière": "Acquisition & Traitement intelligent des Signaux", "Type": "TP", "Groupe": "Groupe Unique", "Volume_Hebdo": 3.0, "Is_New": False},
        {"ID": "M2-RIB-TP05", "Code": "UEM 2.1", "Parcours": "Master 2 RIB", "Matière": "Stage aux entreprises (Suivi/TP)", "Type": "TP", "Groupe": "Groupe Unique", "Volume_Hebdo": 3.0, "Is_New": False},
        {"ID": "M2-RIB-C05", "Code": "UED 2.1", "Parcours": "Master 2 RIB", "Matière": "Intégration professionnelle et entrepreneuriat", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M2-RIB-C06", "Code": "UED 2.1", "Parcours": "Master 2 RIB", "Matière": "Management des projets", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M2-RIB-C07", "Code": "UET 2.1", "Parcours": "Master 2 RIB", "Matière": "Recherche documentaire et conception de mémoire", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": False},
        {"ID": "M2-RIB-NEW01", "Code": "UET 2.1", "Parcours": "Master 2 RIB", "Matière": "Reverse Engineering", "Type": "Cours", "Groupe": "Section Unique", "Volume_Hebdo": 1.5, "Is_New": True},
        {"ID": "M2-RIB-NEW02", "Code": "UET 2.1", "Parcours": "Master 2 RIB", "Matière": "Reverse Engineering", "Type": "Atelier", "Groupe": "Groupe Unique", "Volume_Hebdo": 1.5, "Is_New": True}
    ])

# Gestion des états
if "locked_modules" not in st.session_state:
    st.session_state["locked_modules"] = {}

if "submissions_feed" not in st.session_state:
    st.session_state["submissions_feed"] = [
        {"nom": "Dr. Benali Mohamed", "date": "24/08/2026 à 09:15", "statut": "Vœux enregistrés"},
        {"nom": "Pr. Mansouri Fatima", "date": "24/08/2026 à 10:02", "statut": "Vœux enregistrés"}
    ]

# -------------------------------------------------------------
# EN-TÊTE & NAVIGATION
# -------------------------------------------------------------
st.markdown('<div class="main-title">🏛️ Département de Génie Civil — Université de Tlemcen</div>', unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Plateforme collaborative d'expression des vœux et répartition des charges pédagogiques</div>", unsafe_allow_html=True)

nav = st.sidebar.radio("Espace de Travail", ["📝 Exprimer mes Vœux (Enseignant)", "🔐 Clôture & Arbitrage (Responsable)"])

# URL Google Apps Script Webhook (À remplacer par votre URL de déploiement Apps Script)
GOOGLE_SHEET_WEBHOOK = "https://script.google.com/macros/s/AKfycbz_EXEMPLE_GOOGLE_SHEET/exec"

def send_to_google_sheet(payload):
    try:
        req = urllib.request.Request(
            GOOGLE_SHEET_WEBHOOK,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        urllib.request.urlopen(req, timeout=5)
        return True
    except Exception:
        return False

# =============================================================
# ESPACE 1 : ENSEIGNANT
# =============================================================
if nav == "📝 Exprimer mes Vœux (Enseignant)":
    
    with st.expander("📢 Mur des validations du Département (Suivi en direct)", expanded=False):
        st.caption("Ce mur indique les collègues ayant déjà validé leur formulaire. Le détail de vos choix reste strictement confidentiel.")
        if st.session_state["submissions_feed"]:
            df_feed = pd.DataFrame(st.session_state["submissions_feed"])
            st.table(df_feed[["nom", "date", "statut"]])
        else:
            st.info("Aucune soumission pour le moment.")

    with st.form("form_voeux_departement"):
        st.subheader("1. Identification de l'Enseignant")
        c1, c2 = st.columns(2)
        with c1:
            nom_prenom = st.text_input("Nom & Prénom *")
        with c2:
            email = st.text_input("Email Institutionnel *")

        st.markdown("---")

        # 2. Panier Général (12 Parcours complets incluant la 4ème Année Ingénieur)
        st.subheader("2. Mon Panier (Matières assurées l'an passé et nouvelles matières souhaitées)")
        st.caption("Sélectionnez vos enseignements par parcours. Si une matière a déjà été clôturée par le département, elle apparaît verrouillée.")

        df_all = get_master_modules()
        locked = st.session_state["locked_modules"]

        tab_l2, tab_l3, tab_m1_rib, tab_m2_rib, tab_m1_voa, tab_m2_voa, tab_m1_str, tab_m2_str, tab_ing1, tab_ing2, tab_ing3, tab_ing4 = st.tabs([
            "📙 L2 GC", "📗 L3 GC", "🏢 M1 RIB", "🏬 M2 RIB", "🎓 M1 VOA", "🏛️ M2 VOA", "🏗️ M1 Str.", "🏢 M2 Str.", "📘 1ère Ing.", "📙 2ème Ing.", "📗 3ème Ing.", "📕 4ème Ing."
        ])

        tabs_mapping = [
            (tab_l2, "L2 Génie Civil"),
            (tab_l3, "L3 Génie Civil"),
            (tab_m1_rib, "Master 1 RIB"),
            (tab_m2_rib, "Master 2 RIB"),
            (tab_m1_voa, "Master 1 VOA"),
            (tab_m2_voa, "Master 2 VOA"),
            (tab_m1_str, "Master 1 Structures"),
            (tab_m2_str, "Master 2 Structures"),
            (tab_ing1, "1ère Ingénieur"),
            (tab_ing2, "2ème Ingénieur"),
            (tab_ing3, "3ème Ingénieur"),
            (tab_ing4, "4ème Ingénieur")
        ]

        selected_basket = []
        for tab_elem, parcours_name in tabs_mapping:
            with tab_elem:
                df_sub = df_all[df_all["Parcours"] == parcours_name]
                cols = st.columns(2)
                for idx, row in df_sub.iterrows():
                    target_col = cols[idx % 2]
                    mod_id = row['ID']
                    is_locked = mod_id in locked

                    if is_locked:
                        target_col.markdown(f"🔒 ~~{row['Matière']} [{row['Type']} - {row['Groupe']} - {row['Volume_Hebdo']}h]~~ <span class='badge-closed'>Attribué</span>", unsafe_allow_html=True)
                    else:
                        label = f"**{row['Matière']}** — *{row['Type']}* ({row['Groupe']}) `[{row['Volume_Hebdo']}h/sem]`"
                        if target_col.checkbox(label, key=f"panier_{mod_id}"):
                            selected_basket.append(row)

        df_sel_basket = pd.DataFrame(selected_basket)
        total_heures_panier = df_sel_basket["Volume_Hebdo"].sum() if not df_sel_basket.empty else 0.0

        st.markdown(f"#### ⏱️ Volume Total Sélectionné dans le Panier : `{total_heures_panier} h / semaine`")

        st.markdown("---")

        # 3. Nouvelles Matières & 4ème Ingénieur avec Visibilité Complète [Type - Groupe - Heures]
        st.subheader("3. 🌟 Nouvelles Matières & 4ème Année Ingénieur : Classement Obligatoire")
        st.info("💡 **Incitation Départementale :** Le classement ci-dessous concerne les matières de la **4ème année Ingénieur (Nouvelle formation)**, les modules de **Reverse Engineering**, **Histoire de l'Algérie** et **Éthique & Déontologie**. Veuillez classer au minimum **2 choix distincts**.")

        df_new = df_all[df_all["Is_New"] == True]
        df_new_open = df_new[~df_new["ID"].isin(locked)]
        
        # Formatage avec visibilité maximale : Parcours | Matière | Type d'enseignement | Groupe | Heures
        options_new = ["-- Aucun choix --"] + [
            f"{r['Parcours']} ➔ {r['Matière']} [{r['Type']} | {r['Groupe']} | {r['Volume_Hebdo']}h]" 
            for _, r in df_new_open.iterrows()
        ]

        v1, v2, v3 = st.columns(3)
        with v1:
            choix_1 = st.selectbox("🥇 1er Choix (Prioritaire) *", options_new, index=0)
        with v2:
            choix_2 = st.selectbox("🥈 2e Choix *", options_new, index=0)
        with v3:
            choix_3 = st.selectbox("🥉 3e Choix (Facultatif)", options_new, index=0)

        # 4. Bandeau Nudge / Incitatif "Reverse Engineering"
        st.markdown("""
        <div class="nudge-card">
            <h4 style="margin:0 0 6px 0; color:#1e40af;">🚀 Focus Valorisation Pédagogique — Atelier Reverse Engineering (M2)</h4>
            <p style="margin:0; font-size:13px; color:#1e293b; line-height:1.5;">
                Le module <strong>Reverse Engineering (Cours + Atelier)</strong> est dispensé en M2 Structures, M2 VOA et M2 RIB.
                <br>🎯 <em>Avantages :</em> Priorité d'arbitrage sur vos créneaux d'emploi du temps et sur l'encadrement des projets de fin d'études (PFE) Master.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        opt_reverse = st.checkbox("🙋 Je suis volontaire / intéressé pour assurer le module de Reverse Engineering", key="opt_reverse_eng")

        st.markdown("---")

        # 5. Remarques, souhaits particuliers & Indisponibilités
        st.subheader("4. 💬 Souhaits Particuliers, Contraintes & Remarques")
        commentaires = st.text_area("Observations éventuelles :")

        submitted = st.form_submit_button("🚀 Valider et Transmettre Définitivement mes Vœux", use_container_width=True)

        if submitted:
            if not nom_prenom or not email:
                st.error("❌ Veuillez renseigner votre Nom, Prénom et Email Institutionnel.")
            elif choix_1 == "-- Aucun choix --" or choix_2 == "-- Aucun choix --":
                st.error("❌ Règle obligatoire : Veuillez classer au minimum vos choix 1 et 2 parmi les nouvelles matières.")
            elif choix_1 == choix_2:
                st.error("❌ Vos choix 1 et 2 ne peuvent pas être identiques.")
            else:
                timestamp_str = datetime.now().strftime("%d/%m/%Y à %H:%M")
                
                payload = {
                    "timestamp": timestamp_str,
                    "nom": nom_prenom,
                    "email": email,
                    "volume_panier": total_heures_panier,
                    "matieres_selectionnees": [f"{r['Matière']} ({r['Parcours']} - {r['Type']} - {r['Groupe']})" for r in selected_basket],
                    "choix_nouveau_1": choix_1,
                    "choix_nouveau_2": choix_2,
                    "choix_nouveau_3": choix_3 if choix_3 != "-- Aucun choix --" else "Néant",
                    "volontaire_reverse_engineering": "OUI" if opt_reverse else "NON",
                    "remarques_souhaits": commentaires
                }

                send_to_google_sheet(payload)

                st.session_state["submissions_feed"].append({
                    "nom": f"Dr. {nom_prenom}",
                    "date": timestamp_str,
                    "statut": "Vœux enregistrés"
                })

                st.success(f"✅ Vœux enregistrés avec succès pour {nom_prenom} !")
                st.balloons()
                st.info("Le département a bien reçu votre fiche. Vous pouvez d'ores et déjà préparer vos supports de cours.")

# =============================================================
# ESPACE 2 : RESPONSABLE PÉDAGOGIQUE (CLÔTURE & GESTION DES DOUBLONS)
# =============================================================
else:
    st.subheader("🔐 Espace Responsable Pédagogique — Clôture & Arbitrage des Attributions")
    st.caption("Cette section permet de valider définitivement l'attribution d'une matière à un enseignant et de la clôturer pour éviter tout doublon.")

    pin_code = st.text_input("Code PIN Responsable :", type="password")
    if pin_code == "1234":
        st.success("🔓 Authentification Responsable validée.")
        
        df_all = get_master_modules()
        
        c_act1, c_act2 = st.columns([2, 1])
        with c_act1:
            st.markdown("#### Attribuer et Clôturer un Enseignement")
            available_mods = df_all[~df_all["ID"].isin(st.session_state["locked_modules"])]
            mod_to_lock = st.selectbox("Sélectionner la matière à clôturer :", 
                                       [f"[{r['Parcours']}] {r['Matière']} ({r['Type']}) - ID: {r['ID']}" for _, r in available_mods.iterrows()])
            enseignant_assigne = st.text_input("Enseignant bénéficiaire :")
            
            if st.button("🔒 Valider l'Attribution & Clôturer"):
                if enseignant_assigne and mod_to_lock:
                    selected_id = mod_to_lock.split("ID: ")[-1]
                    st.session_state["locked_modules"][selected_id] = enseignant_assigne
                    st.success(f"Matière {selected_id} clôturée et attribuée à {enseignant_assigne} !")
                    st.rerun()

        with c_act2:
            st.markdown("#### État des Matières Clôturées")
            if st.session_state["locked_modules"]:
                df_locked = pd.DataFrame(list(st.session_state["locked_modules"].items()), columns=["ID Matière", "Enseignant Attribué"])
                st.dataframe(df_locked, use_container_width=True)
                if st.button("🔄 Réinitialiser tous les verrouillages"):
                    st.session_state["locked_modules"] = {}
                    st.rerun()
            else:
                st.info("Aucune matière verrouillée pour l'instant.")

        st.markdown("---")
        st.markdown("#### Tableau Général des 12 Parcours (380h)")
        st.dataframe(df_all, use_container_width=True)
    elif pin_code != "":
        st.error("Code PIN incorrect.")
