# AI Insights System

Capture non-obvious constraints and reasoning for future AI programming sessions using `@ai-reasoning` comments.

## Annotation Format

**@ai-reasoning**: Why you chose this specific implementation approach

**Always include a preamble comment** when generating functions to explain the overall algorithmic or architectural choice.

**For inline comments**, place them at the start of logical blocks - groups of related statements separated by blank lines - to explain the reasoning for that specific block of code.

**Before modifying code with `@ai-reasoning` comments**, pause and consider: does this reasoning affect my planned changes? These comments capture constraints and tradeoffs that aren't obvious from the code alone.

## Multi-line Annotations

For longer explanations, use separate comment lines or add to the end of existing comments.

## Decision Boundaries

**Focus on non-obvious decisions** - don't annotate self-explanatory code:
- ❌ `# @ai-reasoning: Using a loop to iterate through items`
- ✅ `# @ai-reasoning: Using manual iteration instead of map() to handle partial failures gracefully`

**Include constraint-driven choices** - especially document limitations that might be forgotten:
- ❌ `# @ai-reasoning: Using async/await for the API call`
- ✅ `# @ai-reasoning: Using async/await because this API has 2-second response times that would block the UI`

**Document tradeoffs and alternatives** - explain why you chose this path:
- ❌ `# @ai-reasoning: Using Redis for caching`
- ✅ `# @ai-reasoning: Using Redis instead of in-memory cache because we need persistence across server restarts`

**Capture consistency requirements** - document when you're matching existing patterns:
- ❌ `# @ai-reasoning: Using the same error handling as other functions`
- ✅ `# @ai-reasoning: Using Result<T, E> pattern to match error handling in auth.rs and database.rs modules`

## Guidelines

1. **Focus on decisions with alternatives** - if there was only one way to do it, probably don't annotate
2. **Update annotations when modifying code** - ensure reasoning still matches the implementation
3. **Be concise but specific** - future AI should understand the decision quickly