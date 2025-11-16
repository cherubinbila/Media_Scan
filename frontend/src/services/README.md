# Services API - Frontend

Ce dossier contient tous les services pour communiquer avec le backend Django.

## 📁 Structure

```
services/
├── api.config.ts           # Configuration de l'API (URL, endpoints)
├── api.client.ts           # Client HTTP générique
├── types.ts                # Types TypeScript pour toutes les données
├── index.ts                # Point d'entrée principal
├── media.service.ts        # Service pour les médias
├── article.service.ts      # Service pour les articles
├── classification.service.ts # Service pour les classifications
├── social.service.ts       # Service pour Facebook & Twitter
├── audience.service.ts     # Service pour l'analyse d'audience
├── ranking.service.ts      # Service pour le classement
├── scraping.service.ts     # Service pour le scraping
└── stats.service.ts        # Service pour les statistiques
```

## 🚀 Utilisation

### Configuration

Créer un fichier `.env` à la racine du projet frontend :

```env
VITE_API_URL=http://localhost:8000
```

### Import des services

```typescript
import {
  mediaService,
  articleService,
  audienceService,
  rankingService,
  scrapingService,
  statsService,
} from "@/services";
```

### Exemples d'utilisation

#### 1. Récupérer tous les médias

```typescript
const { data, error } = await mediaService.getAll();

if (error) {
  console.error("Erreur:", error);
} else {
  console.log("Médias:", data);
}
```

#### 2. Récupérer les articles récents

```typescript
const { data, error } = await articleService.getRecent(7, 50);

if (data) {
  console.log(`${data.length} articles récents`);
}
```

#### 3. Récupérer l'audience globale

```typescript
const { data, error } = await audienceService.getGlobal(30);

if (data) {
  data.forEach((media) => {
    console.log(`${media.nom}: ${media.score_influence} points`);
  });
}
```

#### 4. Récupérer le classement

```typescript
const { data, error } = await rankingService.get(30);

if (data) {
  data.forEach((media, index) => {
    console.log(`#${index + 1} - ${media.nom}: ${media.engagement_total}`);
  });
}
```

#### 5. Déclencher un scraping

```typescript
const { data, error } = await scrapingService.scrapeMedia(
  "https://www.aib.media",
  {
    days: 30,
    fbPosts: 10,
    tweets: 10,
  }
);

if (data) {
  console.log(`Scraping terminé: ${data.total_articles} articles`);
}
```

#### 6. Récupérer les statistiques

```typescript
const { data, error } = await statsService.get(30);

if (data) {
  console.log(`Total médias: ${data.total_medias}`);
  console.log(`Total articles: ${data.total_articles}`);
  console.log(`Top média: ${data.top_media.nom}`);
}
```

#### 7. Vérifier la santé de l'API

```typescript
const { data, error } = await statsService.health();

if (data) {
  console.log(`API Status: ${data.status}`);
  console.log(`Database: ${data.database}`);
}
```

## 🔧 Utilisation dans React

### Avec useState et useEffect

```typescript
import { useState, useEffect } from "react";
import { mediaService, Media } from "@/services";

function MediaList() {
  const [medias, setMedias] = useState<Media[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchMedias() {
      const { data, error } = await mediaService.getAll();

      if (error) {
        setError(error);
      } else if (data) {
        setMedias(data);
      }

      setLoading(false);
    }

    fetchMedias();
  }, []);

  if (loading) return <div>Chargement...</div>;
  if (error) return <div>Erreur: {error}</div>;

  return (
    <ul>
      {medias.map((media) => (
        <li key={media.id}>{media.nom}</li>
      ))}
    </ul>
  );
}
```

### Avec un hook personnalisé

```typescript
// hooks/useMedias.ts
import { useState, useEffect } from "react";
import { mediaService, Media } from "@/services";

export function useMedias() {
  const [medias, setMedias] = useState<Media[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchMedias() {
      const { data, error } = await mediaService.getAll();

      if (error) {
        setError(error);
      } else if (data) {
        setMedias(data);
      }

      setLoading(false);
    }

    fetchMedias();
  }, []);

  return { medias, loading, error };
}

// Utilisation dans un composant
function MediaList() {
  const { medias, loading, error } = useMedias();

  if (loading) return <div>Chargement...</div>;
  if (error) return <div>Erreur: {error}</div>;

  return (
    <ul>
      {medias.map((media) => (
        <li key={media.id}>{media.nom}</li>
      ))}
    </ul>
  );
}
```

## 📊 Types disponibles

Tous les types sont exportés depuis `types.ts` :

- `Media` - Informations sur un média
- `Article` - Article de presse
- `Classification` - Classification thématique
- `FacebookPost` - Post Facebook
- `Tweet` - Tweet
- `AudienceWeb` - Audience web
- `AudienceFacebook` - Audience Facebook
- `AudienceTwitter` - Audience Twitter
- `AudienceGlobal` - Audience globale
- `Ranking` - Classement d'un média
- `Stats` - Statistiques globales
- `ScrapingRequest` - Requête de scraping
- `ScrapingResponse` - Réponse de scraping

## 🔄 Gestion des erreurs

Toutes les méthodes retournent un objet `ApiResponse<T>` :

```typescript
interface ApiResponse<T> {
  data?: T; // Données si succès
  error?: string; // Message d'erreur si échec
  status: number; // Code HTTP
}
```

Exemple de gestion d'erreur :

```typescript
const { data, error, status } = await mediaService.getAll();

if (error) {
  if (status === 0) {
    console.error("Impossible de contacter le serveur");
  } else if (status === 408) {
    console.error("Timeout de la requête");
  } else {
    console.error(`Erreur ${status}: ${error}`);
  }
} else {
  console.log("Données:", data);
}
```

## 🌐 Endpoints disponibles

Tous les endpoints sont définis dans `api.config.ts` :

- **Health**: `/api/health/`
- **Médias**: `/api/medias/`, `/api/medias/{id}/`
- **Articles**: `/api/articles/`
- **Classifications**: `/api/classifications/`, `/api/classifications/stats/`
- **Facebook**: `/api/facebook/posts/`
- **Twitter**: `/api/twitter/tweets/`
- **Audience**: `/api/audience/web/`, `/api/audience/facebook/`, etc.
- **Classement**: `/api/ranking/`
- **Scraping**: `/api/scraping/trigger/`
- **Statistiques**: `/api/stats/`

## 🔐 Sécurité

- Timeout de 30 secondes par défaut
- Gestion des erreurs réseau
- Validation des réponses
- Types TypeScript stricts

## 📝 Notes

- Tous les services sont asynchrones
- Les paramètres optionnels ont des valeurs par défaut
- Les dates sont au format ISO 8601
- L'API backend doit être lancée sur `http://localhost:8000`
