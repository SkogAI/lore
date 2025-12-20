#!/usr/bin/env python3

import os
import sys
import json
import requests
from typing import Dict, Any, Optional
import time
import logging
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("agent_api")


class AgentAPI:
    """API layer for specialized content creation agents."""

    def __init__(self):
        """Initialize the AgentAPI with configuration."""
        # Default configuration
        self.config = {
            "api_key": os.environ.get("OPENROUTER_API_KEY"),
            "base_url": os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
            "models": {
                "research": "gpt-4o",
                "outline": "gpt-4o",
                "writing": "gpt-4o",
            },
            "temperature": {
                "research": 0.2,  # Lower temperature for factual accuracy
                "outline": 0.4,  # Moderate temperature for structure
                "writing": 0.7,  # Higher temperature for creative writing
            },
            "timeout": 120,
            "max_tokens": {"research": 2000, "outline": 2500, "writing": 4000},
        }

    def process_agent_request(
        self,
        agent_type: str,
        input_data: Dict[str, Any],
        session_id: str,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Process a request through the appropriate specialized agent."""

        # Get context data for this session and phase
        context_data = self.retrieve_context(session_id, agent_type)

        # Build the appropriate prompt for this agent
        prompt = self.build_agent_prompt(agent_type, input_data, context_data)

        # Prepare request parameters
        if parameters is None:
            parameters = {}

        model = parameters.get("model", self.config["models"][agent_type])
        temperature = parameters.get(
            "temperature", self.config["temperature"][agent_type]
        )
        max_tokens = parameters.get("max_tokens", self.config["max_tokens"][agent_type])

        # Call the LLM API
        try:
            response = self._call_llm_api(prompt, model, temperature, max_tokens)

            # Parse and validate the response
            parsed_response = self._parse_and_validate_response(response, agent_type)

            # Store the response in context for next phase
            self.store_context(session_id, agent_type, parsed_response)

            return parsed_response

        except Exception as e:
            logger.error(f"Error processing {agent_type} agent request: {str(e)}")
            raise

    def retrieve_context(self, session_id: str, phase: str) -> Dict[str, Any]:
        """Retrieve context data for a specific workflow phase."""
        repo_root = Path(__file__).parent.parent.parent
        context_dir = str(repo_root / "demo" / f"content_creation_{session_id}")
        context = {
            "session_id": session_id,
            "current_phase": phase,
            "timestamp": time.time(),
        }

        # Add previous phases' output if they exist
        if phase == "outline" or phase == "writing":
            try:
                with open(f"{context_dir}/research_output.json", "r") as f:
                    context["research_data"] = json.load(f)
            except FileNotFoundError:
                logger.warning(f"No research data found for session {session_id}")

        if phase == "writing":
            try:
                with open(f"{context_dir}/outline_output.json", "r") as f:
                    context["outline_data"] = json.load(f)
            except FileNotFoundError:
                logger.warning(f"No outline data found for session {session_id}")

        # Add original request if it exists
        try:
            with open(f"{context_dir}/request.txt", "r") as f:
                context["original_request"] = f.read().strip()
        except FileNotFoundError:
            pass

        return context

    def store_context(self, session_id: str, phase: str, data: Dict[str, Any]) -> bool:
        """Store context data from a workflow phase."""
        repo_root = Path(__file__).parent.parent.parent
        context_dir = repo_root / "demo" / f"content_creation_{session_id}"

        # Ensure directory exists
        context_dir.mkdir(parents=True, exist_ok=True)

        # Store phase-specific output
        output_file = f"{context_dir}/{phase}_output.json"
        try:
            with open(output_file, "w") as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error storing context for {phase}: {str(e)}")
            return False

    def build_agent_prompt(
        self, agent_type: str, input_data: Dict[str, Any], context_data: Dict[str, Any]
    ) -> str:
        """Build an appropriate prompt for the specified agent type."""

        # Get agent instructions
        repo_root = Path(__file__).parent.parent.parent
        agent_path = repo_root / "agents" / "implementations" / "content" / f"{agent_type}-agent.md"
        try:
            with open(agent_path, "r") as f:
                agent_instructions = f.read()
        except FileNotFoundError:
            logger.error(f"Agent instructions not found: {agent_path}")
            agent_instructions = (
                f"You are a {agent_type} agent. Process the given input."
            )

        # Build a prompt based on agent type
        if agent_type == "research":
            topic = input_data.get("topic", context_data.get("original_request", ""))
            depth = input_data.get("depth", "intermediate")
            focus = input_data.get("focus", "general")

            prompt = f"""{agent_instructions}

TOPIC: {topic}
DEPTH: {depth}
FOCUS: {focus}

Conduct thorough research on this topic and return your findings in the specified JSON format.
Be comprehensive, accurate, and focus on the most important aspects of the topic.
"""

        elif agent_type == "outline":
            research_data = context_data.get("research_data", {})
            topic = research_data.get("topic", "")
            purpose = input_data.get("purpose", "inform")
            audience = input_data.get("audience", "general")

            # Convert research_data to a formatted string for inclusion
            research_str = json.dumps(research_data, indent=2)

            prompt = f"""{agent_instructions}

TOPIC: {topic}
PURPOSE: {purpose}
AUDIENCE: {audience}

Based on the following research data, create a comprehensive outline in the specified JSON format.
Organize the information logically and establish clear relationships between sections.

RESEARCH DATA:
{research_str}
"""

        elif agent_type == "writing":
            outline_data = context_data.get("outline_data", {})
            research_data = context_data.get("research_data", {})
            tone = input_data.get("tone", "conversational")

            # Convert input data to formatted strings
            outline_str = json.dumps(outline_data, indent=2)

            prompt = f"""{agent_instructions}

TONE: {tone}
TASK: Write complete content based on the provided outline and research data.

OUTLINE DATA:
{outline_str}

Use the research information to support your writing. Maintain the specified tone
and adhere to the structure provided in the outline. Return your response in the
specified JSON format.
"""

        else:
            prompt = f"{agent_instructions}\n\nInput: {json.dumps(input_data)}"

        return prompt

    def _call_llm_api(
        self, prompt: str, model: str, temperature: float, max_tokens: int
    ) -> str:
        """Call the LLM API with the given prompt."""
        # This is a simplified example for OpenAI's API
        # In production, you might use different APIs or have more complex logic

        headers = {
            "Authorization": f"Bearer {self.config['api_key']}",
            "Content-Type": "application/json",
        }

        data = {
            "model": model,
            "messages": [{"role": "system", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        try:
            logger.info(f"Calling LLM API with model: {model}")
            response = requests.post(
                f"{self.config['base_url']}/chat/completions",
                headers=headers,
                json=data,
                timeout=self.config["timeout"],
            )

            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                logger.error(f"API error: {response.status_code} - {response.text}")
                raise Exception(f"API error: {response.status_code} - {response.text}")

        except requests.RequestException as e:
            logger.error(f"Request error: {str(e)}")
            raise

    def _parse_and_validate_response(
        self, response: str, agent_type: str
    ) -> Dict[str, Any]:
        """Parse and validate the LLM response to ensure it meets the expected format."""
        try:
            # Extract JSON from response (handling cases where LLM might add extra text)
            response = response.strip()

            # Find JSON content between ```json and ``` if present
            import re

            json_match = re.search(r"```json\s*([\s\S]*?)\s*```", response)
            if json_match:
                json_str = json_match.group(1)
            else:
                # Try to find anything that looks like JSON
                json_match = re.search(r"(\{[\s\S]*\})", response)
                if json_match:
                    json_str = json_match.group(1)
                else:
                    json_str = response

            parsed = json.loads(json_str)

            # Validate response based on agent type
            if agent_type == "research":
                required_fields = ["topic", "key_facts", "main_concepts"]
                for field in required_fields:
                    if field not in parsed:
                        logger.warning(
                            f"Missing required field in research response: {field}"
                        )

                        # Add empty placeholder for missing fields
                        if field == "key_facts" or field == "main_concepts":
                            parsed[field] = []
                        else:
                            parsed[field] = ""

            elif agent_type == "outline":
                if "structure" not in parsed or not isinstance(
                    parsed.get("structure", []), list
                ):
                    logger.warning("Missing or invalid structure in outline response")
                    parsed["structure"] = []

            elif agent_type == "writing":
                if "content_sections" not in parsed or not isinstance(
                    parsed.get("content_sections", []), list
                ):
                    logger.warning(
                        "Missing or invalid content_sections in writing response"
                    )
                    parsed["content_sections"] = []

            return parsed

        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON response: {str(e)}")
            logger.debug(f"Raw response: {response}")

            # Return a minimal valid response as fallback
            return {"error": "Failed to parse response", "raw_response": response}
        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            raise


# Example usage
if __name__ == "__main__":
    # Example usage in a test context
    api = AgentAPI()

    # Test with a research request
    session_id = int(time.time())
    result = api.process_agent_request(
        "research",
        {
            "topic": "Claude Code in egypt digging up dinosaur bones",
            "depth": "advanced",
        },
        session_id,
    )

    print(json.dumps(result, indent=2))
