import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Plus, X } from "lucide-react";
import type { InputConfig, WorkflowNode } from "../../schema";

type InputFormProps = {
  node: WorkflowNode;
  onUpdateConfig: (id: string, config: WorkflowNode["config"]) => void;
};

export default function InputForm({ node, onUpdateConfig }: InputFormProps) {
  const config = node.config as InputConfig;

  const updateVariable = (
    index: number,
    patch: Partial<{ name: string; value: string }>,
  ) => {
    const updated = [...config.variables];
    updated[index] = { ...updated[index], ...patch };
    onUpdateConfig(node.id, { ...config, variables: updated });
  };

  const addVariable = () => {
    onUpdateConfig(node.id, {
      ...config,
      variables: [...config.variables, { name: "", value: "" }],
    });
  };

  const removeVariable = (index: number) => {
    onUpdateConfig(node.id, {
      ...config,
      variables: config.variables.filter((_, i) => i !== index),
    });
  };

  return (
    <div className="p-4 flex flex-col gap-3">
      <h3 className="text-sm font-medium">Input Node</h3>
      <div className="flex flex-col gap-2">
        {config.variables.map((v, i) => (
          <div key={i} className="flex flex-col gap-1 border rounded p-2">
            <div className="flex items-center justify-between">
              <Label className="text-xs text-muted-foreground">
                Variable {i + 1}
              </Label>
              <Button
                type="button"
                variant="ghost"
                size="icon"
                className="h-6 w-6"
                onClick={() => removeVariable(i)}
                disabled={config.variables.length === 1}
                aria-label="Remove variable"
              >
                <X className="h-3 w-3" />
              </Button>
            </div>
            <Input
              placeholder="name (e.g. station)"
              value={v.name}
              onChange={(e) => updateVariable(i, { name: e.target.value })}
            />
            <Input
              placeholder="value"
              value={v.value}
              onChange={(e) => updateVariable(i, { value: e.target.value })}
            />
          </div>
        ))}
      </div>
      <Button
        type="button"
        variant="outline"
        size="sm"
        onClick={addVariable}
        className="self-start"
      >
        <Plus className="h-4 w-4 mr-1" />
        Add variable
      </Button>
    </div>
  );
}
