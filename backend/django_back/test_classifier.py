#!/usr/bin/env python3
"""Test du classificateur thématique"""

from analysis.theme_classifier import ThemeClassifier

# Exemples d'articles burkinabè
articles_test = [
    {
        'titre': "Le Président Ibrahim Traoré reçoit le Premier ministre",
        'contenu': "Le Président de la Transition, le Capitaine Ibrahim Traoré, a reçu en audience ce mardi le Premier ministre Apollinaire Joachim Kyélem de Tambèla. Les deux hommes ont échangé sur la situation sécuritaire et les réformes en cours."
    },
    {
        'titre': "Le Burkina Faso enregistre une croissance de 6,5% au premier trimestre",
        'contenu': "L'économie burkinabè affiche une croissance de 6,5% au premier trimestre 2025, portée par le secteur agricole et les exportations d'or. Le ministre de l'Économie a salué ces résultats encourageants."
    },
    {
        'titre': "Les FDS neutralisent plusieurs terroristes dans le Sahel",
        'contenu': "Les Forces de Défense et de Sécurité ont mené une opération d'envergure dans la région du Sahel, neutralisant plusieurs éléments terroristes et récupérant du matériel de guerre."
    },
    {
        'titre': "Lancement de la campagne de vaccination contre la rougeole",
        'contenu': "Le ministère de la Santé a lancé une vaste campagne de vaccination contre la rougeole ciblant les enfants de 9 mois à 5 ans. Plus de 2 millions d'enfants sont concernés."
    },
    {
        'titre': "Le FESPACO 2025 ouvre ses portes à Ouagadougou",
        'contenu': "La 29e édition du Festival panafricain du cinéma et de la télévision de Ouagadougou (FESPACO) a débuté ce samedi avec la projection du film d'ouverture. Plus de 200 films sont en compétition."
    },
    {
        'titre': "Les Étalons se qualifient pour la CAN 2026",
        'contenu': "L'équipe nationale de football du Burkina Faso s'est qualifiée pour la Coupe d'Afrique des Nations 2026 après sa victoire 2-0 contre le Niger. Les supporters ont célébré cette qualification."
    }
]

print("🧪 Test du classificateur thématique\n")
print("="*60)

# Initialiser le classificateur
classifier = ThemeClassifier()

# Vérifier Ollama
print("🔍 Vérification d'Ollama...")
if classifier.check_ollama_status():
    print("✅ Ollama est accessible\n")
else:
    print("❌ Ollama n'est pas accessible")
    print("💡 Démarrez Ollama: ollama serve")
    print("💡 Installez Mistral: ollama pull mistral\n")
    print("🔄 Test avec classification par mots-clés...\n")

print("="*60)
print("📰 CLASSIFICATION DES ARTICLES")
print("="*60 + "\n")

for i, article in enumerate(articles_test, 1):
    print(f"{i}. {article['titre']}")
    print("-" * 60)
    
    result = classifier.classify_article(article['titre'], article['contenu'])
    
    print(f"   📂 Catégorie: {result['categorie']}")
    print(f"   📊 Confiance: {result['confiance']:.2f}")
    print(f"   🔧 Méthode: {result['methode']}")
    
    if result.get('mots_cles'):
        print(f"   🔑 Mots-clés: {', '.join(result['mots_cles'])}")
    
    if result.get('justification'):
        print(f"   💡 Justification: {result['justification']}")
    
    print()

print("="*60)
print("✅ Test terminé")
