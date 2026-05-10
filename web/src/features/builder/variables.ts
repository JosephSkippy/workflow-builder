import type { WorkflowNode } from "./schema";

/**
 * Returns variable names available to a node at the given order position.
 * Pulls from preceding input nodes' variables and earlier tool nodes' output_variable.
 */
export function getAvailableVariables(
  nodes: WorkflowNode[],
  currentOrder: number,
): string[] {
  const names: string[] = [];
  for (const node of nodes) {
    if (node.order >= currentOrder) continue;
    if (node.type === "input") {
      const config = node.config as { variables: { name: string }[] };
      for (const v of config.variables) {
        if (v.name) names.push(v.name);
      }
    } else if (node.type === "tool") {
      const config = node.config as { output_variable: string };
      if (config.output_variable) names.push(config.output_variable);
    }
  }
  return names;
}
