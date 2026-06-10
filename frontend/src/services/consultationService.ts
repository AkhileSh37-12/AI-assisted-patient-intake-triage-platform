import { apiClient } from './api';

export const consultationService = {
  getConsultations: async () => {
    const response = await apiClient.get('/consultations');
    return response.data;
  },
  getConsultationById: async (id: string) => {
    const response = await apiClient.get(`/consultations/${id}`);
    return response.data;
  },
  createConsultation: async (data: Record<string, unknown>) => {
    const response = await apiClient.post('/consultations', data);
    return response.data;
  },
  updateConsultation: async (id: string, data: Record<string, unknown>) => {
    const response = await apiClient.put(`/consultations/${id}`, data);
    return response.data;
  },
};
