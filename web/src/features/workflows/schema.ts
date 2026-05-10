import { z } from "zod/v4";

export const workflowSummarySchema = z.object({
  id: z.string(),
  name: z.string(),
  nodes: z.array(
    z.object({
      id: z.string(),
      type: z.string(),
      order: z.number(),
      config: z.unknown(),
    }),
  ),
});

export type WorkflowSummary = z.infer<typeof workflowSummarySchema>;

export const workflowListSchema = z.array(workflowSummarySchema);
