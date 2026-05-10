import { useState } from "react";
import type { NodeType, WorkflowNode } from "../schema";

export function useWorkflowNodes(initialNodes: WorkflowNode[] = []) {
  const [nodes, setNodes] = useState<WorkflowNode[]>(initialNodes);
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  const [workflowName, setWorkflowName] = useState("My Workflow");

  const addNode = (type: NodeType) => {
    const newNode: WorkflowNode = {
      id: crypto.randomUUID(),
      type,
      order: 0,
      config: getEmptyConfig(type),
    };
    setNodes((prev) => reindex([...prev, newNode]));
  };

  const removeNode = (id: string) => {
    setNodes((prev) => reindex(prev.filter((n) => n.id !== id)));
    setSelectedNodeId((prev) => (prev === id ? null : prev));
  };

  const reorderNodes = (fromIndex: number, toIndex: number) => {
    setNodes((prev) => {
      const updated = [...prev];
      const [moved] = updated.splice(fromIndex, 1);
      updated.splice(toIndex, 0, moved);
      return reindex(updated);
    });
  };

  const updateNodeConfig = (id: string, config: WorkflowNode["config"]) => {
    setNodes((prev) => prev.map((n) => (n.id === id ? { ...n, config } : n)));
  };

  const selectNode = (id: string | null) => {
    setSelectedNodeId(id);
  };

  return {
    nodes,
    selectedNodeId,
    workflowName,
    setWorkflowName,
    addNode,
    removeNode,
    reorderNodes,
    updateNodeConfig,
    selectNode,
  };
}

function reindex(nodes: WorkflowNode[]): WorkflowNode[] {
  return nodes.map((n, i) => ({ ...n, order: i + 1 }));
}

function getEmptyConfig(type: NodeType): WorkflowNode["config"] {
  switch (type) {
    case "input":
      return {
        variables: [{ name: "", value: "" }],
      };
    case "tool":
      return { tool_name: "", inputs: {}, output_variable: "" };
    case "prompt":
      return { template: "" };
  }
}
