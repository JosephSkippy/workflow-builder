import AppProvider from "./AppProvider";
import AppRouter from "./AppRouter";

function App() {
  return (
    <AppProvider>
      <AppRouter />
    </AppProvider>
  );
}

export default App;
