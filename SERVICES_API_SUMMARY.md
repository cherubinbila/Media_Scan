# 📡 Résumé des Services API Frontend

## ✅ Ce qui a été créé

### 📁 Structure complète dans `frontend/services/`

```
frontend/services/
├── api.config.ts              # Configuration API et endpoints
├── api.client.ts              # Client HTTP avec gestion d'erreurs
├── types.ts                   # Types TypeScript (15+ interfaces)
├── vite-env.d.ts             # Définitions TypeScript pour Vite
├── index.ts                   # Point d'entrée principal
│
├── media.service.ts           # Service médias
├── article.service.ts         # Service articles
├── classification.service.ts  # Service classifications
├── social.service.ts          # Service Facebook & Twitter
├── audience.service.ts        # Service analyse d'audience
├── ranking.service.ts         # Service classement
├── scraping.service.ts        # Service scraping
├── stats.service.ts           # Service statistiques
│
├── test-api.ts               # Tests de connexion API
├── README.md                 # Documentation complète
├── EXAMPLES.md               # Exemples d'utilisation React
└── INTEGRATION.md            # Guide d'intégration
```

### 📄 Fichiers de configuration

```
frontend/
├── .env.example              # Exemple de configuration
├── tsconfig.app.json         # Mis à jour pour inclure services/
└── src/vite-env.d.ts        # Mis à jour avec types Vite
```

## 🎯 Services disponibles

### 1. **mediaService** - Gestion des médias

```typescript
await mediaService.getAll(); // Tous les médias
await mediaService.getById(id); // Média par ID
```

### 2. **articleService** - Gestion des articles

```typescript
await articleService.getAll(params); // Tous les articles
await articleService.getByMedia(mediaId); // Articles d'un média
await articleService.getRecent(days, limit); // Articles récents
```

### 3. **classificationService** - Classifications

```typescript
await classificationService.getByCategory(categorie, limit);
await classificationService.getStats(days);
```

### 4. **socialService** - Réseaux sociaux

```typescript
await socialService.facebook.getPosts(mediaId, limit);
await socialService.twitter.getTweets(mediaId, limit);
```

### 5. **audienceService** - Analyse d'audience

```typescript
await audienceService.getWeb(days);
await audienceService.getFacebook(days);
await audienceService.getTwitter(days);
await audienceService.getGlobal(days);
await audienceService.getInactive(daysThreshold);
```

### 6. **rankingService** - Classement

```typescript
await rankingService.get(days);
```

### 7. **scrapingService** - Scraping

```typescript
await scrapingService.scrapeMedia(url, options);
await scrapingService.scrapeAll(options);
await scrapingService.trigger(request);
```

### 8. **statsService** - Statistiques

```typescript
await statsService.get(days);
await statsService.health();
```

## 🔧 Configuration requise

### 1. Créer le fichier `.env`

```bash
cd frontend
cp .env.example .env
```

Contenu :

```env
VITE_API_URL=http://localhost:8000
```

### 2. Vérifier le backend

Le backend Django doit être lancé :

```bash
cd backend/django_back
python manage.py runserver
```

## 🚀 Utilisation rapide

### Import des services

```typescript
import {
  mediaService,
  articleService,
  rankingService,
  Media,
  Article,
} from "@/services";
```

### Exemple basique

```typescript
// Récupérer tous les médias
const { data, error } = await mediaService.getAll();

if (error) {
  console.error("Erreur:", error);
} else {
  console.log("Médias:", data);
}
```

### Exemple avec React

```typescript
import { useState, useEffect } from "react";
import { mediaService, Media } from "@/services";

function MediaList() {
  const [medias, setMedias] = useState<Media[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetch() {
      const { data } = await mediaService.getAll();
      if (data) setMedias(data);
      setLoading(false);
    }
    fetch();
  }, []);

  if (loading) return <div>Chargement...</div>;

  return (
    <ul>
      {medias.map((media) => (
        <li key={media.id}>{media.nom}</li>
      ))}
    </ul>
  );
}
```

## 🧪 Tests

### Test automatique de tous les services

```typescript
import { testApi } from "@/services";

// Dans la console du navigateur ou dans votre code
await testApi();
```

### Tests individuels

```typescript
import { tests } from "@/services";

await tests.health(); // Test health check
await tests.medias(); // Test médias
await tests.articles(); // Test articles
await tests.ranking(); // Test classement
await tests.audience(); // Test audience
await tests.stats(); // Test statistiques
```

## 📊 Types TypeScript disponibles

Tous les types sont fortement typés :

- `Media` - Informations média
- `Article` - Article de presse
- `Classification` - Classification thématique
- `FacebookPost` - Post Facebook
- `Tweet` - Tweet
- `AudienceWeb` - Audience web
- `AudienceFacebook` - Audience Facebook
- `AudienceTwitter` - Audience Twitter
- `AudienceGlobal` - Audience globale
- `Ranking` - Classement média
- `Stats` - Statistiques globales
- `ScrapingRequest` / `ScrapingResponse`
- `HealthCheck` - État de l'API

## 🔄 Gestion des réponses

Toutes les méthodes retournent un objet `ApiResponse<T>` :

```typescript
interface ApiResponse<T> {
  data?: T; // Données si succès
  error?: string; // Message d'erreur si échec
  status: number; // Code HTTP
}
```

## 📚 Documentation

- **README.md** - Documentation complète des services
- **EXAMPLES.md** - Exemples d'utilisation avec React (hooks, composants)
- **INTEGRATION.md** - Guide d'intégration pas à pas
- **Backend API** - `backend/django_back/API_ENDPOINTS.md`

## 🎯 Prochaines étapes recommandées

1. **Créer les hooks personnalisés** dans `src/hooks/`

   - `useMedias()` - Pour les médias
   - `useRanking()` - Pour le classement
   - `useAudience()` - Pour l'audience
   - `useStats()` - Pour les statistiques

2. **Créer les composants UI** dans `src/components/`

   - Dashboard principal
   - Liste des médias
   - Classement
   - Graphiques d'audience
   - Formulaire de scraping

3. **Tester la connexion**

   ```typescript
   import { testApi } from "@/services";
   await testApi();
   ```

4. **Implémenter la gestion d'erreurs**

   - ErrorBoundary
   - Toast notifications
   - Retry logic

5. **Optimiser les performances**
   - Cache avec React Query
   - Lazy loading
   - Pagination

## ✅ Checklist de validation

- [ ] Fichier `.env` créé avec `VITE_API_URL`
- [ ] Backend Django lancé sur `http://localhost:8000`
- [ ] Test de connexion réussi avec `testApi()`
- [ ] Imports des services fonctionnent
- [ ] Types TypeScript reconnus
- [ ] Pas d'erreurs de compilation

## 🔗 Endpoints API disponibles

Tous les endpoints Django sont accessibles via les services :

- `/api/health/` - Health check
- `/api/medias/` - Liste des médias
- `/api/articles/` - Liste des articles
- `/api/classifications/` - Classifications
- `/api/facebook/posts/` - Posts Facebook
- `/api/twitter/tweets/` - Tweets
- `/api/audience/web/` - Audience web
- `/api/audience/facebook/` - Audience Facebook
- `/api/audience/twitter/` - Audience Twitter
- `/api/audience/global/` - Audience globale
- `/api/ranking/` - Classement
- `/api/scraping/trigger/` - Déclencher scraping
- `/api/stats/` - Statistiques

## 🎉 Résultat

Vous disposez maintenant d'une **couche complète de services API** pour communiquer avec le backend Django, avec :

✅ **8 services** modulaires et typés  
✅ **15+ types TypeScript** pour la sécurité du code  
✅ **Gestion d'erreurs** robuste  
✅ **Documentation complète** avec exemples  
✅ **Tests** intégrés  
✅ **Configuration** flexible via `.env`

**Tout est prêt pour l'intégration dans votre application React !** 🚀
