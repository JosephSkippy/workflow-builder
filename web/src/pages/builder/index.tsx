import { Route, Routes } from "react-router-dom";
import BuilderPage from "./BuilderPage";

export default function BuilderRoutes() {
  return (
    <Routes>
      <Route index element={<BuilderPage />} />
      <Route path=":id" element={<BuilderPage />} />
    </Routes>
  );
}
