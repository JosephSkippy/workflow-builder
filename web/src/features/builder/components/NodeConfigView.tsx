import type {
  InputConfig,
  PromptConfig,
  ToolConfig,
  WorkflowNode,
} from "../schema";

type NodeConfigViewProps = {
  node: WorkflowNode;
};

export default function NodeConfigView({ node }: NodeConfigViewProps) {
  return (
    <div className="border rounded p-3 space-y-2">
      <div className="text-sm font-medium text-muted-foreground">
        [{node.type}] #{node.order}
      </div>
      {node.type === "input" && <InputView config={node.config as InputConfig} />}
      {node.type === "tool" && <ToolView config={node.config as ToolConfig} />}
      {node.type === "prompt" && (
        <PromptView config={node.config as PromptConfig} />
      )}
    </div>
  );
}

function InputView({ config }: { config: InputConfig }) {
  return (
    <dl className="text-sm space-y-1">
      {config.variables.map((v, i) => (
        <div key={i} className="flex gap-2">
          <dt className="font-mono text-muted-foreground">{v.name}</dt>
          <dd className="font-mono">{v.value}</dd>
        </div>
      ))}
    </dl>
  );
}

function ToolView({ config }: { config: ToolConfig }) {
  return (
    <div className="text-sm space-y-1">
      <div>
        <span className="text-muted-foreground">tool: </span>
        <span className="font-mono">{config.tool_name}</span>
      </div>
      {Object.entries(config.inputs).length > 0 && (
        <dl className="space-y-0.5">
          {Object.entries(config.inputs).map(([k, v]) => (
            <div key={k} className="flex gap-2">
              <dt className="font-mono text-muted-foreground">{k}</dt>
              <dd className="font-mono">{v}</dd>
            </div>
          ))}
        </dl>
      )}
      <div>
        <span className="text-muted-foreground">output: </span>
        <span className="font-mono">{`{{${config.output_variable}}}`}</span>
      </div>
    </div>
  );
}

function PromptView({ config }: { config: PromptConfig }) {
  return (
    <pre className="text-sm bg-muted p-2 rounded whitespace-pre-wrap font-mono">
      {config.template}
    </pre>
  );
}
