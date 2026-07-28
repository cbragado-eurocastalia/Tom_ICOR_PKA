# myPKA Expansion Spec — v1 (locked at scaffold v1.7.0)

This document is the public, **locked** contract for authoring a myPKA Expansion. If you are writing one, this is what you write to. If you are wondering what an Expansion is allowed to do, this is what defines it.

Schema v1 was locked at scaffold v1.7.0. Last amended at **scaffold v5.4.0**
(2026-07-28): a pack-root `LICENSE` file is now required, `requires_agents`
behaviour on renamed derivatives is stated, and two claims about the scaffold
shipping no Expansion code were corrected. The schema itself is unchanged.

> **Vocabulary.** v1.5/1.6 called these "Extensions." v1.7 renames the architecture to **Expansions** end-to-end (folder `Expansions/`, manifest `expansion.yaml`, adapter doc `ADAPT-EXPANSION.md`). The technical contract is otherwise unchanged from v1.5/1.6 except for the schema additions documented below.

---

## What an Expansion is

An Expansion is a single folder that **grows the user's pre-hired team or wires the team to an external system**. Drop the folder into `Expansions/`. Larry detects it on the next session boot, walks the install workstream ([[WS-003-install-an-expansion]]), and the team grows.

Two important framing notes:

1. **Expansions are how the team grows.** This is the user-facing thesis: "install a pack, hire more specialists, stay non-blocking." Some Expansions add agents, some add connectors, some add runtimes — but the through-line is always "the team learns something new it can do."
2. **Expansions are uninstallable.** `rm -rf` the folder (after running uninstall) and the scaffold is back to its prior shape. This is non-negotiable. No silent state writes outside `residual_paths`.

**What the scaffold's `Expansions/` folder actually contains** (corrected at 5.4.0; earlier revisions of this spec said "structurally empty by design", which stopped being true at 5.0.0): this spec, the README, an `INDEX.md` template, the `.trusted-sources` pin file, and exactly one bundled Expansion, the free myPKA Cockpit at `mypka-cockpit/`, whose source lives in this repository since the 2026-07-23 consolidation. Everything else, including the official Expansion Packs, lives outside this repository, ships as a zip, and is dropped into the user's own `Expansions/` folder.

---

## The four shapes (`expansion_type`)

| Shape | Adds | Examples |
|---|---|---|
| `agent_pack` | New specialists (`adds_agents`), their SOPs, optionally Guidelines/Templates | App Developer Pack (Felix + Vex + Vera) |
| `connector` | OAuth/API/webhook wiring, env vars, MCP server registrations. May add SOPs default-owned by Mack. | Notion, Readwise, Linear |
| `runtime` | Long-lived background process (`start.command` / launchd plist). Listener/relay shape. | myPKA Cockpit, a chat-relay listener |
| `hybrid` | Combines two of the above. Rare. Permitted only when splitting into two Expansions would produce a worse user experience. | An agent pack that also ships a runtime listener |

---

## `expansion.yaml` — schema v1 (LOCKED)

Every Expansion folder MUST contain an `expansion.yaml` at its root. Larry parses it forgivingly: bad YAML or missing required fields produce an `invalid` row in `INDEX.md` rather than crashing the session.

### Required fields (all expansion types)

| Field | Type | Notes |
|---|---|---|
| `name` | string | Human-readable name. |
| `slug` | string | kebab-case. MUST match the folder name. |
| `version` | semver | `MAJOR.MINOR.PATCH`. |
| `description` | string | One sentence. Goes into `Expansions/INDEX.md`. |
| `category` | string | Free-text tag for the AI Library (e.g., `agents`, `connector`, `productivity`). |
| `expansion_type` | enum | `agent_pack` \| `connector` \| `runtime` \| `hybrid` |
| `requires_agents` | list | Pre-hired agents this Expansion uses (e.g., `[Larry, Mack]`). Larry blocks install if any are missing. |
| `license` | string | SPDX identifier or short string (`proprietary`, `MIT`, `CC-BY-SA-4.0`, …). **The declared value MUST match the `LICENSE` file at the pack root** (see "A `LICENSE` file at the pack root is required" below). |
| `author` | string | Who shipped this Expansion. |

### Conditional / optional fields

| Field | When | Shape |
|---|---|---|
| `homepage` | optional | URL to the Expansion's documentation page. |
| `adds_agents` | `agent_pack` or `hybrid` | List of `{ name, role, folder }`. `folder` is the destination subfolder under `Team/`. |
| `adds_sops` | optional, any type | List of `{ default_owner, file }`. The install workstream auto-numbers (next free `SOP-XXX-`) into `Team Knowledge/SOPs/`. |
| `adds_guidelines` | rare | List of `{ slug, file }`. Most Expansions don't ship Guidelines. |
| `adds_workstreams` | rare | List of `{ slug, file }`. Workstreams are emergent — pre-shipping is the exception, not the rule. Permitted when the Expansion ships canonical day-1 multi-agent flows that the user can't reasonably author themselves. |
| `adds_templates` | optional | List of relative paths under the Expansion folder to copy into `Team Knowledge/Templates/`. |
| `env_vars` | `connector`, `runtime`, `hybrid` | List of `{ key, description, required, sensitive }`. The install workstream prompts the user for `required: true` values; `sensitive: true` values are echoed masked and stored in the Expansion's `.env`. |
| `post_install_steps` | optional | Human-readable list. Larry walks the user through these after install completes. |
| `post_install_validation` | optional | Machine-checkable. Either a shell command to run, or a list of checks (`{ type: "file_exists", path: "…" }`, `{ type: "shell", cmd: "…", expect_exit: 0 }`, `{ type: "http", url: "…", expect_status: 200 }`). |
| `mcp_servers` | optional, any type | List of MCP server configs. Mack registers these with the user's LLM tool (Claude Code config, Codex config, etc.). Schema: `{ name, command, args, env_vars }`. |
| `runtime` | `runtime` or `hybrid` | Object describing the long-lived process. See **runtime block** below. |
| `uninstall` | optional | `{ method: "rm-rf-folder", residual_paths: [...] }`. If omitted, defaults to `rm-rf-folder` with no residuals. |
| `requires_scaffold_version` | deprecated (removed 5.0.1) | Former semver-range compatibility pin. No longer required, no longer enforced: the install workstream tolerates the field if present and ignores it. Do not add it to new manifests. |

### Runtime block (when `expansion_type` includes a runtime)

```yaml
runtime:
  start:
    command: ./scripts/start.command          # macOS double-clickable
    sh: ./scripts/start.sh                    # Linux
    bat: ./scripts/start.bat                  # Windows
  launchd_plist: ./scripts/launchd-plist.template  # macOS background daemon (optional)
  port: null                                   # null if no port bound (Socket Mode etc.)
  interactive: false                           # true if the runtime needs a foreground terminal
```

Larry **announces** runtimes. He never auto-launches them. The user double-clicks `start.command` (or platform equivalent) when ready. This rule is enforced by Mack's contract and is a hard line in the scaffold.

---

## Example manifests

### Example 1 — `agent_pack` (App Developer Pack)

```yaml
name: App Developer Pack
slug: app-developer
version: 1.0.0
description: Adds Felix (frontend), Vex (security), Vera (QA) to your team for building, auditing, and quality-gating apps.
category: agents
expansion_type: agent_pack
requires_agents: [Larry, Nolan, Mack]
license: proprietary
author: myICOR

adds_agents:
  - { name: Felix, role: Frontend Developer, folder: "Felix - Frontend Developer" }
  - { name: Vex,   role: Security Engineer,  folder: "Vex - Security Engineer" }
  - { name: Vera,  role: QA Specialist,      folder: "Vera - QA Specialist" }
adds_sops:
  - { default_owner: Felix, file: SOP-felix-build-a-component.md }
  - { default_owner: Vex,   file: SOP-vex-security-audit.md }
  - { default_owner: Vera,  file: SOP-vera-quality-gate.md }
adds_guidelines: []
adds_workstreams: []
adds_templates: []
env_vars: []
post_install_steps:
  - "Larry will introduce the three new specialists in your next session."
  - "If you have a design system, Vera references Team Knowledge/Guidelines/GL-003-design-system.md for visual QA."
post_install_validation:
  - { type: "file_exists", path: "Team/Felix - Frontend Developer/AGENTS.md" }
  - { type: "file_exists", path: "Team/Vex - Security Engineer/AGENTS.md" }
  - { type: "file_exists", path: "Team/Vera - QA Specialist/AGENTS.md" }
```

### Example 2: `runtime` (chat-relay listener, illustrative)

A worked example of the `runtime` shape: a long-lived listener that relays messages
between a third-party chat workspace and `Team Inbox/`. Illustrative only. It is not a
pack anyone ships, and the values below are placeholders.

```yaml
name: Chat Relay
slug: acme-chat-relay
version: 1.0.0
description: Use your chat workspace as a surface for Larry. Inbound DMs and @-mentions land in Team Inbox; replies post back in-thread.
category: connector
expansion_type: runtime
requires_agents: [Larry, Mack]
license: MIT
author: Acme Labs
homepage: https://example.com/chat-relay

adds_agents: []
adds_sops:
  - { default_owner: Larry, file: SOP-chat-relay-incoming-routing.md }
  - { default_owner: Mack,  file: SOP-chat-relay-post-message.md }
  - { default_owner: Mack,  file: SOP-chat-relay-listener-health.md }
adds_guidelines: []
adds_workstreams: []
adds_templates: []
env_vars:
  - { key: CHAT_BOT_TOKEN,         description: "Bot token for the chat workspace",                 required: true,  sensitive: true }
  - { key: CHAT_SOCKET_TOKEN,      description: "App-level token for the socket connection",        required: true,  sensitive: true }
  - { key: CHAT_DEFAULT_CHANNEL,   description: "Default channel ID for outbound posts",            required: false, sensitive: false }
  - { key: CHAT_NOTIFY_OS,         description: "Surface OS notifications on inbound (true/false)", required: false, sensitive: false }
  - { key: CHAT_AUTORESPONDER_MIN, description: "Minutes before autoresponder fires (default 30)",  required: false, sensitive: false }
post_install_steps:
  - "Create the app in your chat workspace's developer console (see INSTALL.md)."
  - "Enable the socket connection, install the app to your workspace, copy both tokens into .env."
  - "Double-click scripts/start.command to launch the listener."
post_install_validation:
  - { type: "shell", cmd: "test -s Expansions/acme-chat-relay/.env", expect_exit: 0 }
runtime:
  start:
    command: ./scripts/start.command
    sh: ./scripts/start.sh
    bat: ./scripts/start.bat
  launchd_plist: ./scripts/launchd-plist.template
  port: null
  interactive: false
uninstall:
  method: rm-rf-folder
  residual_paths:
    - ~/Library/LaunchAgents/com.acme.mypka-chat-relay-listener.plist
    - Team Knowledge/SOPs/SOP-chat-relay-incoming-routing.md
    - Team Knowledge/SOPs/SOP-chat-relay-post-message.md
    - Team Knowledge/SOPs/SOP-chat-relay-listener-health.md
    - Team Inbox/chat-relay-incoming/
    - Team Inbox/chat-relay-outgoing/
```

### Example 3 — `connector` (Notion-style, illustrative)

```yaml
name: Notion Connector
slug: notion-connector
version: 1.0.0
description: OAuth-authenticated Notion API connector. Mack uses it for imports and live reads.
category: connector
expansion_type: connector
requires_agents: [Larry, Mack, Silas]
license: proprietary
author: myICOR

adds_sops:
  - { default_owner: Mack, file: SOP-notion-fetch.md }
env_vars:
  - { key: NOTION_TOKEN, description: "Notion internal integration token", required: true, sensitive: true }
mcp_servers:
  - name: notion
    command: npx
    args: ["-y", "@notionhq/notion-mcp-server"]
    env_vars: [NOTION_TOKEN]
post_install_steps:
  - "Create an integration at https://www.notion.so/profile/integrations and paste the token into .env."
  - "Share the workspaces / pages you want Larry to access with the integration."
post_install_validation:
  - { type: "shell", cmd: "test -n \"$NOTION_TOKEN\"", expect_exit: 0 }
```

---

## A `LICENSE` file at the pack root is REQUIRED (added 5.4.0)

Every Expansion MUST carry a `LICENSE` file at its folder root, and the `license:`
field in `expansion.yaml` MUST name the same terms.

The `license:` field is a label. A label is not a grant. A pack whose manifest says
`MIT` with no `LICENSE` file has given the person installing it a description of a
licence rather than a licence, which leaves both sides guessing about what was
actually permitted. That is the gap this rule closes.

| Rule | Detail |
|---|---|
| **File** | `LICENSE` (no extension) at the pack root, next to `expansion.yaml`. `LICENSE.md` and `LICENSE.txt` are accepted. |
| **Content** | The full licence text, or, for a Creative Commons licence, the canonical summary plus the URI to the legal code. A bare licence name is not sufficient. |
| **Agreement** | `expansion.yaml` `license:` must name the same licence as the `LICENSE` file. Where they differ, the `LICENSE` file wins, and the mismatch is a defect in the pack. |
| **Proprietary packs** | `license: proprietary` is still a valid value. It still requires a `LICENSE` file stating the proprietary terms and who to contact. "Proprietary" is not an excuse to ship nothing. |
| **Bundled third-party assets** | Fonts, icons, libraries and other bundled assets under their own terms are listed in a `NOTICE` file at the pack root, alongside the `LICENSE`. |
| **Enforcement** | A hard requirement of the spec, not a recommendation. Two checks are specified to enforce it: a release-CI check that blocks any pack in this repository whose `expansion.yaml` has no matching pack-root `LICENSE`, and a check in the install workstream ([[WS-003-install-an-expansion]]) that surfaces a missing or mismatched licence before the user grants trust. Neither is wired yet. Until they are, a pack without a `LICENSE` is a spec violation caught in review. |

The bundled Cockpit is the worked example: `Expansions/mypka-cockpit/` carries
`LICENSE` and `NOTICE` at its root, and its `expansion.yaml` declares
`license: LicenseRef-myICOR-Cockpit-Personal-Use-1.0`, which is the name of the
licence in that file. The Cockpit licence is *based on* PolyForm Noncommercial
1.0.0 but is not that licence: it adds attribution conditions and express
disclaimers. Declaring the standard SPDX identifier would therefore be a
mislabel, and `LicenseRef-` is the correct SPDX form for a licence that is not on
the SPDX list. If your pack adapts a standard licence, do the same.

---

## Official packs target the canonical agent names (added 5.4.0)

`requires_agents` names the pre-hired specialists a pack depends on. Official
myICOR-issued packs name the **canonical scaffold specialists** (Larry, Nolan,
Pax, Penn, Mack, Silas). The install workstream blocks the install when a named
agent is not present in `Team/agent-index.md`.

**Consequence, stated so nobody has to discover it:** official Expansion Packs are
**not supported on a renamed derivative of the scaffold**. Renaming the team is
fully permitted under CC BY-SA 4.0 and is encouraged for anyone shipping their own
version (see `DERIVATIVES.md`), but a renamed team will fail the `requires_agents`
check, and that is correct behaviour rather than a bug.

myICOR does not maintain compatibility shims, alias maps, or per-derivative pack
builds, and does not troubleshoot official-pack installs against a renamed team.
An author distributing a derivative owns their own pack story.

The same applies in reverse to third-party packs: name the agents your pack
actually needs, in the naming of the scaffold you support, and say which that is
in your README.

---

## Conventions

- **Folder name = `slug`.** No exceptions.
- **Trinity files at root:** `expansion.yaml`, `README.md`, `ADAPT-EXPANSION.md`. The `ADAPT-EXPANSION.md` is the LLM-facing operating manual (what to do when this Expansion is invoked).
- **`LICENSE` at root: required.** See the section above. `NOTICE` alongside it when the pack bundles third-party assets.
- **Token files never committed.** `.env.example` is committed; `.env` is gitignored and chmod 600 by the install script.
- **SOPs ship as files in the Expansion folder, not pre-numbered.** The install workstream auto-numbers them into the your myPKA. Filename inside the Expansion is descriptive (`SOP-notion-fetch.md`); the installer renames to the next free `SOP-NNN-…` slot.
- **Agent folder names follow `<Name> - <Role>`** to match scaffold convention.
- **No code at the scaffold root.** All Expansion code stays inside the Expansion folder. `runtime/` for long-lived processes; `scripts/` for installers and starters.

---

## Security considerations

| Concern | Rule |
|---|---|
| Token storage | Always env vars in the Expansion's `.env`. Never inline in `expansion.yaml`. Never logged. |
| Sensitive env display | `sensitive: true` env vars are echoed masked and never written to session-logs. |
| Manifest tampering | Tier-2 (myICOR-issued) Expansions are hash-pinned in the canonical `.trusted-sources` registry — maintained in the private `mypka-expansions` repo and generated by the release pipeline. Vex audits before the hash is pinned. Hash mismatch → Larry refuses install. |
| Withdrawn packs | A pack myICOR has withdrawn from the offering is named in the `WITHDRAWN` block of the shipped `Expansions/.trusted-sources`. Larry refuses to install a withdrawn slug regardless of hash, and the slug stays reserved so no one else can claim it. A hash only proves authorship of the bytes; it never proves the pack is still supported. |
| Outbound network defaults | Connectors and runtimes that talk to third-party APIs MUST default to least-permissive options. Slack-specific: `unfurl_links: false` and `unfurl_media: false`. Webhook receivers MUST verify signatures. |
| `requires_agents` enforcement | Larry blocks install if a required pre-hired agent is missing. The user is told which Expansion to install first. |
| Vex security pass | Recommended before public release for any Expansion that touches the network or executes long-lived processes. Required before tier-2 hash-pinning. |

The manifest is **informational only**. Its declarations are not verified, enforced, or guaranteed by Paperless Movement S.L. or by Larry beyond hash-pinning at tier-2. The user is solely responsible for evaluating an Expansion's trustworthiness before installation.

---

## Trust model — three tiers

| Tier | Source | Larry's action on detection |
|---|---|---|
| 1 — Bundled | `author: myICOR` and ships in scaffold | Auto-trust. No prompt. (None ship in v1.7.) |
| 2 — myICOR-issued | `author: myICOR`, manifest hash matches the canonical `.trusted-sources` registry (in `mypka-expansions`, pipeline-generated) | Calm announcement. Auto-trust on hash match; warn on mismatch. |
| 3 — Community / unknown | Anything else | Interactive prompt: declared permissions + three actions (`trust` / `skip` / `inspect`). Decision cached in `Expansions/.trust.yaml`. Re-prompt on major version bump. |

Trust is granted to a `(slug, version)` pair. Major version bumps re-prompt.

---

## Naming convention

| Pattern | Use case |
|---|---|
| `app-developer/`, `designer-pack/`, `mypka-cockpit/` | RESERVED for myICOR-issued Expansions. Brand-protected via `author: myICOR` + hash pinning. |
| `slack/` | RESERVED and WITHDRAWN. myICOR withdrew the Slack Expansion on 2026-07-27; the slug stays reserved so it cannot be claimed by anyone else, and Larry refuses to install it. |
| `community-<name>/` | Community Expansions seeking visibility under the umbrella. |
| `<author>-<name>/` | Default third-party namespace. |

---

## Uninstall expectations

Symmetric to install. The uninstall flow ([[WS-003-install-an-expansion]] §uninstall):

1. Larry detects an uninstall request ("uninstall the Designer Pack", "remove App Developer pack").
2. Nolan reverses the team merge (removes the Expansion's agents from `Team/`, restores `Team/agent-index.md`).
3. Mack tears down connector wiring (stops runtimes, removes launchd plists, deregisters MCP servers).
4. Silas validates the post-uninstall myPKA state.
5. Larry archives the Expansion folder to `Expansions/_uninstalled/<slug>-<version>/.manifest.json` and writes the session-log entry.

`uninstall.method: rm-rf-folder` plus `residual_paths` is the uninstall contract. Anything not declared in `residual_paths` will be left behind — that's a bug in the Expansion, not the scaffold.

---

## Compatibility — refuse-to-install on mismatch

The install workstream refuses to proceed when:

- A required field is missing or malformed → `invalid` row in `INDEX.md`, install blocked.
- A required pre-hired agent listed in `requires_agents` is not in `Team/agent-index.md` → install blocked with a "install X first" message. On a renamed derivative of the scaffold this is the expected outcome for official packs; see "Official packs target the canonical agent names" above.
- No `LICENSE` file at the pack root, or a `LICENSE` that names different terms from the `license:` field → a spec violation since 5.4.0. The install-workstream check that surfaces it to the user before trust is granted is specified and not yet wired; until it is, this is caught in review rather than at install time.

Larry never silently coerces.

**Note on `requires_scaffold_version` (removed 5.0.1).** Older manifests carry a `requires_scaffold_version` semver-range pin. The field is no longer part of the spec: it is tolerated if present, ignored by the install workstream, and never blocks an install. Scaffold compatibility is the Expansion author's testing responsibility, not an install-time gate.

---

## Authoring checklist

Before zipping your Expansion and shipping it:

- Folder name matches `slug`.
- `expansion.yaml` validates against the schema above.
- All required fields present.
- `license` declared; SPDX where possible.
- **`LICENSE` file present at the pack root, and it names the same licence as the `license:` field.** Required since 5.4.0.
- `NOTICE` at the pack root if the pack bundles third-party assets under their own terms.
- `requires_agents` names the agents in the naming of the scaffold you support, and your README says which scaffold that is.
- Tested against the scaffold version(s) you support (there is no install-time version gate — testing is on you).
- `env_vars` match what the runtime/connector actually reads.
- `adds_sops` files exist in the Expansion folder and are LLM-agnostic.
- `adds_agents` folders match `Team/<Name> - <Role>/AGENTS.md` shape.
- `uninstall.residual_paths` lists every path written outside the Expansion folder.
- `README.md` at the folder root: human-facing, in the user's voice, what it does + how to remove it.
- `ADAPT-EXPANSION.md` at the folder root: LLM-facing operating manual.
- Optional but recommended: `INSTALL.md` walking the user through any external setup (creating an OAuth app, generating tokens, etc.).
- Vex security pass before tier-2 hash pinning.

---

## What the scaffold does NOT ship (corrected at 5.4.0)

- **No Expansion binaries or build artifacts.** The bundled Cockpit ships as source-shape; members build it on install. Release CI fails if a build artifact is git-tracked.
- **No third-party Expansion code.** The only in-repo Expansion is the myPKA Cockpit, published by myICOR.
- **No official Expansion Packs.** The Designer Pack and the App Developer Pack left this repository at 5.0.0 and are part of the myICOR membership.
- **No secrets.** `.env` is gitignored at any depth; only `.env.example` is committed.

Everything else lives in its own repository, ships as a zip, and is dropped into the user's `Expansions/` folder. The scaffold ships this spec, the contract, the trust pins, Larry's discovery routine, and the WS-003 install workstream.
