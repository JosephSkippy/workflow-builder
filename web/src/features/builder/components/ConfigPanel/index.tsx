import type { WorkflowNode } from "../../schema";
import InputForm from "./InputForm";
import PromptForm from "./PromptForm";
import ToolForm from "./ToolForm";

type ConfigPanelProps = {
  node: WorkflowNode | undefined;
  nodes: WorkflowNode[];
  onUpdateConfig: (id: string, config: WorkflowNode["config"]) => void;
};

export default function ConfigPanel({
  node,
  nodes,
  onUpdateConfig,
}: ConfigPanelProps) {
  if (!node) {
    return (
      <div className="p-4 text-sm text-muted-foreground">
        Click a node to configure it
      </div>
    );
  }

  switch (node.type) {
    case "input":
      return <InputForm node={node} onUpdateConfig={onUpdateConfig} />;
    case "tool":
      return (
        <ToolForm node={node} nodes={nodes} onUpdateConfig={onUpdateConfig} />
      );
    case "prompt":
      return (
        <PromptForm node={node} nodes={nodes} onUpdateConfig={onUpdateConfig} />
      );
  }
}
