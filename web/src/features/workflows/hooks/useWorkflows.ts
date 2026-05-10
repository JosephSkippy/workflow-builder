import { useQuery } from "@tanstack/react-query";
import { fetchWorkflows } from "../api";

export function useWorkflows() {
  return useQuery({
    queryKey: ["workflows"],
    queryFn: () => fetchWorkflows(),
  });
}
