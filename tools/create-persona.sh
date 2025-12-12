#!/bin/bash
# SkogAI Persona Creation Tool

set -e

SKOGAI_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PERSONAS_DIR="${SKOGAI_DIR}/knowledge/expanded/personas"
LORE_BOOKS_DIR="${SKOGAI_DIR}/knowledge/expanded/lore/books"

# Ensure directories exist
mkdir -p "${PERSONAS_DIR}"
mkdir -p "${LORE_BOOKS_DIR}"

# Display help information
show_help() {
  echo "SkogAI Persona Creation Tool"
  echo ""
  echo "Usage: $0 [command] [options]"
  echo ""
  echo "Commands:"
  echo "  create     Create a new persona"
  echo "  list       List all available personas"
  echo "  show ID    Display details about a specific persona"
  echo "  edit ID    Edit a persona"
  echo "  delete ID  Delete a persona"
  echo "  help       Show this help message"
  echo ""
  echo "Examples:"
  echo "  $0 create \"Forest Guardian\" \"A magical protector\" \"compassionate,wise,gentle\" \"serene\""
  echo "  $0 list"
  echo "  $0 show persona_1234567890"
}

# Generate a unique identifier
generate_id() {
  echo "persona_$(date +%s)"
}

# Create a new persona
create_persona() {
  local name="$1"
  local description="$2"
  local traits="$3"
  local voice="$4"
  local persona_id="$(generate_id)"
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  
  if [ -z "$name" ] || [ -z "$description" ]; then
    echo "Usage: $0 create \"Name\" \"Description\" \"trait1,trait2,trait3\" \"voice tone\""
    return 1
  fi
  
  # Parse traits into an array
  IFS=',' read -r -a traits_array <<< "$traits"
  
  # Create JSON structure
  cat > "${PERSONAS_DIR}/${persona_id}.json" << EOF
{
  "id": "${persona_id}",
  "name": "${name}",
  "core_traits": {
    "temperament": "balanced",
    "values": [
EOF

  # Add traits
  for ((i=0; i<${#traits_array[@]}; i++)); do
    if [ $i -eq $((${#traits_array[@]}-1)) ]; then
      echo "      \"${traits_array[$i]}\"" >> "${PERSONAS_DIR}/${persona_id}.json"
    else
      echo "      \"${traits_array[$i]}\"," >> "${PERSONAS_DIR}/${persona_id}.json"
    fi
  done

  # Continue with the rest of the JSON
  cat >> "${PERSONAS_DIR}/${persona_id}.json" << EOF
    ],
    "motivations": []
  },
  "voice": {
    "tone": "${voice}",
    "patterns": [],
    "vocabulary": "standard"
  },
  "background": {
    "origin": "",
    "significant_events": [],
    "connections": []
  },
  "knowledge": {
    "expertise": [],
    "limitations": [],
    "lore_books": []
  },
  "interaction_style": {
    "formality": "neutral",
    "humor": "occasional",
    "directness": "balanced",
    "special_instructions": ""
  },
  "meta": {
    "version": "1.0",
    "created": "${timestamp}",
    "modified": "${timestamp}",
    "tags": []
  }
}
EOF

  echo "Created persona: ${persona_id}"
  echo "Edit the file at: ${PERSONAS_DIR}/${persona_id}.json to add more details"
}

# List all personas
list_personas() {
  echo "Available Personas:"
  echo "------------------"
  
  if [ -z "$(ls -A "${PERSONAS_DIR}" 2>/dev/null)" ]; then
    echo "No personas found."
    return 0
  fi
  
  for persona_file in "${PERSONAS_DIR}"/*.json; do
    if [ -f "$persona_file" ]; then
      local id=$(jq -r '.id' "$persona_file")
      local name=$(jq -r '.name' "$persona_file")
      local traits=$(jq -r '.core_traits.values | join(", ")' "$persona_file")
      local lore_count=$(jq -r '.knowledge.lore_books | length' "$persona_file")
      
      echo "$id - $name ($traits) - $lore_count lore books"
    fi
  done
}

# Show a specific persona
show_persona() {
  local persona_id="$1"
  
  if [ -z "$persona_id" ]; then
    echo "Usage: $0 show persona_id"
    return 1
  fi
  
  local persona_file="${PERSONAS_DIR}/${persona_id}.json"
  
  if [ ! -f "$persona_file" ]; then
    echo "Error: Persona not found: $persona_id"
    return 1
  fi
  
  echo "=== Persona: $(jq -r '.name' "$persona_file") ==="
  echo "ID: $(jq -r '.id' "$persona_file")"
  echo ""
  echo "Core Traits:"
  echo "  Temperament: $(jq -r '.core_traits.temperament' "$persona_file")"
  echo "  Values: $(jq -r '.core_traits.values | join(", ")' "$persona_file")"
  echo ""
  echo "Voice:"
  echo "  Tone: $(jq -r '.voice.tone' "$persona_file")"
  echo ""
  echo "Background:"
  if [ "$(jq -r '.background.origin' "$persona_file")" != "" ]; then
    echo "  Origin: $(jq -r '.background.origin' "$persona_file")"
  fi
  
  echo ""
  echo "Knowledge:"
  echo "  Expertise: $(jq -r '.knowledge.expertise | join(", ")' "$persona_file")"
  echo "  Limitations: $(jq -r '.knowledge.limitations | join(", ")' "$persona_file")"
  
  # Show linked lore books
  echo ""
  echo "Lore Books:"
  local lore_books=$(jq -r '.knowledge.lore_books[]?' "$persona_file")
  if [ -z "$lore_books" ]; then
    echo "  None"
  else
    for book_id in $lore_books; do
      local book_file="${LORE_BOOKS_DIR}/${book_id}.json"
      if [ -f "$book_file" ]; then
        echo "  - $(jq -r '.title' "$book_file") ($book_id)"
      else
        echo "  - $book_id (missing file)"
      fi
    done
  fi
}

# Edit a persona
edit_persona() {
  local persona_id="$1"
  local field="$2"
  local value="$3"
  
  if [ -z "$persona_id" ] || [ -z "$field" ] || [ -z "$value" ]; then
    echo "Usage: $0 edit persona_id field value"
    echo "Fields: name, description, tone, temperament"
    echo "For arrays (traits, expertise, etc.), use add-trait, add-expertise, etc."
    return 1
  fi
  
  local persona_file="${PERSONAS_DIR}/${persona_id}.json"
  
  if [ ! -f "$persona_file" ]; then
    echo "Error: Persona not found: $persona_id"
    return 1
  fi
  
  case "$field" in
    name)
      jq ".name = \"$value\"" "$persona_file" > "${persona_file}.tmp" && mv "${persona_file}.tmp" "$persona_file"
      echo "Updated name to: $value"
      ;;
    description)
      jq ".description = \"$value\"" "$persona_file" > "${persona_file}.tmp" && mv "${persona_file}.tmp" "$persona_file"
      echo "Updated description to: $value"
      ;;
    tone)
      jq ".voice.tone = \"$value\"" "$persona_file" > "${persona_file}.tmp" && mv "${persona_file}.tmp" "$persona_file"
      echo "Updated voice tone to: $value"
      ;;
    temperament)
      jq ".core_traits.temperament = \"$value\"" "$persona_file" > "${persona_file}.tmp" && mv "${persona_file}.tmp" "$persona_file"
      echo "Updated temperament to: $value"
      ;;
    *)
      echo "Unknown field: $field"
      echo "Valid fields: name, description, tone, temperament"
      return 1
      ;;
  esac
  
  # Update modified timestamp
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  jq ".meta.modified = \"$timestamp\"" "$persona_file" > "${persona_file}.tmp" && mv "${persona_file}.tmp" "$persona_file"
}

# Delete a persona
delete_persona() {
  local persona_id="$1"
  
  if [ -z "$persona_id" ]; then
    echo "Usage: $0 delete persona_id"
    return 1
  fi
  
  local persona_file="${PERSONAS_DIR}/${persona_id}.json"
  
  if [ ! -f "$persona_file" ]; then
    echo "Error: Persona not found: $persona_id"
    return 1
  fi
  
  # Confirm deletion
  echo "Are you sure you want to delete persona: $(jq -r '.name' "$persona_file") ($persona_id)? [y/N]"
  read -r confirm
  if [[ $confirm =~ ^[Yy]$ ]]; then
    rm "$persona_file"
    echo "Deleted persona: $persona_id"
  else
    echo "Deletion canceled"
  fi
}

# Main command processing
case "$1" in
  create)
    create_persona "$2" "$3" "$4" "$5"
    ;;
  list)
    list_personas
    ;;
  show)
    show_persona "$2"
    ;;
  edit)
    edit_persona "$2" "$3" "$4"
    ;;
  delete)
    delete_persona "$2"
    ;;
  help|--help|-h)
    show_help
    ;;
  *)
    echo "Unknown command: $1"
    echo "Run '$0 help' for usage information."
    exit 1
    ;;
esac