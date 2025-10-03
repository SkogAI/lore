#!/usr/bin/env python3

import os
import sys
import json
import time
import argparse
from typing import Dict, Any, Optional

# Add the project root to the path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Import configuration system
from config import paths

# Import the small model agents
from agents.implementations.small_model_agents import SmallModelAgents


def run_workflow(
    topic: str, model_name: str = "smo-agent", output_dir: Optional[str] = None
):
    """Run the complete content creation workflow using small local models.

    Args:
        topic: The topic to create content about
        model_name: Name of the Ollama model to use
        output_dir: Directory to save output files (defaults to timestamped dir)
    """
    # Initialize the small model agents
    agent_manager = SmallModelAgents(model_name=model_name)

    # Create output directory if needed
    if output_dir is None:
        timestamp = int(time.time())
        output_dir = paths.get_demo_output_dir(str(timestamp), "small_model_content")

    paths.ensure_dir(output_dir)

    print(f"Creating content for topic: {topic}")
    print(f"Using model: {model_name}")
    print(f"Output directory: {output_dir}")
    print("-" * 50)

    # Step 1: Research
    print("Step 1: Research...")
    research_response = agent_manager.run_agent("research", topic)

    # Save raw response
    with open(f"{output_dir}/research_raw.txt", "w") as f:
        f.write(research_response)

    # Extract structured data
    research_data = agent_manager.extract_research_facts(research_response)

    # Save structured data
    with open(f"{output_dir}/research_data.json", "w") as f:
        json.dump(research_data, f, indent=2)

    print("  Research complete!")
    print("  Key facts found:", len(research_data.get("key_facts", [])))
    print("  Concepts identified:", len(research_data.get("main_concepts", [])))
    print("-" * 50)

    # Step 2: Outline
    print("Step 2: Creating outline...")
    outline_prompt = f"Create an outline for an informative article about {topic}"
    outline_response = agent_manager.run_agent(
        "outline", outline_prompt, {"research_output": research_data}
    )

    # Save raw response
    with open(f"{output_dir}/outline_raw.txt", "w") as f:
        f.write(outline_response)

    # Extract structured outline
    outline_data = agent_manager.extract_outline_structure(outline_response)

    # Save structured data
    with open(f"{output_dir}/outline_data.json", "w") as f:
        json.dump(outline_data, f, indent=2)

    print("  Outline complete!")
    print("  Title:", outline_data.get("title", ""))
    print("  Sections:", len(outline_data.get("structure", [])))
    print("-" * 50)

    # Step 3: Writing
    print("Step 3: Writing content...")
    writing_prompt = f"Write an article based on this outline about {topic}. Use a conversational tone."
    writing_response = agent_manager.run_agent(
        "writing", writing_prompt, {"outline_output": outline_data}
    )

    # Save raw response
    with open(f"{output_dir}/writing_raw.txt", "w") as f:
        f.write(writing_response)

    # Extract content sections
    content_data = agent_manager.extract_written_content(writing_response)

    # Save structured data
    with open(f"{output_dir}/content_data.json", "w") as f:
        json.dump(content_data, f, indent=2)

    # Save as a clean article
    article_text = content_data.get("full_text", writing_response)
    with open(f"{output_dir}/final_article.md", "w") as f:
        f.write(article_text)

    print("  Writing complete!")
    print("  Title:", content_data.get("title", ""))
    print("  Sections:", len(content_data.get("content_sections", [])))
    print("-" * 50)

    print(
        f"Content creation complete! Final article saved to: {output_dir}/final_article.md"
    )

    return output_dir


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run content creation with small models"
    )
    parser.add_argument("topic", help="Topic to create content about")
    parser.add_argument(
        "--model", default="llama3", help="Name of the Ollama model to use"
    )
    parser.add_argument("--output", help="Directory to save output files")

    args = parser.parse_args()

    run_workflow(args.topic, args.model, args.output)

