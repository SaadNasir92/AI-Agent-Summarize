import React from 'react';
import { WorkflowProvider } from './WorkflowContext';
import WorkflowCanvas from './WorkflowCanvas';

function App() {
  return (
    <WorkflowProvider>
      <div style={{ display: 'flex', height: '100vh' }}>
        {/* Node Palette */}
        <div style={{ width: '20%', padding: '10px', borderRight: '1px solid #ccc' }}>
          <h3>Node Palette</h3>
          <div
            style={{ padding: '10px', margin: '5px', border: '1px solid #aaa', cursor: 'grab' }}
            draggable
            onDragStart={(event) => {
              event.dataTransfer.setData('application/reactflow', 'Connector');
            }}
          >
            Connector Node
          </div>
          <div
            style={{ padding: '10px', margin: '5px', border: '1px solid #aaa', cursor: 'grab' }}
            draggable
            onDragStart={(event) => {
              event.dataTransfer.setData('application/reactflow', 'Summarizer');
            }}
          >
            Summarizer Node
          </div>
          <div
            style={{ padding: '10px', margin: '5px', border: '1px solid #aaa', cursor: 'grab' }}
            draggable
            onDragStart={(event) => {
              event.dataTransfer.setData('application/reactflow', 'EmailNotifier');
            }}
          >
            Email Notifier Node
          </div>
        </div>

        {/* Workflow Canvas */}
        <div style={{ width: '80%' }}>
          <WorkflowCanvas />
        </div>
      </div>
    </WorkflowProvider>
  );
}

export default App;
