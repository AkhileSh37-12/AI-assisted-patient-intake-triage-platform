import React from 'react';
import { Layout, Button, Typography, Space, Avatar } from 'antd';
import { MenuFoldOutlined, MenuUnfoldOutlined, UserOutlined } from '@ant-design/icons';

const { Header } = Layout;
const { Title } = Typography;

interface AppHeaderProps {
  collapsed: boolean;
  setCollapsed: (collapsed: boolean) => void;
}

const AppHeader: React.FC<AppHeaderProps> = ({ collapsed, setCollapsed }) => {
  return (
    <Header style={{ padding: 0, background: '#fff', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <Button
          type="text"
          icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
          onClick={() => setCollapsed(!collapsed)}
          style={{ fontSize: '16px', width: 64, height: 64 }}
        />
        <Title level={4} style={{ margin: 0 }}>AI Triage Platform</Title>
      </div>
      <Space style={{ marginRight: 24 }}>
        <span style={{ marginRight: 8 }}>Hospital Admin</span>
        <Avatar icon={<UserOutlined />} />
      </Space>
    </Header>
  );
};

export default AppHeader;
