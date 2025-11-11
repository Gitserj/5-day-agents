# 5-Day AI Agents Intensive Course with Google!

## Day 1 🚀 Multi-Agent Systems & Workflow Patterns

### 🚥 Sequential Workflows - The Assembly Line

**The Problem: Unpredictable Order**

The previous multi-agent system worked, but it relied on a **detailed instruction prompt** to force the LLM to run steps in order. This can be unreliable. A complex LLM might decide to skip a step, run them in the wrong order, or get "stuck," making the process unpredictable.

**The Solution: A Fixed Pipeline**

When you need tasks to happen in a **guaranteed, specific order**, you can use a `SequentialAgent`. This agent acts like an assembly line, running each sub-agent in the exact order you list them. The output of one agent automatically becomes the input for the next, creating a predictable and reliable workflow.

**Use Sequential when:** Order matters, you need a linear pipeline, or each step builds on the previous one.

To learn more, check out the documentation related to [sequential agents in ADK](https://google.github.io/adk-docs/agents/workflow-agents/sequential-agents/).

**Architecture: Blog Post Creation Pipeline**

```mermaid
flowchart LR
    A["User Input: Blog about AI"] --> B["Outline Agent"]
    B -->|blog_outline| C["Writer Agent"]
    C -->|blog_draft| D["Editor Agent"]
    D -->|final_blog| E["Output"]

    style B fill:#ffcccc
    style C fill:#ccffcc
    style D fill:#ccccff
```

**[Example: blog_writer/agent.py](blog_writer/agent.py)**


### 🛣️ Parallel Workflows - Independent Researchers

**The Problem: The Bottleneck**

The previous sequential agent is great, but it's an assembly line. Each step must wait for the previous one to finish. What if you have several tasks that are **not dependent** on each other? For example, researching three *different* topics. Running them in sequence would be slow and inefficient, creating a bottleneck where each task waits unnecessarily.

**The Solution: Concurrent Execution**

When you have independent tasks, you can run them all at the same time using a `ParallelAgent`. This agent executes all of its sub-agents concurrently, dramatically speeding up the workflow. Once all parallel tasks are complete, you can then pass their combined results to a final 'aggregator' step.

**Use Parallel when:** Tasks are independent, speed matters, and you can execute concurrently.

To learn more, check out the documentation related to [parallel agents in ADK](https://google.github.io/adk-docs/agents/workflow-agents/parallel-agents/).

**Architecture: Multi-Topic Research**

```mermaid
flowchart
    A["User Request: Research 3 topics"] --> B["Parallel Execution"]
    B --> C["Tech Researcher"]
    B --> D["Health Researcher"]
    B --> E["Finance Researcher"]

    C --> F["Aggregator"]
    D --> F
    E --> F
    F --> G["Combined Report"]

    style B fill:#ffffcc
    style F fill:#ffccff
```

**[Example: researcher/agent.py](researcher/agent.py)**


### ➰ Loop Workflows - The Refinement Cycle

**The Problem: One-Shot Quality**

All the workflows we've seen so far run from start to finish. The `SequentialAgent` and `ParallelAgent` produce their final output and then stop. This 'one-shot' approach isn't good for tasks that require refinement and quality control. What if the first draft of our story is bad? We have no way to review it and ask for a rewrite.

**The Solution: Iterative Refinement**

When a task needs to be improved through cycles of feedback and revision, you can use a `LoopAgent`. A `LoopAgent` runs a set of sub-agents repeatedly *until a specific condition is met or a maximum number of iterations is reached.* This creates a refinement cycle, allowing the agent system to improve its own work over and over.

**Use Loop when:** Iterative improvement is needed, quality refinement matters, or you need repeated cycles.

To learn more, check out the documentation related to [loop agents in ADK](https://google.github.io/adk-docs/agents/workflow-agents/loop-agents/).

**Architecture: Story Writing & Critique Loop**

```mermaid
flowchart
    A[Initial Prompt] --> B[Writer Agent]
    B -->|story| C[Critic Agent]
    C -->|critique| D{Iteration < Max<br>AND<br>Not Approved?}
    D -->|Yes| B
    D -->|No| E[Final Story]

    style B fill:#ccffcc
    style C fill:#ffcccc
    style D fill:#ffffcc
```

**[Example: story_writer/agent.py](story_writer/agent.py)**


### Choosing the Right Pattern

#### Decision Tree: Which Workflow Pattern?
```mermaid
flowchart LR
    A{"What kind of workflow do you need?"} --> B["Fixed Pipeline<br>(A → B → C)"];
    A --> C["Concurrent Tasks<br>(Run A, B, C all at once)"];
    A --> D["Iterative Refinement<br>(A ⇆ B)"];
    A --> E["Dynamic Decisions<br>(Let the LLM decide what to do)"];

    B --> B_S["Use <b>SequentialAgent</b>"];
    C --> C_S["Use <b>ParallelAgent</b>"];
    D --> D_S["Use <b>LoopAgent</b>"];
    E --> E_S["Use <b>LLM Orchestrator</b><br>(Agent with other agents as tools)"];

    style B_S fill:#f9f,stroke:#333,stroke-width:2px
    style C_S fill:#ccf,stroke:#333,stroke-width:2px
    style D_S fill:#cff,stroke:#333,stroke-width:2px
    style E_S fill:#cfc,stroke:#333,stroke-width:2px
```

#### Quick Reference Table

| Pattern                    | When to Use                      | Example                                             | Key Feature              |
| -------------------------- | -------------------------------- | --------------------------------------------------- | ------------------------ |
| **LLM-based (sub_agents)** | Dynamic orchestration needed     | [Research + Summarize]()                            | LLM decides what to call |
| **Sequential**             | Order matters, linear pipeline   | [Outline → Write → Edit](blog_writer/agent.py)      | Deterministic order      |
| **Parallel**               | Independent tasks, speed matters | [Multi-topic research](researcher/agent.py)         | Concurrent execution     |
| **Loop**                   | Iterative improvement needed     | [Writer + Critic refinement](story_writer/agent.py) | Repeated cycles          |