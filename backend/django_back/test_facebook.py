#!/usr/bin/env python3
"""
Test du scraper Facebook pour AIB
"""

import os
from dotenv import load_dotenv
from scrapers.facebook_scraper import FacebookScraper
from database.db_manager import DatabaseManager

# Charger les variables d'environnement depuis .env
load_dotenv()


def main():
    print("="*70)
    print("🧪 TEST DU SCRAPER FACEBOOK - AIB")
    print("="*70 + "\n")
    
    # Vérifier le token
    token = os.getenv('FACEBOOK_ACCESS_TOKEN')
    if not token:
        print("❌ Erreur: Token Facebook manquant")
        print("💡 Définissez FACEBOOK_ACCESS_TOKEN dans .env ou en variable d'environnement")
        return
    
    print(f"✅ Token trouvé: {token[:20]}...")
    
    # Initialiser le scraper
    print("\n🔧 Initialisation du scraper...")
    scraper = FacebookScraper(token)
    
    # Tester la connexion
    print("🔌 Test de connexion à l'API Facebook...")
    if not scraper.test_connection():
        print("❌ Impossible de se connecter à l'API Facebook")
        print("💡 Vérifiez votre token et votre connexion internet")
        return
    
    print("✅ Connexion réussie !\n")
    
    # Page AIB
    page_name = "aib.infos"
    print("="*70)
    print(f"📘 SCRAPING DE LA PAGE: {page_name}")
    print("="*70 + "\n")
    
    # Scraper la page
    result = scraper.scrape_page(page_name, limit=5)
    
    if result.get('error'):
        print(f"❌ Erreur: {result['error']}")
        return
    
    # Afficher les résultats
    page_info = result.get('page_info', {})
    posts = result.get('posts', [])
    stats = result.get('stats', {})
    
    print(f"📺 Page: {page_info.get('name', 'N/A')}")
    print(f"🆔 ID: {page_info.get('id', 'N/A')}")
    print(f"📊 Posts récupérés: {len(posts)}\n")
    
    # Détails des posts
    if posts:
        print("="*70)
        print("📝 DÉTAILS DES POSTS")
        print("="*70 + "\n")
        
        for i, post in enumerate(posts, 1):
            print(f"{i}. Post du {post['date_publication']}")
            print(f"   🔗 URL: {post['url']}")
            
            # Message (tronqué)
            message = post.get('message', 'Pas de texte')
            if len(message) > 100:
                message = message[:100] + "..."
            print(f"   💬 Message: {message}")
            
            # Métriques
            print(f"   👍 Likes: {post['likes']:,}")
            print(f"   💬 Commentaires: {post['comments']:,}")
            print(f"   🔄 Partages: {post['shares']:,}")
            print(f"   📊 Engagement: {post['engagement_total']:,}")
            print()
    
    # Statistiques globales
    print("="*70)
    print("📊 STATISTIQUES GLOBALES")
    print("="*70 + "\n")
    print(f"Total likes: {stats.get('total_likes', 0):,}")
    print(f"Total commentaires: {stats.get('total_comments', 0):,}")
    print(f"Total partages: {stats.get('total_shares', 0):,}")
    print(f"Engagement total: {stats.get('total_engagement', 0):,}")
    print(f"Engagement moyen: {stats.get('avg_engagement', 0):.0f} par post")
    
    # Sauvegarder en base de données
    print("\n" + "="*70)
    print("💾 SAUVEGARDE EN BASE DE DONNÉES")
    print("="*70 + "\n")
    
    db = DatabaseManager()
    
    # Ajouter/récupérer le média
    media_id = db.add_media("AIB", "https://www.aib.media")
    print(f"✅ Média AIB (ID: {media_id})")
    
    # Sauvegarder les posts
    saved_count = 0
    for post in posts:
        try:
            db.add_facebook_post(
                media_id=media_id,
                post_id=post['post_id'],
                message=post['message'],
                url=post['url'],
                image_url=post.get('image_url'),
                date_publication=post['date_publication'],
                likes=post['likes'],
                comments=post['comments'],
                shares=post['shares']
            )
            saved_count += 1
        except Exception as e:
            print(f"⚠️ Post déjà existant ou erreur: {post['post_id']}")
    
    print(f"✅ {saved_count} posts sauvegardés")
    
    # Calculer les métriques
    print("\n📈 Calcul des métriques...")
    metrics = db.calculate_media_metrics(media_id, days=30)
    
    if metrics:
        print(f"✅ Métriques calculées:")
        print(f"   Articles: {metrics['total_articles']}")
        print(f"   Posts Facebook: {metrics['total_posts_facebook']}")
        print(f"   Engagement total: {metrics['engagement_total']:,}")
        print(f"   Engagement moyen: {metrics['engagement_moyen']:.0f}")
    
    print("\n" + "="*70)
    print("✅ TEST TERMINÉ AVEC SUCCÈS !")
    print("="*70)


if __name__ == '__main__':
    main()
