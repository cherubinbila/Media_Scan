# 📱 Module Réseaux Sociaux - Facebook & Twitter/X

## 🎯 Objectif

Scraper les métriques d'engagement des médias burkinabè sur **Facebook** et **Twitter/X** pour mesurer leur influence réelle sur les réseaux sociaux.

## ✅ Fonctionnalités implémentées

### 1. Scraping Facebook ✅
- Récupération des derniers posts via Facebook Graph API
- Métriques : likes, commentaires, partages
- Sauvegarde en base de données
- Évite les doublons (mise à jour des métriques)

### 2. Scraping Twitter/X ✅
- Récupération des derniers tweets via Twitter API v2
- Métriques : retweets, replies, likes, quotes, impressions
- Sauvegarde en base de données
- Évite les doublons (mise à jour des métriques)

### 3. Classement unifié ✅
- Ranking par engagement total (Facebook + Twitter)
- Statistiques par média (articles + réseaux sociaux)
- Engagement moyen par post
- Top médias les plus influents

## 📁 Fichiers créés

```
backend/django_back/
├── scrapers/
│   ├── facebook_scraper.py          # Scraper Facebook API
│   └── twitter_scraper.py           # Scraper Twitter API v2
├── database/
│   └── schema.sql                   # Tables Facebook + Twitter (modifié)
│   └── db_manager.py                # Méthodes réseaux sociaux (modifié)
├── scrape_with_social.py            # Script principal Web + Facebook + Twitter
├── test_facebook.py                 # Test du scraper Facebook
├── test_twitter.py                  # Test du scraper Twitter
├── show_ranking.py                  # Afficher le classement
├── facebook_pages.txt               # Config pages Facebook
├── twitter_accounts.txt             # Config comptes Twitter
├── .env.example                     # Template variables d'environnement
├── GET_FACEBOOK_TOKEN.md            # Guide token Facebook
├── GET_TWITTER_TOKEN.md             # Guide token Twitter
└── SOCIAL_MEDIA_README.md           # Ce fichier
```

## 🚀 Configuration

### 1. Tokens API

#### Facebook (User Access Token)
```bash
# Voir GET_FACEBOOK_TOKEN.md pour les détails
FACEBOOK_ACCESS_TOKEN=EAAxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### Twitter (Bearer Token)
```bash
# Voir GET_TWITTER_TOKEN.md pour les détails
TWITTER_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAAxxxxxxxxxxxxxxxxx
```

### 2. Fichier .env

Créez un fichier `.env` avec vos tokens :

```bash
# Facebook
FACEBOOK_ACCESS_TOKEN=votre_token_facebook

# Twitter
TWITTER_BEARER_TOKEN=votre_token_twitter
```

### 3. Configuration des comptes

#### facebook_pages.txt
```
AIB|https://www.aib.media|aib.infos
Sidwaya|https://www.sidwaya.info|sidwayainfo
```

#### twitter_accounts.txt
```
AIB|https://www.aib.media|aibburkina
Sidwaya|https://www.sidwaya.info|sidwayainfo
```

## 🧪 Tests

### Test Facebook
```powershell
python test_facebook.py
```

### Test Twitter
```powershell
python test_twitter.py
```

## 📊 Utilisation

### Scraper un média spécifique

```powershell
# Web + Facebook + Twitter
python scrape_with_social.py --url https://www.aib.media

# Web + Facebook uniquement
python scrape_with_social.py --url https://www.aib.media --skip-twitter

# Web + Twitter uniquement
python scrape_with_social.py --url https://www.aib.media --skip-facebook
```

### Scraper tous les médias

```powershell
# Tous les réseaux
python scrape_with_social.py --all

# Personnaliser
python scrape_with_social.py --all --days 30 --fb-posts 10 --tweets 10
```

### Voir le classement

```powershell
# Classement sur 30 jours
python show_ranking.py

# Classement sur 7 jours
python show_ranking.py --days 7
```

## 📈 Métriques collectées

### Facebook
| Métrique | Description |
|----------|-------------|
| **Likes** | Réactions (👍❤️😂😮😢😡) |
| **Comments** | Nombre de commentaires |
| **Shares** | Nombre de partages |
| **Engagement** | Likes + Comments + Shares |

### Twitter
| Métrique | Description |
|----------|-------------|
| **Retweets** | Nombre de retweets |
| **Replies** | Nombre de réponses |
| **Likes** | Nombre de likes (❤️) |
| **Quotes** | Nombre de citations |
| **Impressions** | Nombre de vues (niveau payant) |
| **Engagement** | Retweets + Replies + Likes + Quotes |

## 📊 Structure de la base de données

### Table facebook_posts
```sql
- post_id (unique)
- media_id
- message
- url
- date_publication
- likes, comments, shares
- engagement_total
```

### Table twitter_tweets
```sql
- tweet_id (unique)
- media_id
- text
- url
- date_publication
- retweets, replies, likes, quotes, impressions
- engagement_total
```

### Table media_metrics
```sql
- total_articles
- total_posts_facebook, total_tweets
- engagement_total_fb, engagement_total_tw
- engagement_total (global)
- engagement_moyen
```

## ⚠️ Limitations

### Facebook API
- **Rate limiting** : ~200 requêtes/heure
- **Token expiration** : Tokens courts (1-2h), longs (60 jours)
- **Permissions** : Nécessite User Access Token
- **Données** : Uniquement posts publics

### Twitter API (Niveau Free)
- **1,500 tweets/mois** (~50/jour)
- **Rate limit** : 15 requêtes/15 minutes
- **Pas d'impressions** (niveau payant requis)
- **Données** : Uniquement tweets publics

## 💡 Bonnes pratiques

### Économiser les requêtes

1. **Limitez le nombre de posts** :
   ```powershell
   python scrape_with_social.py --all --fb-posts 5 --tweets 5
   ```

2. **Scrapez par batch** :
   ```powershell
   # Média 1
   python scrape_with_social.py --url https://www.aib.media
   
   # Attendre 15 minutes
   
   # Média 2
   python scrape_with_social.py --url https://www.sidwaya.info
   ```

3. **Utilisez le cache** : Les posts déjà scrapés sont mis à jour, pas recréés

### Planifier le scraping

Créez un script PowerShell pour automatiser :

```powershell
# scrape_daily.ps1
cd C:\Users\DarkSide\Desktop\Media_Scanne\backend\django_back
env\Scripts\activate
python scrape_with_social.py --all --fb-posts 5 --tweets 5
```

Ajoutez-le au Planificateur de tâches Windows pour exécution quotidienne.

## 📊 Exemple de sortie

```
🏆 CLASSEMENT DES MÉDIAS (30 derniers jours)
================================================================================

1. 📺 AIB
   ──────────────────────────────────────────────────────────────────────
   🌐 URL: https://www.aib.media
   📰 Articles: 38
   
   📘 Facebook:
   👍 Likes: 8,920
   💬 Commentaires: 542
   🔄 Partages: 1,680
   📊 Engagement: 11,142
   
   🐦 Twitter:
   🔄 Retweets: 1,234
   💬 Réponses: 456
   ❤️ Likes: 3,456
   💭 Citations: 123
   📊 Engagement: 5,269
   
   📈 TOTAL: 16,411 engagement
```

## 🔧 Dépannage

### Facebook : "Invalid OAuth access token"
→ Utilisez un **User Access Token** (EAA...), pas un App Token

### Twitter : "Unauthorized"
→ Vérifiez votre Bearer Token dans `.env`

### Twitter : "Rate limit exceeded"
→ Attendez 15 minutes ou réduisez le nombre de requêtes

### "User/Page not found"
→ Vérifiez les noms dans `facebook_pages.txt` et `twitter_accounts.txt`

## 🎯 Prochaines étapes

- [ ] Ajouter Instagram (si API disponible)
- [ ] Graphiques de tendances
- [ ] Analyse de sentiment des commentaires
- [ ] Export des rapports (PDF/Excel)
- [ ] Dashboard web interactif

## 📚 Documentation

- [Facebook Graph API](https://developers.facebook.com/docs/graph-api/)
- [Twitter API v2](https://developer.twitter.com/en/docs/twitter-api)
- [GET_FACEBOOK_TOKEN.md](./GET_FACEBOOK_TOKEN.md)
- [GET_TWITTER_TOKEN.md](./GET_TWITTER_TOKEN.md)

## ✅ Checklist de déploiement

- [ ] Tokens Facebook et Twitter configurés dans `.env`
- [ ] Pages Facebook ajoutées dans `facebook_pages.txt`
- [ ] Comptes Twitter ajoutés dans `twitter_accounts.txt`
- [ ] Base de données migrée (nouvelles tables)
- [ ] Tests Facebook et Twitter réussis
- [ ] Scraping complet fonctionnel
- [ ] Classement des médias affiché

## 🎉 Résultat

Le système peut maintenant :
- ✅ Scraper Facebook et Twitter
- ✅ Calculer l'engagement total multi-plateformes
- ✅ Classer les médias par influence réelle
- ✅ Comparer les performances sur différents réseaux
- ✅ Identifier les médias les plus impactants

**Le module réseaux sociaux est opérationnel ! 🚀**
