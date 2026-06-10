import { apiClient } from './api';

export const queueService = {
  getQueueEntries: async () => {
    const response = await apiClient.get('/queue-entries');
    return response.data;
  },
  callQueueEntry: async (id: string) => {
    const response = await apiClient.post(`/queue-entries/${id}/call`);
    return response.data;
  },
  startQueueEntry: async (id: string) => {
    const response = await apiClient.post(`/queue-entries/${id}/start`);
    return response.data;
  },
  completeQueueEntry: async (id: string) => {
    const response = await apiClient.post(`/queue-entries/${id}/complete`);
    return response.data;
  },
};
