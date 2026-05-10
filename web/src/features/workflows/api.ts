import { api } from "@/lib/api";
import {
  workflowListSchema,
  workflowSummarySchema,
  type WorkflowSummary,
} from "./schema";

export type { WorkflowSummary };

export async function fetchWorkflows() {
  const res = await api.get("/workflows/");
  return workflowListSchema.parse(res.data);
}

export async function fetchWorkflow(workflowId: string) {
  const res = await api.get(`/workflows/${workflowId}`);
  return workflowSummarySchema.parse(res.data);
}
