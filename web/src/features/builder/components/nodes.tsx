import { Handle, Position, type NodeProps } from "@xyflow/react";

export function InputNode({ data, selected }: NodeProps) {
  return (
    <div className="flex flex-col items-center">
      <Handle type="target" position={Position.Top} />
      <div
        className={`w-16 h-16 rounded-full bg-blue-100 border-2 flex items-center justify-center text-xs font-medium ${selected ? "border-blue-500" : "border-blue-300"}`}
      >
        {data.label as string}
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}

export function ToolNode({ data, selected }: NodeProps) {
  return (
    <div className="flex flex-col items-center">
      <Handle type="target" position={Position.Top} />
      <div
        className={`w-16 h-16 flex items-center justify-center text-xs font-medium ${selected ? "border-green-500" : "border-green-300"}`}
        style={{
          clipPath: "polygon(50% 0%, 0% 100%, 100% 100%)",
          backgroundColor: selected ? "#dcfce7" : "#f0fdf4",
          border: "none",
        }}
      >
        {data.label as string}
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}

export function PromptNode({ data, selected }: NodeProps) {
  return (
    <div className="flex flex-col items-center">
      <Handle type="target" position={Position.Top} />
      <div
        className={`w-16 h-16 bg-purple-100 border-2 flex items-center justify-center text-xs font-medium ${selected ? "border-purple-500" : "border-purple-300"}`}
      >
        {data.label as string}
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}

export function StartNode() {
  return (
    <div className="flex flex-col items-center">
      <div className="w-10 h-10 rounded-full bg-gray-800 border-2 border-gray-900 flex items-center justify-center text-xs font-medium text-white">
        Start
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}

export const nodeTypes = {
  start: StartNode,
  input: InputNode,
  tool: ToolNode,
  prompt: PromptNode,
};
