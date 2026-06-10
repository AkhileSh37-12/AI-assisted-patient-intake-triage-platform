import React from 'react';
import { createBrowserRouter, Navigate } from 'react-router-dom';
import AppLayout from '../components/layout/AppLayout';
import PatientIntakePage from '../features/patient-intake/pages/PatientIntakePage';
import StaffVerificationPage from '../features/staff-verification/pages/StaffVerificationPage';
import QueueManagementPage from '../features/queue-management/pages/QueueManagementPage';
import ConsultationDashboardPage from '../features/consultation/pages/ConsultationDashboardPage';
import AnalyticsDashboardPage from '../features/analytics/pages/AnalyticsDashboardPage';
import MonitoringPage from '../features/monitoring/pages/MonitoringPage';

export const router = createBrowserRouter([
  {
    path: '/',
    // Redirect directly to queue dashboard, no login route
    element: <Navigate to="/app/queue" replace />,
  },
  {
    path: '/app',
    element: <AppLayout />,
    children: [
      {
        path: 'intake',
        element: <PatientIntakePage />,
      },
      {
        path: 'verification',
        element: <StaffVerificationPage />,
      },
      {
        path: 'queue',
        element: <QueueManagementPage />,
      },
      {
        path: 'consultation/:patientId?',
        element: <ConsultationDashboardPage />,
      },
      {
        path: 'analytics',
        element: <AnalyticsDashboardPage />,
      },
      {
        path: 'monitoring',
        element: <MonitoringPage />,
      },
    ],
  },
]);
