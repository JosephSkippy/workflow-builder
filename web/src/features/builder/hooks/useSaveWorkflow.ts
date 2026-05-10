import { useMutation } from "@tanstack/react-query";
import { AxiosError } from "axios";
import { useNavigate } from "react-router-dom";
import { toast } from "sonner";
import { saveWorkflow } from "../api";
import type { Workflow } from "../schema";

export function useSaveWorkflow(workflowId: string) {
  const navigate = useNavigate();

  return useMutation({
    mutationFn: (payload: Workflow) => saveWorkflow(workflowId, payload),
    onSuccess: () => {
      toast.success("Workflow saved");
      navigate(`/workflows/${workflowId}`);
    },
    onError: (error) => {
      let message = "Failed to save workflow";
      if (error instanceof AxiosError) {
        const detail = error.response?.data?.detail;
        if (typeof detail === "string") {
          message = detail;
        } else if (Array.isArray(detail)) {
          message = detail[0]?.msg ?? message;
        }
      }
      toast.error(message);
    },
  });
}
