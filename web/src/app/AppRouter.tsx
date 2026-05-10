import BuilderPage from "@/pages/builder/BuilderPage";
import WorkflowDetailPage from "@/pages/workflows/WorkflowDetailPage";
import WorkflowListPage from "@/pages/workflows/WorkflowListPage";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

const router = createBrowserRouter([
  {
    path: "/",
    element: <WorkflowListPage />,
  },
  {
    path: "/workflows/:id",
    element: <WorkflowDetailPage />,
  },
  {
    path: "/builder",
    element: <BuilderPage />,
  },
]);

export default function AppRouter() {
  return <RouterProvider router={router} />;
}
