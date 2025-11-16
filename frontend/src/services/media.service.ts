/**
 * Service pour la gestion des médias
 */

import { apiClient, ApiResponse } from './api.client';
import { API_ENDPOINTS } from './api.config';
import { Media } from './types';

export const mediaService = {
  /**
   * Récupérer tous les médias
   */
  async getAll(): Promise<ApiResponse<Media[]>> {
    return apiClient.get<Media[]>(API_ENDPOINTS.MEDIAS);
  },

  /**
   * Récupérer un média par son ID
   */
  async getById(id: number): Promise<ApiResponse<Media>> {
    return apiClient.get<Media>(API_ENDPOINTS.MEDIA_DETAIL(id));
  },
};
