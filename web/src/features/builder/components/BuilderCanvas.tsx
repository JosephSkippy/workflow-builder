import { Background, ReactFlow, type Edge, type Node } from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import React from "react";
import type { WorkflowNode } from "../schema";
import "./builder-canvas.css";
import { nodeTypes } from "./nodes";

type BuilderCanvasProps = {
  nodes: WorkflowNode[];
  selectedNodeId: string | null;
  onSelectNode: (id: string | null) => void;
  onReorder: (fromIndex: number, toIndex: number) => void;
  readonly?: boolean;
};

const START_NODE: Node = {
  id: "__start",
  type: "start",
  position: { x: 200, y: 0 },
  data: {},
  draggable: false,
  selectable: false,
};

function toFlowNodes(
  nodes: WorkflowNode[],
  selectedNodeId: string | null,
  readonly?: boolean,
): Node[] {
  const workflowNodes = nodes.map((n, i) => ({
    id: n.id,
    type: n.type,
    position: { x: 200, y: (i + 1) * 120 },
    data: { label: `${n.type} #${n.order}` },
    selected: !readonly && n.id === selectedNodeId,
    draggable: !readonly,
    selectable: !readonly,
  }));
  return [START_NODE, ...workflowNodes];
}

function toFlowEdges(nodes: WorkflowNode[]): Edge[] {
  const edges: Edge[] = [];
  if (nodes.length > 0) {
    edges.push({
      id: `e-start-${nodes[0].id}`,
      source: "__start",
      target: nodes[0].id,
    });
  }
  for (let i = 1; i < nodes.length; i++) {
    edges.push({
      id: `e-${nodes[i - 1].id}-${nodes[i].id}`,
      source: nodes[i - 1].id,
      target: nodes[i].id,
    });
  }
  return edges;
}

export default function BuilderCanvas({
  nodes,
  selectedNodeId,
  onSelectNode,
  onReorder,
  readonly,
}: BuilderCanvasProps) {
  const flowNodes = toFlowNodes(nodes, selectedNodeId, readonly);
  const flowEdges = toFlowEdges(nodes);

  const handleNodeDragStop = (_event: React.MouseEvent, draggedNode: Node) => {
    const draggedIndex = nodes.findIndex((n) => n.id === draggedNode.id);
    const targetIndex = Math.round((draggedNode.position.y - 120) / 120);
    const clampedTarget = Math.max(0, Math.min(nodes.length - 1, targetIndex));

    if (draggedIndex !== clampedTarget) {
      onReorder(draggedIndex, clampedTarget);
    }
  };

  return (
    <ReactFlow
      nodes={flowNodes}
      edges={flowEdges}
      nodeTypes={nodeTypes}
      onNodeClick={readonly ? undefined : (_, node) => onSelectNode(node.id)}
      onPaneClick={readonly ? undefined : () => onSelectNode(null)}
      onNodeDragStop={readonly ? undefined : handleNodeDragStop}
      nodesDraggable={!readonly}
      nodesConnectable={false}
      elementsSelectable={!readonly}
      fitView
    >
      <Background />
    </ReactFlow>
  );
}
