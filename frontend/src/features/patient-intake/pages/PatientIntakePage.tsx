import React, { useState, useEffect, useRef } from 'react';
import { Typography, Card, Button, Input, Space, Descriptions, message, Row, Col, Tag, Spin, Alert, Badge, Collapse } from 'antd';
import { 
  AudioOutlined, 
  AudioMutedOutlined, 
  PlayCircleOutlined, 
  StopOutlined, 
  RobotOutlined, 
  CheckCircleOutlined 
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { intakeService } from '../../../services/intakeService';

const { Title, Text } = Typography;
const { TextArea } = Input;

// Define exact response interface mapped from FastAPI backend
interface ProcessResponse {
  transcript?: string;
  intake?: {
    full_name?: string;
    age?: number | string;
    gender?: string;
    phone_number?: string;
    symptoms?: string | string[];
  };
  triage?: {
    urgency_level?: string;
    confidence_score?: number;
    safety_override?: boolean;
    safety_reason?: string;
  };
  routing?: {
    suggested_department?: string;
    assigned_doctor?: string;
  };
  rag_context?: {
    retrieved_documents?: unknown;
    specialty?: string;
  };
  verification_status?: {
    staff_verified?: boolean;
    status?: string;
  };
}

// Define the SpeechRecognition types for TypeScript
declare global {
  interface Window {
    SpeechRecognition: unknown;
    webkitSpeechRecognition: unknown;
  }
}

const PatientIntakePage: React.FC = () => {
  const navigate = useNavigate();
  const [isRecording, setIsRecording] = useState(false);
  const [liveTranscript, setLiveTranscript] = useState('');
  const [manualEntry, setManualEntry] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [processedData, setProcessedData] = useState<ProcessResponse | null>(null);
  
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const recognitionRef = useRef<any>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  useEffect(() => {
    // TODO: Browser transcription will eventually be removed in favor of exclusive backend Faster Whisper processing.
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.lang = 'en-US';

      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      recognition.onresult = (event: any) => {
        let finalTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; ++i) {
          if (event.results[i].isFinal) {
            finalTranscript += event.results[i][0].transcript;
          }
        }
        if (finalTranscript) {
          setLiveTranscript((prev) => (prev ? prev + ' ' : '') + finalTranscript);
        }
      };

      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      recognition.onerror = (event: any) => {
        console.error('Speech recognition error', event.error);
        message.error('Live speech recognition failed: ' + event.error);
      };

      recognitionRef.current = recognition;
    }
  }, []);

  const startVoiceWorkflow = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        await handleVoiceProcess(audioBlob);
      };

      mediaRecorder.start();
      // Start live transcription (optional helper)
      if (recognitionRef.current) {
        recognitionRef.current.start();
      }
      setIsRecording(true);
      setLiveTranscript('');
      setProcessedData(null);
    } catch (error) {
      console.error('Error accessing microphone:', error);
      message.error('Could not access microphone. Please check permissions.');
    }
  };

  const stopVoiceWorkflow = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
      setIsRecording(false);
      mediaRecorderRef.current.stream.getTracks().forEach((track: MediaStreamTrack) => track.stop());
    }
  };

  const handleVoiceProcess = async (audioBlob: Blob) => {
    setIsProcessing(true);
    try {
      // POST /voice-process expects multipart form with audio_file
      const response = await intakeService.processVoiceIntake(audioBlob);
      
      setProcessedData({
        ...response.result,
        transcript: response.transcript,
      });

      if (response.transcript) {
        setLiveTranscript(response.transcript);
      }
      message.success('Voice intake processed successfully');
    } catch (error) {
      console.error('Error processing voice intake:', error);
      message.error('Failed to process voice intake.');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleTextProcess = async () => {
    const query = manualEntry.trim();
    if (!query) {
      message.error('Please describe patient symptoms in the text area before processing.');
      return;
    }

    setIsProcessing(true);
    setProcessedData(null);
    try {
      // POST /process expects {"patient_input": "..."}
      const result = await intakeService.processIntake({ patient_input: query });
      setProcessedData(result);
      message.success('Manual text intake processed successfully');
    } catch (error) {
      console.error('Error processing text intake:', error);
      message.error('Failed to process text intake.');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleSendToVerification = () => {
    message.success('Routing to verification dashboard...');
    navigate('/app/verification');
  };

  const getUrgencyColor = (level?: string) => {
    if (!level) return 'default';
    const l = level.toLowerCase();
    if (l === 'critical') return 'red';
    if (l === 'high') return 'orange';
    if (l === 'medium') return 'blue';
    if (l === 'low') return 'green';
    return 'default';
  };

  const formatSymptoms = (symptoms: string | string[] | undefined) => {
    if (!symptoms) return 'N/A';
    if (Array.isArray(symptoms)) return symptoms.join(', ');
    return symptoms;
  };

  return (
    <div style={{ padding: '24px', width: '100%' }}>
      {/* Page Header */}
      <div style={{ marginBottom: 32 }}>
        <Title level={2} style={{ margin: 0, fontWeight: 600, color: '#1f2937' }}>Patient Intake</Title>
        <Text type="secondary" style={{ fontSize: 16 }}>AI-assisted voice and text patient intake</Text>
      </div>

      <Row gutter={[24, 24]}>
        {/* Voice Intake (Primary) */}
        <Col span={24}>
          <Card 
            title={<span style={{ fontSize: 18, fontWeight: 700, color: '#1890ff' }}>VOICE INTAKE (PRIMARY WORKFLOW)</span>} 
            bordered={false} 
            style={{ 
              borderRadius: 12, 
              boxShadow: '0 4px 6px -1px rgba(24, 144, 255, 0.1), 0 2px 4px -1px rgba(24, 144, 255, 0.06)',
              borderTop: '6px solid #1890ff'
            }}
          >
            <Row gutter={32} align="middle">
              <Col xs={24} md={8} style={{ textAlign: 'center' }}>
                <Button
                  type={isRecording ? 'primary' : 'default'}
                  danger={isRecording}
                  shape="circle"
                  icon={isRecording ? <AudioOutlined /> : <AudioMutedOutlined />}
                  style={{ width: 120, height: 120, fontSize: 48, boxShadow: isRecording ? '0 0 20px rgba(255, 77, 79, 0.6)' : 'none', transition: 'all 0.3s' }}
                  onClick={isRecording ? stopVoiceWorkflow : startVoiceWorkflow}
                />
                <div style={{ marginTop: 24 }}>
                  {isRecording ? (
                    <Badge status="processing" color="red" text={<Text strong type="danger" style={{ fontSize: 16 }}>Recording Audio...</Text>} />
                  ) : (
                    <Badge status="default" text={<Text type="secondary" style={{ fontSize: 16 }}>Ready</Text>} />
                  )}
                </div>
                <Space style={{ marginTop: 24 }}>
                  <Button 
                    type="primary" 
                    size="large"
                    icon={<PlayCircleOutlined />} 
                    onClick={startVoiceWorkflow}
                    disabled={isRecording}
                    style={{ borderRadius: 6 }}
                  >
                    Start Recording
                  </Button>
                  <Button 
                    danger 
                    size="large"
                    icon={<StopOutlined />} 
                    onClick={stopVoiceWorkflow}
                    disabled={!isRecording}
                    style={{ borderRadius: 6 }}
                  >
                    Stop Recording
                  </Button>
                </Space>
              </Col>
              
              <Col xs={24} md={16}>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 8, height: '100%' }}>
                  <Text strong style={{ color: '#4b5563', fontSize: 16 }}>Live Transcript Preview:</Text>
                  <TextArea
                    value={processedData?.transcript || liveTranscript}
                    readOnly
                    placeholder="Voice transcript will appear here..."
                    style={{ minHeight: 220, borderRadius: 8, fontSize: 16, padding: 16, backgroundColor: '#f9fafb' }}
                  />
                </div>
              </Col>
            </Row>
          </Card>
        </Col>

        {/* Text Intake (Secondary) */}
        <Col span={24}>
          <Collapse 
            style={{ backgroundColor: '#ffffff', borderRadius: 12, border: 'none', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05)' }}
            items={[
              {
                key: '1',
                label: <span style={{ fontWeight: 600, fontSize: 16, color: '#4b5563' }}>Manual Text Intake (Secondary Workflow)</span>,
                children: (
                  <Space direction="vertical" style={{ width: '100%' }} size="large">
                    <TextArea
                      value={manualEntry}
                      onChange={(e) => setManualEntry(e.target.value)}
                      placeholder="Describe patient symptoms, medical history, and concerns..."
                      style={{ minHeight: 150, borderRadius: 8, fontSize: 15, padding: 16 }}
                    />
                    <div style={{ textAlign: 'right' }}>
                      <Button 
                        type="primary" 
                        size="large" 
                        icon={<RobotOutlined />} 
                        onClick={handleTextProcess}
                        loading={isProcessing && !isRecording}
                        style={{ borderRadius: 6 }}
                      >
                        Process Text Intake
                      </Button>
                    </div>
                  </Space>
                )
              }
            ]}
          />
        </Col>
      </Row>

      {/* Loader for Processing */}
      {isProcessing && (
         <div style={{ textAlign: 'center', padding: 40, marginTop: 32 }}>
           <Spin size="large" tip="Processing AI Intake Analysis..." />
         </div>
      )}

      {/* AI Results Section - Separate Cards */}
      {processedData && !isProcessing && (
        <div style={{ marginTop: 48 }}>
          <div style={{ marginBottom: 24, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Title level={3} style={{ margin: 0, color: '#1f2937' }}>AI Intake Results</Title>
            <Button 
              type="primary" 
              size="large"
              icon={<CheckCircleOutlined />} 
              onClick={handleSendToVerification}
              style={{ borderRadius: 6, background: '#10b981', borderColor: '#10b981', padding: '0 32px' }}
            >
              Send To Verification
            </Button>
          </div>
          
          {processedData.triage?.safety_override && (
            <Alert
              message="Safety Override Activated"
              description={processedData.triage?.safety_reason ?? 'N/A'}
              type="error"
              showIcon
              style={{ marginBottom: 24, borderRadius: 8 }}
            />
          )}

          <Row gutter={[24, 24]}>
            {/* Patient Information */}
            <Col xs={24} lg={12} xl={6}>
              <Card title="Patient Information" bordered={false} style={{ height: '100%', borderRadius: 12, boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05)' }}>
                <Descriptions column={1} labelStyle={{ fontWeight: 600, color: '#4b5563' }}>
                  <Descriptions.Item label="Name">{processedData.intake?.full_name ?? 'N/A'}</Descriptions.Item>
                  <Descriptions.Item label="Age">{processedData.intake?.age ?? 'N/A'}</Descriptions.Item>
                  <Descriptions.Item label="Gender">{processedData.intake?.gender ?? 'N/A'}</Descriptions.Item>
                  <Descriptions.Item label="Phone">{processedData.intake?.phone_number ?? 'N/A'}</Descriptions.Item>
                </Descriptions>
              </Card>
            </Col>

            {/* AI Triage */}
            <Col xs={24} lg={12} xl={6}>
              <Card title="AI Triage" bordered={false} style={{ height: '100%', borderRadius: 12, boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05)' }}>
                <Descriptions column={1} labelStyle={{ fontWeight: 600, color: '#4b5563' }}>
                  <Descriptions.Item label="Urgency">
                    <Tag color={getUrgencyColor(processedData.triage?.urgency_level)} style={{ padding: '2px 8px', fontSize: 13 }}>
                      {processedData.triage?.urgency_level?.toUpperCase() ?? 'N/A'}
                    </Tag>
                  </Descriptions.Item>
                  <Descriptions.Item label="Confidence">{processedData.triage?.confidence_score ?? 'N/A'}</Descriptions.Item>
                  <Descriptions.Item label="Safety Override">
                    {processedData.triage?.safety_override ? <Tag color="red">YES</Tag> : <Tag color="green">NO</Tag>}
                  </Descriptions.Item>
                </Descriptions>
              </Card>
            </Col>

            {/* Routing */}
            <Col xs={24} lg={12} xl={6}>
              <Card title="Routing" bordered={false} style={{ height: '100%', borderRadius: 12, boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05)' }}>
                <Descriptions column={1} labelStyle={{ fontWeight: 600, color: '#4b5563' }}>
                  <Descriptions.Item label="Department">{processedData.routing?.suggested_department ?? 'N/A'}</Descriptions.Item>
                  <Descriptions.Item label="Assigned Doctor">{processedData.routing?.assigned_doctor ?? 'N/A'}</Descriptions.Item>
                </Descriptions>
              </Card>
            </Col>

            {/* Verification Status */}
            <Col xs={24} lg={12} xl={6}>
              <Card title="Verification Status" bordered={false} style={{ height: '100%', borderRadius: 12, boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05)' }}>
                <Descriptions column={1} labelStyle={{ fontWeight: 600, color: '#4b5563' }}>
                  <Descriptions.Item label="Staff Verified">
                    {processedData.verification_status?.staff_verified ? <Tag color="green">Verified</Tag> : <Tag color="warning">Pending</Tag>}
                  </Descriptions.Item>
                  <Descriptions.Item label="Status">{processedData.verification_status?.status ?? 'N/A'}</Descriptions.Item>
                </Descriptions>
              </Card>
            </Col>

            {/* Symptoms (Full Width or Half Width) */}
            <Col xs={24} lg={12}>
              <Card title="Symptoms" bordered={false} style={{ height: '100%', borderRadius: 12, boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05)' }}>
                <Text style={{ fontSize: 15 }}>{formatSymptoms(processedData.intake?.symptoms)}</Text>
              </Card>
            </Col>

            {/* RAG Context */}
            <Col xs={24} lg={12}>
              <Card title="RAG Context" bordered={false} style={{ height: '100%', borderRadius: 12, boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05)' }}>
                <Descriptions column={1} labelStyle={{ fontWeight: 600, color: '#4b5563' }}>
                  <Descriptions.Item label="Retrieved Documents">
                    {processedData.rag_context?.retrieved_documents 
                      ? (Array.isArray(processedData.rag_context.retrieved_documents) 
                          ? processedData.rag_context.retrieved_documents.length 
                          : JSON.stringify(processedData.rag_context.retrieved_documents))
                      : '0'}
                  </Descriptions.Item>
                  <Descriptions.Item label="Specialty">{processedData.rag_context?.specialty ?? 'N/A'}</Descriptions.Item>
                </Descriptions>
              </Card>
            </Col>
          </Row>
        </div>
      )}
    </div>
  );
};

export default PatientIntakePage;
