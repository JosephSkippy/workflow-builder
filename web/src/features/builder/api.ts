import { api } from "@/lib/api";
import type { Workflow } from "./schema";

export interface WorkflowResponse {
  id: string;
  name: string;
  nodes: Workflow["nodes"];
}

export function saveWorkflow(id: string, body: Workflow) {
  return api.put<WorkflowResponse>(`/workflows/${id}`, body);
}
