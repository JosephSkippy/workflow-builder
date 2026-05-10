import { useQuery } from "@tanstack/react-query";
import { fetchWorkflow } from "../api";

export function useWorkflow(workflowId: string) {
  return useQuery({
    queryKey: ["workflow", workflowId],
    queryFn: () => fetchWorkflow(workflowId),
  });
}
