export const TOOLS = [
  {
    name: "query_subway_db",
    description: "Query Toronto subway delay records by station",
    inputs: [{ name: "station", type: "string", required: true }],
  },
  {
    name: "calculate_average_delay",
    description: "Calculate average delay in minutes for a station",
    inputs: [{ name: "station", type: "string", required: true }],
  },
] as const;
