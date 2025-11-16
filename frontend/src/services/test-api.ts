/**
 * Script de test pour vérifier la connexion avec l'API
 * 
 * Pour l'utiliser dans la console du navigateur :
 * import { testApi } from '@/services/test-api';
 * testApi();
 */

import { statsService } from './stats.service';
import { mediaService } from './media.service';
import { articleService } from './article.service';
import { rankingService } from './ranking.service';
import { audienceService } from './audience.service';

export async function testApi() {
  console.log('🧪 Test de connexion à l\'API...\n');

  // Test 1: Health Check
  console.log('1️⃣ Test Health Check...');
  const health = await statsService.health();
  if (health.error) {
    console.error('❌ Health Check échoué:', health.error);
    console.log('⚠️  Assurez-vous que le backend est lancé sur http://localhost:8000\n');
    return;
  }
  console.log('✅ Health Check réussi:', health.data);
  console.log('');

  // Test 2: Récupération des médias
  console.log('2️⃣ Test récupération des médias...');
  const medias = await mediaService.getAll();
  if (medias.error) {
    console.error('❌ Erreur:', medias.error);
  } else {
    console.log(`✅ ${medias.data?.length || 0} médias récupérés`);
    if (medias.data && medias.data.length > 0) {
      console.log('Premier média:', medias.data[0]);
    }
  }
  console.log('');

  // Test 3: Récupération des articles
  console.log('3️⃣ Test récupération des articles...');
  const articles = await articleService.getRecent(7, 10);
  if (articles.error) {
    console.error('❌ Erreur:', articles.error);
  } else {
    console.log(`✅ ${articles.data?.length || 0} articles récupérés`);
    if (articles.data && articles.data.length > 0) {
      console.log('Premier article:', articles.data[0].titre);
    }
  }
  console.log('');

  // Test 4: Récupération du classement
  console.log('4️⃣ Test récupération du classement...');
  const ranking = await rankingService.get(30);
  if (ranking.error) {
    console.error('❌ Erreur:', ranking.error);
  } else {
    console.log(`✅ ${ranking.data?.length || 0} médias dans le classement`);
    if (ranking.data && ranking.data.length > 0) {
      console.log('Top 3:');
      ranking.data.slice(0, 3).forEach((media, index) => {
        console.log(`  ${index + 1}. ${media.nom} - ${media.engagement_total} engagements`);
      });
    }
  }
  console.log('');

  // Test 5: Récupération de l'audience
  console.log('5️⃣ Test récupération de l\'audience...');
  const audience = await audienceService.getGlobal(30);
  if (audience.error) {
    console.error('❌ Erreur:', audience.error);
  } else {
    console.log(`✅ ${audience.data?.length || 0} médias avec données d'audience`);
    if (audience.data && audience.data.length > 0) {
      const top = audience.data[0];
      console.log(`Top média: ${top.nom} - Score: ${top.score_influence.toFixed(2)}`);
    }
  }
  console.log('');

  // Test 6: Récupération des statistiques
  console.log('6️⃣ Test récupération des statistiques...');
  const stats = await statsService.get(30);
  if (stats.error) {
    console.error('❌ Erreur:', stats.error);
  } else {
    console.log('✅ Statistiques récupérées:');
    console.log(`  - Total médias: ${stats.data?.total_medias}`);
    console.log(`  - Total articles: ${stats.data?.total_articles}`);
    console.log(`  - Top média: ${stats.data?.top_media.nom}`);
  }
  console.log('');

  console.log('🎉 Tests terminés !');
}

// Test individuel pour chaque service
export const tests = {
  async health() {
    console.log('Test Health Check...');
    const result = await statsService.health();
    console.log(result.error ? '❌ Erreur:' : '✅ Succès:', result.data || result.error);
    return result;
  },

  async medias() {
    console.log('Test Médias...');
    const result = await mediaService.getAll();
    console.log(result.error ? '❌ Erreur:' : `✅ ${result.data?.length} médias`, result.data || result.error);
    return result;
  },

  async articles(days = 7, limit = 10) {
    console.log(`Test Articles (${days} jours, max ${limit})...`);
    const result = await articleService.getRecent(days, limit);
    console.log(result.error ? '❌ Erreur:' : `✅ ${result.data?.length} articles`, result.data || result.error);
    return result;
  },

  async ranking(days = 30) {
    console.log(`Test Classement (${days} jours)...`);
    const result = await rankingService.get(days);
    console.log(result.error ? '❌ Erreur:' : `✅ ${result.data?.length} médias`, result.data || result.error);
    return result;
  },

  async audience(days = 30) {
    console.log(`Test Audience (${days} jours)...`);
    const result = await audienceService.getGlobal(days);
    console.log(result.error ? '❌ Erreur:' : `✅ ${result.data?.length} médias`, result.data || result.error);
    return result;
  },

  async stats(days = 30) {
    console.log(`Test Statistiques (${days} jours)...`);
    const result = await statsService.get(days);
    console.log(result.error ? '❌ Erreur:' : '✅ Succès:', result.data || result.error);
    return result;
  },
};

// Export pour utilisation dans la console
if (typeof window !== 'undefined') {
  (window as any).testApi = testApi;
  (window as any).apiTests = tests;
}
