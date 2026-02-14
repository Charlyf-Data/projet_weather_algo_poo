import pytest
from projet.structure.arbre_binaire import ArbreBinaire


# =========================================================
# 1️ Test arbre vide
# =========================================================
def test_arbre_initialement_vide():

    arbre = ArbreBinaire()

    assert arbre.est_vide()
    assert arbre.get_valeur() is None
    assert arbre.retirer() is None


# =========================================================
# 2️ Test ajouter valeur racine
# =========================================================
def test_ajouter_racine():

    arbre = ArbreBinaire()
    arbre.ajouter(10)

    assert not arbre.est_vide()
    assert arbre.get_valeur() == 10


# =========================================================
# 3️ Test ajouter gauche puis droite
# =========================================================
def test_ajouter_gauche_et_droite():

    arbre = ArbreBinaire()
    arbre.ajouter(1)
    arbre.ajouter(2)
    arbre.ajouter(3)

    assert arbre.get_valeur() == 1
    assert arbre.get_gauche().get_valeur() == 2
    assert arbre.get_droite().get_valeur() == 3


# =========================================================
# 4️ Test ajout récursif quand plein
# =========================================================
def test_ajout_recursif():

    arbre = ArbreBinaire()
    arbre.ajouter(1)
    arbre.ajouter(2)
    arbre.ajouter(3)
    arbre.ajouter(4)  # doit aller dans sous-arbre gauche

    assert arbre.get_gauche().get_gauche().get_valeur() == 4


# =========================================================
# 5️ Test retirer
# =========================================================
def test_retirer():

    arbre = ArbreBinaire()
    arbre.ajouter(42)

    valeur = arbre.retirer()

    assert valeur == 42
    assert arbre.est_vide()
    assert arbre.get_gauche() is None
    assert arbre.get_droite() is None


# =========================================================
# 6️ Test parcours préfixe (__iter__)
# =========================================================
def test_iter_prefixe():

    arbre = ArbreBinaire()
    arbre.ajouter(1)
    arbre.ajouter(2)
    arbre.ajouter(3)

    valeurs = list(arbre)

    # Préfixe : racine, gauche, droite
    assert valeurs == [1, 2, 3]


# =========================================================
# 7️ Test as_list
# =========================================================
def test_as_list():

    arbre = ArbreBinaire()
    arbre.ajouter("a")
    arbre.ajouter("b")

    assert arbre.as_list() == ["a", "b"]


# =========================================================
# 8️ Test inserer_gauche sans enfant existant
# =========================================================
def test_inserer_gauche_simple():

    arbre = ArbreBinaire(1)
    arbre.inserer_gauche(2)

    assert arbre.get_gauche().get_valeur() == 2


# =========================================================
# 9️ Test inserer_gauche avec enfant existant
# =========================================================
def test_inserer_gauche_avec_remplacement():

    arbre = ArbreBinaire(1)
    arbre.inserer_gauche(2)
    arbre.inserer_gauche(3)

    assert arbre.get_gauche().get_valeur() == 3
    assert arbre.get_gauche().get_gauche().get_valeur() == 2


# =========================================================
# 10 Test inserer_droite simple
# =========================================================
def test_inserer_droite_simple():

    arbre = ArbreBinaire(1)
    arbre.inserer_droite(5)

    assert arbre.get_droite().get_valeur() == 5


# =========================================================
# 11 Test inserer_droite avec remplacement
# =========================================================
def test_inserer_droite_avec_remplacement():

    arbre = ArbreBinaire(1)
    arbre.inserer_droite(2)
    arbre.inserer_droite(3)

    assert arbre.get_droite().get_valeur() == 3
    assert arbre.get_droite().get_droite().get_valeur() == 2
