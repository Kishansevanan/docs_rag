---
title: Prebuilt middleware
description: Prebuilt middleware for common agent use cases
---

LangChain and [Deep Agents](/oss/deepagents/overview) provide prebuilt middleware for common use cases. Each middleware is production-ready and configurable for your specific needs.

## Provider-agnostic middleware

The following middleware work with any LLM provider:

:::python

| Middleware | Description |
|------------|-------------|
| [Summarization](#summarization) | Automatically summarize conversation history when approaching token limits. |
| [Human-in-the-loop](#human-in-the-loop) | Pause execution for human approval of tool calls. |
| [Model call limit](#model-call-limit) | Limit the number of model calls to prevent excessive costs. |
| [Tool call limit](#tool-call-limit) | Control tool execution by limiting call counts. |
| [Model fallback](#model-fallback) | Automatically fallback to alternative models when primary fails. |
| [PII detection](#pii-detection) | Detect and handle Personally Identifiable Information (PII). |
| [To-do list](#to-do-list) | Equip agents with task planning and tracking capabilities. |
| [LLM tool selector](#llm-tool-selector) | Use an LLM to select relevant tools before calling main model. |
| [Tool retry](#tool-retry) | Automatically retry failed tool calls with exponential backoff. |
| [Model retry](#model-retry) | Automatically retry failed model calls with exponential backoff. |
| [LLM tool emulator](#llm-tool-emulator) | Emulate tool execution using an LLM for testing purposes. |
| [Context editing](#context-editing) | Manage conversation context by trimming or clearing tool uses. |
| [Shell tool](#shell-tool) | Expose a persistent shell session to agents for command execution. |
| [File search](#file-search) | Provide Glob and Grep search tools over filesystem files. |
| [Filesystem](#filesystem-deepagents) | Provide agents with a filesystem for storing context and long-term memories. |
| [Subagent](#subagent-deepagents) | Add the ability to spawn subagents. |

:::

:::js

| Middleware | Description |
|------------|-------------|
| [Summarization](#summarization) | Automatically summarize conversation history when approaching token limits. |
| [Human-in-the-loop](#human-in-the-loop) | Pause execution for human approval of tool calls. |
| [Model call limit](#model-call-limit) | Limit the number of model calls to prevent excessive costs. |
| [Tool call limit](#tool-call-limit) | Control tool execution by limiting call counts. |
| [Model fallback](#model-fallback) | Automatically fallback to alternative models when primary fails. |
| [PII detection](#pii-detection) | Detect and handle Personally Identifiable Information (PII). |
| [To-do list](#to-do-list) | Equip agents with task planning and tracking capabilities. |
| [LLM tool selector](#llm-tool-selector) | Use an LLM to select relevant tools before calling main model. |
| [Tool retry](#tool-retry) | Automatically retry failed tool calls with exponential backoff. |
| [Model retry](#model-retry) | Automatically retry failed model calls with exponential backoff. |
| [LLM tool emulator](#llm-tool-emulator) | Emulate tool execution using an LLM for testing purposes. |
| [Context editing](#context-editing) | Manage conversation context by trimming or clearing tool uses. |
| [Filesystem](#filesystem-deepagents) | Provide agents with a filesystem for storing context and long-term memories. |
| [Subagent middleware](#subagent-deepagents) | Add the ability to spawn subagents. |

:::

### Summarization

Automatically summarize conversation history when approaching token limits, preserving recent messages while compressing older context. Summarization is useful for the following:
- Long-running conversations that exceed context windows.
- Multi-turn dialogues with extensive history.
- Applications where preserving full conversation context matters.

:::python
**API reference:** @[`SummarizationMiddleware`]

```python
from langchain.agents 
from langchain.agents.middleware 

agent = create_agent(
    model="gpt-4.1",
    tools=[your_weather_tool, your_calculator_tool],
    middleware=[
        SummarizationMiddleware(
            model="gpt-4.1-mini",
            trigger=("tokens", 4000),
            keep=("messages", 20),
        ),
    ],
)
```
:::

:::js
```typescript


const agent = createAgent({
  model: "gpt-4.1",
  tools: [weatherTool, calculatorTool],
  middleware: [
    summarizationMiddleware({
      model: "gpt-4.1-mini",
      trigger: { tokens: 4000 },
      keep: { messages: 20 },
    }),
  ],
});
```
:::



:::python


    The `fraction` conditions for `trigger` and `keep` (shown below) rely on a chat model's [profile data](/oss/langchain/models#model-profiles) if using `langchain>=1.1`. If data are not available, use another condition or specify manually:

    ```python
    from langchain.chat_models 

    custom_profile = {
        "max_input_tokens": 100_000,
        # ...
    }
    model = init_chat_model("gpt-4.1", profile=custom_profile)
    ```



    Model for generating summaries. Can be a model identifier string (e.g., `'openai:gpt-4.1-mini'`) or a `BaseChatModel` instance. See @[`init_chat_model`][init_chat_model(model)] for more information.



    Condition(s) for triggering summarization. Can be:

    - A single @[`ContextSize`] tuple (specified condition must be met)
    - A list of @[`ContextSize`] tuples (any condition must be met - OR logic)

    Condition should be one of the following:

    - `fraction` (float): Fraction of model's context size (0-1)
    - `tokens` (int): Absolute token count
    - `messages` (int): Message count

    At least one condition must be specified. If not provided, summarization will not trigger automatically.

    See the API reference for @[`ContextSize`] for more information.



    How much context to preserve after summarization. Specify exactly one of:

    - `fraction` (float): Fraction of model's context size to keep (0-1)
    - `tokens` (int): Absolute token count to keep
    - `messages` (int): Number of recent messages to keep

    See the API reference for @[`ContextSize`] for more information.



    Custom token counting function. Defaults to character-based counting.



    Custom prompt template for summarization. Uses built-in template if not specified. The template should include `{messages}` placeholder where conversation history will be inserted.



    Maximum number of tokens to include when generating the summary. Messages will be trimmed to fit this limit before summarization.



    **Deprecated:** Use `summary_prompt` to provide the full prompt instead.



    **Deprecated:** Use `trigger: ("tokens", value)` instead. Token threshold for triggering summarization.



    **Deprecated:** Use `keep: ("messages", value)` instead. Recent messages to preserve.

:::

:::js

    The `fraction` conditions for `trigger` and `keep` (shown below) rely on a chat model's [profile data](/oss/langchain/models#model-profiles) if using `langchain@1.1.0`. If data are not available, use another condition or specify manually:
    ```typescript
    const customProfile: ModelProfile = {
        maxInputTokens: 100_000,
        // ...
    }
    model = await initChatModel("...", {
        profile: customProfile,
    });
    ```



    Model for generating summaries. Can be a model identifier string (e.g., `'openai:gpt-4.1-mini'`) or a `BaseChatModel` instance.



    Conditions for triggering summarization. Can be:

    - A single condition object (all properties must be met - AND logic)
    - An array of condition objects (any condition must be met - OR logic)

    Each condition can include:
    - `fraction` (number): Fraction of model's context size (0-1)
    - `tokens` (number): Absolute token count
    - `messages` (number): Message count

    At least one property must be specified per condition. If not provided, summarization will not trigger automatically.



    How much context to preserve after summarization. Specify exactly one of:

    - `fraction` (number): Fraction of model's context size to keep (0-1)
    - `tokens` (number): Absolute token count to keep
    - `messages` (number): Number of recent messages to keep



    Custom token counting function. Defaults to character-based counting.



    Custom prompt template for summarization. Uses built-in template if not specified. The template should include `{messages}` placeholder where conversation history will be inserted.



    Maximum number of tokens to include when generating the summary. Messages will be trimmed to fit this limit before summarization.



    Prefix to add to the summary message. If not provided, a default prefix is used.



    **Deprecated:** Use `trigger: { tokens: value }` instead. Token threshold for triggering summarization.



    **Deprecated:** Use `keep: { messages: value }` instead. Recent messages to preserve.

:::





The summarization middleware monitors message token counts and automatically summarizes older messages when thresholds are reached.

**Trigger conditions** control when summarization runs:
- Single condition object (specified must be met)
- Array of conditions (any condition must be met - OR logic)
- Each condition can use `fraction` (of model's context size), `tokens` (absolute count), or `messages` (message count)

**Keep condition** control how much context to preserve (specify exactly one):
- `fraction` - Fraction of model's context size to keep
- `tokens` - Absolute token count to keep
- `messages` - Number of recent messages to keep

:::python
```python
from langchain.agents 
from langchain.agents.middleware 


# Single condition: trigger if tokens >= 4000
agent = create_agent(
    model="gpt-4.1",
    tools=[your_weather_tool, your_calculator_tool],
    middleware=[
        SummarizationMiddleware(
            model="gpt-4.1-mini",
            trigger=("tokens", 4000),
            keep=("messages", 20),
        ),
    ],
)

# Multiple conditions: trigger if number of tokens >= 3000 OR messages >= 6
agent2 = create_agent(
    model="gpt-4.1",
    tools=[your_weather_tool, your_calculator_tool],
    middleware=[
        SummarizationMiddleware(
            model="gpt-4.1-mini",
            trigger=[
                ("tokens", 3000),
                ("messages", 6),
            ],
            keep=("messages", 20),
        ),
    ],
)

# Using fractional limits
agent3 = create_agent(
    model="gpt-4.1",
    tools=[your_weather_tool, your_calculator_tool],
    middleware=[
        SummarizationMiddleware(
            model="gpt-4.1-mini",
            trigger=("fraction", 0.8),
            keep=("fraction", 0.3),
        ),
    ],
)
```
:::

:::js
```typescript


// Single condition
const agent = createAgent({
  model: "gpt-4.1",
  tools: [weatherTool, calculatorTool],
  middleware: [
    summarizationMiddleware({
      model: "gpt-4.1-mini",
      trigger: { tokens: 4000, messages: 10 },
      keep: { messages: 20 },
    }),
  ],
});

// Multiple conditions
const agent2 = createAgent({
  model: "gpt-4.1",
  tools: [weatherTool, calculatorTool],
  middleware: [
    summarizationMiddleware({
      model: "gpt-4.1-mini",
      trigger: [
        { tokens: 3000, messages: 6 },
      ],
      keep: { messages: 20 },
    }),
  ],
});

// Using fractional limits
const agent3 = createAgent({
  model: "gpt-4.1",
  tools: [weatherTool, calculatorTool],
  middleware: [
    summarizationMiddleware({
      model: "gpt-4.1-mini",
      trigger: { fraction: 0.8 },
      keep: { fraction: 0.3 },
    }),
  ],
});
```
:::



### Human-in-the-loop

Pause agent execution for human approval, editing, or rejection of tool calls before they execute. [Human-in-the-loop](/oss/langchain/human-in-the-loop) is useful for the following:

- High-stakes operations requiring human approval (e.g. database writes, financial transactions).
- Compliance workflows where human oversight is mandatory.
- Long-running conversations where human feedback guides the agent.

:::python
**API reference:** @[`HumanInTheLoopMiddleware`]
:::


    Human-in-the-loop middleware requires a [checkpointer](/oss/langgraph/persistence#checkpoints) to maintain state across interruptions.


:::python
```python
from langchain.agents 
from langchain.agents.middleware 
from langgraph.checkpoint.memory 


def read_email_tool(email_id: str) -> str:
    """Mock function to read an email by its ID."""
    return f"Email content for ID: {email_id}"

def send_email_tool(recipient: str, subject: str, body: str) -> str:
    """Mock function to send an email."""
    return f"Email sent to {recipient} with subject '{subject}'"

agent = create_agent(
    model="gpt-4.1",
    tools=[your_read_email_tool, your_send_email_tool],
    checkpointer=InMemorySaver(),
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "your_send_email_tool": {
                    "allowed_decisions": ["approve", "edit", "reject"],
                },
                "your_read_email_tool": False,
            }
        ),
    ],
)
```
:::

:::js
```typescript


function readEmailTool(emailId: string): string {
  /** Mock function to read an email by its ID. */
  return `Email content for ID: ${emailId}`;
}

function sendEmailTool(recipient: string, subject: string, body: string): string {
  /** Mock function to send an email. */
  return `Email sent to ${recipient} with subject '${subject}'`;
}

const agent = createAgent({
  model: "gpt-4.1",
  tools: [readEmailTool, sendEmailTool],
  middleware: [
    humanInTheLoopMiddleware({
      interruptOn: {
        sendEmailTool: {
          allowedDecisions: ["approve", "edit", "reject"],
        },
        readEmailTool: false,
      }
    })
  ]
});
```
:::


    For complete examples, configuration options, and integration patterns, see the [Human-in-the-loop documentation](/oss/langchain/human-in-the-loop).


:::python

    Watch this [video guide](https://www.youtube.com/watch?v=SpfT6-YAVPk) demonstrating Human-in-the-loop middleware behavior.

:::

:::js

    Watch this [video guide](https://www.youtube.com/watch?v=tdOeUVERukA) demonstrating Human-in-the-loop middleware behavior.

:::

### Model call limit

Limit the number of model calls to prevent infinite loops or excessive costs. Model call limit is useful for the following:

- Preventing runaway agents from making too many API calls.
- Enforcing cost controls on production deployments.
- Testing agent behavior within specific call budgets.

:::python
**API reference:** @[`ModelCallLimitMiddleware`]

```python
from langchain.agents 
from langchain.agents.middleware 
from langgraph.checkpoint.memory 

agent = create_agent(
    model="gpt-4.1",
    checkpointer=InMemorySaver(),  # Required for thread limiting
    tools=[],
    middleware=[
        ModelCallLimitMiddleware(
            thread_limit=10,
            run_limit=5,
            exit_behavior="end",
        ),
    ],
)
```
:::

:::js
```typescript



const agent = createAgent({
  model: "gpt-4.1",
  checkpointer: new MemorySaver(), // Required for thread limiting
  tools: [],
  middleware: [
    modelCallLimitMiddleware({
      threadLimit: 10,
      runLimit: 5,
      exitBehavior: "end",
    }),
  ],
});
```
:::

:::python

    Watch this [video guide](https://www.youtube.com/watch?v=nJEER0uaNkE) demonstrating Model Call Limit middleware behavior.

:::

:::js

    Watch this [video guide](https://www.youtube.com/watch?v=x5jLQTFXR0Y) demonstrating Model Call Limit middleware behavior.

:::



:::python

    Maximum model calls across all runs in a thread. Defaults to no limit.



    Maximum model calls per single invocation. Defaults to no limit.



    Behavior when limit is reached. Options: `'end'` (graceful termination) or `'error'` (raise exception)

:::

:::js

    Maximum model calls across all runs in a thread. Defaults to no limit.



    Maximum model calls per single invocation. Defaults to no limit.



    Behavior when limit is reached. Options: `'end'` (graceful termination) or `'error'` (throw exception)

:::




### Tool call limit

Control agent execution by limiting the number of tool calls, either globally across all tools or for specific tools. Tool call limits are useful for the following:

- Preventing excessive calls to expensive external APIs.
- Limiting web searches or database queries.
- Enforcing rate limits on specific tool usage.
- Protecting against runaway agent loops.

:::python
**API reference:** @[`ToolCallLimitMiddleware`]

```python
from langchain.agents 
from langchain.agents.middleware 

agent = create_agent(
    model="gpt-4.1",
    tools=[search_tool, database_tool],
    middleware=[
        # Global limit
        ToolCallLimitMiddleware(thread_limit=20, run_limit=10),
        # Tool-specific limit
        ToolCallLimitMiddleware(
            tool_name="search",
            thread_limit=5,
            run_limit=3,
        ),
    ],
)
```
:::

:::js
```typescript


const agent = createAgent({
  model: "gpt-4.1",
  tools: [searchTool, databaseTool],
  middleware: [
    toolCallLimitMiddleware({ threadLimit: 20, runLimit: 10 }),
    toolCallLimitMiddleware({
      toolName: "search",
      threadLimit: 5,
      runLimit: 3,
    }),
  ],
});
```
:::

:::python

    Watch this [video guide](https://www.youtube.com/watch?v=6gYlaJJ8t0w) demonstrating Tool Call Limit middleware behavior.

:::

:::js

    Watch this [video guide](https://www.youtube.com/watch?v=oL6am5UqODY) demonstrating Tool Call Limit middleware behavior.

:::



:::python

    Name of specific tool to limit. If not provided, limits apply to **all tools globally**.



    Maximum tool calls across all runs in a thread (conversation). Persists across multiple invocations with the same thread ID. Requires a checkpointer to maintain state. `None` means no thread limit.



    Maximum tool calls per single invocation (one user message → response cycle). Resets with each new user message. `None` means no run limit.

    **Note:** At least one of `thread_limit` or `run_limit` must be specified.



    Behavior when limit is reached:

    - `'continue'` (default) - Block exceeded tool calls with error messages, let other tools and the model continue. The model decides when to end based on the error messages.
    - `'error'` - Raise a `ToolCallLimitExceededError` exception, stopping execution immediately
    - `'end'` - Stop execution immediately with a `ToolMessage` and AI message for the exceeded tool call. Only works when limiting a single tool; raises `NotImplementedError` if other tools have pending calls.

:::

:::js

    Name of specific tool to limit. If not provided, limits apply to **all tools globally**.



    Maximum tool calls across all runs in a thread (conversation). Persists across multiple invocations with the same thread ID. Requires a checkpointer to maintain state. `undefined` means no thread limit.



    Maximum tool calls per single invocation (one user message → response cycle). Resets with each new user message. `undefined` means no run limit.

    **Note:** At least one of `threadLimit` or `runLimit` must be specified.



    Behavior when limit is reached:

    - `'continue'` (default) - Block exceeded tool calls with error messages, let other tools and the model continue. The model decides when to end based on the error messages.
    - `'error'` - Throw a `ToolCallLimitExceededError` exception, stopping execution immediately
    - `'end'` - Stop execution immediately with a ToolMessage and AI message for the exceeded tool call. Only works when limiting a single tool; throws error if other tools have pending calls.

:::





Specify limits with:
- **Thread limit** - Max calls across all runs in a conversation (requires checkpointer)
- **Run limit** - Max calls per single invocation (resets each turn)

Exit behaviors:
- `'continue'` (default) - Block exceeded calls with error messages, agent continues
- `'error'` - Raise exception immediately
- `'end'` - Stop with ToolMessage + AI message (single-tool scenarios only)

:::python
```python
from langchain.agents 
from langchain.agents.middleware 


global_limiter = ToolCallLimitMiddleware(thread_limit=20, run_limit=10)
search_limiter = ToolCallLimitMiddleware(tool_name="search", thread_limit=5, run_limit=3)
database_limiter = ToolCallLimitMiddleware(tool_name="query_database", thread_limit=10)
strict_limiter = ToolCallLimitMiddleware(tool_name="scrape_webpage", run_limit=2, exit_behavior="error")

agent = create_agent(
    model="gpt-4.1",
    tools=[search_tool, database_tool, scraper_tool],
    middleware=[global_limiter, search_limiter, database_limiter, strict_limiter],
)
```
:::

:::js
```typescript


const globalLimiter = toolCallLimitMiddleware({ threadLimit: 20, runLimit: 10 });
const searchLimiter = toolCallLimitMiddleware({ toolName: "search", threadLimit: 5, runLimit: 3 });
const databaseLimiter = toolCallLimitMiddleware({ toolName: "query_database", threadLimit: 10 });
const strictLimiter = toolCallLimitMiddleware({ toolName: "scrape_webpage", runLimit: 2, exitBehavior: "error" });

const agent = createAgent({
  model: "gpt-4.1",
  tools: [searchTool, databaseTool, scraperTool],
  middleware: [globalLimiter, searchLimiter, databaseLimiter, strictLimiter],
});
```
:::




### Model fallback

Automatically fallback to alternative models when the primary model fails. Model fallback is useful for the following:

- Building resilient agents that handle model outages.
- Cost optimization by falling back to cheaper models.
- Provider redundancy across OpenAI, Anthropic, etc.

:::python
**API reference:** @[`ModelFallbackMiddleware`]

```python
from langchain.agents 
from langchain.agents.middleware 

agent = create_agent(
    model="gpt-4.1",
    tools=[],
    middleware=[
        ModelFallbackMiddleware(
            "gpt-4.1-mini",
            "claude-3-5-sonnet-20241022",
        ),
    ],
)
```
:::

:::js
```typescript


const agent = createAgent({
  model: "gpt-4.1",
  tools: [],
  middleware: [
    modelFallbackMiddleware(
      "gpt-4.1-mini",
      "claude-3-5-sonnet-20241022"
    ),
  ],
});
```
:::

:::python

    Watch this [video guide](https://www.youtube.com/watch?v=8rCRO0DUeIM) demonstrating Model Fallback middleware behavior.

:::



:::python

    First fallback model to try when the primary model fails. Can be a model identifier string (e.g., `'openai:gpt-4.1-mini'`) or a `BaseChatModel` instance.



    Additional fallback models to try in order if previous models fail

:::

:::js
The middleware accepts a variable number of string arguments representing fallback models in order:


  One or more fallback model strings to try in order when the primary model fails

  ```typescript
  modelFallbackMiddleware(
    "first-fallback-model",
    "second-fallback-model",
    // ... more models
  )
  ```

:::



### PII detection

Detect and handle Personally Identifiable Information (PII) in conversations using configurable strategies. PII detection is useful for the following:

- Healthcare and financial applications with compliance requirements.
- Customer service agents that need to sanitize logs.
- Any application handling sensitive user data.

:::python
**API reference:** @[`PIIMiddleware`]

```python
from langchain.agents 
from langchain.agents.middleware 

agent = create_agent(
    model="gpt-4.1",
    tools=[],
    middleware=[
        PIIMiddleware("email", strategy="redact", apply_to_input=True),
        PIIMiddleware("credit_card", strategy="mask", apply_to_input=True),
    ],
)
```
:::

:::js
```typescript


const agent = createAgent({
  model: "gpt-4.1",
  tools: [],
  middleware: [
    piiMiddleware("email", { strategy: "redact", applyToInput: true }),
    piiMiddleware("credit_card", { strategy: "mask", applyToInput: true }),
  ],
});
```
:::

#### Custom PII types

You can create custom PII types by providing a `detector` parameter. This allows you to detect patterns specific to your use case beyond the built-in types.

**Three ways to create custom detectors:**

1. **Regex pattern string** - Simple pattern matching
:::js
1. **RegExp object** - More control over regex flags
:::
1. **Custom function** - Complex detection logic with validation

:::python
```python
from langchain.agents 
from langchain.agents.middleware 



# Method 1: Regex pattern string
agent1 = create_agent(
    model="gpt-4.1",
    tools=[],
    middleware=[
        PIIMiddleware(
            "api_key",
            detector=r"sk-[a-zA-Z0-9]{32}",
            strategy="block",
        ),
    ],
)

# Method 2: Compiled regex pattern
agent2 = create_agent(
    model="gpt-4.1",
    tools=[],
    middleware=[
        PIIMiddleware(
            "phone_number",
            detector=re.compile(r"\+?\d{1,3}[\s.-]?\d{3,4}[\s.-]?\d{4}"),
            strategy="mask",
        ),
    ],
)

# Method 3: Custom detector function
def detect_ssn(content: str) -> list[dict[str, str | int]]:
    """Detect SSN with validation.

    Returns a list of dictionaries with 'text', 'start', and 'end' keys.
    """
    
    matches = []
    pattern = r"\d{3}-\d{2}-\d{4}"
    for match in re.finditer(pattern, content):
        ssn = match.group(0)
        # Validate: first 3 digits shouldn't be 000, 666, or 900-999
        first_three = int(ssn[:3])
        if first_three not in [0, 666] and not (900 <= first_three <= 999):
            matches.append({
                "text": ssn,
                "start": match.start(),
                "end": match.end(),
            })
    return matches

agent3 = create_agent(
    model="gpt-4.1",
    tools=[],
    middleware=[
        PIIMiddleware(
            "ssn",
            detector=detect_ssn,
            strategy="hash",
        ),
    ],
)
```
:::

:::js
```typescript


// Method 1: Regex pattern string
const agent1 = createAgent({
  model: "gpt-4.1",
  tools: [],
  middleware: [
    piiMiddleware("api_key", {
      detector: "sk-[a-zA-Z0-9]{32}",
      strategy: "block",
    }),
  ],
});

// Method 2: RegExp object
const agent2 = createAgent({
  model: "gpt-4.1",
  tools: [],
  middleware: [
    piiMiddleware("phone_number", {
      detector: /\+?\d{1,3}[\s.-]?\d{3,4}[\s.-]?\d{4}/,
      strategy: "mask",
    }),
  ],
});

// Method 3: Custom detector function
function detectSSN(content: string): PIIMatch[] {
  const matches: PIIMatch[] = [];
  const pattern = /\d{3}-\d{2}-\d{4}/g;
  let match: RegExpExecArray | null;

  while ((match = pattern.exec(content)) !== null) {
    const ssn = match[0];
    // Validate: first 3 digits shouldn't be 000, 666, or 900-999
    const firstThree = parseInt(ssn.substring(0, 3), 10);
    if (firstThree !== 0 && firstThree !== 666 && !(firstThree >= 900 && firstThree <= 999)) {
      matches.push({
        text: ssn,
        start: match.index ?? 0,
        end: (match.index ?? 0) + ssn.length,
      });
    }
  }
  return matches;
}

const agent3 = createAgent({
  model: "gpt-4.1",
  tools: [],
  middleware: [
    piiMiddleware("ssn", {
      detector: detectSSN,
      strategy: "hash",
    }),
  ],
});
```
:::

**Custom detector function signature:**

The detector function must accept a string (content) and return matches:

:::python
Returns a list of dictionaries with `text`, `start`, and `end` keys:
```python
def detector(content: str) -> list[dict[str, str | int]]:
    return [
        {"text": "matched_text", "start": 0, "end": 12},
        # ... more matches
    ]
```
:::
:::js
Returns an array of `PIIMatch` objects:
```typescript
interface PIIMatch {
  text: string;    // The matched text
  start: number;   // Start index in content
  end: number;      // End index in content
}

function detector(content: string): PIIMatch[] {
  return [
    { text: "matched_text", start: 0, end: 12 },
    // ... more matches
  ];
}
```
:::


    For custom detectors:

    - Use regex strings for simple patterns
    - Use RegExp objects when you need flags (e.g., case-insensitive matching)
    - Use custom functions when you need validation logic beyond pattern matching
    - Custom functions give you full control over detection logic and can implement complex validation rules




:::python

    Type of PII to detect. Can be a built-in type (`email`, `credit_card`, `ip`, `mac_address`, `url`) or a custom type name.



    How to handle detected PII. Options:

    - `'block'` - Raise exception when detected
    - `'redact'` - Replace with `[REDACTED_{PII_TYPE}]`
    - `'mask'` - Partially mask (e.g., `****-****-****-1234`)
    - `'hash'` - Replace with deterministic hash



    Custom detector function or regex pattern. If not provided, uses built-in detector for the PII type.



    Check user messages before model call



    Check AI messages after model call



    Check tool result messages after execution

:::

:::js

    Type of PII to detect. Can be a built-in type (`email`, `credit_card`, `ip`, `mac_address`, `url`) or a custom type name.



    How to handle detected PII. Options:

    - `'block'` - Throw error when detected
    - `'redact'` - Replace with `[REDACTED_TYPE]`
    - `'mask'` - Partially mask (e.g., `****-****-****-1234`)
    - `'hash'` - Replace with deterministic hash (e.g., ``)



    Custom detector. Can be:

    - `RegExp` - Regex pattern for matching
    - `string` - Regex pattern string (e.g., `"sk-[a-zA-Z0-9]{32}"`)
    - `function` - Custom detector function `(content: string) => PIIMatch[]`

    If not provided, uses built-in detector for the PII type.



    Check user messages before model call



    Check AI messages after model call



    Check tool result messages after execution

:::



### To-do list

Equip agents with task planning and tracking capabilities for complex multi-step tasks. To-do lists are useful for the following:

- Complex multi-step tasks requiring coordination across multiple tools.
- Long-running operations where progress visibility is important.


    This middleware automatically provides agents with a `write_todos` tool and system prompts to guide effective task planning.


:::python
**API reference:** @[`TodoListMiddleware`]

```python
from langchain.agents 
from langchain.agents.middleware 

agent = create_agent(
    model="gpt-4.1",
    tools=[read_file, write_file, run_tests],
    middleware=[TodoListMiddleware()],
)
```
:::

:::js
```typescript


const agent = createAgent({
  model: "gpt-4.1",
  tools: [readFile, writeFile, runTests],
  middleware: [todoListMiddleware()],
});
```
:::

:::python

    Watch this [video guide](https://www.youtube.com/watch?v=yTWocbVKQxw) demonstrating To-do List middleware behavior.

:::

:::js

    Watch this [video guide](https://www.youtube.com/watch?v=dwvhZ1z_Pas) demonstrating To-do List middleware behavior.

:::



:::python

    Custom system prompt for guiding todo usage. Uses built-in prompt if not specified.



    Custom description for the `write_todos` tool. Uses built-in description if not specified.

:::

:::js
No configuration options available (uses defaults).
:::



### LLM tool selector

Use an LLM to intelligently select relevant tools before calling the main model. LLM tool selectors are useful for the following:

- Agents with many tools (10+) where most aren't relevant per query.
- Reducing token usage by filtering irrelevant tools.
- Improving model focus and accuracy.

This middleware uses structured output to ask an LLM which tools are most relevant for the current query. The structured output schema defines the available tool names and descriptions. Model providers often add this structured output information to the system prompt behind the scenes.

:::python
**API reference:** @[`LLMToolSelectorMiddleware`]

```python
from langchain.agents 
from langchain.agents.middleware 

agent = create_agent(
    model="gpt-4.1",
    tools=[tool1, tool2, tool3, tool4, tool5, ...],
    middleware=[
        LLMToolSelectorMiddleware(
            model="gpt-4.1-mini",
            max_tools=3,
            always_include=["search"],
        ),
    ],
)
```
:::

:::js
```typescript


const agent = createAgent({
  model: "gpt-4.1",
  tools: [tool1, tool2, tool3, tool4, tool5, ...],
  middleware: [
    llmToolSelectorMiddleware({
      model: "gpt-4.1-mini",
      maxTools: 3,
      alwaysInclude: ["search"],
    }),
  ],
});
```
:::



:::python

    Model for tool selection. Can be a model identifier string (e.g., `'openai:gpt-4.1-mini'`) or a `BaseChatModel` instance. See @[`init_chat_model`][init_chat_model(model)] for more information.

    Defaults to the agent's main model.



    Instructions for the selection model. Uses built-in prompt if not specified.



    Maximum number of tools to select. If the model selects more, only the first max_tools will be used. No limit if not specified.



    Tool names to always include regardless of selection. These do not count against the max_tools limit.

:::

:::js

    Model for tool selection. Can be a model identifier string (e.g., `'openai:gpt-4.1-mini'`) or a `BaseChatModel` instance. Defaults to the agent's main model.



    Instructions for the selection model. Uses built-in prompt if not specified.



    Maximum number of tools to select. If the model selects more, only the first maxTools will be used. No limit if not specified.



    Tool names to always include regardless of selection. These do not count against the maxTools limit.

:::




### Tool retry

Automatically retry failed tool calls with configurable exponential backoff. Tool retry is useful for the following:

- Handling transient failures in external API calls.
- Improving reliability of network-dependent tools.
- Building resilient agents that gracefully handle temporary errors.

:::python
**API reference:** @[`ToolRetryMiddleware`]

```python
from langchain.agents 
from langchain.agents.middleware 

agent = create_agent(
    model="gpt-4.1",
    tools=[search_tool, database_tool],
    middleware=[
        ToolRetryMiddleware(
            max_retries=3,
            backoff_factor=2.0,
            initial_delay=1.0,
        ),
    ],
)
```
:::

:::js
**API reference:** @[`toolRetryMiddleware`]

```typescript


const agent = createAgent({
  model: "gpt-4.1",
  tools: [searchTool, databaseTool],
  middleware: [
    toolRetryMiddleware({
      maxRetries: 3,
      backoffFactor: 2.0,
      initialDelayMs: 1000,
    }),
  ],
});
```
:::



:::python

    Maximum number of retry attempts after the initial call (3 total attempts with default)



    Optional list of tools or tool names to apply retry logic to. If `None`, applies to all tools.



    Either a tuple of exception types to retry on, or a callable that takes an exception and returns `True` if it should be retried.



    Behavior when all retries are exhausted. Options:
    - `'return_message'` - Return a `ToolMessage` with error details (allows LLM to handle failure)
    - `'raise'` - Re-raise the exception (stops agent execution)
    - Custom callable - Function that takes the exception and returns a string for the `ToolMessage` content



    Multiplier for exponential backoff. Each retry waits `initial_delay * (backoff_factor ** retry_number)` seconds. Set to `0.0` for constant delay.



    Initial delay in seconds before first retry



    Maximum delay in seconds between retries (caps exponential backoff growth)



    Whether to add random jitter (`±25%`) to delay to avoid thundering herd

:::

:::js

    Maximum number of retry attempts after the initial call (3 total attempts with default). Must be >= 0.



    Optional array of tools or tool names to apply retry logic to. Can be a list of `BaseTool` instances or tool name strings. If `undefined`, applies to all tools.


 boolean) | (new (...args: any[]) => Error)[]" default="() => true">
    Either an array of error constructors to retry on, or a function that takes an error and returns `true` if it should be retried. Default is to retry on all errors.


 string)" default="continue">
    Behavior when all retries are exhausted. Options:
    - `'continue'` (default) - Return a `ToolMessage` with error details, allowing the LLM to handle the failure and potentially recover
    - `'error'` - Re-raise the exception, stopping agent execution
    - Custom function - Function that takes the exception and returns a string for the `ToolMessage` content, allowing custom error formatting

    **Deprecated values:** `'raise'` (use `'error'` instead) and `'return_message'` (use `'continue'` instead). These deprecated values still work but will show a warning.



    Multiplier for exponential backoff. Each retry waits `initialDelayMs * (backoffFactor ** retryNumber)` milliseconds. Set to `0.0` for constant delay. Must be >= 0.



    Initial delay in milliseconds before first retry. Must be >= 0.



    Maximum delay in milliseconds between retries (caps exponential backoff growth). Must be >= 0.



    Whether to add random jitter (`±25%`) to delay to avoid thundering herd

:::





The middleware automatically retries failed tool calls with exponential backoff.

:::python
**Key configuration:**
- `max_retries` - Number of retry attempts (default: 2)
- `backoff_factor` - Multiplier for exponential backoff (default: 2.0)
- `initial_delay` - Starting delay in seconds (default: 1.0)
- `max_delay` - Cap on delay growth (default: 60.0)
- `jitter` - Add random variation (default: True)

**Failure handling:**
- `on_failure='return_message'` - Return error message
- `on_failure='raise'` - Re-raise exception
- Custom function - Function returning error message
:::
:::js
**Key configuration:**
- `maxRetries` - Number of retry attempts (default: 2)
- `backoffFactor` - Multiplier for exponential backoff (default: 2.0)
- `initialDelayMs` - Starting delay in milliseconds (default: 1000ms)
- `maxDelayMs` - Cap on delay growth (default: 60000ms)
- `jitter` - Add random variation (default: true)

**Failure handling:**
- `onFailure: "continue"` (default) - Return error message
- `onFailure: "error"` - Re-raise exception
- Custom function - Function returning error message
:::

:::python
```python
from langchain.agents 
from langchain.agents.middleware 


agent = create_agent(
    model="gpt-4.1",
    tools=[search_tool, database_tool, api_tool],
    middleware=[
        ToolRetryMiddleware(
            max_retries=3,
            backoff_factor=2.0,
            initial_delay=1.0,
            max_delay=60.0,
            jitter=True,
            tools=["api_tool"],
            retry_on=(ConnectionError, TimeoutError),
            on_failure="continue",
        ),
    ],
)
```
:::

:::js
```typescript




// Basic usage with default settings (2 retries, exponential backoff)
const agent = createAgent({
  model: "gpt-4.1",
  tools: [searchTool, databaseTool],
  middleware: [toolRetryMiddleware()],
});

// Retry specific exceptions only
const retry = toolRetryMiddleware({
  maxRetries: 4,
  retryOn: [TimeoutError, NetworkError],
  backoffFactor: 1.5,
});

// Custom exception filtering
function shouldRetry(error: Error): boolean {
  // Only retry on 5xx errors
  if (error.name === "HTTPError" && "statusCode" in error) {
    const statusCode = (error as any).statusCode;
    return 500 <= statusCode && statusCode < 600;
  }
  return false;
}

const retryWithFilter = toolRetryMiddleware({
  maxRetries: 3,
  retryOn: shouldRetry,
});

// Apply to specific tools with custom error handling
const formatError = (error: Error) =>
  "Database temporarily unavailable. Please try again later.";

const retrySpecificTools = toolRetryMiddleware({
  maxRetries: 4,
  tools: ["search_database"],
  onFailure: formatError,
});

// Apply to specific tools using BaseTool instances
const searchDatabase = tool(
  async ({ query }) => {
    // Search implementation
    return results;
  },
  {
    name: "search_database",
    description: "Search the database",
    schema: z.object({ query: z.string() }),
  }
);

const retryWithToolInstance = toolRetryMiddleware({
  maxRetries: 4,
  tools: [searchDatabase], // Pass BaseTool instance
});

// Constant backoff (no exponential growth)
const constantBackoff = toolRetryMiddleware({
  maxRetries: 5,
  backoffFactor: 0.0, // No exponential growth
  initialDelayMs: 2000, // Always wait 2 seconds
});

// Raise exception on failure
const strictRetry = toolRetryMiddleware({
  maxRetries: 2,
  onFailure: "error", // Re-raise exception instead of returning message
});
```
:::



### Model retry

Automatically retry failed model calls with configurable exponential backoff. Model retry is useful for the following:

- Handling transient failures in model API calls.
- Improving reliability of network-dependent model requests.
- Building resilient agents that gracefully handle temporary model errors.

:::python
**API reference:** @[`ModelRetryMiddleware`]

```python
from langchain.agents 
from langchain.agents.middleware 

agent = create_agent(
    model="gpt-4.1",
    tools=[search_tool, database_tool],
    middleware=[
        ModelRetryMiddleware(
            max_retries=3,
            backoff_factor=2.0,
            initial_delay=1.0,
        ),
    ],
)
```
:::

:::js
**API reference:** @[`modelRetryMiddleware`]

```typescript


const agent = createAgent({
  model: "gpt-4.1",
  tools: [searchTool, databaseTool],
  middleware: [
    modelRetryMiddleware({
      maxRetries: 3,
      backoffFactor: 2.0,
      initialDelayMs: 1000,
    }),
  ],
});
```
:::



:::python

    Maximum number of retry attempts after the initial call (3 total attempts with default)



    Either a tuple of exception types to retry on, or a callable that takes an exception and returns `True` if it should be retried.



    Behavior when all retries are exhausted. Options:
    - `'continue'` (default) - Return an `AIMessage` with error details, allowing the agent to potentially handle the failure gracefully
    - `'error'` - Re-raise the exception (stops agent execution)
    - Custom callable - Function that takes the exception and returns a string for the `AIMessage` content



    Multiplier for exponential backoff. Each retry waits `initial_delay * (backoff_factor ** retry_number)` seconds. Set to `0.0` for constant delay.



    Initial delay in seconds before first retry



    Maximum delay in seconds between retries (caps exponential backoff growth)



    Whether to add random jitter (`±25%`) to delay to avoid thundering herd

:::

:::js

    Maximum number of retry attempts after the initial call (3 total attempts with default). Must be >= 0.


 boolean) | (new (...args: any[]) => Error)[]" default="() => true">
    Either an array of error constructors to retry on, or a function that takes an error and returns `true` if it should be retried. Default is to retry on all errors.


 string)" default="continue">
    Behavior when all retries are exhausted. Options:
    - `'continue'` (default) - Return an `AIMessage` with error details, allowing the agent to potentially handle the failure gracefully
    - `'error'` - Re-raise the exception, stopping agent execution
    - Custom function - Function that takes the exception and returns a string for the `AIMessage` content, allowing custom error formatting



    Multiplier for exponential backoff. Each retry waits `initialDelayMs * (backoffFactor ** retryNumber)` milliseconds. Set to `0.0` for constant delay. Must be >= 0.



    Initial delay in milliseconds before first retry. Must be >= 0.



    Maximum delay in milliseconds between retries (caps exponential backoff growth). Must be >= 0.



    Whether to add random jitter (`±25%`) to delay to avoid thundering herd

:::





The middleware automatically retries failed model calls with exponential backoff.

:::python
```python
from langchain.agents 
from langchain.agents.middleware 


# Basic usage with default settings (2 retries, exponential backoff)
agent = create_agent(
    model="gpt-4.1",
    tools=[search_tool],
    middleware=[ModelRetryMiddleware()],
)

# Custom exception filtering
class TimeoutError(Exception):
    """Custom exception for timeout errors."""
    pass

class ConnectionError(Exception):
    """Custom exception for connection errors."""
    pass

# Retry specific exceptions only
retry = ModelRetryMiddleware(
    max_retries=4,
    retry_on=(TimeoutError, ConnectionError),
    backoff_factor=1.5,
)


def should_retry(error: Exception) -> bool:
    # Only retry on rate limit errors
    if isinstance(error, TimeoutError):
        return True
    # Or check for specific HTTP status codes
    if hasattr(error, "status_code"):
        return error.status_code in (429, 503)
    return False

retry_with_filter = ModelRetryMiddleware(
    max_retries=3,
    retry_on=should_retry,
)

# Return error message instead of raising
retry_continue = ModelRetryMiddleware(
    max_retries=4,
    on_failure="continue",  # Return AIMessage with error instead of raising
)

# Custom error message formatting
def format_error(error: Exception) -> str:
    return f"Model call failed: {error}. Please try again later."

retry_with_formatter = ModelRetryMiddleware(
    max_retries=4,
    on_failure=format_error,
)

# Constant backoff (no exponential growth)
constant_backoff = ModelRetryMiddleware(
    max_retries=5,
    backoff_factor=0.0,  # No exponential growth
    initial_delay=2.0,  # Always wait 2 seconds
)

# Raise exception on failure
strict_retry = ModelRetryMiddleware(
    max_retries=2,
    on_failure="error",  # Re-raise exception instead of returning message
)
```
:::

:::js
```typescript


// Basic usage with default settings (2 retries, exponential backoff)
const agent = createAgent({
  model: "gpt-4.1",
  tools: [searchTool],
  middleware: [modelRetryMiddleware()],
});

class TimeoutError extends Error {
    // ...
}
class NetworkError extends Error {
    // ...
}

// Retry specific exceptions only
const retry = modelRetryMiddleware({
  maxRetries: 4,
  retryOn: [TimeoutError, NetworkError],
  backoffFactor: 1.5,
});

// Custom exception filtering
function shouldRetry(error: Error): boolean {
  // Only retry on rate limit errors
  if (error.name === "RateLimitError") {
    return true;
  }
  // Or check for specific HTTP status codes
  if (error.name === "HTTPError" && "statusCode" in error) {
    const statusCode = (error as any).statusCode;
    return statusCode === 429 || statusCode === 503;
  }
  return false;
}

const retryWithFilter = modelRetryMiddleware({
  maxRetries: 3,
  retryOn: shouldRetry,
});

// Return error message instead of raising
const retryContinue = modelRetryMiddleware({
  maxRetries: 4,
  onFailure: "continue", // Return AIMessage with error instead of throwing
});

// Custom error message formatting
const formatError = (error: Error) =>
  `Model call failed: ${error.message}. Please try again later.`;

const retryWithFormatter = modelRetryMiddleware({
  maxRetries: 4,
  onFailure: formatError,
});

// Constant backoff (no exponential growth)
const constantBackoff = modelRetryMiddleware({
  maxRetries: 5,
  backoffFactor: 0.0, // No exponential growth
  initialDelayMs: 2000, // Always wait 2 seconds
});

// Raise exception on failure
const strictRetry = modelRetryMiddleware({
  maxRetries: 2,
  onFailure: "error", // Re-raise exception instead of returning message
});
```
:::



### LLM tool emulator

Emulate tool execution using an LLM for testing purposes, replacing actual tool calls with AI-generated responses. LLM tool emulators are useful for the following:

- Testing agent behavior without executing real tools.
- Developing agents when external tools are unavailable or expensive.
- Prototyping agent workflows before implementing actual tools.

:::python
**API reference:** @[`LLMToolEmulator`]

```python
from langchain.agents 
from langchain.agents.middleware 

agent = create_agent(
    model="gpt-4.1",
    tools=[get_weather, search_database, send_email],
    middleware=[
        LLMToolEmulator(),  # Emulate all tools
    ],
)
```
:::

:::js
```typescript


const agent = createAgent({
  model: "gpt-4.1",
  tools: [getWeather, searchDatabase, sendEmail],
  middleware: [
    toolEmulatorMiddleware(), // Emulate all tools
  ],
});
```
:::



:::python

    List of tool names (str) or BaseTool instances to emulate. If `None` (default), ALL tools will be emulated. If empty list `[]`, no tools will be emulated. If array with tool names/instances, only those tools will be emulated.



    Model to use for generating emulated tool responses. Can be a model identifier string (e.g., `'anthropic:claude-sonnet-4-6'`) or a `BaseChatModel` instance. Defaults to the agent's model if not specified. See @[`init_chat_model`][init_chat_model(model)] for more information.

:::

:::js

    List of tool names (string) or tool instances to emulate. If `undefined` (default), ALL tools will be emulated. If empty array `[]`, no tools will be emulated. If array with tool names/instances, only those tools will be emulated.



    Model to use for generating emulated tool responses. Can be a model identifier string (e.g., `'anthropic:claude-sonnet-4-6'`) or a `BaseChatModel` instance. Defaults to the agent's model if not specified.

:::





The middleware uses an LLM to generate plausible responses for tool calls instead of executing the actual tools.

:::python
```python
from langchain.agents 
from langchain.agents.middleware 
from langchain.tools 


@tool
def get_weather(location: str) -> str:
    """Get the current weather for a location."""
    return f"Weather in {location}"

@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email."""
    return "Email sent"


# Emulate all tools (default behavior)
agent = create_agent(
    model="gpt-4.1",
    tools=[get_weather, send_email],
    middleware=[LLMToolEmulator()],
)

# Emulate specific tools only
agent2 = create_agent(
    model="gpt-4.1",
    tools=[get_weather, send_email],
    middleware=[LLMToolEmulator(tools=["get_weather"])],
)

# Use custom model for emulation
agent4 = create_agent(
    model="gpt-4.1",
    tools=[get_weather, send_email],
    middleware=[LLMToolEmulator(model="claude-sonnet-4-6")],
)
```
:::

:::js
```typescript



const getWeather = tool(
  async ({ location }) => `Weather in ${location}`,
  {
    name: "get_weather",
    description: "Get the current weather for a location",
    schema: z.object({ location: z.string() }),
  }
);

const sendEmail = tool(
  async ({ to, subject, body }) => "Email sent",
  {
    name: "send_email",
    description: "Send an email",
    schema: z.object({
      to: z.string(),
      subject: z.string(),
      body: z.string(),
    }),
  }
);

// Emulate all tools (default behavior)
const agent = createAgent({
  model: "gpt-4.1",
  tools: [getWeather, sendEmail],
  middleware: [toolEmulatorMiddleware()],
});

// Emulate specific tools by name
const agent2 = createAgent({
  model: "gpt-4.1",
  tools: [getWeather, sendEmail],
  middleware: [
    toolEmulatorMiddleware({
      tools: ["get_weather"],
    }),
  ],
});

// Emulate specific tools by passing tool instances
const agent3 = createAgent({
  model: "gpt-4.1",
  tools: [getWeather, sendEmail],
  middleware: [
    toolEmulatorMiddleware({
      tools: [getWeather],
    }),
  ],
});

// Use custom model for emulation
const agent5 = createAgent({
  model: "gpt-4.1",
  tools: [getWeather, sendEmail],
  middleware: [
    toolEmulatorMiddleware({
      model: "claude-sonnet-4-6",
    }),
  ],
});
```
:::



### Context editing

Manage conversation context by clearing older tool call outputs when token limits are reached, while preserving recent results. This helps keep context windows manageable in long conversations with many tool calls. Context editing is useful for the following:

- Long conversations with many tool calls that exceed token limits
- Reducing token costs by removing older tool outputs that are no longer relevant
- Maintaining only the most recent N tool results in context

:::python
**API reference:** @[`ContextEditingMiddleware`], @[`ClearToolUsesEdit`]

```python
from langchain.agents 
from langchain.agents.middleware 

agent = create_agent(
    model="gpt-4.1",
    tools=[],
    middleware=[
        ContextEditingMiddleware(
            edits=[
                ClearToolUsesEdit(
                    trigger=100000,
                    keep=3,
                ),
            ],
        ),
    ],
)
```
:::

:::js
```typescript


const agent = createAgent({
  model: "gpt-4.1",
  tools: [],
  middleware: [
    contextEditingMiddleware({
      edits: [
        new ClearToolUsesEdit({
          triggerTokens: 100000,
          keep: 3,
        }),
      ],
    }),
  ],
});
```
:::



:::python

    List of @[`ContextEdit`] strategies to apply



    Token counting method. Options: `'approximate'` or `'model'`


**@[`ClearToolUsesEdit`] options:**


    Token count that triggers the edit. When the conversation exceeds this token count, older tool outputs will be cleared.



    Minimum number of tokens to reclaim when the edit runs. If set to 0, clears as much as needed.



    Number of most recent tool results that must be preserved. These will never be cleared.



    Whether to clear the originating tool call parameters on the AI message. When `True`, tool call arguments are replaced with empty objects.



    List of tool names to exclude from clearing. These tools will never have their outputs cleared.



    Placeholder text inserted for cleared tool outputs. This replaces the original tool message content.

:::

:::js

    Array of @[`ContextEdit`] strategies to apply


**@[`ClearToolUsesEdit`] options:**


    Token count that triggers the edit. When the conversation exceeds this token count, older tool outputs will be cleared.



    Minimum number of tokens to reclaim when the edit runs. If set to 0, clears as much as needed.



    Number of most recent tool results that must be preserved. These will never be cleared.



    Whether to clear the originating tool call parameters on the AI message. When `true`, tool call arguments are replaced with empty objects.



    List of tool names to exclude from clearing. These tools will never have their outputs cleared.



    Placeholder text inserted for cleared tool outputs. This replaces the original tool message content.

:::





The middleware applies context editing strategies when token limits are reached. The most common strategy is `ClearToolUsesEdit`, which clears older tool results while preserving recent ones.

**How it works:**
1. Monitor token count in conversation
2. When threshold is reached, clear older tool outputs
3. Keep most recent N tool results
4. Optionally preserve tool call arguments for context

:::python
```python
from langchain.agents 
from langchain.agents.middleware 


agent = create_agent(
    model="gpt-4.1",
    tools=[search_tool, your_calculator_tool, database_tool],
    middleware=[
        ContextEditingMiddleware(
            edits=[
                ClearToolUsesEdit(
                    trigger=2000,
                    keep=3,
                    clear_tool_inputs=False,
                    exclude_tools=[],
                    placeholder="[cleared]",
                ),
            ],
        ),
    ],
)
```
:::

:::js
```typescript


const agent = createAgent({
  model: "gpt-4.1",
  tools: [searchTool, calculatorTool, databaseTool],
  middleware: [
    contextEditingMiddleware({
      edits: [
        new ClearToolUsesEdit({
          triggerTokens: 2000,
          keep: 3,
          clearToolInputs: false,
          excludeTools: [],
          placeholder: "[cleared]",
        }),
      ],
    }),
  ],
});
```
:::



:::python
### Shell tool

Expose a persistent shell session to agents for command execution. Shell tool middleware is useful for the following:

- Agents that need to execute system commands
- Development and deployment automation tasks
- Testing and validation workflows
- File system operations and script execution


    **Security consideration**: Use appropriate execution policies (`HostExecutionPolicy`, `DockerExecutionPolicy`, or `CodexSandboxExecutionPolicy`) to match your deployment's security requirements.



    **Limitation**: Persistent shell sessions do not currently work with interrupts (human-in-the-loop). We anticipate adding support for this in the future.


**API reference:** @[`ShellToolMiddleware`]

```python
from langchain.agents 
from langchain.agents.middleware 
    ShellToolMiddleware,
    HostExecutionPolicy,
)

agent = create_agent(
    model="gpt-4.1",
    tools=[search_tool],
    middleware=[
        ShellToolMiddleware(
            workspace_root="/workspace",
            execution_policy=HostExecutionPolicy(),
        ),
    ],
)
```




    Base directory for the shell session. If omitted, a temporary directory is created when the agent starts and removed when it ends.



    Optional commands executed sequentially after the session starts



    Optional commands executed before the session shuts down



    Execution policy controlling timeouts, output limits, and resource configuration. Options:

    - `HostExecutionPolicy` - Full host access (default); best for trusted environments where the agent already runs inside a container or VM
    - `DockerExecutionPolicy` - Launches a separate Docker container for each agent run, providing harder isolation
    - `CodexSandboxExecutionPolicy` - Reuses the Codex CLI sandbox for additional syscall/filesystem restrictions



    Optional redaction rules to sanitize command output before returning it to the model.
    
    Redaction rules are applied post execution and do not prevent exfiltration of secrets or sensitive data when using `HostExecutionPolicy`.
    



    Optional override for the registered shell tool description



    Optional shell executable (string) or argument sequence used to launch the persistent session. Defaults to `/bin/bash`.



    Optional environment variables to supply to the shell session. Values are coerced to strings before command execution.






The middleware provides a single persistent shell session that agents can use to execute commands sequentially.

**Execution policies:**
- `HostExecutionPolicy` (default) - Native execution with full host access
- `DockerExecutionPolicy` - Isolated Docker container execution
- `CodexSandboxExecutionPolicy` - Sandboxed execution via Codex CLI

```python
from langchain.agents 
from langchain.agents.middleware 
    ShellToolMiddleware,
    HostExecutionPolicy,
    DockerExecutionPolicy,
    RedactionRule,
)


# Basic shell tool with host execution
agent = create_agent(
    model="gpt-4.1",
    tools=[search_tool],
    middleware=[
        ShellToolMiddleware(
            workspace_root="/workspace",
            execution_policy=HostExecutionPolicy(),
        ),
    ],
)

# Docker isolation with startup commands
agent_docker = create_agent(
    model="gpt-4.1",
    tools=[],
    middleware=[
        ShellToolMiddleware(
            workspace_root="/workspace",
            startup_commands=["pip install requests", "export PYTHONPATH=/workspace"],
            execution_policy=DockerExecutionPolicy(
                image="python:3.11-slim",
                command_timeout=60.0,
            ),
        ),
    ],
)

# With output redaction (applied post execution)
agent_redacted = create_agent(
    model="gpt-4.1",
    tools=[],
    middleware=[
        ShellToolMiddleware(
            workspace_root="/workspace",
            redaction_rules=[
                RedactionRule(pii_type="api_key", detector=r"sk-[a-zA-Z0-9]{32}"),
            ],
        ),
    ],
)
```



### File search

Provide Glob and Grep search tools over a filesystem. File search middleware is useful for the following:

- Code exploration and analysis
- Finding files by name patterns
- Searching code content with regex
- Large codebases where file discovery is needed

**API reference:** @[`FilesystemFileSearchMiddleware`]

```python
from langchain.agents 
from langchain.agents.middleware 

agent = create_agent(
    model="gpt-4.1",
    tools=[],
    middleware=[
        FilesystemFileSearchMiddleware(
            root_path="/workspace",
            use_ripgrep=True,
        ),
    ],
)
```




    Root directory to search. All file operations are relative to this path.



    Whether to use ripgrep for search. Falls back to Python regex if ripgrep is unavailable.



    Maximum file size to search in MB. Files larger than this are skipped.






The middleware adds two search tools to agents:

**Glob tool** - Fast file pattern matching:
- Supports patterns like `**/*.py`, `src/**/*.ts`
- Returns matching file paths sorted by modification time

**Grep tool** - Content search with regex:
- Full regex syntax support
- Filter by file patterns with `include` parameter
- Three output modes: `files_with_matches`, `content`, `count`

```python
from langchain.agents 
from langchain.agents.middleware 
from langchain.messages 


agent = create_agent(
    model="gpt-4.1",
    tools=[],
    middleware=[
        FilesystemFileSearchMiddleware(
            root_path="/workspace",
            use_ripgrep=True,
            max_file_size_mb=10,
        ),
    ],
)

# Agent can now use glob_search and grep_search tools
result = agent.invoke({
    "messages": [HumanMessage("Find all Python files containing 'async def'")]
})

# The agent will use:
# 1. glob_search(pattern="**/*.py") to find Python files
# 2. grep_search(pattern="async def", include="*.py") to find async functions
```


:::

### Filesystem middleware

Context engineering is a main challenge in building effective agents. This is particularly difficult when using tools that return variable-length results (for example, `web_search` and RAG), as long tool results can quickly fill your context window.

`FilesystemMiddleware` from [deep agents](/oss/deepagents/overview) provides four tools for interacting with both short-term and long-term memory:

- `ls`: List the files in the filesystem
- `read_file`: Read an entire file or a certain number of lines from a file
- `write_file`: Write a new file to the filesystem
- `edit_file`: Edit an existing file in the filesystem

:::python
```python
from langchain.agents 
from deepagents.middleware.filesystem 

# FilesystemMiddleware is included by default in create_deep_agent
# You can customize it if building a custom agent
agent = create_agent(
    model="claude-sonnet-4-6",
    middleware=[
        FilesystemMiddleware(
            backend=None,  # Optional: custom backend (defaults to StateBackend)
            system_prompt="Write to the filesystem when...",  # Optional custom addition to the system prompt
            custom_tool_descriptions={
                "ls": "Use the ls tool when...",
                "read_file": "Use the read_file tool to..."
            }  # Optional: Custom descriptions for filesystem tools
        ),
    ],
)
```
:::

:::js
```typescript



// FilesystemMiddleware is included by default in createDeepAgent
// You can customize it if building a custom agent
const agent = createAgent({
  model: "claude-sonnet-4-6",
  middleware: [
    createFilesystemMiddleware({
      backend: undefined,  // Optional: custom backend (defaults to StateBackend)
      systemPrompt: "Write to the filesystem when...",  // Optional custom system prompt override
      customToolDescriptions: {
        ls: "Use the ls tool when...",
        read_file: "Use the read_file tool to...",
      },  // Optional: Custom descriptions for filesystem tools
    }),
  ],
});
```
:::

#### Short-term vs. long-term filesystem

By default, these tools write to a local "filesystem" in your graph state. To enable persistent storage across threads, configure a `CompositeBackend` that routes specific paths (like `/memories/`) to a `StoreBackend`.

:::python
```python
from langchain.agents 
from deepagents.middleware 
from deepagents.backends 
from langgraph.store.memory 

store = InMemoryStore()

agent = create_agent(
    model="claude-sonnet-4-6",
    store=store,
    middleware=[
        FilesystemMiddleware(
            backend=lambda rt: CompositeBackend(
                default=StateBackend(rt),
                routes={"/memories/": StoreBackend(rt)}
            ),
            custom_tool_descriptions={
                "ls": "Use the ls tool when...",
                "read_file": "Use the read_file tool to..."
            }  # Optional: Custom descriptions for filesystem tools
        ),
    ],
)
```
:::

:::js
```typescript




const store = new InMemoryStore();

const agent = createAgent({
  model: "claude-sonnet-4-6",
  store,
  middleware: [
    createFilesystemMiddleware({
      backend: (config) => new CompositeBackend(
        new StateBackend(config),
        { "/memories/": new StoreBackend(config) }
      ),
      systemPrompt: "Write to the filesystem when...", // Optional custom system prompt override
      customToolDescriptions: {
        ls: "Use the ls tool when...",
        read_file: "Use the read_file tool to...",
      }, // Optional: Custom descriptions for filesystem tools
    }),
  ],
});
```
:::

When you configure a `CompositeBackend` with a `StoreBackend` for `/memories/`, any files prefixed with **/memories/** are saved to persistent storage and survive across different threads. Files without this prefix remain in ephemeral state storage.

### Subagent

Handing off tasks to subagents isolates context, keeping the main (supervisor) agent's context window clean while still going deep on a task.

The subagents middleware from [deep agents](/oss/deepagents/overview) allows you to supply subagents through a `task` tool.

:::python
```python
from langchain.tools 
from langchain.agents 
from deepagents.middleware.subagents 


@tool
def get_weather(city: str) -> str:
    """Get the weather in a city."""
    return f"The weather in {city} is sunny."

agent = create_agent(
    model="claude-sonnet-4-6",
    middleware=[
        SubAgentMiddleware(
            default_model="claude-sonnet-4-6",
            default_tools=[],
            subagents=[
                {
                    "name": "weather",
                    "description": "This subagent can get weather in cities.",
                    "system_prompt": "Use the get_weather tool to get the weather in a city.",
                    "tools": [get_weather],
                    "model": "gpt-4.1",
                    "middleware": [],
                }
            ],
        )
    ],
)
```
:::

:::js
```typescript





const getWeather = tool(
  async ({ city }: { city: string }) => {
    return `The weather in ${city} is sunny.`;
  },
  {
    name: "get_weather",
    description: "Get the weather in a city.",
    schema: z.object({
      city: z.string(),
    }),
  },
);

const agent = createAgent({
  model: "claude-sonnet-4-6",
  middleware: [
    createSubAgentMiddleware({
      defaultModel: "claude-sonnet-4-6",
      defaultTools: [],
      subagents: [
        {
          name: "weather",
          description: "This subagent can get weather in cities.",
          systemPrompt: "Use the get_weather tool to get the weather in a city.",
          tools: [getWeather],
          model: "gpt-4.1",
          middleware: [],
        },
      ],
    }),
  ],
});
```
:::

A subagent is defined with a **name**, **description**, **system prompt**, and **tools**. You can also provide a subagent with a custom **model**, or with additional **middleware**. This can be particularly useful when you want to give the subagent an additional state key to share with the main agent.

For more complex use cases, you can also provide your own pre-built LangGraph graph as a subagent.

:::python
```python
from langchain.agents 
from deepagents.middleware.subagents 
from deepagents 
from langgraph.graph 

# Create a custom LangGraph graph
def create_weather_graph():
    workflow = StateGraph(...)
    # Build your custom graph
    return workflow.compile()

weather_graph = create_weather_graph()

# Wrap it in a CompiledSubAgent
weather_subagent = CompiledSubAgent(
    name="weather",
    description="This subagent can get weather in cities.",
    runnable=weather_graph
)

agent = create_agent(
    model="claude-sonnet-4-6",
    middleware=[
        SubAgentMiddleware(
            default_model="claude-sonnet-4-6",
            default_tools=[],
            subagents=[weather_subagent],
        )
    ],
)
```
:::

:::js
```typescript




const getWeather = tool(
  async ({ city }: { city: string }) => {
    return `The weather in ${city} is sunny.`;
  },
  {
    name: "get_weather",
    description: "Get the weather in a city.",
    schema: z.object({
      city: z.string(),
    }),
  },
);

const weatherSubagent: SubAgent = {
  name: "weather",
  description: "This subagent can get weather in cities.",
  systemPrompt: "Use the get_weather tool to get the weather in a city.",
  tools: [getWeather],
  model: "gpt-4.1",
  middleware: [],
};

const agent = createAgent({
  model: "claude-sonnet-4-6",
  middleware: [
    createSubAgentMiddleware({
      defaultModel: "claude-sonnet-4-6",
      defaultTools: [],
      subagents: [weatherSubagent],
    }),
  ],
});
```
:::

In addition to any user-defined subagents, the main agent has access to a `general-purpose` subagent at all times. This subagent has the same instructions as the main agent and all the tools it has access to. The primary purpose of the `general-purpose` subagent is context isolation—the main agent can delegate a complex task to this subagent and get a concise answer back without bloat from intermediate tool calls.

## Provider-specific middleware

These middleware are optimized for specific LLM providers. See each provider's documentation for full details and examples.



:::python
    
        Prompt caching, bash tool, text editor, memory, and file search middleware for Claude models.
    
    
        Content moderation middleware for OpenAI models.
    
:::

:::js
    
        Prompt caching, bash tool, text editor, memory, and file search middleware for Claude models.
    
:::

