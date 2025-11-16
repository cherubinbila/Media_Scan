#!/usr/bin/env python3
"""
Script pour classifier automatiquement les articles
Utilise Mistral via Ollama pour la classification thématique
"""

import argparse
from database.db_manager import DatabaseManager
from analysis.theme_classifier import ThemeClassifier


def main():
    parser = argparse.ArgumentParser(description='Classifier les articles par thème')
    parser.add_argument('--limit', type=int, default=100, 
                       help='Nombre maximum d\'articles à classifier')
    parser.add_argument('--force', action='store_true',
                       help='Reclassifier tous les articles (même déjà classifiés)')
    parser.add_argument('--stats', action='store_true',
                       help='Afficher uniquement les statistiques')
    
    args = parser.parse_args()
    
    # Initialiser la base de données
    print("🔧 Initialisation de la base de données...")
    db = DatabaseManager()
    
    # Si stats uniquement
    if args.stats:
        print("\n" + "="*60)
        print("📊 STATISTIQUES DE CLASSIFICATION")
        print("="*60 + "\n")
        
        stats = db.get_classification_stats()
        
        print(f"📰 Total articles: {stats['total_articles']}")
        print(f"✅ Articles classifiés: {stats['total_classifies']} ({stats['pourcentage_classifies']}%)")
        
        if stats['par_categorie']:
            print(f"\n📋 Par catégorie:")
            for cat, count in sorted(stats['par_categorie'].items(), key=lambda x: x[1], reverse=True):
                confiance = stats['confiance_par_categorie'].get(cat, 0)
                print(f"   • {cat}: {count} articles (confiance moyenne: {confiance})")
        
        if stats['par_methode']:
            print(f"\n🔧 Par méthode:")
            for methode, count in stats['par_methode'].items():
                print(f"   • {methode}: {count} classifications")
        
        return
    
    # Initialiser le classificateur
    print("🤖 Initialisation du classificateur Mistral...")
    classifier = ThemeClassifier()
    
    # Vérifier Ollama
    if not classifier.check_ollama_status():
        print("❌ Ollama n'est pas accessible!")
        print("💡 Assurez-vous qu'Ollama est démarré: ollama serve")
        print("💡 Et que Mistral est installé: ollama pull mistral")
        return
    
    print("✅ Ollama accessible\n")
    
    # Récupérer les articles à classifier
    if args.force:
        print(f"📚 Récupération de tous les articles (limit: {args.limit})...")
        # TODO: Ajouter méthode get_all_articles dans db_manager
        articles = db.get_unclassified_articles(args.limit)
    else:
        print(f"📚 Récupération des articles non classifiés (limit: {args.limit})...")
        articles = db.get_unclassified_articles(args.limit)
    
    if not articles:
        print("✅ Aucun article à classifier")
        return
    
    print(f"📊 {len(articles)} articles à classifier\n")
    
    # Classifier les articles
    print("="*60)
    print("🚀 CLASSIFICATION EN COURS")
    print("="*60 + "\n")
    
    classified_count = 0
    errors = 0
    
    for i, article in enumerate(articles, 1):
        try:
            print(f"[{i}/{len(articles)}] {article['titre'][:60]}...")
            
            # Classifier
            result = classifier.classify_article(
                article['titre'],
                article['contenu'] or ''
            )
            
            # Sauvegarder
            db.add_classification(
                article_id=article['id'],
                categorie=result['categorie'],
                confiance=result['confiance'],
                mots_cles=result.get('mots_cles', []),
                justification=result.get('justification', ''),
                methode=result.get('methode', 'mistral_ollama')
            )
            
            print(f"   ✅ {result['categorie']} (confiance: {result['confiance']:.2f})")
            if result.get('mots_cles'):
                print(f"   🔑 Mots-clés: {', '.join(result['mots_cles'][:3])}")
            
            classified_count += 1
        
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
            errors += 1
        
        print()
    
    # Résumé
    print("="*60)
    print("📊 RÉSUMÉ")
    print("="*60 + "\n")
    
    print(f"✅ Articles classifiés: {classified_count}")
    if errors > 0:
        print(f"❌ Erreurs: {errors}")
    
    # Statistiques finales
    print("\n" + "="*60)
    print("📊 STATISTIQUES FINALES")
    print("="*60 + "\n")
    
    stats = db.get_classification_stats()
    
    print(f"📰 Total articles: {stats['total_articles']}")
    print(f"✅ Articles classifiés: {stats['total_classifies']} ({stats['pourcentage_classifies']}%)")
    
    if stats['par_categorie']:
        print(f"\n📋 Par catégorie:")
        for cat, count in sorted(stats['par_categorie'].items(), key=lambda x: x[1], reverse=True):
            confiance = stats['confiance_par_categorie'].get(cat, 0)
            print(f"   • {cat}: {count} articles (confiance: {confiance})")


if __name__ == '__main__':
    main()
