# 🔑 Comment obtenir un Token Facebook valide

## ⚠️ Problème actuel
Le token dans votre `.env` est un **App Token** (858322950071403|...), mais nous avons besoin d'un **User Access Token**.

## ✅ Solution : Obtenir un User Access Token

### Méthode 1 : Graph API Explorer (Recommandé pour les tests)

1. **Allez sur** : https://developers.facebook.com/tools/explorer/

2. **Sélectionnez votre application** dans le menu déroulant en haut

3. **Cliquez sur "Get Token"** → **"Get User Access Token"**

4. **Cochez les permissions suivantes** :
   - ✅ `pages_read_engagement`
   - ✅ `pages_show_list`
   - ✅ `pages_read_user_content`
   - ✅ `public_profile`

5. **Cliquez sur "Generate Access Token"**

6. **Acceptez les permissions**

7. **Copiez le token** affiché (commence par EAA...)

8. **Collez-le dans votre `.env`** :
   ```
   FACEBOOK_ACCESS_TOKEN=EAAxxxxxxxxxxxxxxxxxxxx
   ```

### Méthode 2 : Token longue durée (60 jours)

Une fois que vous avez un token court :

1. Allez sur : https://developers.facebook.com/tools/debug/accesstoken/

2. Collez votre token court

3. Cliquez sur **"Extend Access Token"**

4. Copiez le nouveau token longue durée

## 🧪 Tester le token

```powershell
# Dans PowerShell
cd C:\Users\DarkSide\Desktop\Media_Scanne\backend\django_back

# Tester
python test_facebook.py
```

## ⚠️ Limitations importantes

### Token d'application vs Token utilisateur

| Type | Format | Utilisation |
|------|--------|-------------|
| **App Token** | `APP_ID\|APP_SECRET` | API publiques uniquement |
| **User Token** | `EAAxxxxxxxxx...` | Accès aux pages, posts, etc. |

**Vous avez actuellement** : App Token ❌  
**Vous avez besoin de** : User Token ✅

### Permissions requises

Pour scraper les posts Facebook publics, vous devez avoir :

1. ✅ **pages_read_engagement** : Lire l'engagement (likes, commentaires, partages)
2. ✅ **pages_show_list** : Lister les pages
3. ✅ **pages_read_user_content** : Lire le contenu des pages

## 🔒 Sécurité

- ⚠️ Ne partagez JAMAIS votre User Access Token
- 🔄 Les tokens courts expirent en 1-2 heures
- 📅 Les tokens longs expirent en 60 jours
- 🔐 Ajoutez `.env` dans `.gitignore` (déjà fait)

## 📝 Format du fichier .env

```bash
# Token utilisateur Facebook (commence par EAA...)
FACEBOOK_ACCESS_TOKEN=EAAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## ❓ Problèmes courants

### "Invalid OAuth access token"
→ Le token a expiré ou est invalide. Générez-en un nouveau.

### "Permissions error"
→ Vous n'avez pas les bonnes permissions. Régénérez avec toutes les permissions listées.

### "Page not found"
→ Vérifiez le nom de la page dans `facebook_pages.txt`

## 🎯 Une fois le token configuré

```powershell
# Tester avec AIB
python test_facebook.py

# Scraper AIB (web + Facebook)
python scrape_with_facebook.py --url https://www.aib.media

# Voir le classement
python show_ranking.py
```

## 💡 Astuce

Pour vérifier votre token actuel :

```powershell
python -c "import os; from dotenv import load_dotenv; load_dotenv(); token = os.getenv('FACEBOOK_ACCESS_TOKEN'); print('Type:', 'App Token' if '|' in token else 'User Token', '\nToken:', token[:30] + '...')"
```

---

**Prochaine étape** : Obtenez un User Access Token et testez ! 🚀
