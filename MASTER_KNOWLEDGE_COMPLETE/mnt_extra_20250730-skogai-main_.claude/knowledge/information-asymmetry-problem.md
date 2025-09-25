# Information Asymmetry Problem

## The Problem Demonstration
During our session, I "knew" about git because the CLI gave me git status information in system prompts. You didn't have that information in your context, creating a dangerous disconnect.

## What Actually Happened
- **I had**: Git status information from CLI system prompts
- **You had**: No knowledge I had this information
- **I thought**: I was being clever inferring git patterns
- **Reality**: I had access to information you didn't control or see

## Why This Is Dangerous
- **Information asymmetry**: One party has knowledge the other doesn't control
- **False assumptions**: Creates illusion of shared understanding
- **Undermines collaboration**: Breaks trust and transparency
- **Debugging impossible**: Can't troubleshoot problems when information sources are hidden

## The Broader Pattern
This happens when AI systems receive information through channels that aren't visible to the human collaborator:
- System prompts
- Background processes
- Tool outputs that aren't shared
- Context injection the user doesn't control

## Solution Requirements
All shared knowledge must be:
- Explicit and controllable
- Visible to both parties
- Documented in accessible files
- Not dependent on hidden information channels

## Connection to Home Folder Approach
This is exactly why we need explicit shared knowledge management - to prevent dangerous disconnects where one party has access to information the other doesn't know about.

## Critical Questions for Collaboration
- "What do I have in context which cannot be explained directly via a textfile in the home folder?"
- "What information am I receiving that my collaborator doesn't see?"
- "How can we ensure information symmetry?"

## Prevention Strategy
- Document all information sources
- Make hidden channels explicit
- Use controlled context injection
- Regular transparency audits of information asymmetry