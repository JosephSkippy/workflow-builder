import { useQuery } from "@tanstack/react-query";
import { listExecutions } from "../api";

export function useExecutionHistory(workflowId: string) {
  return useQuery({
    queryKey: ["executions", workflowId],
    queryFn: () => listExecutions(workflowId),
  });
}
