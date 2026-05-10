import {
  BuilderCanvas,
  ConfigPanel,
  NodePalette,
  SaveButton,
  useWorkflowNodes,
} from "@/features/builder";
import { useCallback, useEffect, useMemo } from "react";

export default function BuilderPage() {
  const workflowId = useMemo(() => crypto.randomUUID(), []);
  const {
    nodes,
    selectedNodeId,
    workflowName,
    setWorkflowName,
    addNode,
    removeNode,
    selectNode,
    reorderNodes,
    updateNodeConfig,
  } = useWorkflowNodes();
  const selectedNode = nodes.find((n) => n.id === selectedNodeId);

  const handleKeyDown = useCallback(
    (e: KeyboardEvent) => {
      if (!selectedNodeId) return;
      const tag = (e.target as HTMLElement).tagName;
      if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return;
      if (e.key === "Delete" || e.key === "Backspace") {
        e.preventDefault();
        removeNode(selectedNodeId);
      }
    },
    [selectedNodeId, removeNode],
  );

  useEffect(() => {
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [handleKeyDown]);

  return (
    <div className="h-screen flex flex-col">
      <div className="flex items-center gap-2 p-2 border-b">
        <input
          type="text"
          value={workflowName}
          onChange={(e) => setWorkflowName(e.target.value)}
          placeholder="Rename Workflow"
          className="text-sm font-medium bg-transparent border-none outline-none w-48 placeholder:text-muted-foreground"
        />
        <div className="ml-auto flex items-center gap-2">
          <SaveButton
            workflowId={workflowId}
            workflowName={workflowName}
            nodes={nodes}
          />
        </div>
      </div>

      <div className="flex items-center gap-4 px-4 py-1.5 border-b bg-muted/50 text-xs text-muted-foreground">
        <span>Add node: click sidebar</span>
        <span>·</span>
        <span>Select node: click on it</span>
        <span>·</span>
        <span>Delete node: select + press Delete</span>
        <span>·</span>
        <span>Reorder: drag vertically</span>
      </div>

      <div className="flex flex-1 min-h-0">
        <aside className="w-20 border-r">
          <NodePalette onAdd={addNode} />
        </aside>
        <main className="flex-1">
          <BuilderCanvas
            nodes={nodes}
            selectedNodeId={selectedNodeId}
            onSelectNode={selectNode}
            onReorder={reorderNodes}
          />
        </main>
        <aside className="w-80 border-l">
          <ConfigPanel
            node={selectedNode}
            nodes={nodes}
            onUpdateConfig={updateNodeConfig}
          />
        </aside>
      </div>
    </div>
  );
}
