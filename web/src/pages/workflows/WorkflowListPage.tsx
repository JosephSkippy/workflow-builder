import { Button } from "@/components/ui/button";
import { Spinner } from "@/components/ui/spinner";
import { useWorkflows } from "@/features/workflows";
import WorkflowTable from "@/features/workflows/components/WorkflowTable";
import { useNavigate } from "react-router-dom";

export default function WorkflowListPage() {
  const navigate = useNavigate();
  const { data: workflows, isLoading } = useWorkflows();

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-semibold">Workflows</h1>
        <Button onClick={() => navigate("/builder")}>Create Workflow</Button>
      </div>

      {isLoading && (
        <div className="flex justify-center py-12">
          <Spinner className="size-6" />
        </div>
      )}

      {workflows && workflows.length === 0 && (
        <p className="text-muted-foreground">No workflows yet.</p>
      )}

      {workflows && workflows.length > 0 && (
        <WorkflowTable
          workflows={workflows}
          onSelect={(id) => navigate(`/workflows/${id}`)}
        />
      )}
    </div>
  );
}
