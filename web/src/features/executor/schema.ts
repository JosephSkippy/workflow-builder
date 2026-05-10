import { z } from "zod/v4";

export const stepResultSchema = z.object({
  node_id: z.string(),
  node_type: z.string(),
  output: z.string(),
});

export type StepResult = z.infer<typeof stepResultSchema>;

export const executionStartedSchema = z.object({
  execution_id: z.string(),
  status: z.string(),
});

export type ExecutionStarted = z.infer<typeof executionStartedSchema>;

export const executionResponseSchema = z.object({
  execution_id: z.string(),
  workflow_id: z.string(),
  status: z.string(),
  steps: z.array(stepResultSchema),
});

export type ExecutionResponse = z.infer<typeof executionResponseSchema>;

export const executionSummarySchema = z.object({
  execution_id: z.string(),
  status: z.string(),
  created_at: z.string(),
});

export type ExecutionSummary = z.infer<typeof executionSummarySchema>;
