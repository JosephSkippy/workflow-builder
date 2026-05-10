import { Button } from "@/components/ui/button";
import type { NodeType } from "../schema";

type NodePaletteProps = {
  onAdd: (type: NodeType) => void;
};

export default function NodePalette({ onAdd }: NodePaletteProps) {
  return (
    <div className="flex flex-col gap-3 p-4">
      <h3 className="text-sm font-medium text-muted-foreground">Nodes</h3>
      <Button
        variant="outline"
        className="w-12 h-12 rounded-full bg-blue-100 border-blue-300"
        onClick={() => onAdd("input")}
      >
        In
      </Button>
      <Button
        variant="outline"
        className="w-12 h-12 bg-green-100 border-green-300"
        style={{ clipPath: "polygon(50% 0%, 0% 100%, 100% 100%)" }}
        onClick={() => onAdd("tool")}
      >
        Tool
      </Button>
      <Button
        variant="outline"
        className="w-12 h-12 bg-purple-100 border-purple-300"
        onClick={() => onAdd("prompt")}
      >
        Pr
      </Button>
    </div>
  );
}
