# Sources

## Primary Source

The KeyWe application codebase at `/home/corey/workspace/keywe-app/` was analyzed via an autonomous exploration agent to produce a comprehensive summary of all API routes, database schema, server load functions, form actions, library files, and infrastructure.

## Source Coverage

| Domain                                | Source                                                                                                                                          | Coverage                           |
| ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| Properties, Access Points, Locks CRUD | `src/routes/api/properties/*`, `src/routes/api/access-points/*`, `src/routes/api/locks/*`, `src/lib/server/db/properties.ts`                    | Full                               |
| Schlage API proxy                     | `src/routes/api/schlage/[...path]/+server.ts`, `src/lib/api/schlage.ts`, `src/lib/server/db/auth-keys.ts`                                       | Full                               |
| Reservations                          | `src/routes/api/reservations/*`, `src/lib/server/db/reservations.ts`                                                                            | Full                               |
| Messaging & Templates                 | `src/routes/api/templates/*`, `src/routes/api/messages/*`, `src/lib/server/db/messaging.ts`, `src/lib/server/sms.ts`, `src/lib/server/email.ts` | Full                               |
| Automations                           | `src/routes/api/automations/*`, `src/lib/server/db/automations.ts`                                                                              | Full                               |
| Account & Auth                        | `src/routes/api/account/*`, `src/lib/server/auth.ts`, `src/lib/server/api-keys.ts`, `src/lib/server/db/auth-keys.ts`                            | Full                               |
| Dashboard                             | `src/lib/server/db/dashboard.ts`                                                                                                                | Partial (not in reference files)   |
| Embed Widget                          | `src/routes/embed/*`, `src/routes/api/embed/*`, `static/embed.js`                                                                               | Full                               |
| MCP Server                            | `src/lib/mcp/index.ts`                                                                                                                          | Partial (schlage tools referenced) |
| Chat/WebSocket                        | `src/durable-objects/chat-room.ts`                                                                                                              | Not covered                        |

## Synthesis Method

Codebase exploration via task agent (subagent_type: general) with comprehensive read of all API route files, database schema files, and library files. Skill authored as `integration-documentation` class with reference files for each API domain, common use cases, and troubleshooting.

## Changelog

- 2025-06-18: Initial skill creation with 6 API domain reference files
- 2025-06-18: Added SCHLAGE_EMAIL/SCHLAGE_PASSWORD env var pattern, schlage-login/schlage-logout actions
- 2025-06-18: Fixed SKILL.md compliance (emojis removed, frontmatter corrected), added SOURCES.md, common-use-cases.md, troubleshooting-workarounds.md, moved to .opencode/skills/
- 2025-06-19: Added embed.md reference, embed widget section to SKILL.md, textOptIn fields to reservations.md
