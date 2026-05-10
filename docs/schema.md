# Schema

Reflects current code (`backend/app/workflows/`, `backend/app/executions/`).

> **Note:** the `train` table (`backend/app/tools/subway_db_query/models.py`) is reference data for the Toronto Subway tool, not part of the core builder/execution schema. Omitted here — can be removed from any schema discussion.

## `workflows` table

| Field        | Type     | Consumed by                                                |
| ------------ | -------- | ---------------------------------------------------------- |
| `id`         | str (uuid) | URL key on builder + execution pages, click target on landing |
| `name`       | str      | Landing list row, builder name field                       |
| `nodes_json` | text     | Builder canvas, execution Node Viewer, executor at run time |
| `created_at` | datetime | Sort key for landing list                                  |

`nodes_json` is a JSON blob of `WorkflowNode[]`:

| Field    | Type                                       | Consumed by                                  |
| -------- | ------------------------------------------ | -------------------------------------------- |
| `id`     | str (uuid, client-generated)               | React key on canvas, selected-node tracking  |
| `type`   | `"input" \| "tool" \| "prompt"`            | Renders correct config form, dispatches handler |
| `order`  | int (1-indexed)                            | Canvas vertical position, executor sequence  |
| `config` | `InputConfig \| ToolConfig \| PromptConfig` | Configurator form, executor at run time      |

`config` shapes:

| Type     | Fields                                                        | Consumed by                                                  |
| -------- | ------------------------------------------------------------- | ------------------------------------------------------------ |
| `input`  | `variables: [{ name, value }]`                                | Seeds variable scope at execution start                      |
| `tool`   | `tool_name: str`, `inputs: dict[str, str]`, `output_variable: str` | Executor resolves `{{var}}` in inputs, calls tool, stores result under `output_variable` |
| `prompt` | `template: str`                                               | Executor resolves `{{var}}` in template, calls LLM           |

## `execution` table

| Field        | Type     | Consumed by                                                  |
| ------------ | -------- | ------------------------------------------------------------ |
| `id`         | str      | URL key for `GET /executions/{id}`, click target on past-execution row |
| `workflow_id`| str (indexed) | Filter past executions by workflow                       |
| `status`     | str (`running`/`succeeded`/`failed`) | Polling loop terminator, status badge |
| `steps_json` | text     | Result panel, expanded past-execution detail                 |
| `created_at` | datetime | "run_at" column on past-execution row, sort key              |
| `updated_at` | datetime | (currently unused on UI — auto-bumped on writes)             |

`steps_json` is a JSON blob of `StepResult[]`:

| Field       | Type | Consumed by                                |
| ----------- | ---- | ------------------------------------------ |
| `node_id`   | str  | Match step back to source node in viewer   |
| `node_type` | str  | Render step output in the right format     |
| `output`    | any  | Result panel + step expand                 |
