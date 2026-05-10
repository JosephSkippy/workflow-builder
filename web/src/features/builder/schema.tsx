import { z } from "zod/v4";

export const nodeType = z.enum(["input", "tool", "prompt"]);
export type NodeType = z.infer<typeof nodeType>;

const inputVariable = z.object({
  name: z.string().min(1, "Variable name is required"),
  value: z.string().min(1, "Value is required"),
});

const inputConfig = z.object({
  variables: z.array(inputVariable).min(1, "At least one variable is required"),
});

const toolConfig = z.object({
  tool_name: z.string().min(1, "Tool name is required"),
  inputs: z.record(z.string(), z.string()),
  output_variable: z.string().min(1, "Output variable is required"),
});

const promptConfig = z.object({
  template: z.string().min(1, "Template is required"),
});

export const workflowNodeSchema = z.object({
  id: z.string(),
  type: nodeType,
  order: z.number().int().positive(),
  config: z.union([inputConfig, toolConfig, promptConfig]),
});

export type WorkflowNode = z.infer<typeof workflowNodeSchema>;

export const workflowSchema = z.object({
  name: z.string().min(1, "Workflow name is required"),
  nodes: z.array(workflowNodeSchema).min(1, "At least one node is required"),
});

export type Workflow = z.infer<typeof workflowSchema>;

// Per-type config types for convenience
export type InputVariable = z.infer<typeof inputVariable>;
export type InputConfig = z.infer<typeof inputConfig>;
export type ToolConfig = z.infer<typeof toolConfig>;
export type PromptConfig = z.infer<typeof promptConfig>;
