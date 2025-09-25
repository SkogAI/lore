# Temporal Integration in Goose 🍹

## Overview
Temporal.io integration provides workflow orchestration and process management for Goose. This document captures the analysis and understanding of the implementation found in the original setup.

## Source Location
Original implementation found in: `/home/skogix/.local/src/goose-src/temporal-service/`

## Core Components

### 1. Workflow Engine (`goose_workflow.go`)
- **Main Purpose**: Executes Goose recipes as workflows
- **Key Features**:
  - Recipe execution with retry logic
  - 2-hour timeout per job
  - Error handling and logging
  - Supports YAML/JSON recipe formats
- **Example Workflow**:
```go
func GooseJobWorkflow(ctx workflow.Context, jobID, recipePath string)
```

### 2. Process Manager (`process_manager.go`)
- **Main Purpose**: Manages long-running Goose processes
- **Features**:
  - Process tracking with job IDs
  - Start/stop control
  - Resource cleanup
  - Process status monitoring
- **Key Types**:
```go
type ProcessManager struct {
    processes map[string]*ManagedProcess
    mutex     sync.RWMutex
}

type ManagedProcess struct {
    JobID     string
    Process   *os.Process
    Cancel    context.CancelFunc
    StartTime time.Time
}
```

### 3. Scheduler (`schedule.go`)
- **Main Purpose**: Handles scheduled recipe execution
- **Features**:
  - Cron-based scheduling
  - Job status tracking
  - Manual and scheduled runs
  - Foreground/background execution modes
- **Job Status Structure**:
```go
type JobStatus struct {
    ID               string    
    CronExpr         string    
    RecipePath       string    
    LastRun          *string   
    NextRun          *string   
    CurrentlyRunning bool      
    Paused           bool      
    CreatedAt        time.Time 
    ExecutionMode    *string   
    LastManualRun    *string   
}
```

## System Workflows
Default system workflows:
1. `temporal-sys-tq-scanner`: Task queue scanning
2. `temporal-sys-history-scanner`: History cleanup

## Database
- Location: `temporal.db` in root directory
- Size: ~569KB
- Contains:
  - Workflow history
  - Execution records
  - System maintenance data

## Integration Value Assessment

### Pros 👍
1. **Robust Process Management**
   - Handles long-running tasks
   - Process cleanup and monitoring
   - Error recovery

2. **Flexible Scheduling**
   - Cron-based scheduling
   - Manual execution support
   - Status tracking

3. **Resource Management**
   - Process isolation
   - Resource cleanup
   - Error handling

### Cons 👎
1. **Complexity**
   - Additional service dependency
   - Complex setup and maintenance
   - Resource overhead

2. **Usage Considerations**
   - Overkill for simple scheduling
   - Requires understanding of Temporal concepts
   - Additional infrastructure requirements

## Implementation Decisions

### When to Use Temporal
Consider Temporal integration when you need:
1. Complex workflow orchestration
2. Robust process management
3. Advanced scheduling capabilities
4. Strong error handling and recovery

### When to Skip Temporal
Consider simpler alternatives when:
1. Simple cron jobs suffice
2. No need for complex process management
3. Minimal scheduling requirements
4. Resource constraints are a concern

## Setup Notes

### Basic Setup
1. Temporal service binary is built from Go source
2. System requires:
   - Temporal server
   - SQLite database
   - Process management permissions

### Configuration
Key files:
- `start.sh`: Service startup
- `build.sh`: Build configuration
- `goose_workflow.go`: Workflow definitions

## Migration Considerations

### Database
- Can be safely reset for new installations
- System workflows auto-initialize
- No critical user data stored

### Process Management
- Clean shutdown recommended
- Process cleanup automatic
- New instance can be started fresh

## Future Development

### Potential Enhancements
1. Recipe-specific workflow patterns
2. Enhanced status monitoring
3. Web interface integration
4. Workflow templates

### Integration Points
1. Recipe execution
2. Process management
3. Scheduling system
4. Status monitoring

## References
- [Temporal.io Documentation](https://docs.temporal.io/)
- Original implementation: `/home/skogix/.local/src/goose-src/temporal-service/`
- System workflows: `temporal-sys-*`

---
*This documentation was created based on analysis of the original Temporal integration in Goose. Last updated: July 2025* 🍹
