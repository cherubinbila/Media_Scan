# 🔑 Comment obtenir un Bearer Token Twitter/X

## 🎯 Objectif

Obtenir un **Bearer Token** pour accéder à l'API Twitter v2 et scraper les tweets des médias burkinabè.

## ✅ Étapes détaillées

### 1. Créer un compte développeur Twitter

1. **Allez sur** : https://developer.twitter.com/
2. **Cliquez sur "Sign up"** (ou connectez-vous si vous avez déjà un compte)
3. **Remplissez le formulaire** :
   - Nom
   - Email
   - Pays
   - Cas d'usage (sélectionnez "Exploring the API" ou "Academic research")
4. **Acceptez les conditions**
5. **Vérifiez votre email**

### 2. Créer un projet et une app

1. **Allez dans le Developer Portal** : https://developer.twitter.com/en/portal/dashboard
2. **Cliquez sur "Create Project"**
3. **Remplissez les informations** :
   - **Project name** : Media Scanner
   - **Use case** : Exploring the API
   - **Project description** : Scraping media tweets for analysis
4. **Créez une App** :
   - **App name** : media-scanner-app (doit être unique)
   - **App environment** : Development
5. **Cliquez sur "Complete"**

### 3. Obtenir le Bearer Token

1. **Dans le Dashboard**, sélectionnez votre app
2. **Allez dans "Keys and tokens"**
3. **Section "Bearer Token"** :
   - Cliquez sur **"Generate"** ou **"Regenerate"**
   - ⚠️ **COPIEZ LE TOKEN IMMÉDIATEMENT** (vous ne pourrez plus le voir après)
   - Le token ressemble à : `AAAAAAAAAAAAAAAAAAAAAxxxxxxxxxxxxxxxxxxxx...`

4. **Sauvegardez le token** dans votre `.env` :
   ```bash
   TWITTER_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAAxxxxxxxxxxxxxxxxxxxx...
   ```

### 4. Configurer les permissions (optionnel)

1. **Allez dans "User authentication settings"**
2. **Type of App** : Web App
3. **App permissions** :
   - ✅ Read (suffisant pour scraper)
4. **Callback URL** : http://localhost:3000 (si nécessaire)

## 📋 Niveaux d'accès Twitter API

| Niveau | Tweets/mois | Prix | Idéal pour |
|--------|-------------|------|------------|
| **Free** | 1,500 | Gratuit | Tests |
| **Basic** | 10,000 | $100/mois | Petits projets |
| **Pro** | 1,000,000 | $5,000/mois | Production |

**Pour ce projet** : Le niveau **Free** suffit pour tester avec quelques médias.

## 🧪 Tester le token

```powershell
# Dans PowerShell
cd C:\Users\DarkSide\Desktop\Media_Scanne\backend\django_back

# Ajouter le token dans .env
# Ouvrez .env et ajoutez :
# TWITTER_BEARER_TOKEN=votre_token_ici

# Tester
python test_twitter.py
```

## 📝 Format du fichier .env

```bash
# Facebook
FACEBOOK_ACCESS_TOKEN=EAAxxxxxxxxxxxxxxxxxxxxxxxxx

# Twitter
TWITTER_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAAxxxxxxxxxxxxxxxxxxxxxxxxx
```

## ⚠️ Limitations importantes

### API Twitter v2 - Niveau Free

- ✅ **1,500 tweets/mois** (environ 50 tweets/jour)
- ✅ **Lecture des tweets publics**
- ✅ **Métriques publiques** (likes, retweets, replies)
- ❌ **Pas d'impressions** (nécessite niveau payant)
- ❌ **Rate limit** : 15 requêtes/15 minutes

### Conseils pour économiser les requêtes

1. **Limitez le nombre de tweets** : 5-10 par média
2. **Scrapez 1-2 médias à la fois**
3. **Espacez les requêtes** (15 min entre chaque batch)
4. **Utilisez le cache** (évitez de rescraper les mêmes tweets)

## 🔒 Sécurité

- ⚠️ **Ne partagez JAMAIS** votre Bearer Token
- 🔄 **Régénérez le token** si compromis
- 📁 **Ajoutez `.env` dans `.gitignore`** (déjà fait)
- 🔐 **Ne commitez pas** le token dans Git

## ❓ Problèmes courants

### "Unauthorized" (401)
→ Le Bearer Token est invalide ou expiré. Régénérez-le.

### "Rate limit exceeded" (429)
→ Vous avez dépassé la limite de requêtes. Attendez 15 minutes.

### "User not found"
→ Le nom d'utilisateur Twitter est incorrect. Vérifiez dans `twitter_accounts.txt`.

### "Monthly cap exceeded"
→ Vous avez atteint la limite de 1,500 tweets/mois. Attendez le mois prochain ou passez au niveau Basic.

## 📊 Métriques disponibles

### Niveau Free
- ✅ Retweets
- ✅ Replies (réponses)
- ✅ Likes
- ✅ Quotes (citations)
- ❌ Impressions (vues)

### Niveau Basic/Pro
- ✅ Tout ce qui précède
- ✅ Impressions
- ✅ Engagement rate
- ✅ Video views

## 🎯 Une fois le token configuré

```powershell
# Tester avec AIB
python test_twitter.py

# Scraper AIB (web + Facebook + Twitter)
python scrape_with_social.py --url https://www.aib.media

# Voir le classement
python show_ranking.py
```

## 💡 Astuce

Pour vérifier votre token actuel :

```powershell
python -c "import os; from dotenv import load_dotenv; load_dotenv(); token = os.getenv('TWITTER_BEARER_TOKEN'); print('Token:', token[:30] + '...' if token else 'Non trouvé')"
```

## 📚 Ressources

- [Twitter API Documentation](https://developer.twitter.com/en/docs/twitter-api)
- [Rate Limits](https://developer.twitter.com/en/docs/twitter-api/rate-limits)
- [API v2 Endpoints](https://developer.twitter.com/en/docs/twitter-api/tweets/lookup/introduction)

---

**Prochaine étape** : Obtenez votre Bearer Token et testez ! 🚀
