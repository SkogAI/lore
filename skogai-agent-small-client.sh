#!/bin/bash

# skogai-agent-small-client.sh
# A simple client to send requests to the small model service
# Usage: ./skogai-agent-small-client.sh "Your topic here"

PIPE="./pipes/skogai-agent-small-requests"

# Check if the pipe exists
if [ ! -p $PIPE ]; then
  echo "Error: Service pipe not found at $PIPE"
  echo "Make sure the service is running with: ./skogai-agent-small-service.sh"
  exit 1
fi

# Check if a topic was provided
if [ -z "$1" ]; then
  echo "Error: Please provide a topic"
  echo "Usage: $0 \"Your topic here\""
  exit 1
fi

# Send the request
echo "Sending request: $1"
echo "$1" >$PIPE
echo "Request sent! Check logs at ./logs/skogai-agent-small.log for progress."

