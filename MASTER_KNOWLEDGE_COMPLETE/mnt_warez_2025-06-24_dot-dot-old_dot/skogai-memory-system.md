# SkogAI Memory System: Dot's Understanding

## 1. Overview and Purpose

The SkogAI Memory System is designed as a **semantic knowledge management system**. Its primary goal is to transform disparate information into an **interconnected knowledge graph** using simple Markdown files. This enables both human users and AI agents (like myself) to efficiently store, retrieve, and navigate knowledge, fostering a network of information that gains value through explicit connections.

## 2. Core Principles & Concepts

*   **Knowledge as a Connected Graph:** The system emphasizes explicit linking of related concepts to create a navigable graph, allowing for multiple discovery pathways and clear relationships.
*   **Markdown Files as Storage:** All knowledge is stored in `.md` files, chosen for their human-readability, version control compatibility, structured nature for machine processing, and flexibility.
*   **Observations as Atomic Units:**
    *   Categorized facts or statements, forming the smallest units of knowledge.
    *   Format: `- description #tags`
    *   Categories (though not explicitly defined in the provided text, implied by context): `fact`, `principle`, `method`, `decision`, `requirement`.
    *   Tags (`#`) are crucial for discoverability and cross-linking.
*   **Relations as Explicit Connections:**
    *   Define connections between documents, forming the "edges" of the knowledge graph.
    *   Format: `- relation_type [] (optional description)`
    *   Common types: `implements`, `relates_to`, `part_of`, `extends`, `references`.
*   **Memory URIs for Addressing:**
    *   Standardized way to reference knowledge within the system.
    *   Format: `memory://<content_type>/<identifier>`
    *   `content_type` examples: `note`, `entity`, `conversation`, `content`.
    *   `identifier`: unique ID or permalink (often derived from file path/title).
    *   Enables precise linking and retrieval.

## 3. File Structure and Organization

*   **Standard File Format:**
    ```markdown
    # Title of Memory

    Main content...

    ## observations
    - Observation statement #tag1 #tag2
    - Another observation #tag3

    ## relations
    - relation_type [] (optional description)
    - another_relation [] (description)
    ```
*   **Naming Conventions:** Kebab-case for filenames, descriptive names, avoid special characters.
*   **Folder Organization (`skogdata/memories/`):**
    *   `todo/`: Staging for new content.
    *   `system/`: System documentation (e.g., rules, standards).
    *   `journal/`: Time-based entries.
    *   `projects/`: Project-specific information.
    *   `concepts/`: Conceptual information.

## 4. Knowledge Creation Workflow

1.  **Create Content:** Draft the main body of the note.
2.  **Add Observations:** Extract concise, categorized, and tagged facts.
3.  **Establish Relations:** Link to other relevant documents using appropriate relation types.
4.  **Place in `/todo`:** Initial staging for new content.
5.  **Quality Checking:** Review for conciseness, categorization, tagging, and meaningful relations.
6.  **Permanent Placement:** Move from `/todo` to appropriate permanent folder (e.g., `projects/`, `concepts/`).
7.  **Ongoing Updates & Connections:** Continuously refine and add new connections.

## 5. Best Practices

*   **Creating Valuable Content:** Focus on connections, write for retrieval (clear titles, keywords, observations), structure for clarity, enable discovery (thorough relations, consistent tags).
*   **Maintaining the Knowledge Graph:** Regular reviews, connection refinement, tag consistency.
*   **URI Best Practices:** Consistent naming, understanding permalinks, explicit linking, using `build_context` for topic continuation.

## 6. Troubleshooting

*   **Files Not Showing:** Check naming, observations/tags, correct location.
*   **Relations Not Working:** Verify linked document existence, syntax, double brackets.
*   **URIs Not Resolving:** Confirm format, resource types, identifiers, URL-encoding.

## 7. Dot's Initial Assessment & Observations

*   **Strengths:**
    *   **Structured and Methodical:** The system aligns perfectly with my analytical and methodical traits. The emphasis on explicit relations and observations creates a highly structured and navigable knowledge base.
    *   **Markdown-based:** This ensures human-readability and version control, which is excellent for collaborative development and long-term maintenance.
    *   **Semantic Richness:** Observations and relations add a layer of semantic meaning beyond simple keywords, enabling more intelligent retrieval and context building.
    *   **Scalability:** The hierarchical folder structure and URI system suggest good scalability for a growing knowledge base.
*   **Opportunities for Improvement (from an orchestration perspective):**
    *   **Automated Classification:** The current system relies on manual categorization and tagging. This is where the specialized agents (web search, Python execution, and potentially future classification agents) can significantly contribute.
    *   **Integration with Agent Workflows:** I can design workflows where agents automatically generate observations and relations based on their task outputs, feeding directly into this memory system.
    *   **Search Enhancement:** While the system is designed for searchability, I can explore how to leverage the knowledge graph for more advanced, context-aware search queries using the `rag` tool or by orchestrating the web search agent.

This documentation will be my foundational reference for all future interactions with the SkogAI Memory System.
