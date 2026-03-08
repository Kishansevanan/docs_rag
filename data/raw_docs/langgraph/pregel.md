---
title: LangGraph runtime
sidebarTitle: Runtime
---



:::python
@[`Pregel`] implements LangGraph's runtime, managing the execution of LangGraph applications.

Compiling a @[StateGraph][StateGraph] or creating an @[`@entrypoint`] produces a @[`Pregel`] instance that can be invoked with input.
:::

:::js
@[`Pregel`] implements LangGraph's runtime, managing the execution of LangGraph applications.

Compiling a @[StateGraph][StateGraph] or creating an @[entrypoint][entrypoint] produces a @[`Pregel`] instance that can be invoked with input.
:::

This guide explains the runtime at a high level and provides instructions for directly implementing applications with Pregel.

:::python
> **Note:** The @[`Pregel`] runtime is named after [Google's Pregel algorithm](https://research.google/pubs/pub37252/), which describes an efficient method for large-scale parallel computation using graphs.
:::

:::js
> **Note:** The @[`Pregel`] runtime is named after [Google's Pregel algorithm](https://research.google/pubs/pub37252/), which describes an efficient method for large-scale parallel computation using graphs.
:::

## Overview

In LangGraph, Pregel combines [**actors**](https://en.wikipedia.org/wiki/Actor_model) and **channels** into a single application. **Actors** read data from channels and write data to channels. Pregel organizes the execution of the application into multiple steps, following the **Pregel Algorithm**/**Bulk Synchronous Parallel** model.

Each step consists of three phases:

* **Plan**: Determine which **actors** to execute in this step. For example, in the first step, select the **actors** that subscribe to the special **input** channels; in subsequent steps, select the **actors** that subscribe to channels updated in the previous step.
* **Execution**: Execute all selected **actors** in parallel, until all complete, or one fails, or a timeout is reached. During this phase, channel updates are invisible to actors until the next step.
* **Update**: Update the channels with the values written by the **actors** in this step.

Repeat until no **actors** are selected for execution, or a maximum number of steps is reached.

## Actors

An **actor** is a `PregelNode`. It subscribes to channels, reads data from them, and writes data to them. It can be thought of as an **actor** in the Pregel algorithm. `PregelNodes` implement LangChain's Runnable interface.

## Channels

Channels are used to communicate between actors (PregelNodes). Each channel has a value type, an update type, and an update function – which takes a sequence of updates and modifies the stored value. Channels can be used to send data from one chain to another, or to send data from a chain to itself in a future step. LangGraph provides a number of built-in channels:

:::python
* @[`LastValue`]: The default channel, stores the last value sent to the channel, useful for input and output values, or for sending data from one step to the next.
* @[`Topic`]: A configurable PubSub Topic, useful for sending multiple values between **actors**, or for accumulating output. Can be configured to deduplicate values or to accumulate values over the course of multiple steps.
* @[`BinaryOperatorAggregate`]: stores a persistent value, updated by applying a binary operator to the current value and each update sent to the channel, useful for computing aggregates over multiple steps; e.g.,`total = BinaryOperatorAggregate(int, operator.add)`
:::

:::js
* @[`LastValue`]: The default channel, stores the last value sent to the channel, useful for input and output values, or for sending data from one step to the next.
* @[`Topic`]: A configurable PubSub Topic, useful for sending multiple values between **actors**, or for accumulating output. Can be configured to deduplicate values or to accumulate values over the course of multiple steps.
* @[`BinaryOperatorAggregate`]: stores a persistent value, updated by applying a binary operator to the current value and each update sent to the channel, useful for computing aggregates over multiple steps; e.g.,`total = BinaryOperatorAggregate(int, operator.add)`
:::

## Examples

:::python
While most users will interact with Pregel through the @[StateGraph][StateGraph] API or the @[`@entrypoint`] decorator, it is possible to interact with Pregel directly.
:::

:::js
While most users will interact with Pregel through the @[StateGraph] API or the @[entrypoint] decorator, it is possible to interact with Pregel directly.
:::

Below are a few different examples to give you a sense of the Pregel API.


    
    :::python
    ```python
    from langgraph.channels 
    from langgraph.pregel 

    node1 = (
        NodeBuilder().subscribe_only("a")
        .do(lambda x: x + x)
        .write_to("b")
    )

    app = Pregel(
        nodes={"node1": node1},
        channels={
            "a": EphemeralValue(str),
            "b": EphemeralValue(str),
        },
        input_channels=["a"],
        output_channels=["b"],
    )

    app.invoke({"a": "foo"})
    ```

    ```con
    {'b': 'foofoo'}
    ```
    :::

    :::js
    ```typescript
    
    

    const node1 = new NodeBuilder()
      .subscribeOnly("a")
      .do((x: string) => x + x)
      .writeTo("b");

    const app = new Pregel({
      nodes: { node1 },
      channels: {
        a: new EphemeralValue(),
        b: new EphemeralValue(),
      },
      inputChannels: ["a"],
      outputChannels: ["b"],
    });

    await app.invoke({ a: "foo" });
    ```

    ```console
    { b: 'foofoo' }
    ```
    :::
    
    
    :::python
    ```python
    from langgraph.channels 
    from langgraph.pregel 

    node1 = (
        NodeBuilder().subscribe_only("a")
        .do(lambda x: x + x)
        .write_to("b")
    )

    node2 = (
        NodeBuilder().subscribe_only("b")
        .do(lambda x: x + x)
        .write_to("c")
    )


    app = Pregel(
        nodes={"node1": node1, "node2": node2},
        channels={
            "a": EphemeralValue(str),
            "b": LastValue(str),
            "c": EphemeralValue(str),
        },
        input_channels=["a"],
        output_channels=["b", "c"],
    )

    app.invoke({"a": "foo"})
    ```

    ```con
    {'b': 'foofoo', 'c': 'foofoofoofoo'}
    ```
    :::

    :::js
    ```typescript
    
    

    const node1 = new NodeBuilder()
      .subscribeOnly("a")
      .do((x: string) => x + x)
      .writeTo("b");

    const node2 = new NodeBuilder()
      .subscribeOnly("b")
      .do((x: string) => x + x)
      .writeTo("c");

    const app = new Pregel({
      nodes: { node1, node2 },
      channels: {
        a: new EphemeralValue(),
        b: new LastValue(),
        c: new EphemeralValue(),
      },
      inputChannels: ["a"],
      outputChannels: ["b", "c"],
    });

    await app.invoke({ a: "foo" });
    ```

    ```console
    { b: 'foofoo', c: 'foofoofoofoo' }
    ```
    :::
    
    
    :::python
    ```python
    from langgraph.channels 
    from langgraph.pregel 

    node1 = (
        NodeBuilder().subscribe_only("a")
        .do(lambda x: x + x)
        .write_to("b", "c")
    )

    node2 = (
        NodeBuilder().subscribe_to("b")
        .do(lambda x: x["b"] + x["b"])
        .write_to("c")
    )

    app = Pregel(
        nodes={"node1": node1, "node2": node2},
        channels={
            "a": EphemeralValue(str),
            "b": EphemeralValue(str),
            "c": Topic(str, accumulate=True),
        },
        input_channels=["a"],
        output_channels=["c"],
    )

    app.invoke({"a": "foo"})
    ```

    ```pycon
    {'c': ['foofoo', 'foofoofoofoo']}
    ```
    :::

    :::js
    ```typescript
    
    

    const node1 = new NodeBuilder()
      .subscribeOnly("a")
      .do((x: string) => x + x)
      .writeTo("b", "c");

    const node2 = new NodeBuilder()
      .subscribeTo("b")
      .do((x: { b: string }) => x.b + x.b)
      .writeTo("c");

    const app = new Pregel({
      nodes: { node1, node2 },
      channels: {
        a: new EphemeralValue(),
        b: new EphemeralValue(),
        c: new Topic({ accumulate: true }),
      },
      inputChannels: ["a"],
      outputChannels: ["c"],
    });

    await app.invoke({ a: "foo" });
    ```

    ```console
    { c: ['foofoo', 'foofoofoofoo'] }
    ```
    :::
    
    
    This example demonstrates how to use the @[`BinaryOperatorAggregate`] channel to implement a reducer.

    :::python
    ```python
    from langgraph.channels 
    from langgraph.pregel 


    node1 = (
        NodeBuilder().subscribe_only("a")
        .do(lambda x: x + x)
        .write_to("b", "c")
    )

    node2 = (
        NodeBuilder().subscribe_only("b")
        .do(lambda x: x + x)
        .write_to("c")
    )

    def reducer(current, update):
        if current:
            return current + " | " + update
        else:
            return update

    app = Pregel(
        nodes={"node1": node1, "node2": node2},
        channels={
            "a": EphemeralValue(str),
            "b": EphemeralValue(str),
            "c": BinaryOperatorAggregate(str, operator=reducer),
        },
        input_channels=["a"],
        output_channels=["c"],
    )

    app.invoke({"a": "foo"})
    ```
    :::

    :::js
    ```typescript
    
    

    const node1 = new NodeBuilder()
      .subscribeOnly("a")
      .do((x: string) => x + x)
      .writeTo("b", "c");

    const node2 = new NodeBuilder()
      .subscribeOnly("b")
      .do((x: string) => x + x)
      .writeTo("c");

    const reducer = (current: string, update: string) => {
      if (current) {
        return current + " | " + update;
      } else {
        return update;
      }
    };

    const app = new Pregel({
      nodes: { node1, node2 },
      channels: {
        a: new EphemeralValue(),
        b: new EphemeralValue(),
        c: new BinaryOperatorAggregate({ operator: reducer }),
      },
      inputChannels: ["a"],
      outputChannels: ["c"],
    });

    await app.invoke({ a: "foo" });
    ```
    :::
    
    
    :::python
    This example demonstrates how to introduce a cycle in the graph, by having
    a chain write to a channel it subscribes to. Execution will continue
    until a `None` value is written to the channel.

    ```python
    from langgraph.channels 
    from langgraph.pregel 

    example_node = (
        NodeBuilder().subscribe_only("value")
        .do(lambda x: x + x if len(x) < 10 else None)
        .write_to(ChannelWriteEntry("value", skip_none=True))
    )

    app = Pregel(
        nodes={"example_node": example_node},
        channels={
            "value": EphemeralValue(str),
        },
        input_channels=["value"],
        output_channels=["value"],
    )

    app.invoke({"value": "a"})
    ```

    ```pycon
    {'value': 'aaaaaaaaaaaaaaaa'}
    ```
    :::

    :::js
    This example demonstrates how to introduce a cycle in the graph, by having
    a chain write to a channel it subscribes to. Execution will continue
    until a `null` value is written to the channel.

    ```typescript
    
    

    const exampleNode = new NodeBuilder()
      .subscribeOnly("value")
      .do((x: string) => x.length < 10 ? x + x : null)
      .writeTo(new ChannelWriteEntry("value", { skipNone: true }));

    const app = new Pregel({
      nodes: { exampleNode },
      channels: {
        value: new EphemeralValue(),
      },
      inputChannels: ["value"],
      outputChannels: ["value"],
    });

    await app.invoke({ value: "a" });
    ```

    ```console
    { value: 'aaaaaaaaaaaaaaaa' }
    ```
    :::
    


## High-level API

LangGraph provides two high-level APIs for creating a Pregel application: the [StateGraph (Graph API)](/oss/langgraph/graph-api) and the [Functional API](/oss/langgraph/functional-api).


    
    :::python
    The @[StateGraph (Graph API)][StateGraph] is a higher-level abstraction that simplifies the creation of Pregel applications. It allows you to define a graph of nodes and edges. When you compile the graph, the StateGraph API automatically creates the Pregel application for you.

    ```python
    from typing 

    from langgraph.constants 
    from langgraph.graph 

    class Essay(TypedDict):
        topic: str
        content: str | None
        score: float | None

    def write_essay(essay: Essay):
        return {
            "content": f"Essay about {essay['topic']}",
        }

    def score_essay(essay: Essay):
        return {
            "score": 10
        }

    builder = StateGraph(Essay)
    builder.add_node(write_essay)
    builder.add_node(score_essay)
    builder.add_edge(START, "write_essay")
    builder.add_edge("write_essay", "score_essay")

    # Compile the graph.
    # This will return a Pregel instance.
    graph = builder.compile()
    ```
    :::

    :::js
    The @[StateGraph (Graph API)][StateGraph] is a higher-level abstraction that simplifies the creation of Pregel applications. It allows you to define a graph of nodes and edges. When you compile the graph, the StateGraph API automatically creates the Pregel application for you.

    ```typescript
    

    interface Essay {
      topic: string;
      content?: string;
      score?: number;
    }

    const writeEssay = (essay: Essay) => {
      return {
        content: `Essay about ${essay.topic}`,
      };
    };

    const scoreEssay = (essay: Essay) => {
      return {
        score: 10
      };
    };

    const builder = new StateGraph({
      channels: {
        topic: null,
        content: null,
        score: null,
      }
    })
      .addNode("writeEssay", writeEssay)
      .addNode("scoreEssay", scoreEssay)
      .addEdge(START, "writeEssay")
      .addEdge("writeEssay", "scoreEssay");

    // Compile the graph.
    // This will return a Pregel instance.
    const graph = builder.compile();
    ```
    :::

    The compiled Pregel instance will be associated with a list of nodes and channels. You can inspect the nodes and channels by printing them.

    :::python
    ```python
    print(graph.nodes)
    ```

    You will see something like this:

    ```pycon
    {'__start__': ,
     'write_essay': ,
     'score_essay': }
    ```

    ```python
    print(graph.channels)
    ```

    You should see something like this

    ```pycon
    {'topic': ,
     'content': ,
     'score': ,
     '__start__': ,
     'write_essay': ,
     'score_essay': ,
     'branch:__start__:__self__:write_essay': ,
     'branch:__start__:__self__:score_essay': ,
     'branch:write_essay:__self__:write_essay': ,
     'branch:write_essay:__self__:score_essay': ,
     'branch:score_essay:__self__:write_essay': ,
     'branch:score_essay:__self__:score_essay': ,
     'start:write_essay': }
    ```
    :::

    :::js
    ```typescript
    console.log(graph.nodes);
    ```

    You will see something like this:

    ```console
    {
      __start__: PregelNode { ... },
      writeEssay: PregelNode { ... },
      scoreEssay: PregelNode { ... }
    }
    ```

    ```typescript
    console.log(graph.channels);
    ```

    You should see something like this

    ```console
    {
      topic: LastValue { ... },
      content: LastValue { ... },
      score: LastValue { ... },
      __start__: EphemeralValue { ... },
      writeEssay: EphemeralValue { ... },
      scoreEssay: EphemeralValue { ... },
      'branch:__start__:__self__:writeEssay': EphemeralValue { ... },
      'branch:__start__:__self__:scoreEssay': EphemeralValue { ... },
      'branch:writeEssay:__self__:writeEssay': EphemeralValue { ... },
      'branch:writeEssay:__self__:scoreEssay': EphemeralValue { ... },
      'branch:scoreEssay:__self__:writeEssay': EphemeralValue { ... },
      'branch:scoreEssay:__self__:scoreEssay': EphemeralValue { ... },
      'start:writeEssay': EphemeralValue { ... }
    }
    ```
    :::
    
    
    :::python
    In the [Functional API](/oss/langgraph/functional-api), you can use an @[`@entrypoint`] to create a Pregel application. The `entrypoint` decorator allows you to define a function that takes input and returns output.

    ```python
    from typing 

    from langgraph.checkpoint.memory 
    from langgraph.func 

    class Essay(TypedDict):
        topic: str
        content: str | None
        score: float | None


    checkpointer = InMemorySaver()

    @entrypoint(checkpointer=checkpointer)
    def write_essay(essay: Essay):
        return {
            "content": f"Essay about {essay['topic']}",
        }

    print("Nodes: ")
    print(write_essay.nodes)
    print("Channels: ")
    print(write_essay.channels)
    ```

    ```pycon
    Nodes:
    {'write_essay': }
    Channels:
    {'__start__': , '__end__': , '__previous__': }
    ```
    :::

    :::js
    In the [Functional API](/oss/langgraph/functional-api), you can use an @[`entrypoint`][entrypoint] to create a Pregel application. The `entrypoint` decorator allows you to define a function that takes input and returns output.

    ```typescript
    
    

    interface Essay {
      topic: string;
      content?: string;
      score?: number;
    }

    const checkpointer = new MemorySaver();

    const writeEssay = entrypoint(
      { checkpointer, name: "writeEssay" },
      async (essay: Essay) => {
        return {
          content: `Essay about ${essay.topic}`,
        };
      }
    );

    console.log("Nodes: ");
    console.log(writeEssay.nodes);
    console.log("Channels: ");
    console.log(writeEssay.channels);
    ```

    ```console
    Nodes:
    { writeEssay: PregelNode { ... } }
    Channels:
    {
      __start__: EphemeralValue { ... },
      __end__: LastValue { ... },
      __previous__: LastValue { ... }
    }
    ```
    :::
    

