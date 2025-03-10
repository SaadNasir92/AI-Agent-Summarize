// frontend/WorkflowCanvas.js
import React, { useContext, useCallback } from 'react';
import ReactFlow, { addEdge, MiniMap, Controls, Background } from 'react-flow-renderer';
import { WorkflowContext } from './WorkflowContext';

const WorkflowCanvas = () => {
  const { nodes, setNodes, edges, setEdges } = useContext(WorkflowContext);

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  const onDragOver = (event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  };

  const onDrop = (event) => {
    event.preventDefault();

    // Get the node type from the dropped element.
    const nodeType = event.dataTransfer.getData('application/reactflow');
    if (!nodeType) {
      return;
    }

    // Determine the drop position. In a production app you'd convert these using ReactFlow's transform.
    const dropX = event.nativeEvent.offsetX;
    const dropY = event.nativeEvent.offsetY;

    const newNode = {
      id: `${+new Date()}`, // simple unique id
      type: 'default',
      position: { x: dropX, y: dropY },
      data: { label: `${nodeType} Node`, nodeType },
    };

    setNodes((nds) => [...nds, newNode]);
  };

  return (
    <div style={{ height: '500px', border: '1px solid #ddd' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onConnect={onConnect}
        onDrop={onDrop}
        onDragOver={onDragOver}
        fitView
      >
        <MiniMap />
        <Controls />
        <Background />
      </ReactFlow>
    </div>
  );
};

export default WorkflowCanvas;
