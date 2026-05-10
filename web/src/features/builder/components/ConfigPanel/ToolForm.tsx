import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { TOOLS } from "@/config/tools";
import type { ToolConfig, WorkflowNode } from "../../schema";
import { getAvailableVariables } from "../../variables";

type ToolFormProps = {
  node: WorkflowNode;
  nodes: WorkflowNode[];
  onUpdateConfig: (id: string, config: WorkflowNode["config"]) => void;
};

export default function ToolForm({
  node,
  nodes,
  onUpdateConfig,
}: ToolFormProps) {
  const config = node.config as ToolConfig;
  const selectedTool = TOOLS.find((t) => t.name === config.tool_name);
  const availableVars = getAvailableVariables(nodes, node.order);

  const handleToolChange = (toolName: string | null) => {
    if (!toolName) return;
    const tool = TOOLS.find((t) => t.name === toolName);
    const inputs: Record<string, string> = {};
    tool?.inputs.forEach((input) => {
      inputs[input.name] = config.inputs[input.name] ?? "";
    });
    onUpdateConfig(node.id, {
      ...config,
      tool_name: toolName,
      inputs,
      output_variable: `${toolName}_result`,
    });
  };

  return (
    <div className="p-4 flex flex-col gap-3">
      <h3 className="text-sm font-medium">Tool Node</h3>
      <Select value={config.tool_name} onValueChange={handleToolChange}>
        <SelectTrigger>
          <SelectValue placeholder="Select a tool..." />
        </SelectTrigger>
        <SelectContent>
          {TOOLS.map((tool) => (
            <SelectItem key={tool.name} value={tool.name}>
              {tool.name}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
      {selectedTool && (
        <div className="flex flex-col gap-2">
          <p className="text-xs text-muted-foreground">
            {selectedTool.description}
          </p>
          {selectedTool.inputs.map((input) => {
            const currentValue = config.inputs[input.name] ?? "";
            // Stored as "{{varname}}" — strip braces to match SelectItem values.
            const selectedVar = currentValue.replace(/^\{\{|\}\}$/g, "");
            return (
              <div key={input.name} className="flex flex-col gap-1">
                <Label className="text-xs">
                  {input.name}
                  {input.required && <span className="text-red-500"> *</span>}
                </Label>
                <Select
                  value={selectedVar}
                  onValueChange={(varName) =>
                    onUpdateConfig(node.id, {
                      ...config,
                      inputs: {
                        ...config.inputs,
                        [input.name]: `{{${varName}}}`,
                      },
                    })
                  }
                  disabled={availableVars.length === 0}
                >
                  <SelectTrigger>
                    {selectedVar ? (
                      <span className="font-mono text-sm">{`{{${selectedVar}}}`}</span>
                    ) : (
                      <SelectValue
                        placeholder={
                          availableVars.length === 0
                            ? "No variables available — add an input node above"
                            : "Select a variable..."
                        }
                      />
                    )}
                  </SelectTrigger>
                  <SelectContent>
                    {availableVars.map((v) => (
                      <SelectItem key={v} value={v}>
                        {`{{${v}}}`}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            );
          })}
        </div>
      )}
      {config.output_variable && (
        <div className="flex flex-col gap-1">
          <Label className="text-xs">Output variable</Label>
          <p className="text-sm text-muted-foreground">
            {`{{${config.output_variable}}}`}
          </p>
        </div>
      )}
    </div>
  );
}
