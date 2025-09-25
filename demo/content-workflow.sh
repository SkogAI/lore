#!/bin/bash

# Content Creation Demo Workflow for SkogAI

# Get the current timestamp for this session
SESSION_ID=$(date +%s)
DEMO_DIR="/home/skogix/skogai/demo/content_creation_$SESSION_ID"
mkdir -p $DEMO_DIR

# Create a new context for this session
echo "Creating new session context..."
echo "Simulating: /home/skogix/skogai/tools/context-manager.sh create base content-creation"
CONTEXT_ID=$SESSION_ID

# Get topic from user
TOPIC=$1
if [ -z "$TOPIC" ]; then
  read -p "Enter a topic for content creation: " TOPIC
fi

echo "Topic: $TOPIC" > $DEMO_DIR/request.txt
echo "Starting content creation workflow for topic: $TOPIC"

# RESEARCH PHASE
echo "===== RESEARCH PHASE ====="
echo "Activating Research Agent..."
RESEARCH_PROMPT=$(cat /home/skogix/skogai/agents/implementations/content/research-agent.md)

# In a real implementation, this would call an LLM API with the research prompt
echo "Generating research data..."
echo '{
  "topic": "'"$TOPIC"'",
  "key_facts": [
    "This is a simulated key fact about '"$TOPIC"'",
    "This is another key fact about '"$TOPIC"'",
    "This is a third important fact about '"$TOPIC"'"
  ],
  "main_concepts": [
    {
      "name": "Main concept of '"$TOPIC"'",
      "definition": "Definition of this concept",
      "importance": "Why this concept matters to '"$TOPIC"'"
    },
    {
      "name": "Secondary concept",
      "definition": "Definition of second concept",
      "importance": "Relevance to '"$TOPIC"'"
    }
  ],
  "relationships": [
    "How main concepts relate to each other",
    "Historical or logical progression of concepts"
  ],
  "potential_sections": [
    "Introduction to '"$TOPIC"'",
    "Historical background",
    "Main elements of '"$TOPIC"'",
    "Practical applications",
    "Future developments"
  ],
  "sources": [
    {
      "title": "Simulated source 1",
      "key_contribution": "Provides historical context"
    },
    {
      "title": "Simulated source 2",
      "key_contribution": "Offers technical details"
    }
  ],
  "confidence": 85
}' > $DEMO_DIR/research_output.json

echo "Research completed with 85% confidence."

# OUTLINE PHASE
echo "===== OUTLINE PHASE ====="
echo "Activating Outline Agent..."
OUTLINE_PROMPT=$(cat /home/skogix/skogai/agents/implementations/content/outline-agent.md)

# In a real implementation, this would call an LLM API with the outline prompt
# and the research data as context
echo "Generating content outline..."
echo '{
  "title": "Comprehensive Guide to '"$TOPIC"'",
  "target_audience": "General audience with basic interest in '"$TOPIC"'",
  "purpose": "To inform and educate about '"$TOPIC"'",
  "structure": [
    {
      "section_title": "Introduction to '"$TOPIC"'",
      "key_points": [
        "Opening with engaging hook about '"$TOPIC"'",
        "Why '"$TOPIC"' matters",
        "What reader will learn"
      ],
      "target_length": "2-3 paragraphs",
      "research_references": [
        "Use key_facts[0] for opening statement"
      ]
    },
    {
      "section_title": "Background and Context",
      "key_points": [
        "Historical development of '"$TOPIC"'",
        "Evolution of understanding",
        "Current relevance"
      ],
      "target_length": "3-4 paragraphs",
      "research_references": [
        "Include main_concepts[0] definition",
        "Reference sources[0] for historical context"
      ]
    },
    {
      "section_title": "Key Elements of '"$TOPIC"'",
      "key_points": [
        "Main component 1",
        "Main component 2",
        "How components interact"
      ],
      "target_length": "4-5 paragraphs",
      "research_references": [
        "Use relationships[0] to explain interactions",
        "Connect to main_concepts[1]"
      ]
    },
    {
      "section_title": "Applications and Implications",
      "key_points": [
        "Practical uses of '"$TOPIC"'",
        "Impact on related fields",
        "Future potential"
      ],
      "target_length": "3-4 paragraphs",
      "research_references": [
        "Build on key_facts[2]",
        "Reference sources[1] for technical applications"
      ]
    },
    {
      "section_title": "Conclusion",
      "key_points": [
        "Summary of key points",
        "Importance of continued learning about '"$TOPIC"'",
        "Final thought or call to action"
      ],
      "target_length": "2 paragraphs",
      "research_references": [
        "Reinforce main_concepts importance"
      ]
    }
  ],
  "flow_notes": [
    "Use transitional phrases between sections to maintain flow",
    "Gradually increase technical depth as content progresses"
  ],
  "confidence": 90,
  "areas_for_expansion": [
    "Could expand Applications section if more practical examples needed",
    "Historical section could be expanded for academic audience"
  ]
}' > $DEMO_DIR/outline_output.json

echo "Outline completed with 90% confidence."

# WRITING PHASE
echo "===== WRITING PHASE ====="
echo "Activating Writing Agent..."
WRITING_PROMPT=$(cat /home/skogix/skogai/agents/implementations/content/writing-agent.md)

# In a real implementation, this would call an LLM API with the writing prompt
# plus the research and outline as context
echo "Generating written content..."
# This would normally be much longer, but simplified for demo
echo '{
  "title": "Comprehensive Guide to '"$TOPIC"'",
  "content_sections": [
    {
      "section_title": "Introduction to '"$TOPIC"'",
      "content": "Have you ever wondered about the fascinating world of '"$TOPIC"'? This guide will take you on a journey through the key concepts, historical development, and practical applications of this important subject. Whether youre new to '"$TOPIC"' or looking to deepen your understanding, youll find valuable insights in the following sections.\n\nAs we explore '"$TOPIC"' together, youll discover why this subject continues to captivate experts and novices alike, and how understanding it can enhance your perspective on related fields.",
      "word_count": 75
    },
    {
      "section_title": "Background and Context",
      "content": "The history of '"$TOPIC"' dates back to [simulated historical context]. Over time, our understanding has evolved significantly, shaped by discoveries, technological advances, and changing perspectives.\n\nIn its earliest forms, '"$TOPIC"' was understood primarily through [simulated historical understanding]. Modern interpretations have broadened this view, incorporating elements from [simulated related fields].\n\nToday, '"$TOPIC"' stands as a critical component of [simulated current relevance], influencing how we approach [simulated applications].",
      "word_count": 85
    },
    {
      "section_title": "Key Elements of '"$TOPIC"'",
      "content": "[Simulated content about key components of '"$TOPIC"']",
      "word_count": 120
    },
    {
      "section_title": "Applications and Implications",
      "content": "[Simulated content about applications and implications]",
      "word_count": 110
    },
    {
      "section_title": "Conclusion",
      "content": "[Simulated conclusion content]",
      "word_count": 65
    }
  ],
  "total_word_count": 455,
  "reading_level": "General audience",
  "stylistic_notes": [
    "Conversational tone used throughout",
    "Technical terms explained when introduced"
  ],
  "sources_used": [
    "Simulated source 1",
    "Simulated source 2"
  ],
  "confidence": 88
}' > $DEMO_DIR/writing_output.json

echo "Writing completed with 88% confidence."

# FINAL OUTPUT
echo "===== GENERATING FINAL CONTENT ====="
echo "Orchestrator integrating all components..."

# Create a final markdown document from the writing agent's output
echo "# Comprehensive Guide to $TOPIC" > $DEMO_DIR/final_content.md
echo "" >> $DEMO_DIR/final_content.md
echo "## Introduction to $TOPIC" >> $DEMO_DIR/final_content.md
echo "" >> $DEMO_DIR/final_content.md
echo "Have you ever wondered about the fascinating world of $TOPIC? This guide will take you on a journey through the key concepts, historical development, and practical applications of this important subject. Whether you're new to $TOPIC or looking to deepen your understanding, you'll find valuable insights in the following sections." >> $DEMO_DIR/final_content.md
echo "" >> $DEMO_DIR/final_content.md
echo "As we explore $TOPIC together, you'll discover why this subject continues to captivate experts and novices alike, and how understanding it can enhance your perspective on related fields." >> $DEMO_DIR/final_content.md
echo "" >> $DEMO_DIR/final_content.md
echo "## Background and Context" >> $DEMO_DIR/final_content.md
echo "" >> $DEMO_DIR/final_content.md
echo "The history of $TOPIC dates back to [simulated historical context]. Over time, our understanding has evolved significantly, shaped by discoveries, technological advances, and changing perspectives." >> $DEMO_DIR/final_content.md
echo "" >> $DEMO_DIR/final_content.md
echo "In its earliest forms, $TOPIC was understood primarily through [simulated historical understanding]. Modern interpretations have broadened this view, incorporating elements from [simulated related fields]." >> $DEMO_DIR/final_content.md
echo "" >> $DEMO_DIR/final_content.md
echo "Today, $TOPIC stands as a critical component of [simulated current relevance], influencing how we approach [simulated applications]." >> $DEMO_DIR/final_content.md
echo "" >> $DEMO_DIR/final_content.md
echo "## Key Elements of $TOPIC" >> $DEMO_DIR/final_content.md
echo "" >> $DEMO_DIR/final_content.md
echo "[Simulated content about key components of $TOPIC]" >> $DEMO_DIR/final_content.md
echo "" >> $DEMO_DIR/final_content.md
echo "## Applications and Implications" >> $DEMO_DIR/final_content.md
echo "" >> $DEMO_DIR/final_content.md
echo "[Simulated content about applications and implications]" >> $DEMO_DIR/final_content.md
echo "" >> $DEMO_DIR/final_content.md
echo "## Conclusion" >> $DEMO_DIR/final_content.md
echo "" >> $DEMO_DIR/final_content.md
echo "[Simulated conclusion content]" >> $DEMO_DIR/final_content.md
echo "" >> $DEMO_DIR/final_content.md

# Create a workflow summary
echo "===== WORKFLOW SUMMARY =====" > $DEMO_DIR/workflow_summary.txt
echo "Topic: $TOPIC" >> $DEMO_DIR/workflow_summary.txt
echo "Session ID: $SESSION_ID" >> $DEMO_DIR/workflow_summary.txt
echo "Timestamp: $(date)" >> $DEMO_DIR/workflow_summary.txt
echo "" >> $DEMO_DIR/workflow_summary.txt
echo "Agent Performance:" >> $DEMO_DIR/workflow_summary.txt
echo "- Research Agent: 85% confidence" >> $DEMO_DIR/workflow_summary.txt
echo "- Outline Agent: 90% confidence" >> $DEMO_DIR/workflow_summary.txt
echo "- Writing Agent: 88% confidence" >> $DEMO_DIR/workflow_summary.txt
echo "" >> $DEMO_DIR/workflow_summary.txt
echo "Content Statistics:" >> $DEMO_DIR/workflow_summary.txt
echo "- Total word count: 455" >> $DEMO_DIR/workflow_summary.txt
echo "- Sections: 5" >> $DEMO_DIR/workflow_summary.txt
echo "- Reading level: General audience" >> $DEMO_DIR/workflow_summary.txt
echo "" >> $DEMO_DIR/workflow_summary.txt
echo "Workflow path: Research → Outline → Writing → Final Integration" >> $DEMO_DIR/workflow_summary.txt

# Archive context for this session
echo "Archiving session context..."
echo "Simulating: /home/skogix/skogai/tools/context-manager.sh archive $SESSION_ID"

echo "Content creation workflow completed successfully."
echo "Results stored in: $DEMO_DIR"
echo "Final content available at: $DEMO_DIR/final_content.md"