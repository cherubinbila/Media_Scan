#!/usr/bin/env python3
"""
Test du scraper Twitter/X pour AIB
"""

import os
from dotenv import load_dotenv
from scrapers.twitter_scraper import TwitterScraper
from database.db_manager import DatabaseManager

# Charger les variables d'environnement depuis .env
load_dotenv()


def main():
    print("="*70)
    print("🧪 TEST DU SCRAPER TWITTER/X - AIB")
    print("="*70 + "\n")
    
    # Vérifier le token
    token = os.getenv('TWITTER_BEARER_TOKEN')
    if not token:
        print("❌ Erreur: Bearer Token Twitter manquant")
        print("💡 Définissez TWITTER_BEARER_TOKEN dans .env ou en variable d'environnement")
        return
    
    print(f"✅ Bearer Token trouvé: {token[:20]}...")
    
    # Initialiser le scraper
    print("\n🔧 Initialisation du scraper...")
    scraper = TwitterScraper(token)
    
    # Tester la connexion
    print("🔌 Test de connexion à l'API Twitter...")
    if not scraper.test_connection():
        print("❌ Impossible de se connecter à l'API Twitter")
        print("💡 Vérifiez votre Bearer Token et votre connexion internet")
        return
    
    print("✅ Connexion réussie !\n")
    
    # Compte AIB
    username = "aibburkina"
    print("="*70)
    print(f"🐦 SCRAPING DU COMPTE: @{username}")
    print("="*70 + "\n")
    
    # Scraper le compte
    result = scraper.scrape_user(username, max_results=5)
    
    if result.get('error'):
        print(f"❌ Erreur: {result['error']}")
        return
    
    # Afficher les résultats
    user_info = result.get('user_info', {})
    tweets = result.get('tweets', [])
    stats = result.get('stats', {})
    
    print(f"👤 Utilisateur: @{user_info.get('username', 'N/A')}")
    print(f"🆔 ID: {user_info.get('id', 'N/A')}")
    print(f"📊 Tweets récupérés: {len(tweets)}\n")
    
    # Détails des tweets
    if tweets:
        print("="*70)
        print("📝 DÉTAILS DES TWEETS")
        print("="*70 + "\n")
        
        for i, tweet in enumerate(tweets, 1):
            print(f"{i}. Tweet du {tweet['date_publication']}")
            print(f"   🔗 URL: {tweet['url']}")
            
            # Texte (tronqué)
            text = tweet.get('text', 'Pas de texte')
            if len(text) > 100:
                text = text[:100] + "..."
            print(f"   💬 Texte: {text}")
            
            # Métriques
            print(f"   🔄 Retweets: {tweet['retweets']:,}")
            print(f"   💬 Réponses: {tweet['replies']:,}")
            print(f"   ❤️ Likes: {tweet['likes']:,}")
            print(f"   💭 Citations: {tweet['quotes']:,}")
            if tweet['impressions'] > 0:
                print(f"   👁️ Impressions: {tweet['impressions']:,}")
            print(f"   📊 Engagement: {tweet['engagement_total']:,}")
            print()
    
    # Statistiques globales
    print("="*70)
    print("📊 STATISTIQUES GLOBALES")
    print("="*70 + "\n")
    print(f"Total retweets: {stats.get('total_retweets', 0):,}")
    print(f"Total réponses: {stats.get('total_replies', 0):,}")
    print(f"Total likes: {stats.get('total_likes', 0):,}")
    print(f"Total citations: {stats.get('total_quotes', 0):,}")
    if stats.get('total_impressions', 0) > 0:
        print(f"Total impressions: {stats.get('total_impressions', 0):,}")
    print(f"Engagement total: {stats.get('total_engagement', 0):,}")
    print(f"Engagement moyen: {stats.get('avg_engagement', 0):.0f} par tweet")
    
    # Sauvegarder en base de données
    print("\n" + "="*70)
    print("💾 SAUVEGARDE EN BASE DE DONNÉES")
    print("="*70 + "\n")
    
    db = DatabaseManager()
    
    # Ajouter/récupérer le média
    media_id = db.add_media("AIB", "https://www.aib.media")
    print(f"✅ Média AIB (ID: {media_id})")
    
    # Sauvegarder les tweets
    saved_count = 0
    for tweet in tweets:
        try:
            db.add_twitter_tweet(
                media_id=media_id,
                tweet_id=tweet['tweet_id'],
                text=tweet['text'],
                url=tweet['url'],
                image_url=tweet.get('image_url'),
                date_publication=tweet['date_publication'],
                retweets=tweet['retweets'],
                replies=tweet['replies'],
                likes=tweet['likes'],
                quotes=tweet['quotes'],
                impressions=tweet['impressions']
            )
            saved_count += 1
        except Exception as e:
            print(f"⚠️ Tweet déjà existant ou erreur: {tweet['tweet_id']}")
    
    print(f"✅ {saved_count} tweets sauvegardés")
    
    # Calculer les métriques
    print("\n📈 Calcul des métriques...")
    metrics = db.calculate_media_metrics_with_twitter(media_id, days=30)
    
    if metrics:
        print(f"✅ Métriques calculées:")
        print(f"   Articles: {metrics['total_articles']}")
        print(f"   Posts Facebook: {metrics['total_posts_facebook']}")
        print(f"   Tweets: {metrics['total_tweets']}")
        print(f"   Engagement Facebook: {metrics['engagement_total_fb']:,}")
        print(f"   Engagement Twitter: {metrics['engagement_total_tw']:,}")
        print(f"   Engagement total: {metrics['engagement_total']:,}")
        print(f"   Engagement moyen: {metrics['engagement_moyen']:.0f}")
    
    print("\n" + "="*70)
    print("✅ TEST TERMINÉ AVEC SUCCÈS !")
    print("="*70)


if __name__ == '__main__':
    main()
