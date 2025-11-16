#!/usr/bin/env python3
"""
Script de scraping complet : Web + Facebook + Twitter
1. Scrape les articles du site web (RSS/HTML)
2. Classifie automatiquement les articles
3. Scrape les posts Facebook avec métriques d'engagement
4. Scrape les tweets Twitter avec métriques d'engagement
"""

import argparse
import os
from dotenv import load_dotenv
from database.db_manager import DatabaseManager
from scrapers.scraper_manager import ScraperManager
from scrapers.facebook_scraper import FacebookScraper
from scrapers.twitter_scraper import TwitterScraper

# Charger les variables d'environnement
load_dotenv()


def load_config_file(file_path: str) -> dict:
    """
    Charger un fichier de configuration
    
    Returns:
        Dictionnaire {url_site: identifiant}
    """
    config = {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                parts = line.split('|')
                if len(parts) >= 3:
                    nom, url, identifier = parts[0], parts[1], parts[2]
                    config[url] = identifier
    
    except FileNotFoundError:
        print(f"⚠️ Fichier {file_path} non trouvé")
    
    return config


def scrape_facebook_for_media(db: DatabaseManager, fb_scraper: FacebookScraper, 
                              media_id: int, fb_page: str, limit: int = 5):
    """Scraper Facebook pour un média"""
    print(f"\n📘 Scraping Facebook: {fb_page}")
    
    try:
        result = fb_scraper.scrape_page(fb_page, limit=limit)
        
        if result.get('error'):
            print(f"   ❌ Erreur: {result['error']}")
            return
        
        posts = result.get('posts', [])
        
        if not posts:
            print(f"   ⚠️ Aucun post récupéré")
            return
        
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
            except Exception:
                continue
        
        stats = result.get('stats', {})
        print(f"   ✅ {saved_count} posts sauvegardés")
        print(f"   📊 Engagement: {stats.get('total_engagement', 0):,}")
    
    except Exception as e:
        print(f"   ❌ Erreur: {e}")


def scrape_twitter_for_media(db: DatabaseManager, tw_scraper: TwitterScraper,
                             media_id: int, tw_account: str, limit: int = 5):
    """Scraper Twitter pour un média"""
    print(f"\n🐦 Scraping Twitter: @{tw_account}")
    
    try:
        result = tw_scraper.scrape_user(tw_account, max_results=limit)
        
        if result.get('error'):
            print(f"   ❌ Erreur: {result['error']}")
            return
        
        tweets = result.get('tweets', [])
        
        if not tweets:
            print(f"   ⚠️ Aucun tweet récupéré")
            return
        
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
            except Exception:
                continue
        
        stats = result.get('stats', {})
        print(f"   ✅ {saved_count} tweets sauvegardés")
        print(f"   📊 Engagement: {stats.get('total_engagement', 0):,}")
    
    except Exception as e:
        print(f"   ❌ Erreur: {e}")


def main():
    parser = argparse.ArgumentParser(description='Scraping Web + Facebook + Twitter')
    parser.add_argument('--url', type=str, help='URL d\'un média spécifique')
    parser.add_argument('--all', action='store_true', help='Scraper tous les sites')
    parser.add_argument('--days', type=int, default=30, help='Nombre de jours à scraper')
    parser.add_argument('--fb-posts', type=int, default=5, 
                       help='Nombre de posts Facebook à récupérer')
    parser.add_argument('--tweets', type=int, default=5,
                       help='Nombre de tweets à récupérer')
    parser.add_argument('--skip-facebook', action='store_true',
                       help='Ignorer le scraping Facebook')
    parser.add_argument('--skip-twitter', action='store_true',
                       help='Ignorer le scraping Twitter')
    
    args = parser.parse_args()
    
    # Initialiser
    print("🔧 Initialisation...")
    db = DatabaseManager()
    scraper_manager = ScraperManager(db, auto_classify=True)
    
    # Charger les configurations
    fb_pages = load_config_file('facebook_pages.txt')
    tw_accounts = load_config_file('twitter_accounts.txt')
    
    # Initialiser le scraper Facebook
    fb_scraper = None
    if not args.skip_facebook:
        fb_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        if fb_token:
            fb_scraper = FacebookScraper(fb_token)
            if fb_scraper.test_connection():
                print("✅ Facebook API connectée")
            else:
                print("⚠️ Facebook API non accessible")
                fb_scraper = None
        else:
            print("⚠️ Token Facebook manquant")
    
    # Initialiser le scraper Twitter
    tw_scraper = None
    if not args.skip_twitter:
        tw_token = os.getenv('TWITTER_BEARER_TOKEN')
        if tw_token:
            tw_scraper = TwitterScraper(tw_token)
            if tw_scraper.test_connection():
                print("✅ Twitter API connectée")
            else:
                print("⚠️ Twitter API non accessible")
                tw_scraper = None
        else:
            print("⚠️ Bearer Token Twitter manquant")
    
    print()
    
    # Scraper un site spécifique
    if args.url:
        print("="*60)
        print(f"🎯 Scraping: {args.url}")
        print("="*60)
        
        # Scraping web
        count, method, message = scraper_manager.scrape_site(args.url, days=args.days)
        print(message)
        
        # Récupérer le média
        media = db.get_media_by_url(args.url)
        if media:
            # Scraping Facebook
            if fb_scraper and args.url in fb_pages:
                scrape_facebook_for_media(
                    db, fb_scraper, media.id, 
                    fb_pages[args.url], args.fb_posts
                )
            
            # Scraping Twitter
            if tw_scraper and args.url in tw_accounts:
                scrape_twitter_for_media(
                    db, tw_scraper, media.id,
                    tw_accounts[args.url], args.tweets
                )
    
    # Scraper tous les sites
    elif args.all:
        print("="*60)
        print("🚀 SCRAPING MULTI-SITES")
        print("="*60)
        
        # Lire sites.txt
        try:
            with open('sites.txt', 'r', encoding='utf-8') as f:
                sites = [line.strip() for line in f 
                        if line.strip() and not line.startswith('#')]
        except FileNotFoundError:
            print("❌ Fichier sites.txt non trouvé")
            return
        
        total_articles = 0
        
        for i, url in enumerate(sites, 1):
            print(f"\n[{i}/{len(sites)}] {url}")
            print("-"*60)
            
            # Scraping web
            count, method, message = scraper_manager.scrape_site(url, days=args.days)
            total_articles += count
            print(f"   {message}")
            
            # Récupérer le média
            media = db.get_media_by_url(url)
            if media:
                # Scraping Facebook
                if fb_scraper and url in fb_pages:
                    scrape_facebook_for_media(
                        db, fb_scraper, media.id,
                        fb_pages[url], args.fb_posts
                    )
                
                # Scraping Twitter
                if tw_scraper and url in tw_accounts:
                    scrape_twitter_for_media(
                        db, tw_scraper, media.id,
                        tw_accounts[url], args.tweets
                    )
        
        # Résumé
        print("\n" + "="*60)
        print("📊 RÉSUMÉ")
        print("="*60)
        print(f"✅ Total articles: {total_articles}")
        
        # Afficher le classement
        print("\n" + "="*60)
        print("🏆 CLASSEMENT DES MÉDIAS")
        print("="*60 + "\n")
        
        ranking = db.get_media_ranking_with_twitter(days=args.days)
        for i, media in enumerate(ranking[:5], 1):
            print(f"{i}. {media['nom']}")
            print(f"   Articles: {media['total_articles']}")
            if media['total_posts_facebook'] > 0:
                print(f"   Facebook: {media['engagement_total_fb']:,}")
            if media['total_tweets'] > 0:
                print(f"   Twitter: {media['engagement_total_tw']:,}")
            if media['engagement_total'] > 0:
                print(f"   Total: {media['engagement_total']:,}")
            print()
    
    else:
        print("❌ Spécifiez --url ou --all")
        print("💡 Exemples:")
        print("   python scrape_with_social.py --url https://www.aib.media")
        print("   python scrape_with_social.py --all")
        print("   python scrape_with_social.py --all --skip-facebook")


if __name__ == '__main__':
    main()
