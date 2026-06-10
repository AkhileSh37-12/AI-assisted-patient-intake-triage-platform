import React from 'react';
import { Layout, Menu } from 'antd';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  UserAddOutlined,
  CheckCircleOutlined,
  UnorderedListOutlined,
  MedicineBoxOutlined,
  LineChartOutlined,
  DashboardOutlined,
} from '@ant-design/icons';

const { Sider } = Layout;

interface SidebarProps {
  collapsed: boolean;
}

const Sidebar: React.FC<SidebarProps> = ({ collapsed }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const menuItems = [
    {
      key: '/app/queue',
      icon: <UnorderedListOutlined />,
      label: 'Queue Management',
      onClick: () => navigate('/app/queue'),
    },
    {
      key: '/app/intake',
      icon: <UserAddOutlined />,
      label: 'Patient Intake',
      onClick: () => navigate('/app/intake'),
    },
    {
      key: '/app/consultation',
      icon: <MedicineBoxOutlined />,
      label: 'Consultation',
      onClick: () => navigate('/app/consultation'),
    },
    {
      key: '/app/verification',
      icon: <CheckCircleOutlined />,
      label: 'Staff Verification',
      onClick: () => navigate('/app/verification'),
    },
    {
      key: '/app/analytics',
      icon: <LineChartOutlined />,
      label: 'Analytics',
      onClick: () => navigate('/app/analytics'),
    },
    {
      key: '/app/monitoring',
      icon: <DashboardOutlined />,
      label: 'System Monitoring',
      onClick: () => navigate('/app/monitoring'),
    },
  ];

  const selectedKey = menuItems.find(item => location.pathname.startsWith(item.key))?.key || '/app/queue';

  return (
    <Sider trigger={null} collapsible collapsed={collapsed} theme="dark" width={250}>
      <div style={{ height: 32, margin: 16, background: 'rgba(255, 255, 255, 0.2)', borderRadius: 6 }} />
      <Menu
        theme="dark"
        mode="inline"
        selectedKeys={[selectedKey]}
        items={menuItems}
      />
    </Sider>
  );
};

export default Sidebar;
