# shopify-dev-mcp MCP Server

## Purpose
Shopify development tools and documentation access

## Functions
- `mcp__shopify-dev-mcp__introspect_admin_schema`
- `mcp__shopify-dev-mcp__search_dev_docs`
- `mcp__shopify-dev-mcp__fetch_docs_by_path`
- `mcp__shopify-dev-mcp__get_started`

## Parameters

### introspect_admin_schema
- `query` (string): Search term to filter schema elements by name (e.g., 'product', 'discountProduct')
- `filter` (array, optional): Filter sections - 'types', 'queries', 'mutations', or 'all' (default)

### search_dev_docs
- `prompt` (string): Search query for Shopify documentation

### fetch_docs_by_path
- `paths` (array): Document paths relative to root (e.g., ["/docs/api/app-home", "/docs/api/functions"])

### get_started
- `api` (string): Shopify API type - 'admin', 'functions', 'hydrogen', or 'storefront-web-components'

## Use Cases
- Shopify app development and API integration
- GraphQL Admin API schema exploration
- Documentation lookup and reference
- Getting started with specific Shopify APIs
- Building apps, functions, and storefronts

## Test Results
✅ **Tested**: Successfully searched for "getting started with Shopify app development" and retrieved comprehensive documentation

## Status
Available and functional