import React, { createContext, useState } from 'react';

export const WorkflowContext = createContext();

export const WorkflowProvider = ({ children }) => {
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);

  const addNode = (node) => {
    setNodes((nds) => [...nds, node]);
  };

  const updateNode = (nodeId, newData) => {
    setNodes((nds) =>
      nds.map((node) =>
        node.id === nodeId ? { ...node, data: { ...node.data, ...newData } } : node
      )
    );
  };

  const addEdge = (edge) => {
    setEdges((eds) => [...eds, edge]);
  };

  return (
    <WorkflowContext.Provider value={{ nodes, setNodes, edges, setEdges, addNode, updateNode, addEdge }}>
      {children}
    </WorkflowContext.Provider>
  );
};
