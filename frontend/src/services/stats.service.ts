/**
 * Service pour les statistiques
 */

import { apiClient, ApiResponse } from './api.client';
import { API_ENDPOINTS } from './api.config';
import { Stats, HealthCheck } from './types';

export const statsService = {
  /**
   * Récupérer les statistiques globales
   */
  async get(days = 30): Promise<ApiResponse<Stats>> {
    return apiClient.get<Stats>(API_ENDPOINTS.STATS, { days });
  },

  /**
   * Vérifier l'état de santé de l'API
   */
  async health(): Promise<ApiResponse<HealthCheck>> {
    return apiClient.get<HealthCheck>(API_ENDPOINTS.HEALTH);
  },
};
