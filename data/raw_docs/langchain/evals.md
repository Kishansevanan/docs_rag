---
title: Evaluate agent performance
---

To evaluate your agent's performance you can use [LangSmith evaluations](/langsmith/evaluation).
For evaluations, you must first define an evaluator function to judge the results from an agent, such as final outputs or trajectory. Depending on your evaluation technique, this may or may not involve a reference output.


Run evaluations in LangSmith with datasets and LLM-as-judge evaluators. See the [evaluation quickstart](/langsmith/evaluation-quickstart) to get started.


:::python
```python
def evaluator(*, outputs: dict, reference_outputs: dict):
    # compare agent outputs against reference outputs
    output_messages = outputs["messages"]
    reference_messages = reference_outputs["messages"]
    score = compare_messages(output_messages, reference_messages)
    return {"key": "evaluator_score", "score": score}
```
:::

:::js
```typescript
type EvaluatorParams = {
    outputs: Record;
    referenceOutputs: Record;
};

function evaluator({ outputs, referenceOutputs }: EvaluatorParams) {
    // compare agent outputs against reference outputs
    const outputMessages = outputs.messages;
    const referenceMessages = referenceOutputs.messages;
    const score = compareMessages(outputMessages, referenceMessages);
    return { key: "evaluator_score", score: score };
}
```
:::

To get started, you can use prebuilt evaluators from `AgentEvals` package:

:::python

```bash pip
pip install -U agentevals
```

```bash uv
uv add agentevals
```

:::

:::js
```bash
npm install agentevals
```
:::

## Create evaluator

A common way to evaluate agent performance is by comparing its trajectory (the order in which it calls its tools) against a reference trajectory:

:::python
```python

from agentevals.trajectory.match 

outputs = [
    {
        "role": "assistant",
        "tool_calls": [
            {
                "function": {
                    "name": "get_weather",
                    "arguments": json.dumps({"city": "san francisco"}),
                }
            },
            {
                "function": {
                    "name": "get_directions",
                    "arguments": json.dumps({"destination": "presidio"}),
                }
            }
        ],
    }
]
reference_outputs = [
    {
        "role": "assistant",
        "tool_calls": [
            {
                "function": {
                    "name": "get_weather",
                    "arguments": json.dumps({"city": "san francisco"}),
                }
            },
        ],
    }
]

# Create the evaluator
evaluator = create_trajectory_match_evaluator(
    trajectory_match_mode="superset",    # [!code highlight]
)

# Run the evaluator
result = evaluator(
    outputs=outputs, reference_outputs=reference_outputs
)
```
:::

:::js
```typescript


const outputs = [
    {
        role: "assistant",
        tool_calls: [
        {
            function: {
            name: "get_weather",
            arguments: JSON.stringify({ city: "san francisco" }),
            },
        },
        {
            function: {
            name: "get_directions",
            arguments: JSON.stringify({ destination: "presidio" }),
            },
        },
        ],
    },
];

const referenceOutputs = [
    {
        role: "assistant",
        tool_calls: [
        {
            function: {
            name: "get_weather",
            arguments: JSON.stringify({ city: "san francisco" }),
            },
        },
        ],
    },
];

// Create the evaluator
const evaluator = createTrajectoryMatchEvaluator({
  // Specify how the trajectories will be compared. `superset` will accept output trajectory as valid if it's a superset of the reference one. Other options include: strict, unordered and subset
  trajectoryMatchMode: "superset", // [!code highlight]
});

// Run the evaluator
const result = evaluator({
    outputs: outputs,
    referenceOutputs: referenceOutputs,
});
```
:::

1. Specify how the trajectories will be compared. `superset` will accept output trajectory as valid if it's a superset of the reference one. Other options include: [strict](https://github.com/langchain-ai/agentevals?tab=readme-ov-file#strict-match), [unordered](https://github.com/langchain-ai/agentevals?tab=readme-ov-file#unordered-match) and [subset](https://github.com/langchain-ai/agentevals?tab=readme-ov-file#subset-and-superset-match)

As a next step, learn more about how to [customize trajectory match evaluator](https://github.com/langchain-ai/agentevals?tab=readme-ov-file#agent-trajectory-match).

### LLM-as-a-judge

You can use LLM-as-a-judge evaluator that uses an LLM to compare the trajectory against the reference outputs and output a score:

:::python
```python

from agentevals.trajectory.llm 
    create_trajectory_llm_as_judge,  # [!code highlight]
    TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE
)

evaluator = create_trajectory_llm_as_judge(
    prompt=TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE,
    model="openai:o3-mini"
)
```
:::

:::js
```typescript

    createTrajectoryLlmAsJudge,
    TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE,
} from "agentevals/trajectory/llm";

const evaluator = createTrajectoryLlmAsJudge({
    prompt: TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE,
    model: "openai:o3-mini",
});
```
:::

## Run evaluator

To run an evaluator, you first need to create a [LangSmith dataset](/langsmith/manage-datasets). To use the prebuilt AgentEvals evaluators, you must have a dataset with the following schema:

* **input**: `{"messages": [...]}` input messages to call the agent with.
* **output**: `{"messages": [...]}` expected message history in the agent output. For trajectory evaluation, you can choose to keep only assistant messages.

:::python
```python
from langsmith 
from langchain.agents 
from agentevals.trajectory.match 


client = Client()
agent = create_agent(...)
evaluator = create_trajectory_match_evaluator(...)

experiment_results = client.evaluate(
    lambda inputs: agent.invoke(inputs),
    # replace with your dataset name
    data="",
    evaluators=[evaluator]
)
```
:::

:::js
```typescript




const client = new Client();
const agent = createAgent({...});
const evaluator = createTrajectoryMatchEvaluator({...});

const experimentResults = await client.evaluate(
    (inputs) => agent.invoke(inputs),
    // replace with your dataset name
    { data: "" },
    { evaluators: [evaluator] }
);
```
:::
