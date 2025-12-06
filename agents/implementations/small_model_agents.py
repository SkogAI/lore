#!/usr/bin/env python3

import os
import sys
import subprocess
import re
from typing import Dict, Any, List, Optional
import logging
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("small_model_agents")

class SmallModelAgents:
    """Implementation for running specialized agents using small local models (200MB range)."""

    def __init__(self, model_name: str = "llama3",
                 prompt_dir: str = None,
                 ollama_path: str = "ollama"):
        """Initialize the small model agents manager.

        Args:
            model_name: Name of the Ollama model to use
            prompt_dir: Directory containing simple prompt templates (defaults to agents/templates/small_models)
            ollama_path: Path to the ollama executable
        """
        self.model_name = model_name
        if prompt_dir is None:
            repo_root = Path(__file__).parent.parent.parent
            prompt_dir = str(repo_root / "agents" / "templates" / "small_models")
        self.prompt_dir = prompt_dir
        self.ollama_path = ollama_path

        # Ensure template directory exists
        os.makedirs(self.prompt_dir, exist_ok=True)
        Args:
            agent_type: "research", "outline", or "writing"
            input_text: Simple text input for the agent
            context: Optional additional context information

        Returns:
            str: Text response from the model
        """
        # Validate agent type
        if agent_type not in ["research", "outline", "writing"]:
            raise ValueError(f"Unsupported agent type: {agent_type}")
        # Create a simplified prompt with context if provided
        if context:
            context_str = self._format_context(agent_type, context)
            prompt = f"{prompt_template}\n\nContext:\n{context_str}\n\nInput: {input_text}\n\n"
        else:
            prompt = f"{prompt_template}\n\nInput: {input_text}\n\n"

        logger.info(f"Running {agent_type} agent with small model")

        try:
            # Call the local model via Ollama
            result = subprocess.run(
                [self.ollama_path, "run", self.model_name, prompt],
                capture_output=True,
                text=True,
                check=True
            )

            return result.stdout.strip()

        except subprocess.CalledProcessError as e:
            logger.error(f"Error running small model: {str(e)}")
            logger.error(f"Error output: {e.stderr}")
            raise RuntimeError(f"Model execution failed: {str(e)}")
        # Check if the prompt file exists
        if not os.path.exists(prompt_path):
            # Create default prompt template if it doesn't exist
            self._create_default_prompt(agent_type, prompt_path)
    def _create_default_prompt(self, agent_type: str, prompt_path: str) -> None:
        """Create a default prompt template for the specified agent type."""
        if agent_type == "research":
            prompt = """You are a research agent.

Your task is to find key information about a topic.

Format your answer like this:

KEY FACTS:
* Fact 1
* Fact 2
* Fact 3

MAIN CONCEPTS:
* Concept 1: Brief definition
* Concept 2: Brief definition

RELATIONSHIPS:
* How concept 1 relates to concept 2
* Other important relationships

POTENTIAL SECTIONS:
* First section to include
* Second section to include
"""

        elif agent_type == "outline":
            prompt = """You are an outline agent.

Your task is to create a structured outline for content.

Format your answer like this:

TITLE:
[Suggested title]

INTRODUCTION:
* Key point 1
* Key point 2

SECTIONS:
1. First Section Title
   * Subsection 1.1
   * Subsection 1.2

2. Second Section Title
   * Subsection 2.1
   * Subsection 2.2

CONCLUSION:
* Summary point 1
* Summary point 2
"""

        elif agent_type == "writing":
            prompt = """You are a writing agent.

Your task is to write content based on an outline.

Write in a clear, informative style.
Use simple language.
Include all major sections from the outline.
Use paragraph breaks for readability.

Start with a title and introduction, then cover each section in order.
"""

        # Ensure the directory exists
        os.makedirs(os.path.dirname(prompt_path), exist_ok=True)
    def _format_context(self, agent_type: str, context: Dict[str, Any]) -> str:
        """Format context information for inclusion in the prompt."""
        if agent_type == "outline" and "research_output" in context:
            # Format research output for the outline agent
            research = context["research_output"]
            # Try to format structured data
            try:
                if "structure" in outline and isinstance(outline["structure"], list):
                    sections = []
                    for i, section in enumerate(outline["structure"], 1):
                        if isinstance(section, dict) and "title" in section:
                            section_title = section["title"]
                            subsections = ""
                            if "subsections" in section and section["subsections"]:
                                sub_items = "\n".join([f"  * {sub}" for sub in section["subsections"]])
                                subsections = f"\n{sub_items}"
                            sections.append(f"{i}. {section_title}{subsections}")
                        else:
                            sections.append(f"{i}. {str(section)}")
        Returns:
            Dict containing extracted key facts, concepts, etc.
        """
        result = {
            "key_facts": [],
            "main_concepts": [],
            "relationships": [],
            "potential_sections": []
        }

        # Extract key facts section
        if "KEY FACTS:" in research_text:
            facts_section = research_text.split("KEY FACTS:")[1]
            if "MAIN CONCEPTS:" in facts_section:
                facts_section = facts_section.split("MAIN CONCEPTS:")[0]
            elif "CONCEPTS:" in facts_section:
                facts_section = facts_section.split("CONCEPTS:")[0]

            # Find bullet points
            facts = []
            for line in facts_section.strip().split('\n'):
                line = line.strip()
                if line.startswith(('*', '-', '•')):
                    facts.append(line.lstrip('*-• ').strip())

            result["key_facts"] = facts

        # Extract main concepts
        concepts_marker = "MAIN CONCEPTS:" if "MAIN CONCEPTS:" in research_text else "CONCEPTS:"
        if concepts_marker in research_text:
            concepts_section = research_text.split(concepts_marker)[1]

            # Find next section marker
            next_markers = ["RELATIONSHIPS:", "POTENTIAL SECTIONS:"]
            for marker in next_markers:
                if marker in concepts_section:
                    concepts_section = concepts_section.split(marker)[0]
                    break

            # Extract concepts
            concepts = []
            for line in concepts_section.strip().split('\n'):
                line = line.strip()
                if line.startswith(('*', '-', '•')):
                    concept_line = line.lstrip('*-• ').strip()
                    if ":" in concept_line:
                        # Format with definition
                        name, definition = concept_line.split(":", 1)
                        concepts.append({"name": name.strip(), "definition": definition.strip()})
                    else:
                        concepts.append(concept_line)

            result["main_concepts"] = concepts

        # Extract other sections with simple name:list pattern
        sections_to_extract = [
            ("RELATIONSHIPS:", "relationships"),
            ("POTENTIAL SECTIONS:", "potential_sections")
        ]
                # Find next section marker to limit extraction
                for next_marker, _ in sections_to_extract:
                    if next_marker in section and next_marker != marker:
                        section = section.split(next_marker)[0]
                        break

                items = []
                for line in section.strip().split('\n'):
                    line = line.strip()
                    if line.startswith(('*', '-', '•')):
                        items.append(line.lstrip('*-• ').strip())
        Returns:
            Dict containing extracted title, introduction, sections, etc.
        """
        result = {
            "title": "",
            "introduction": [],
            "structure": [],
            "conclusion": []
        }

        # Extract title
        if "TITLE:" in outline_text:
            title_section = outline_text.split("TITLE:")[1].split("\n")[0]
            result["title"] = title_section.strip()

        # Extract introduction
        if "INTRODUCTION:" in outline_text:
            intro_section = outline_text.split("INTRODUCTION:")[1]
            if "SECTIONS:" in intro_section:
                intro_section = intro_section.split("SECTIONS:")[0]

            # Find bullet points
            intro_points = []
            for line in intro_section.strip().split('\n'):
                line = line.strip()
                if line.startswith(('*', '-', '•')):
                    intro_points.append(line.lstrip('*-• ').strip())

            result["introduction"] = intro_points

        # Extract sections
        if "SECTIONS:" in outline_text:
            sections_text = outline_text.split("SECTIONS:")[1]
            if "CONCLUSION:" in sections_text:
                sections_text = sections_text.split("CONCLUSION:")[0]
            for line in sections_text.strip().split('\n'):
                line = line.strip()
                if not line:
                    continue
                if section_match:
                    # If we were working on a previous section, add it to the list
                    if current_section:
                        sections.append(current_section)
                # Check for subsection (assuming they're indented with * or -)
                elif line.startswith(('*', '-', '•')) and current_section is not None:
                    subsection = line.lstrip('*-• ').strip()
                    current_section["subsections"].append(subsection)
            # Find bullet points
            conclusion_points = []
            for line in conclusion_section.strip().split('\n'):
                line = line.strip()
                if line.startswith(('*', '-', '•')):
                    conclusion_points.append(line.lstrip('*-• ').strip())
        Returns:
            Dict containing extracted title and content sections
        """
        # For writing content, we'll use a simpler approach since the structure
        # might be difficult to parse reliably with a small model's output

        result = {
            "title": "",
            "content_sections": [],
            "full_text": writing_text.strip()
        }

        # Try to extract a title (first line if it looks like a title)
        lines = writing_text.strip().split('\n')
        if lines and not lines[0].startswith(('*', '-', '•', '#')) and len(lines[0]) < 100:
            result["title"] = lines[0].strip()
            content = '\n'.join(lines[1:]).strip()
        else:
            content = writing_text.strip()

        # Try to identify sections by looking for headers
        # Headers might be indicated by:
        # 1. Lines ending with colon (Section:)
        # 2. Lines in all caps (SECTION NAME)
        # 3. Lines with markdown headings (## Section)
                # Determine where this section ends
                if i < len(section_matches) - 1:
                    end_idx = section_matches[i+1].start()
                else:
                    end_idx = len(content)
                # Remove the header from the section text
                section_content = section_text[len(section_header):].strip()
                if section_content.startswith(':'):
                    section_content = section_content[1:].strip()

                sections.append({
                    "title": section_header.strip(),
                    "content": section_content
                })
        else:
            # If no sections were found, just use the full content
            sections.append({
                "title": "Content",
                "content": content
            })

        result["content_sections"] = sections
        return result
    # Use the research data for an outline request
    outline_response = agent_manager.run_agent(
        "outline",
        "Create an outline for an introductory article on quantum computing",
        {"research_output": research_data}
    )
    # Use the outline for writing
    writing_response = agent_manager.run_agent(
        "writing",
        "Write an article based on this outline. Use a conversational tone.",
        {"outline_output": outline_data}
    )

    print("\nWriting Response:\n", writing_response)
