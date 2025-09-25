#!/bin/bash

# Script to collect system performance metrics

METRICS_FILE="/home/skogix/skogai/metrics/system-metrics.json"

# Collect basic metrics
echo "{" > $METRICS_FILE
echo "  \"timestamp\": \"$(date -Iseconds)\"," >> $METRICS_FILE
echo "  \"context_count\": $(ls -1 /home/skogix/skogai/context/archive/ 2>/dev/null | wc -l)," >> $METRICS_FILE
echo "  \"knowledge_modules\": {" >> $METRICS_FILE
echo "    \"core\": $(find /home/skogix/skogai/knowledge/core -type f -name "*.md" | wc -l)," >> $METRICS_FILE
echo "    \"expanded\": $(find /home/skogix/skogai/knowledge/expanded -type f -name "*.md" | wc -l)," >> $METRICS_FILE
echo "    \"implementation\": $(find /home/skogix/skogai/knowledge/implementation -type f -name "*.md" | wc -l)" >> $METRICS_FILE
echo "  }," >> $METRICS_FILE
echo "  \"agents\": $(find /home/skogix/skogai/agents/implementations -type f -name "*.md" | wc -l)," >> $METRICS_FILE

# Add placeholder for performance metrics
echo "  \"performance\": {" >> $METRICS_FILE
echo "    \"average_response_time\": \"N/A\"," >> $METRICS_FILE
echo "    \"context_switches\": \"N/A\"," >> $METRICS_FILE
echo "    \"knowledge_retrieval_time\": \"N/A\"" >> $METRICS_FILE
echo "  }" >> $METRICS_FILE
echo "}" >> $METRICS_FILE

echo "Metrics collected successfully in $METRICS_FILE"