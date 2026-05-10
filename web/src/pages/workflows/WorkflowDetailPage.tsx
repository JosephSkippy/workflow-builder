import { Button } from "@/components/ui/button";
import { Spinner } from "@/components/ui/spinner";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { BuilderCanvas, NodeConfigView } from "@/features/builder";
import { workflowNodeSchema } from "@/features/builder/schema";
import { useExecuteWorkflow, useExecutionHistory } from "@/features/executor";
import { useWorkflow } from "@/features/workflows";
import { useNavigate, useParams } from "react-router-dom";

export default function WorkflowDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: workflow, isLoading: isLoadingWorkflow } = useWorkflow(id!);
  const { execute, isPending, result, selectExecution } = useExecuteWorkflow(
    id!,
  );
  const { data: executions, isLoading: isLoadingExecutions } =
    useExecutionHistory(id!);

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Workflow Execution</h1>
        <div className="flex items-center gap-2">
          <Button variant="outline" onClick={() => navigate("/")}>
            Back
          </Button>
          <Button onClick={() => execute()} disabled={isPending}>
            {isPending ? "Running..." : "Run"}
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6">
        {/* Left — Node Chain */}
        <div className="space-y-2">
          <h2 className="text-lg font-medium">Node Chain</h2>
          {isLoadingWorkflow && (
            <div className="flex justify-center py-4">
              <Spinner className="size-5" />
            </div>
          )}
          {workflow && (
            <div className="h-[500px] border rounded">
              <BuilderCanvas
                nodes={workflow.nodes.map((n) => workflowNodeSchema.parse(n))}
                selectedNodeId={null}
                onSelectNode={() => {}}
                onReorder={() => {}}
                readonly
              />
            </div>
          )}
        </div>

        {/* Right — Node Configurations */}
        <div className="space-y-2">
          <h2 className="text-lg font-medium">Node Configurations</h2>
          <div className="space-y-2 max-h-[500px] overflow-auto pr-1">
            {workflow?.nodes.map((n) => (
              <NodeConfigView key={n.id} node={workflowNodeSchema.parse(n)} />
            ))}
          </div>
        </div>
      </div>

      {/* Execution Results */}
      <div className="space-y-2">
        <h2 className="text-lg font-medium">
          Execution Results
          {result && (
            <span className="ml-2 text-sm text-muted-foreground">
              ({result.status})
            </span>
          )}
        </h2>
        {!result && (
          <p className="text-muted-foreground text-sm">
            Click Run or select a past execution.
          </p>
        )}
        {result &&
          result.steps.map((step) => (
            <div key={step.node_id} className="border rounded p-3 space-y-1">
              <div className="text-sm font-medium text-muted-foreground">
                [{step.node_type}] {step.node_id}
              </div>
              <pre className="text-sm bg-muted p-2 rounded overflow-auto max-h-48">
                {step.output}
              </pre>
            </div>
          ))}
      </div>

      {/* Bottom — Past Executions */}
      <div className="space-y-2">
        <h2 className="text-lg font-medium">Past Executions</h2>
        {isLoadingExecutions && (
          <div className="flex justify-center py-4">
            <Spinner className="size-5" />
          </div>
        )}
        {executions && executions.length === 0 && (
          <p className="text-muted-foreground text-sm">No executions yet.</p>
        )}
        {executions && executions.length > 0 && (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Execution ID</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Executed At</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {executions.map((e) => (
                <TableRow
                  key={e.execution_id}
                  onClick={() => selectExecution(e.execution_id)}
                  className="cursor-pointer"
                >
                  <TableCell className="font-mono text-xs">
                    {e.execution_id}
                  </TableCell>
                  <TableCell>{e.status}</TableCell>
                  <TableCell>
                    {new Date(e.created_at).toLocaleString()}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </div>
    </div>
  );
}
