import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import type { ReactNode } from "react";
import { Toaster } from "sonner";

type AppProviderProps = {
  children: ReactNode;
};

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
    },
  },
});

export default function AppProvider({ children }: AppProviderProps) {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <Toaster richColors />
    </QueryClientProvider>
  );
}
