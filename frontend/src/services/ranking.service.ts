/**
 * Service pour le classement des médias
 */

import { apiClient, ApiResponse } from './api.client';
import { API_ENDPOINTS } from './api.config';
import { Ranking } from './types';

export const rankingService = {
  /**
   * Récupérer le classement des médias par influence
   */
  async get(days = 30): Promise<ApiResponse<Ranking[]>> {
    return apiClient.get<Ranking[]>(API_ENDPOINTS.RANKING, { days });
  },
};
