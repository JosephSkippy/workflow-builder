import type { PromptConfig, WorkflowNode } from "../../schema";
import { getAvailableVariables } from "../../variables";

type PromptFormProps = {
  node: WorkflowNode;
  nodes: WorkflowNode[];
  onUpdateConfig: (id: string, config: WorkflowNode["config"]) => void;
};

export default function PromptForm({
  node,
  nodes,
  onUpdateConfig,
}: PromptFormProps) {
  const config = node.config as PromptConfig;
  const availableVars = getAvailableVariables(nodes, node.order);

  return (
    <div className="p-4 flex flex-col gap-3">
      <h3 className="text-sm font-medium">Prompt Node</h3>
      {availableVars.length > 0 && (
        <div className="text-xs text-muted-foreground">
          Available variables:{" "}
          {availableVars.map((v) => (
            <code
              key={v}
              className="mx-0.5 px-1 py-0.5 rounded bg-muted text-foreground"
            >
              {`{{${v}}}`}
            </code>
          ))}
        </div>
      )}
      <textarea
        className="border rounded px-2 py-1 text-sm min-h-[120px]"
        placeholder="Enter prompt template... use {{variable}} for references"
        value={config.template}
        onChange={(e) =>
          onUpdateConfig(node.id, { ...config, template: e.target.value })
        }
      />
    </div>
  );
}
