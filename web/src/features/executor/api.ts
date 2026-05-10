import { api } from "@/lib/api";
import {
  executionResponseSchema,
  executionStartedSchema,
  executionSummarySchema,
  type ExecutionResponse,
  type ExecutionStarted,
  type ExecutionSummary,
} from "./schema";

export type { ExecutionResponse, ExecutionStarted, ExecutionSummary };

export async function startExecution(workflowId: string) {
  const res = await api.post(`/executions/${workflowId}`);
  return executionStartedSchema.parse(res.data);
}

export async function getExecution(executionId: string) {
  const res = await api.get(`/executions/${executionId}`);
  return executionResponseSchema.parse(res.data);
}

export async function listExecutions(workflowId: string) {
  const res = await api.get(`/executions/workflow/${workflowId}`);
  return executionSummarySchema.array().parse(res.data);
}
