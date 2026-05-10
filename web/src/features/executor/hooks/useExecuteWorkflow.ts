import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { AxiosError } from "axios";
import { useState } from "react";
import { toast } from "sonner";
import { getExecution, startExecution, type ExecutionResponse } from "../api";

export function useExecuteWorkflow(workflowId: string) {
  const queryClient = useQueryClient();
  const [executionId, setExecutionId] = useState<string | null>(null);

  const mutation = useMutation({
    mutationFn: () => startExecution(workflowId),
    onSuccess: (res) => {
      setExecutionId(res.execution_id);
      queryClient.invalidateQueries({ queryKey: ["executions", workflowId] });
      toast.success("Workflow execution started");
    },
    onError: (error) => {
      let message = "Execution failed";
      if (error instanceof AxiosError) {
        const detail = error.response?.data?.detail;
        if (typeof detail === "string") {
          message = detail;
        }
      }
      toast.error(message);
    },
  });

  const poll = useQuery({
    queryKey: ["execution", executionId],
    queryFn: () => getExecution(executionId!),
    enabled: !!executionId,
    refetchInterval: (query) => {
      const status = query.state.data?.status;
      if (status === "completed" || status === "failed") {
        queryClient.invalidateQueries({
          queryKey: ["executions", workflowId],
        });
        return false;
      }
      return 1000;
    },
  });

  return {
    execute: mutation.mutate,
    isPending: mutation.isPending,
    result: poll.data ?? null,
    selectExecution: setExecutionId,
  };
}

export type { ExecutionResponse };
