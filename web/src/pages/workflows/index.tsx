import { Route, Routes } from "react-router-dom";
import WorkflowDetailPage from "./WorkflowDetailPage";
import WorkflowListPage from "./WorkflowListPage";

export default function WorkflowRoutes() {
  return (
    <Routes>
      <Route index element={<WorkflowListPage />} />
      <Route path=":id" element={<WorkflowDetailPage />} />
    </Routes>
  );
}
