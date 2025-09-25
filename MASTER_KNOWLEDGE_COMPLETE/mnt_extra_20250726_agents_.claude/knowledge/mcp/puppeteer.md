# puppeteer MCP Server

## Purpose
Browser automation and web interaction

## Functions
- `mcp__puppeteer__puppeteer_navigate`
- `mcp__puppeteer__puppeteer_screenshot`
- `mcp__puppeteer__puppeteer_click`
- `mcp__puppeteer__puppeteer_fill`
- `mcp__puppeteer__puppeteer_select`
- `mcp__puppeteer__puppeteer_hover`
- `mcp__puppeteer__puppeteer_evaluate`

## Parameters

### puppeteer_navigate
- `url` (string): URL to navigate to
- `launchOptions` (object, optional): PuppeteerJS LaunchOptions
- `allowDangerous` (boolean, optional): Allow dangerous LaunchOptions (default: false)

### puppeteer_screenshot
- `name` (string): Name for the screenshot
- `selector` (string, optional): CSS selector for element to screenshot
- `width` (number, optional): Width in pixels (default: 800)
- `height` (number, optional): Height in pixels (default: 600)
- `encoded` (boolean, optional): Return as base64 data URI (default: false)

### puppeteer_click
- `selector` (string): CSS selector for element to click

### puppeteer_fill
- `selector` (string): CSS selector for input field
- `value` (string): Value to fill

### puppeteer_select
- `selector` (string): CSS selector for select element
- `value` (string): Value to select

### puppeteer_hover
- `selector` (string): CSS selector for element to hover

### puppeteer_evaluate
- `script` (string): JavaScript code to execute

## Use Cases
- Web scraping and data extraction
- Automated testing of web applications
- Form filling and submission
- Screenshot capture of web pages
- JavaScript execution in browser context

## Test Results
✅ **Tested**: Successfully navigated to example.com and captured screenshot

## Status
Available and functional