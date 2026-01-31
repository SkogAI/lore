# Services Architecture

## System Overview

The SkogAI integration services implement a dual-service architecture for continuous lore generation using local LLM models via Ollama.

```
┌─────────────────────────────────────────────────────────────┐
│                         User Space                           │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────────────────┐         ┌─────────────────────────┐ │
│  │ Lore Service       │         │ Small Agent Service     │ │
│  │ (Autonomous)       │         │ (On-Demand)            │ │
│  ├────────────────────┤         ├─────────────────────────┤ │
│  │ • Weighted random  │         │ • Request queue         │ │
│  │ • Timed intervals  │         │ • Python workflow       │ │
│  │ • Command interface│         │ • Background processing │ │
│  └──────┬─────────────┘         └──────┬──────────────────┘ │
│         │                               │                     │
│         ├───► Named Pipe ◄──────────────┤                     │
│         │    (IPC)                      │                     │
│         │                               │                     │
│         └───────────────┬───────────────┘                     │
│                         │                                      │
│                    ┌────▼────┐                                │
│                    │ Ollama  │                                │
│                    │ Service │                                │
│                    └────┬────┘                                │
│                         │                                      │
│                    ┌────▼────┐                                │
│                    │  Models │                                │
│                    │ (Local) │                                │
│                    └─────────┘                                │
└─────────────────────────────────────────────────────────────┘
         │                                │
         └───► Lore Entries ◄─────────────┘
               (JSON Files)
```

## Components

### 1. Lore Generation Service

**File**: `skogai-lore-service.sh`

**Purpose**: Autonomous 24/7 lore creation daemon

**Architecture**:
```bash
#!/bin/bash
set -e

# Configuration
SKOGAI_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
MODEL_NAME=${1:-"llama3.2:latest"}
PIPE_PATH="/tmp/skogai-lore-generator"
GENERATION_INTERVAL=${2:-"600"}  # 10 minutes

# Weighted Probabilities
ENTRY_WEIGHT=20   # 57% chance (20/35)
BOOK_WEIGHT=10    # 29% chance (10/35)
PERSONA_WEIGHT=5  # 14% chance (5/35)

# Main Loop
while true; do
  # Check pipe for commands (non-blocking)
  read -t 0.1 command <$PIPE_PATH

  # Process commands or generate automatically
  case "$command" in
    generate-entry|generate-book|generate-persona)
      execute_generation
      ;;
    set-weights|set-interval)
      update_configuration
      ;;
    *)
      # Weighted random generation
      select_and_generate_based_on_weights
      sleep $GENERATION_INTERVAL
      ;;
  esac
done
```

**Key Design Decisions**:

1. **Non-blocking pipe reads** (`read -t 0.1`)
   - Allows service to continue generation even without commands
   - Responsive to commands when sent
   - Doesn't block on waiting for input

2. **Weighted random selection**
   ```bash
   TOTAL_WEIGHT=$((ENTRY_WEIGHT + BOOK_WEIGHT + PERSONA_WEIGHT))
   RANDOM_VALUE=$((RANDOM % TOTAL_WEIGHT))

   if [ $RANDOM_VALUE -lt $ENTRY_WEIGHT ]; then
     generate_entry
   elif [ $RANDOM_VALUE -lt $((ENTRY_WEIGHT + BOOK_WEIGHT)) ]; then
     generate_book
   else
     generate_persona
   fi
   ```

3. **History tracking with limits**
   - Saves last 50 generations
   - Automatic cleanup prevents disk bloat
   - Timestamped files for debugging

4. **Runtime reconfiguration**
   - Change weights without restart
   - Adjust intervals on the fly
   - Temporary disable via flag file

### 2. Small Agent Service

**File**: `skogai-agent-small-service.sh`

**Purpose**: Request-response service for on-demand generation

**Architecture**:
```bash
#!/bin/bash

MODEL_NAME=${1:-"llama3.2"}
PIPE="./pipes/skogai-agent-small-requests"

# Process request function
process_request() {
  local topic="$1"
  python /path/to/small_model_workflow.py "$topic" --model "$MODEL_NAME"
}

# Main loop
while true; do
  # Blocking read - waits for request
  if read topic <$PIPE; then
    if [ "$topic" == "exit" ]; then
      break
    fi

    # Background processing for concurrency
    process_request "$topic" &
  fi

  sleep 1  # Prevent CPU overload
done
```

**Key Design Decisions**:

1. **Blocking pipe reads** (`read topic <$PIPE`)
   - Waits for requests efficiently
   - No CPU waste during idle
   - Simple request queueing

2. **Background processing** (`&`)
   - Process requests concurrently
   - Don't block on slow operations
   - Allow new requests while processing

3. **Relative paths**
   - Uses `./pipes/` and `./logs/`
   - Depends on working directory
   - **Note**: Should migrate to `${SKOGAI_LORE}` standard

4. **Exit mechanism**
   - Simple string comparison
   - Clean shutdown
   - Removes pipe on exit

## Inter-Process Communication (IPC)

### Named Pipes (FIFOs)

Both services use named pipes for different purposes:

#### Lore Service Pipe

**Path**: `/tmp/skogai-lore-generator`
**Permissions**: `660` (rw-rw----)

**Protocol**:
```
Client → Pipe → Service
  ↓
"command [args...]"
  ↓
Service executes & responds
```

**Commands**:
| Command | Args | Effect |
|---------|------|--------|
| `generate-entry` | None | Generate single entry |
| `generate-book` | None | Generate book with 3-7 entries |
| `generate-persona` | None | Generate persona + linked book |
| `set-interval` | seconds | Change generation interval (min 60s) |
| `set-weights` | entry book persona | Adjust probability weights |
| `stop` | None | Terminate service |

**Example**:
```bash
# Trigger specific generation
echo "generate-book" > /tmp/skogai-lore-generator

# Adjust to generate more entries
echo "set-weights 40 10 5" > /tmp/skogai-lore-generator

# Change to 5-minute intervals
echo "set-interval 300" > /tmp/skogai-lore-generator
```

#### Agent Service Pipe

**Path**: `./pipes/skogai-agent-small-requests`
**Permissions**: Default (created with `mkfifo`)

**Protocol**:
```
Client → Pipe → Service
  ↓
"topic string"
  ↓
Service invokes Python workflow
  ↓
Background processing & logging
```

**Messages**:
- Any string (except "exit" or "quit")
- Topic for content generation
- Passed directly to Python script

**Example**:
```bash
# Request content generation
echo "Ancient ruins of the digital realm" > ./pipes/skogai-agent-small-requests

# Stop service
echo "exit" > ./pipes/skogai-agent-small-requests
```

### Pipe Lifecycle

```
[Service Startup]
    ↓
Check if pipe exists
    ↓
Remove old pipe (if exists)
    ↓
Create new pipe (mkfifo)
    ↓
Set permissions (lore service only)
    ↓
[Service Running]
    ↓
Read from pipe
    ↓
Process command/request
    ↓
Repeat
    ↓
[Service Shutdown]
    ↓
Cleanup trap (lore service)
Remove pipe
    ↓
Exit
```

## Service Lifecycle

### Startup Sequence

#### Lore Service
```
1. Parse arguments (model, interval)
2. Set SKOGAI_DIR to script location
3. Create history directory
4. Check Ollama installation
5. Verify/pull model
6. Create named pipe
7. Register cleanup trap
8. Enter main loop
```

#### Agent Service
```
1. Parse arguments (model)
2. Create log directory
3. Log startup event
4. Create pipes directory
5. Remove old pipe
6. Create new pipe
7. Check Ollama installation
8. Verify/pull model
9. Log readiness
10. Enter main loop
```

### Runtime Operation

#### Lore Service Loop

```
┌─────────────────────────────────────┐
│ Check pipe (timeout 0.1s)           │
├─────────────────────────────────────┤
│ Command received?                   │
│   Yes: Execute command              │
│   No:  Continue to generation       │
├─────────────────────────────────────┤
│ Check disable flag                  │
│   Disabled: Sleep 5s, loop          │
│   Enabled:  Continue                │
├─────────────────────────────────────┤
│ Calculate weighted random           │
│   RANDOM % TOTAL_WEIGHT             │
├─────────────────────────────────────┤
│ Select generation type              │
│   Entry, Book, or Persona           │
├─────────────────────────────────────┤
│ Generate with Ollama + llama-lore-creator.sh │
├─────────────────────────────────────┤
│ Save to history                     │
├─────────────────────────────────────┤
│ Sleep GENERATION_INTERVAL           │
├─────────────────────────────────────┤
│ Loop                                │
└─────────────────────────────────────┘
```

#### Agent Service Loop

```
┌─────────────────────────────────────┐
│ Wait for pipe input (blocking)      │
├─────────────────────────────────────┤
│ Message received                    │
├─────────────────────────────────────┤
│ Check for exit command              │
│   exit/quit: Break loop             │
│   Other: Continue                   │
├─────────────────────────────────────┤
│ Fork background process             │
│   process_request "$topic" &        │
├─────────────────────────────────────┤
│ Log request                         │
├─────────────────────────────────────┤
│ Sleep 1s (prevent CPU overload)     │
├─────────────────────────────────────┤
│ Loop (wait for next request)        │
└─────────────────────────────────────┘
```

### Shutdown Sequence

#### Lore Service
```
1. Receive stop command OR signal (INT/TERM)
2. Trigger cleanup trap
3. Log shutdown
4. Remove named pipe
5. Exit 0
```

#### Agent Service
```
1. Receive "exit" message OR Ctrl+C
2. Break main loop
3. Remove named pipe
4. Log shutdown
5. Exit 0
```

## Integration Points

### Shared Dependencies

Both services depend on:
1. **Ollama** - Local LLM runtime
2. **Model availability** - llama3.2 or llama3.2:latest
3. **Lore tools** - `llama-lore-creator.sh`, `small_model_workflow.py`

### Lore System Integration

```
Services
   ↓
Generate Content
   ↓
Call Lore Tools
   ↓
Create JSON Files
   ↓
knowledge/expanded/lore/
   ├── entries/
   ├── books/
   └── personas/
```

### Data Flow

```
[Lore Service]
   Ollama (title generation)
      ↓
   tools/llama-lore-creator.sh
      ↓
   tools/manage-lore.sh
      ↓
   JSON files + jq operations
      ↓
   knowledge/expanded/lore/

[Agent Service]
   Python workflow
      ↓
   Ollama (content generation)
      ↓
   [Unknown output format]
      ↓
   [To be documented]
```

## Resource Management

### Ollama Connection

```
Services → localhost:11434 (default)
   ↓
Single Ollama instance
   ↓
Model loaded on first use
   ↓
Shared across services
```

**Concurrency**:
- Both services can run simultaneously
- Ollama handles request queueing
- Models stay loaded in memory
- Requests processed sequentially by Ollama

### Memory Footprint

| Component | Idle | Active |
|-----------|------|--------|
| Lore Service | ~10 MB | ~50 MB (during generation) |
| Agent Service | ~5 MB | ~40 MB (during processing) |
| Ollama | ~200 MB | ~4 GB (model loaded) |
| Model (llama3.2) | - | ~2.8 GB |

### Disk Usage

**Lore Service**:
- History files: 50 × ~1 KB = ~50 KB max
- Generated lore: Varies (entries ~2-5 KB each)

**Agent Service**:
- Log file: Grows unbounded (needs rotation)
- Generated content: Depends on workflow

### CPU Usage

**Lore Service**:
- Idle: < 1% (sleeping or waiting on pipe)
- Generation: 100% for ~5-30 seconds (Ollama processing)
- Average: ~5% over time (depends on interval)

**Agent Service**:
- Idle: < 0.1% (blocked on pipe read)
- Processing: 100% during Python workflow execution
- Average: Depends on request frequency

## File System Layout

```
${SKOGAI_LORE}/
├── integration/
│   └── services/
│       ├── README.md                     (this documentation)
│       ├── ARCHITECTURE.md              (current file)
│       ├── CONFIGURATION.md             (setup guide)
│       ├── TROUBLESHOOTING.md           (problem solving)
│       ├── skogai-lore-service.sh       (lore daemon)
│       ├── skogai-lore-service.service  (systemd unit)
│       ├── setup-lore-service.sh        (lore setup)
│       ├── skogai-agent-small-service.sh (agent daemon)
│       ├── skogai-agent-small.service   (systemd unit)
│       ├── setup-skogai-agent-small.sh  (agent setup)
│       ├── skogai-agent-small-client.sh (agent client)
│       └── logs/
│           └── lore_generation/         (history files)
├── pipes/                               (agent service pipes)
│   └── skogai-agent-small-requests
├── logs/                                (agent service logs)
│   └── skogai-agent-small.log
└── knowledge/expanded/lore/             (output)
    ├── entries/
    ├── books/
    └── personas/

/tmp/
└── skogai-lore-generator                (lore service pipe)

~/.config/systemd/user/
├── skogai-lore-service.service
└── skogai-agent-small.service
```

## Systemd Integration

### Service Units

Both services use systemd user units for lifecycle management.

#### Lore Service Unit

```ini
[Unit]
Description=SkogAI Lore Generator Service
After=network.target

[Service]
Type=simple
WorkingDirectory=${SKOGAI_LORE}
ExecStart=${SKOGAI_LORE}/integration/services/skogai-lore-service.sh llama3.2:latest 600
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal
Environment=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
Environment=OLLAMA_HOST=localhost:11434

[Install]
WantedBy=default.target
```

#### Agent Service Unit

```ini
[Unit]
Description=SkogAI Small Agent Service
After=network.target

[Service]
Type=simple
WorkingDirectory=${SKOGAI_LORE}
ExecStart=${SKOGAI_LORE}/integration/services/skogai-agent-small-service.sh llama3.2
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
```

### Lifecycle Commands

```bash
# Enable (start on boot)
systemctl --user enable skogai-lore-service
systemctl --user enable skogai-agent-small

# Start
systemctl --user start skogai-lore-service
systemctl --user start skogai-agent-small

# Stop
systemctl --user stop skogai-lore-service
systemctl --user stop skogai-agent-small

# Restart
systemctl --user restart skogai-lore-service
systemctl --user restart skogai-agent-small

# Status
systemctl --user status skogai-lore-service
systemctl --user status skogai-agent-small

# Logs
journalctl --user -u skogai-lore-service -f
journalctl --user -u skogai-agent-small -f
```

## Future Architecture Considerations

### Planned Unifications

1. **Common Library** (`lib-common.sh`)
   - Shared pipe management functions
   - Model availability checking
   - Logging utilities
   - Path standardization (${SKOGAI_LORE})

2. **Unified Setup** (`setup-services.sh`)
   - Single entry point for both services
   - Detect which to install
   - Shared dependency validation
   - Consistent prompts

3. **Service Manager** (`service-manager.sh`)
   ```bash
   ./service-manager.sh start [lore|agent|all]
   ./service-manager.sh stop [lore|agent|all]
   ./service-manager.sh status
   ./service-manager.sh logs [lore|agent]
   ```

4. **Path Standardization**
   - All paths use `${SKOGAI_LORE}` base
   - Consistent directory structure
   - No hardcoded absolute paths
   - No relative path dependencies

### Service Coordination

Future enhancement: Services aware of each other

```
┌──────────────────────────────────────┐
│    Service Coordinator Daemon        │
├──────────────────────────────────────┤
│  • Monitors both services            │
│  • Coordinates resource usage        │
│  • Prevents conflicts                │
│  • Aggregates statistics             │
│  • Unified command interface         │
└──────────────────────────────────────┘
         │              │
    ┌────┴──┐      ┌────┴──┐
    │ Lore  │      │ Agent │
    └───────┘      └───────┘
```

### Scalability Considerations

**Horizontal Scaling**:
- Multiple lore services with different weights
- Distributed agent services
- Load balancing across Ollama instances

**Vertical Scaling**:
- Larger models for better quality
- More concurrent requests
- Faster generation intervals

## Security Considerations

### Named Pipe Permissions

**Current**:
- Lore service: 660 (group readable/writable)
- Agent service: Default permissions

**Recommendation**:
- Both should use 660 or stricter
- Consider user-only access (600)
- Document security implications

### Process Isolation

- Services run as user processes (systemd --user)
- No root privileges required
- Separate log files
- Independent failure domains

### Data Validation

**Current**: None
**Needed**:
- Validate pipe input before processing
- Sanitize file paths
- Check command format
- Prevent injection attacks

## Performance Characteristics

### Latency

| Operation | Lore Service | Agent Service |
|-----------|--------------|---------------|
| Command processing | < 100ms | < 100ms |
| Entry generation | 5-15s | Variable |
| Book generation | 30-120s | N/A |
| Persona generation | 20-60s | N/A |

### Throughput

**Lore Service**:
- Theoretical max: 360 entries/hour (10-minute interval)
- Practical: ~6 entries/hour (considering book/persona weights)
- Configurable via interval and weights

**Agent Service**:
- Limited by Python workflow speed
- Background processing allows queuing
- No built-in rate limiting

### Bottlenecks

1. **Ollama processing** - Single instance handles all requests
2. **Model loading** - First request loads model (slow)
3. **Disk I/O** - JSON file operations (minor)
4. **Shell overhead** - Fork/exec for each generation (minor)

## Debugging and Monitoring

### Log Locations

```bash
# Systemd journal (both services)
journalctl --user -u skogai-lore-service
journalctl --user -u skogai-agent-small

# Generation history (lore service)
${SKOGAI_LORE}/integration/services/logs/lore_generation/*.log

# Request log (agent service)
./logs/skogai-agent-small.log
```

### Debug Mode

**Lore Service**:
```bash
# Run manually with debugging
bash -x ./skogai-lore-service.sh llama3.2:latest 60
```

**Agent Service**:
```bash
# Run manually with debugging
bash -x ./skogai-agent-small-service.sh llama3.2
```

### Monitoring Points

1. **Pipe status**: `ls -l /tmp/skogai-lore-generator ./pipes/*`
2. **Process status**: `systemctl --user status skogai-*`
3. **Ollama status**: `curl http://localhost:11434/api/version`
4. **Generation count**: `ls -1 ${SKOGAI_LORE}/integration/services/logs/lore_generation/ | wc -l`
5. **Recent activity**: `ls -lt ./logs/lore_generation/ | head`

## Conclusion

The dual-service architecture provides complementary approaches to lore generation:

- **Lore Service** = Autonomous background mythology creation
- **Agent Service** = Interactive on-demand content generation

Both leverage local LLMs via Ollama, use named pipes for IPC, and integrate with the broader lore system through shared tools and data structures.

The architecture prioritizes simplicity and reliability over complexity, with clear separation of concerns and minimal dependencies.

---

*Architecture evolves. Documentation persists. The services run eternal.*
