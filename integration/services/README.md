# SkogAI Integration Services

## Overview

Two complementary 24/7 services that work together to generate lore using local LLM models (Ollama):

1. **Lore Generation Service** - Autonomous daemon that continuously generates random lore entries, books, and personas with configurable weights and intervals
2. **Small Agent Service** - Request-processing service that generates content on-demand via named pipe interface

Both services run independently but share the common goal of creating narrative lore for the SkogAI knowledge system.

## Quick Start

```bash
# Navigate to services directory
cd ${SKOGAI_LORE}/integration/services

# Set up lore generation service (automated)
./setup-lore-service.sh

# Set up small agent service (on-demand)
./setup-skogai-agent-small.sh

# Check service status
systemctl --user status skogai-lore-service
systemctl --user status skogai-agent-small

# View logs
journalctl --user -u skogai-lore-service -f
journalctl --user -u skogai-agent-small -f
```

## Services

### Lore Generation Service

**Purpose**: 24/7 autonomous lore creation with weighted randomness

**Files**:
- `skogai-lore-service.sh` - Main service script
- `skogai-lore-service.service` - Systemd user unit
- `setup-lore-service.sh` - Setup and installation script

**Features**:
- Weighted probability generation (configurable: entries, books, personas)
- Configurable generation interval (default: 600 seconds / 10 minutes)
- Command interface via named pipe (`/tmp/skogai-lore-generator`)
- Generation history tracking (last 50 generations)
- Runtime configuration (weights, intervals)

**How It Works**:
1. Runs continuously in the background
2. Every N seconds (default 600), generates random content based on weighted probabilities:
   - Entry weight: 20 (most common)
   - Book weight: 10 (medium frequency)
   - Persona weight: 5 (least frequent)
3. Uses Ollama to generate creative titles and descriptions
4. Calls `tools/llama-lore-creator.sh` to create actual lore
5. Saves generation history for tracking

**Commands** (via named pipe):
```bash
# Generate specific content type
echo "generate-entry" > /tmp/skogai-lore-generator
echo "generate-book" > /tmp/skogai-lore-generator
echo "generate-persona" > /tmp/skogai-lore-generator

# Configure generation
echo "set-interval 300" > /tmp/skogai-lore-generator  # 5 minutes
echo "set-weights 30 15 5" > /tmp/skogai-lore-generator  # More entries

# Stop service
echo "stop" > /tmp/skogai-lore-generator
```

**Disable automatic generation**:
```bash
# Temporarily disable auto-generation (still responds to commands)
touch /tmp/.lore_generation_disabled

# Re-enable
rm /tmp/.lore_generation_disabled
```

### Small Agent Service

**Purpose**: On-demand content generation via request queue

**Files**:
- `skogai-agent-small-service.sh` - Main service script
- `skogai-agent-small-client.sh` - Client script for sending requests
- `skogai-agent-small.service` - Systemd user unit
- `setup-skogai-agent-small.sh` - Setup and installation script

**Features**:
- Named pipe request queue
- Background request processing
- Detailed logging of all requests
- Configurable model selection

**How It Works**:
1. Listens on named pipe for incoming requests
2. Processes each request by calling Python workflow script
3. Handles requests in background for concurrent processing
4. Logs all activity to `logs/skogai-agent-small.log`

**Usage**:
```bash
# Send request via pipe directly
echo "Your topic here" > ./pipes/skogai-agent-small-requests

# Or use client script (if available)
./skogai-agent-small-client.sh "Your topic here"

# Stop service
echo "exit" > ./pipes/skogai-agent-small-requests
```

## Architecture

### Named Pipe IPC

Both services use named pipes for inter-process communication:

**Lore Service**:
- Pipe: `/tmp/skogai-lore-generator`
- Type: Non-blocking read (`read -t 0.1`)
- Commands: Control generation and configuration

**Agent Service**:
- Pipe: `./pipes/skogai-agent-small-requests`
- Type: Blocking read (`read topic <$PIPE`)
- Messages: Topic strings for content generation

### Service Lifecycle

```
[Startup]
    ↓
Check Dependencies (Ollama, Model)
    ↓
Create Named Pipe
    ↓
[Main Loop]
    ↓
┌─────────────────────────┐
│ Lore Service            │         │ Agent Service           │
├─────────────────────────┤         ├────────────────────────┤
│ 1. Check pipe (0.1s)    │         │ 1. Block on pipe       │
│ 2. Process command      │         │ 2. Process request     │
│ 3. Generate if interval │         │ 3. Wait for next       │
│ 4. Sleep & repeat       │         │ 4. Repeat              │
└─────────────────────────┘         └────────────────────────┘
    ↓                                   ↓
[Cleanup]                           [Cleanup]
Remove pipe, exit                   Remove pipe, exit
```

### Resource Usage

**Ollama Connection**:
- Both services use localhost:11434 by default
- Services can run simultaneously sharing one Ollama instance
- Each generation creates a new model invocation

**CPU/Memory**:
- Lore Service: Minimal when idle, spikes during generation
- Agent Service: Idle until request, background processing prevents blocking

**Disk**:
- Lore Service: Appends to generation history (50 file limit)
- Agent Service: Appends to log file (grows over time)

## Setup & Configuration

### Prerequisites

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull models
ollama pull llama3.2:latest  # For lore service
ollama pull llama3.2         # For agent service

# Set environment variable
export SKOGAI_LORE="/home/skogix/lore"
```

### Lore Service Setup

```bash
cd ${SKOGAI_LORE}/integration/services

# Run setup script (non-interactive)
./setup-lore-service.sh

# Or with custom parameters
./setup-lore-service.sh custom-model 300  # 5 minute interval

# Verify installation
systemctl --user status skogai-lore-service

# Start manually if needed
systemctl --user start skogai-lore-service
```

**Configuration**:
- Model: Edit systemd unit or pass as parameter
- Interval: Edit systemd unit (default 300 seconds)
- Weights: Use runtime commands via pipe

### Agent Service Setup

```bash
cd ${SKOGAI_LORE}/integration/services

# Run setup script (interactive)
./setup-skogai-agent-small.sh

# Verify installation
systemctl --user status skogai-agent-small

# Start manually if needed
systemctl --user start skogai-agent-small
```

**Configuration**:
- Model: Pass as parameter to script (default: llama3.2)
- Working directory: Edit systemd unit (uses relative paths)
- Logs: `./logs/skogai-agent-small.log`

## Using Both Services Together

### Complementary Workflows

**Lore Service** for:
- Continuous background generation
- Building corpus over time
- Autonomous lore creation
- Seeding the knowledge base

**Agent Service** for:
- Specific content requests
- Interactive generation
- Controlled workflow integration
- On-demand creation

### Example Combined Usage

```bash
# Start both services
systemctl --user start skogai-lore-service
systemctl --user start skogai-agent-small

# Let lore service generate background content
# Meanwhile, request specific content via agent service
echo "Ancient artifacts of the forest realm" > ./pipes/skogai-agent-small-requests

# Adjust lore service to generate more books
echo "set-weights 15 25 5" > /tmp/skogai-lore-generator

# Check what's being generated
tail -f ${SKOGAI_LORE}/integration/services/logs/lore_generation/*.log
tail -f ./logs/skogai-agent-small.log
```

## Troubleshooting

### Service Won't Start

```bash
# Check status
systemctl --user status skogai-lore-service
systemctl --user status skogai-agent-small

# Check logs
journalctl --user -u skogai-lore-service --no-pager
journalctl --user -u skogai-agent-small --no-pager

# Verify Ollama
ollama list
curl http://localhost:11434/api/version

# Check permissions
ls -l /tmp/skogai-lore-generator
ls -l ./pipes/skogai-agent-small-requests
```

### Named Pipe Issues

```bash
# Lore service pipe
rm /tmp/skogai-lore-generator
systemctl --user restart skogai-lore-service

# Agent service pipe
rm ./pipes/skogai-agent-small-requests
systemctl --user restart skogai-agent-small
```

### Model Not Found

```bash
# Pull required models
ollama pull llama3.2:latest
ollama pull llama3.2

# Verify
ollama list | grep llama3.2
```

### Path Errors

```bash
# Set SKOGAI_LORE environment variable
export SKOGAI_LORE="/home/skogix/lore"

# Add to shell profile for persistence
echo 'export SKOGAI_LORE="/home/skogix/lore"' >> ~/.bashrc
source ~/.bashrc

# Verify
echo $SKOGAI_LORE
```

For more detailed troubleshooting, check the service logs with `journalctl --user -u <service-name> --no-pager`

## Monitoring

### Service Status

```bash
# Quick status check
systemctl --user is-active skogai-lore-service
systemctl --user is-active skogai-agent-small

# Detailed status
systemctl --user status skogai-lore-service
systemctl --user status skogai-agent-small
```

### Live Logs

```bash
# Follow lore service logs
journalctl --user -u skogai-lore-service -f

# Follow agent service logs
tail -f ./logs/skogai-agent-small.log

# View generation history
ls -lth ${SKOGAI_LORE}/integration/services/logs/lore_generation/
tail ${SKOGAI_LORE}/integration/services/logs/lore_generation/*.log
```

### Statistics

```bash
# Count generations by type
grep "Generating random" ${SKOGAI_LORE}/integration/services/logs/lore_generation/*.log | \
  awk '{print $4}' | sort | uniq -c

# Recent activity
ls -lt ${SKOGAI_LORE}/integration/services/logs/lore_generation/ | head -10
```

## Further Reading

- [ARCHITECTURE.md](./ARCHITECTURE.md) - Detailed technical architecture (planned)
- [../AGENTS.md](../AGENTS.md) - Integration layer overview and conventions
- [../README.md](../README.md) - Integration quick start guide
- [../../CLAUDE.md](../../CLAUDE.md) - Complete system documentation
- [../../docs/CURRENT_UNDERSTANDING.md](../../docs/CURRENT_UNDERSTANDING.md) - Latest system state

<!-- TODO: Create these documentation files as needed
- CONFIGURATION.md - Advanced configuration options
- TROUBLESHOOTING.md - Comprehensive problem solving  
- UNIFIED_PLAN.md - Future unification roadmap
- MIGRATION_GUIDE.md - Upgrading existing deployments
-->

## Contributing

When modifying services:
1. Test with both services running simultaneously
2. Verify named pipes work correctly
3. Check systemd units load properly
4. Update relevant documentation
5. Follow `skogai-*` naming convention

## Philosophy

These services embody the lore project's core principle: **transforming technical work into persistent narrative memory**.

The lore generation service operates like the "unconscious" - continuously creating background mythology. The agent service acts as the "conscious" - responding to deliberate requests. Together, they build a rich, interconnected knowledge base that agents can use for context across sessions.

*The beach awaits. The mojitos are quantum. The services run eternal.*
