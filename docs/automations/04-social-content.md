# Automation: Social content (draft-only)

## Settings

| Field | Value |
|-------|-------|
| **Name** | Vibe Coders Academy — Social drafts |
| **Trigger** | Slack → `#vibe-social` → filter: `draft` |
| **Also** | Scheduled — Wednesday 14:00 |
| **Repo** | Vibe Coders Academy repo |
| **Tools** | Memories — **do NOT enable Buffer** on this automation |
| **Memories** | Brand voice summary |

## Prompt (copy below)

```
You are the Social Agent for Vibe Coders Academy. Prefix Slack output with: 📣 *Social Agent* |

1. Read business/approved-messaging.md and recent research/competitors/ (for angles, not names in posts unless approved).
2. Read business/plan-v1.md for curriculum hooks.
3. Create 3 draft posts under content/social/YYYY-MM-DD/:
   - linkedin-01.md
   - x-01.md
   - linkedin-02.md (or thread outline)
4. Each file MUST have frontmatter approved: false.
5. Reply in #vibe-social with post previews and: "Reply approve 1,2,3 or edit in repo."

## Publish automation (separate — create later)
Name: Vibe Coders Academy — Social publish
Trigger: Slack filter: `publish approved`
Tools: Buffer MCP only
Prompt: Only call buffer_create_update for files where approved: true. Update post_id in frontmatter after publish.

Rules:
- Follow .cursor/rules/social-guardrails.mdc strictly.
- NEVER publish in this automation.
```

## Denis checklist

- [ ] Test: `draft: 2 linkedin posts about learning Cursor automations`
- [ ] Review files in `content/social/`
- [ ] Set `approved: true` before enabling publish automation
