import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import type { WorkflowSummary } from "../api";

type WorkflowTableProps = {
  workflows: WorkflowSummary[];
  onSelect: (id: string) => void;
};

export default function WorkflowTable({
  workflows,
  onSelect,
}: WorkflowTableProps) {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead className="text-center">Name</TableHead>
          <TableHead className="text-center">ID</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {workflows.map((w) => (
          <TableRow
            key={w.id}
            onClick={() => onSelect(w.id)}
            className="cursor-pointer"
          >
            <TableCell className="font-medium">{w.name}</TableCell>
            <TableCell className="text-muted-foreground text-xs font-mono text-center">
              {w.id}
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
