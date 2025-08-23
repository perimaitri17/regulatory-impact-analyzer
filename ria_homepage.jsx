import React, { useState, useEffect } from 'react';
import { Search, Filter, Bell, Settings, Home, Eye, Navigation, Database, Calendar, TrendingUp, FileText, AlertTriangle, CheckCircle, Clock, Users, BarChart3, MapPin, Activity, Shield, Beaker, Factory, DollarSign, ArrowRight, Target, Zap } from 'lucide-react';

const RIAMainApp = () => {
  const [currentPage, setCurrentPage] = useState('Home');
  const [notifications, setNotifications] = useState([]);
  const [globalState, setGlobalState] = useState({
    alerts: [],
    workflows: [],
    products: [],
    selectedAlert: null,
    selectedProduct: null,
    selectedWorkflow: null
  });

  // Initialize sample data
  useEffect(() => {
    setGlobalState(prev => ({
      ...prev,
      alerts: [
        {
          id: 'AL001',
          title: 'FDA: New Diabetes Labeling Requirements',
          priority: 'HIGH',
          source: 'FDA.gov',
          published: '2025-08-20',
          impact: 3,
          timeline: 30,
          priorityScore: 85,
          therapeuticArea: 'Endocrinology',
          status: 'Active',
          affectedProducts: ['DiabeSure', 'GlucoMax', 'InsulinPro'],
          regions: ['US'],
          type: 'Labeling Update',
          description: 'New mandatory labeling requirements for all diabetes medications including enhanced warnings and patient information.',
          workflowsCreated: ['WF001'],
          documentsRequired: ['Label Update', 'Risk Assessment', 'Variation Submission']
        },
        {
          id: 'AL002',
          title: 'EMA: Cardiovascular Risk Assessment Update',
          priority: 'MEDIUM',
          source: 'EMA.europa.eu',
          published: '2025-08-19',
          impact: 2,
          timeline: 60,
          priorityScore: 65,
          therapeuticArea: 'Cardiology',
          status: 'In Progress',
          affectedProducts: ['CardioX', 'HeartShield'],
          regions: ['EU', 'UK'],
          type: 'Safety Guideline',
          description: 'Updated guidelines for cardiovascular safety assessment in clinical trials and post-market surveillance.',
          workflowsCreated: ['WF002'],
          documentsRequired: ['Safety Update', 'Clinical Assessment']
        },
        {
          id: 'AL003',
          title: 'Health Canada: New Manufacturing Standards',
          priority: 'LOW',
          source: 'health-canada.gc.ca',
          published: '2025-08-18',
          impact: 1,
          timeline: 90,
          priorityScore: 35,
          therapeuticArea: 'Manufacturing',
          status: 'Under Review',
          affectedProducts: ['GeneTherapy-X'],
          regions: ['Canada'],
          type: 'Manufacturing Guideline',
          description: 'Updated manufacturing standards for gene therapy products.',
          workflowsCreated: [],
          documentsRequired: ['Manufacturing Assessment']
        }
      ],
      workflows: [
        {
          id: 'WF001',
          alertId: 'AL001',
          title: 'FDA Diabetes Labeling Implementation',
          priority: 'HIGH',
          timeline: 30,
          remainingDays: 25,
          currentPhase: 'dossier-preparation',
          progress: 45,
          affectedProducts: ['DiabeSure'],
          regions: ['US'],
          assignedTeam: ['Sarah Johnson', 'Mike Chen', 'Lisa Wang'],
          milestones: [
            { id: 'M1', phase: 'pre-submission', name: 'Impact Analysis', status: 'completed', dueDate: '2025-08-21', assignee: 'AI System' },
            { id: 'M2', phase: 'pre-submission', name: 'Product Identification', status: 'completed', dueDate: '2025-08-22', assignee: 'Sarah Johnson' },
            { id: 'M3', phase: 'dossier-preparation', name: 'Label Text Drafting', status: 'in-progress', dueDate: '2025-08-30', assignee: 'Mike Chen' },
            { id: 'M4', phase: 'dossier-preparation', name: 'Medical Review', status: 'pending', dueDate: '2025-09-05', assignee: 'Lisa Wang' },
            { id: 'M5', phase: 'submission-assembly', name: 'eCTD Assembly', status: 'pending', dueDate: '2025-09-15', assignee: 'Publishing Team' }
          ],
          impact: {
            documentsToUpdate: 3,
            estimatedEffort: '40-60 hours',
            riskLevel: 'High',
            complianceDate: '2025-09-20'
          }
        },
        {
          id: 'WF002',
          alertId: 'AL002',
          title: 'EMA Cardiovascular Safety Update',
          priority: 'MEDIUM',
          timeline: 60,
          remainingDays: 45,
          currentPhase: 'pre-submission',
          progress: 20,
          affectedProducts: ['CardioX'],
          regions: ['EU'],
          assignedTeam: ['Emma Davis', 'John Smith'],
          milestones: [
            { id: 'M6', phase: 'pre-submission', name: 'Guideline Review', status: 'in-progress', dueDate: '2025-08-28', assignee: 'Emma Davis' }
          ],
          impact: {
            documentsToUpdate: 2,
            estimatedEffort: '25-35 hours',
            riskLevel: 'Medium',
            complianceDate: '2025-10-15'
          }
        },
        {
          id: 'WF003',
          title: 'Quarterly Safety Report - Q3 2025',
          priority: 'MEDIUM',
          timeline: 15,
          remainingDays: 10,
          currentPhase: 'submission-assembly',
          progress: 80,
          affectedProducts: ['DiabeSure', 'CardioX'],
          regions: ['US', 'EU'],
          assignedTeam: ['Safety Team'],
          milestones: [],
          impact: {
            documentsToUpdate: 1,
            estimatedEffort: '5-10 hours',
            riskLevel: 'Low',
            complianceDate: '2025-09-02'
          }
        }
      ],
      products: [
        {
          id: 'PRD001',
          name: 'DiabeSure',
          category: 'Commercial',
          therapeuticArea: 'Endocrinology/Diabetes',
          lifecycle: 'pharmacovigilance',
          markets: ['US', 'EU', 'India', 'LATAM'],
          activeAlerts: ['AL001'],
          activeWorkflows: ['WF001'],
          submissions: {
            'US': { stage: 'post-approval', progress: 100, nextMilestone: 'Annual Safety Report', lastUpdate: '2025-08-15' },
            'EU': { stage: 'submission-assembly', progress: 80, nextMilestone: 'eCTD Submission', lastUpdate: '2025-08-10' }
          },
          recentApprovals: ['US: NDA Approved (Jun 2025)', 'India: Marketing Authorization (Jul 2025)'],
          variations: [
            { type: 'Safety Update Required', region: 'US', status: 'pending', priority: 'HIGH' },
            { type: 'CMC Variation', region: 'EU', status: 'in-progress', priority: 'MEDIUM' }
          ],
          complianceItems: [
            { type: 'Annual Safety Report', dueDate: '2025-09-15', status: 'on-track' },
            { type: 'Label Update', dueDate: '2025-09-20', status: 'at-risk' }
          ]
        },
        {
          id: 'PRD002',
          name: 'CardioX',
          category: 'Commercial',
          therapeuticArea: 'Cardiovascular',
          lifecycle: 'regulatory',
          markets: ['US', 'EU', 'Japan', 'Canada'],
          activeAlerts: ['AL002'],
          activeWorkflows: ['WF002'],
          submissions: {
            'US': { stage: 'approval-launch', progress: 100, nextMilestone: 'Post-Market Commitments', lastUpdate: '2025-08-01' },
            'EU': { stage: 'regulatory-review', progress: 75, nextMilestone: 'CHMP Opinion', lastUpdate: '2025-08-18' }
          },
          recentApprovals: ['US: NDA Approved (Aug 2025)'],
          variations: [
            { type: 'Manufacturing Site Change', region: 'EU', status: 'approved', priority: 'LOW' }
          ],
          complianceItems: [
            { type: 'Post-Marketing Study', dueDate: '2025-10-30', status: 'on-track' }
          ]
        }
      ]
    }));
  }, []);

  // Real-time notification system
  const addNotification = (message, type = 'info') => {
    const newNotification = {
      id: Date.now(),
      message,
      type,
      timestamp: new Date().toLocaleTimeString()
    };
    setNotifications(prev => [newNotification, ...prev.slice(0, 4)]);
  };

  // Cross-dashboard integration functions
  const createWorkflowFromAlert = (alertId) => {
    const alert = globalState.alerts.find(a => a.id === alertId);
    if (alert) {
      addNotification(`Workflow created for ${alert.title}`, 'success');
      setCurrentPage('RISE Guider');
    }
  };

  const viewProductImpact = (productId) => {
    setGlobalState(prev => ({ ...prev, selectedProduct: productId }));
    setCurrentPage('PRISM Keeper');
  };

  // Header Component
  const Header = () => (
    <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white p-4 shadow-lg">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="bg-blue-500 text-white px-3 py-1 rounded-full text-sm">
            Live: {globalState.workflows.length} Active Workflows
          </div>
        </div>
        <div className="flex items-center space-x-4">
          <div className="relative">
            <Bell className="w-6 h-6 cursor-pointer hover:text-blue-200" />
            {notifications.length > 0 && (
              <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                {notifications.length}
              </span>
            )}
          </div>
        </div>
      </div>
    </div>
  );

  // Sidebar Component
  const Sidebar = () => (
    <div className="bg-gray-900 text-white w-64 min-h-screen p-4">
      {/* Logo Section */}
      <div className="flex items-center space-x-3 mb-8 pb-4 border-b border-gray-700">
        <div className="bg-white text-blue-600 rounded-lg p-2">
          <Target className="w-6 h-6" />
        </div>
        <h1 className="text-2xl font-bold">RIA</h1>
      </div>

      <div className="space-y-2">
        {[
          { id: 'Home', name: 'Home', icon: Home },
          { id: 'RIA Detective', name: 'RIA Detective', icon: Eye },
          { id: 'RISE Guider', name: 'RISE Guider', icon: Navigation },
          { id: 'PRISM Keeper', name: 'PRISM Keeper', icon: Database }
        ].map((item) => (
          <button
            key={item.id}
            onClick={() => setCurrentPage(item.id)}
            className={`w-full text-left p-3 rounded-lg flex items-center space-x-3 transition-colors ${
              currentPage === item.id ? 'bg-blue-600' : 'hover:bg-gray-800'
            }`}
          >
            <item.icon className="w-5 h-5" />
            <span>{item.name}</span>
          </button>
        ))}
      </div>
      
      <div className="mt-8 pt-8 border-t border-gray-700">
        <h3 className="text-gray-400 text-sm font-medium mb-4">SYSTEM</h3>
        <div className="space-y-2">
          <button className="w-full text-left p-3 rounded-lg flex items-center space-x-3 hover:bg-gray-800">
            <Bell className="w-5 h-5" />
            <span>Notifications</span>
            {notifications.length > 0 && (
              <span className="bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center ml-auto">
                {notifications.length}
              </span>
            )}
          </button>
          <button className="w-full text-left p-3 rounded-lg flex items-center space-x-3 hover:bg-gray-800">
            <Settings className="w-5 h-5" />
            <span>Settings</span>
          </button>
        </div>
      </div>
    </div>
  );

  // Home Page with Integration Dashboard
  const HomePage = () => (
    <div className="p-6 space-y-8">
      {/* Main Header Section */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-700 text-white rounded-lg p-8 text-center">
        <h1 className="text-4xl font-bold mb-2">RIA - Regulatory Impact Analyzer</h1>
        <p className="text-xl text-blue-100">AI-Powered Regulatory Intelligence & Compliance Automation Platform</p>
      </div>

      {/* Key Statistics Dashboard */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow-lg p-6 border-l-4 border-red-500">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-2xl font-bold text-gray-800">
                {globalState.alerts.filter(a => a.priority === 'HIGH').length}
              </div>
              <div className="text-sm text-gray-600">High Priority Alerts</div>
            </div>
            <div className="bg-red-100 p-3 rounded-full">
              <AlertTriangle className="w-6 h-6 text-red-600" />
            </div>
          </div>
          <div className="mt-2 text-xs text-red-600">
            {globalState.alerts.filter(a => a.priority === 'HIGH' && a.timeline <= 30).length} due within 30 days
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-6 border-l-4 border-blue-500">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-2xl font-bold text-gray-800">
                {globalState.workflows.length}
              </div>
              <div className="text-sm text-gray-600">Active Workflows</div>
            </div>
            <div className="bg-blue-100 p-3 rounded-full">
              <Navigation className="w-6 h-6 text-blue-600" />
            </div>
          </div>
          <div className="mt-2 text-xs text-blue-600">
            {globalState.workflows.filter(w => w.remainingDays <= 15).length} due soon
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-6 border-l-4 border-green-500">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-2xl font-bold text-gray-800">
                {globalState.products.length}
              </div>
              <div className="text-sm text-gray-600">Products Monitored</div>
            </div>
            <div className="bg-green-100 p-3 rounded-full">
              <Database className="w-6 h-6 text-green-600" />
            </div>
          </div>
          <div className="mt-2 text-xs text-green-600">
            {globalState.products.reduce((sum, p) => sum + p.markets.length, 0)} markets covered
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-6 border-l-4 border-purple-500">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-2xl font-bold text-gray-800">
                {globalState.products.reduce((sum, p) => sum + p.complianceItems.filter(c => c.status === 'at-risk').length, 0)}
              </div>
              <div className="text-sm text-gray-600">At-Risk Items</div>
            </div>
            <div className="bg-purple-100 p-3 rounded-full">
              <Clock className="w-6 h-6 text-purple-600" />
            </div>
          </div>
          <div className="mt-2 text-xs text-purple-600">
            Compliance tracking active
          </div>
        </div>
      </div>

      {/* Integration Flow Visualization */}
      <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
        <h3 className="text-xl font-bold text-gray-800 mb-6 text-center">Integrated Workflow</h3>
        <div className="flex items-center justify-center space-x-4">
          <div className="text-center">
            <div className="bg-blue-100 p-4 rounded-lg border-2 border-blue-300">
              <Eye className="w-8 h-8 text-blue-600 mx-auto mb-2" />
              <div className="font-semibold text-blue-800">RIA Detects</div>
              <div className="text-sm text-blue-600">Regulatory Change</div>
            </div>
          </div>
          <ArrowRight className="text-gray-400 w-6 h-6" />
          <div className="text-center">
            <div className="bg-green-100 p-4 rounded-lg border-2 border-green-300">
              <Navigation className="w-8 h-8 text-green-600 mx-auto mb-2" />
              <div className="font-semibold text-green-800">RISE Creates</div>
              <div className="text-sm text-green-600">Workflow</div>
            </div>
          </div>
          <ArrowRight className="text-gray-400 w-6 h-6" />
          <div className="text-center">
            <div className="bg-purple-100 p-4 rounded-lg border-2 border-purple-300">
              <Database className="w-8 h-8 text-purple-600 mx-auto mb-2" />
              <div className="font-semibold text-purple-800">PRISM Updates</div>
              <div className="text-sm text-purple-600">Product Data</div>
            </div>
          </div>
        </div>
      </div>

      {/* Three Main Modules */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow-lg p-6 border-l-4 border-blue-500 hover:shadow-xl transition-shadow cursor-pointer"
             onClick={() => setCurrentPage('RIA Detective')}>
          <div className="flex items-center mb-4">
            <Eye className="w-8 h-8 text-blue-500 mr-3" />
            <h3 className="text-xl font-bold text-gray-800">RIA - The Detective</h3>
          </div>
          <p className="text-gray-600 mb-4">Regulatory Impact Analyzer - Monitors global regulatory changes, identifies impacts, and provides intelligent alerts</p>
          <div className="text-sm text-gray-500 space-y-1">
            <div>• Real-time regulatory monitoring</div>
            <div>• AI-powered impact analysis</div>
            <div>• Priority-based alerting system</div>
            <div>• Cross-reference with internal database</div>
          </div>
          <div className="mt-4 pt-4 border-t border-gray-100">
            <div className="flex justify-between text-sm">
              <span className="text-blue-600">Total Alerts: {globalState.alerts.length}</span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-6 border-l-4 border-green-500 hover:shadow-xl transition-shadow cursor-pointer"
             onClick={() => setCurrentPage('RISE Guider')}>
          <div className="flex items-center mb-4">
            <Navigation className="w-8 h-8 text-green-500 mr-3" />
            <h3 className="text-xl font-bold text-gray-800">RISE - The Guide</h3>
          </div>
          <p className="text-gray-600 mb-4">Regulatory Integration & Submission Engine - Manages workflows, tracks milestones, and guides submission processes</p>
          <div className="text-sm text-gray-500 space-y-1">
            <div>• Automated workflow creation</div>
            <div>• Milestone tracking & dependencies</div>
            <div>• Team collaboration tools</div>
            <div>• Timeline visualization</div>
          </div>
          <div className="mt-4 pt-4 border-t border-gray-100">
            <div className="flex justify-between text-sm">
              <span className="text-green-600 font-medium">Total Workflows: {globalState.workflows.length}</span>
              <span className="text-orange-600">Due Soon: {globalState.workflows.filter(w => w.remainingDays <= 15).length}</span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-6 border-l-4 border-purple-500 hover:shadow-xl transition-shadow cursor-pointer"
             onClick={() => setCurrentPage('PRISM Keeper')}>
          <div className="flex items-center mb-4">
            <Database className="w-8 h-8 text-purple-500 mr-3" />
            <h3 className="text-xl font-bold text-gray-800">PRISM - The Librarian</h3>
          </div>
          <p className="text-gray-600 mb-4">Product Regulatory Information & Submission Management - Central repository for all regulatory documents and product data</p>
          <div className="text-sm text-gray-500 space-y-1">
            <div>• Product portfolio management</div>
            <div>• Document version control</div>
            <div>• Compliance tracking</div>
            <div>• Approval & variation monitoring</div>
          </div>
          <div className="mt-4 pt-4 border-t border-gray-100">
            <div className="flex justify-between text-sm">
              <span className="text-purple-600 font-medium">Total Products: {globalState.products.length}</span>
              <span className="text-red-600">At Risk: {globalState.products.reduce((sum, p) => sum + p.complianceItems.filter(c => c.status === 'at-risk').length, 0)}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Activity & Critical Alerts with Integration Links */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
            <Activity className="w-6 h-6 text-blue-500 mr-2" />
            Recent Activity & Cross-Platform Impact
          </h3>
          <div className="space-y-4">
            {globalState.alerts.map((alert) => (
              <div key={alert.id} className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <div className="font-medium text-gray-800">{alert.title}</div>
                    <div className="text-sm text-gray-500">Source: {alert.source}</div>
                  </div>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    alert.priority === 'HIGH' ? 'bg-red-100 text-red-800' :
                    alert.priority === 'MEDIUM' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-green-100 text-green-800'
                  }`}>
                    {alert.priority}
                  </span>
                </div>
                
                <div className="text-sm text-gray-600 mb-3">
                  Affects: {alert.affectedProducts.join(', ')} • Regions: {alert.regions.join(', ')}
                </div>
                
                <div className="flex flex-wrap gap-2">
                  <button 
                    onClick={() => createWorkflowFromAlert(alert.id)}
                    className="bg-green-500 hover:bg-green-600 text-white px-3 py-1 rounded text-xs flex items-center"
                  >
                    <Zap className="w-3 h-3 mr-1" />
                    Create Workflow
                  </button>
                  <button 
                    onClick={() => viewProductImpact(alert.affectedProducts[0])}
                    className="bg-purple-500 hover:bg-purple-600 text-white px-3 py-1 rounded text-xs flex items-center"
                  >
                    <Database className="w-3 h-3 mr-1" />
                    View Products
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
            <AlertTriangle className="w-6 h-6 text-red-500 mr-2" />
            Critical Integration Points
          </h3>
          <div className="space-y-4">
            {globalState.products.map((product) => (
              <div key={product.id} className="border-l-4 border-red-500 pl-4 py-3 bg-red-50 rounded-r-lg">
                <div className="font-medium text-gray-800">{product.name}</div>
                <div className="text-sm text-gray-600 mt-1 space-y-1">
                  <div>Active Alerts: {product.activeAlerts.length}</div>
                  <div>Running Workflows: {product.activeWorkflows.length}</div>
                  <div>Compliance Items: {product.complianceItems.filter(c => c.status === 'at-risk').length} at risk</div>
                </div>
                <div className="mt-2 flex gap-2">
                  <button 
                    onClick={() => {setGlobalState(prev => ({...prev, selectedAlert: product.activeAlerts[0]})); setCurrentPage('RIA Detective');}}
                    className="text-blue-600 hover:text-blue-800 text-xs"
                  >
                    View Alert
                  </button>
                  <button 
                    onClick={() => {setGlobalState(prev => ({...prev, selectedWorkflow: product.activeWorkflows[0]})); setCurrentPage('RISE Guider');}}
                    className="text-green-600 hover:text-green-800 text-xs"
                  >
                    View Workflow
                  </button>
                  <button 
                    onClick={() => viewProductImpact(product.id)}
                    className="text-purple-600 hover:text-purple-800 text-xs"
                  >
                    View Product
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Notifications Panel */}
      {notifications.length > 0 && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Recent Notifications</h3>
          <div className="space-y-2">
            {notifications.map((notification) => (
              <div key={notification.id} className={`p-3 rounded-lg text-sm ${
                notification.type === 'success' ? 'bg-green-50 text-green-800 border border-green-200' :
                notification.type === 'warning' ? 'bg-yellow-50 text-yellow-800 border border-yellow-200' :
                notification.type === 'error' ? 'bg-red-50 text-red-800 border border-red-200' :
                'bg-blue-50 text-blue-800 border border-blue-200'
              }`}>
                <div className="flex justify-between items-center">
                  <span>{notification.message}</span>
                  <span className="text-xs opacity-70">{notification.timestamp}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );

  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar />
      
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        
        <main className="flex-1 overflow-y-auto">
          {currentPage === 'Home' && <HomePage />}
          {currentPage === 'RIA Detective' && (
            <div className="p-6">
              <div className="bg-yellow-100 border border-yellow-400 rounded-lg p-4 mb-4">
                <div className="text-yellow-800">RIA Detective page will be loaded here. This shows regulatory monitoring, alerts analysis, and impact assessment.</div>
              </div>
            </div>
          )}
          {currentPage === 'RISE Guider' && (
            <div className="p-6">
              <div className="bg-green-100 border border-green-400 rounded-lg p-4 mb-4">
                <div className="text-green-800">RISE Guider page will be loaded here. This shows workflow management, milestone tracking, and submission guidance.</div>
              </div>
            </div>
          )}
          {currentPage === 'PRISM Keeper' && (
            <div className="p-6">
              <div className="bg-purple-100 border border-purple-400 rounded-lg p-4 mb-4">
                <div className="text-purple-800">PRISM Keeper page will be loaded here. This shows product portfolio, document management, and compliance tracking.</div>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
};

export default RIAMainApp;
