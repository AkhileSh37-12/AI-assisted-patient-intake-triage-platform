import React from 'react';
import { Typography, Row, Col, Card } from 'antd';

const { Title, Paragraph } = Typography;

const MonitoringPage: React.FC = () => {
  const aspireDashboardUrl = import.meta.env.VITE_ASPIRE_DASHBOARD_URL || '#';
  const logsUrl = import.meta.env.VITE_LOGS_URL || '#';
  const tracesUrl = import.meta.env.VITE_TRACES_URL || '#';
  const metricsUrl = import.meta.env.VITE_METRICS_URL || '#';

  return (
    <div>
      <Title level={2}>System Monitoring</Title>
      <Paragraph>Access external monitoring tools using the configurable URLs below.</Paragraph>
      <Row gutter={16} style={{ marginTop: 24 }}>
        <Col span={6}>
          <Card title="Aspire Dashboard" hoverable onClick={() => window.open(aspireDashboardUrl, '_blank')}>
            View orchestrator details.
          </Card>
        </Col>
        <Col span={6}>
          <Card title="Logs" hoverable onClick={() => window.open(logsUrl, '_blank')}>
            View system logs.
          </Card>
        </Col>
        <Col span={6}>
          <Card title="Traces" hoverable onClick={() => window.open(tracesUrl, '_blank')}>
            View distributed traces.
          </Card>
        </Col>
        <Col span={6}>
          <Card title="Metrics" hoverable onClick={() => window.open(metricsUrl, '_blank')}>
            View performance metrics.
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default MonitoringPage;
