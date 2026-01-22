from __future__ import annotations

from typing import Dict, List, Tuple
import pandas as pd


# --- Catégorisation simple (V1) ---
CATEGORY_KEYWORDS: Dict[str, List[str]] = {
    "Paiement": [
        "paiement", "payer", "carte", "cb", "facture", "facturation",
        "prélèvement", "prelevement", "rembourse", "remboursement"
    ],
    "Connexion / Compte": [
        "connexion", "connecter", "login", "mot de passe", "mdp", "compte",
        "identifiant", "inscription"
    ],
    "Performance / Bugs": [
        "bug", "erreur", "crash", "plante", "lent", "lenteur", "freeze",
        "bloque", "impossible", "ne marche pas", "ne fonctionne pas"
    ],
    "Livraison": [
        "livraison", "livrer", "retard", "colis", "transporteur", "reçu", "recu"
    ],
    "Support": [
        "service client", "support", "assistance", "ticket", "réponse", "reponse",
        "contact", "appel"
    ],
    "UX / Parcours": [
        "interface", "ux", "parcours", "navigation", "bouton", "écran", "ecran",
        "formulaire"
    ],
}

# Sévérité (V1) : patterns explicites
SEVERITY_RULES: List[Tuple[str, str]] = [
    ("P0", r"crash|plante|bloque|impossible|ne marche pas|erreur 500|urgent|inutilisable"),
    ("P1", r"lent|lenteur|bug|erreur|problème|probleme|ne fonctionne pas"),
]

URGENCY_KEYWORDS = {
    "P0": ["crash", "plante", "bloque", "impossible", "urgent", "inutilisable"],
    "P1": ["bug", "erreur", "lent", "lenteur", "problème", "probleme"],
}


def urgency_score(text: str) -> int:
    t = (text or "").lower()
    score = 0
    for kw in URGENCY_KEYWORDS["P0"]:
        if kw in t:
            score += 3
    for kw in URGENCY_KEYWORDS["P1"]:
        if kw in t:
            score += 1
    return min(score, 10)


def classify_category(text: str) -> str:
    t = (text or "").lower()
    best_cat = "Général"
    best_hits = 0
    for cat, kws in CATEGORY_KEYWORDS.items():
        hits = sum(1 for k in kws if k in t)
        if hits > best_hits:
            best_hits = hits
            best_cat = cat
    return best_cat


def classify_severity(text: str) -> str:
    import re
    t = (text or "").lower()
    for sev, pattern in SEVERITY_RULES:
        if re.search(pattern, t):
            return sev
    return "P2"


def severity_weight(sev: str) -> int:
    return {"P0": 100, "P1": 60, "P2": 30}.get(sev, 30)


def suggest_action(category: str, severity: str) -> str:
    """
    Action suggérée (V1) : simple, crédible, orientée décision.
    """
    if severity == "P0":
        return "Correction immédiate / hotfix"
    if category in ["Paiement", "Connexion / Compte"]:
        return "Analyse technique + correctif prioritaire"
    if category == "Performance / Bugs":
        return "Debug + stabilisation"
    if category == "UX / Parcours":
        return "Amélioration UX / test utilisateur"
    if category == "Support":
        return "Process / formation support"
    return "Analyse complémentaire"


def build_backlog(df_analysis: pd.DataFrame, text_col: str) -> pd.DataFrame:
    """
    Entrée : df d'analyse contenant idéalement topic_label (+ texte original)
    Sortie : backlog priorisé avec category / severity / urgency_score / priority_score / action_suggeree
    """
    dfx = df_analysis.copy()

    if text_col not in dfx.columns:
        raise ValueError(f"Colonne texte introuvable: {text_col}")

    # fallback si topic_label absent
    if "topic_label" not in dfx.columns:
        if "topic" in dfx.columns:
            dfx["topic_label"] = dfx["topic"].apply(lambda x: f"Topic {x}")
        else:
            dfx["topic_label"] = "Thème"

    # Classification
    dfx["category"] = dfx[text_col].astype(str).apply(classify_category)
    dfx["severity"] = dfx[text_col].astype(str).apply(classify_severity)
    dfx["urgency_score"] = dfx[text_col].astype(str).apply(urgency_score)

    # Score global
    dfx["priority_score"] = dfx["severity"].apply(severity_weight) + dfx["urgency_score"]

    # Action suggérée
    dfx["action_suggeree"] = dfx.apply(
        lambda r: suggest_action(r["category"], r["severity"]),
        axis=1
    )

    # Tri (plus prioritaire en haut)
    dfx = dfx.sort_values(["priority_score", "severity"], ascending=[False, True]).reset_index(drop=True)
    return dfx
