import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { useSaveWorkflow } from "../hooks/useSaveWorkflow";
import { workflowSchema, type WorkflowNode } from "../schema";

type SaveButtonProps = {
  workflowId: string;
  workflowName: string;
  nodes: WorkflowNode[];
};

export default function SaveButton({
  workflowId,
  workflowName,
  nodes,
}: SaveButtonProps) {
  const { mutate, isPending } = useSaveWorkflow(workflowId);

  function handleSave() {
    const result = workflowSchema.safeParse({ name: workflowName, nodes });
    if (!result.success) {
      toast.error(result.error.issues[0].message);
      return;
    }
    mutate(result.data);
  }

  return (
    <Button size="sm" onClick={handleSave} disabled={isPending}>
      {isPending ? "Saving..." : "Save"}
    </Button>
  );
}
