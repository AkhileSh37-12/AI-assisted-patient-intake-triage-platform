import { apiClient } from './api';

export const intakeService = {
  // Uses POST /process for text-based intake
  processIntake: async (data: { patient_input: string }) => {
    const response = await apiClient.post('/process', data);
    return response.data;
  },
  
  // Uses POST /voice-process for audio-based intake
  processVoiceIntake: async (audioFile: Blob) => {
    const formData = new FormData();
    formData.append('audio_file', audioFile, 'recording.webm');
    
    const response = await apiClient.post('/voice-process', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }
};
