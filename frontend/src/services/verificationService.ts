import { apiClient } from './api';

export const verificationService = {
  getPatientIntakes: async () => {
    const response = await apiClient.get('/patient-intakes');
    return response.data;
  },
  getPatientIntakeById: async (id: string) => {
    const response = await apiClient.get(`/patient-intakes/${id}`);
    return response.data;
  },
  verifyPatientIntake: async (id: string, data?: Record<string, unknown>) => {
    const response = await apiClient.post(`/patient-intakes/${id}/verify`, data);
    return response.data;
  },
};
