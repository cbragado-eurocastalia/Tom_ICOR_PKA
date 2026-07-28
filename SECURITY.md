# Security Policy

myPKA is a **local-first, single-user, markdown folder**. It has no server, no
account, no database of ours, and no telemetry. It runs on your machine, under
your LLM tool, on files you own. That shape is the security model, and most of
this page follows from it.

## Supported versions

| Version | Supported |
|---|---|
| 5.4.x | Yes. Current release line. |
| 5.0.x to 5.3.x | Security fixes only, on the next 5.4.x release. |
| < 5.0.0 | Not supported. Update to the current line. |

Security fixes land on the current minor line. `manifest.json` `scaffold_version`
is the single source of truth for what you are running; `VERSION` and
`.scaffold-version` mirror it.

## Reporting a vulnerability

**Report privately. Do not open a public issue for an unfixed vulnerability.**

- **Preferred:** GitHub private vulnerability reporting on this repository
  (Security tab, "Report a vulnerability").
- **Email:** `support@myicor.com`, marked SECURITY in the subject line.

Please include the affected version (from `manifest.json`), what you observed,
how to reproduce it, and the impact you think it has. A proof of concept helps
and is not required.

**What to expect.** We acknowledge within 5 working days and give you an initial
assessment within 10. Coordinated disclosure is the default: we agree a fix
timeline with you, ship the fix, and credit you in the release notes if you want
credit. Please give us a reasonable window before public disclosure. Our target
is 90 days from your report, shorter when the fix is simple, and we will tell you
if something is going to take longer rather than going quiet.

We do not run a paid bug bounty.

## Scope

**In scope**

- The scaffold's own scripts: `scripts/update-scaffold.py`, `scripts/check-version.py`,
  `validation-script.sh`, and the scripts under `Team Knowledge/scripts/`.
- The framework and user-state path boundary in `manifest.json`. A path that lets
  an update bundle write outside `framework_paths`, or write anything under
  `user_state_paths`, is a vulnerability and we want to hear about it.
- The bundled myPKA Cockpit at `Expansions/mypka-cockpit/`. It has its own, more
  detailed policy at `Expansions/mypka-cockpit/SECURITY.md`; report Cockpit
  issues through the same channels above.
- Anything in a published release artifact that should not be there: a credential,
  a private path, a key of any kind.

**Out of scope**

- Your own vault contents, your notes, and anything your LLM tool does with them.
  The scaffold is text on disk; it does not execute your notes.
- Third-party Expansions you install, and third-party MCP servers you register.
  `Expansions/README.md` states this: an Expansion is someone else's code that you
  chose to run. We do not vet, audit, sandbox, or accept authorial responsibility
  for third-party Expansions.
- Your LLM provider, your LLM tool, and your operating system.
- Prompt injection against your own LLM through content you deliberately imported.
  Treat imported content as untrusted, the same as you would in any other tool.

## What the scaffold does over the network

Exactly one thing, and it is worth knowing precisely.

`scripts/check-version.py` makes a single read-only HTTPS GET for one plain-text
version string, at most 64 bytes, with a 3 second timeout, and fails silent when
offline. It sends no vault contents, no filenames, no identifiers, and no
telemetry. It never downloads or applies anything. The destination is declared in
`manifest.json` under `update_check.remote_version_url` and the disclosure text
sits next to it. Set `update_check.enabled` to `false` to turn it off.

`scripts/update-scaffold.py` makes **no** network call at all. It works on an
update bundle already on your disk, is dry-run by default, and fails closed: it
refuses any path outside the `framework_paths` allow-list, refuses any path
inside `user_state_paths` even if an update bundle asks for it, refuses to write
outside the scaffold root, and backs up any framework file you have locally
modified before overwriting it.

Nothing else in the scaffold core reaches the network.

## Standing distribution rules (release-blocking)

These apply to every release of the scaffold and to every Expansion, connector,
or pack built on it. A release that breaks one of these does not ship.

### Keys never leave the user's machine (bring your own key)

- Anything that talks to an LLM provider is **bring your own key**. Each user
  supplies their own key. It is read from that user's local environment or
  config, held in memory locally, and **never** pooled, proxied, centrally
  stored, or reused across users.
- A frontend never calls a provider API directly. It calls the local server on
  `localhost`, and only that.
- Routing multiple users through one key, or through consumer subscription
  credentials, is an outright provider Terms of Service violation and is
  prohibited outright, not discouraged.
- **No key of any kind ships in any artifact.** Not in a release ZIP, not in a
  manifest, not in an example file, not in a commit.

### Secrets by reference, never by value

- API keys and tokens live in `Team Knowledge/.env` (gitignored, file mode
  `0600`) or in an Expansion's own `.env`. `.env` at any depth is gitignored;
  `.env.example` is the only committed form.
- Code resolves a secret by key **name** at the point of use. A secret value must
  never appear in a route response, a log line, an error message, a session-log
  entry, a derived database, or a commit.
- `expansion.yaml` declares secrets as `env_vars` with `sensitive: true`. It never
  contains a secret value.

### Release integrity

- Release artifacts are built deterministically and the ZIP sha256 is published on
  the release page, so any downloader can verify the bytes they received.
- CI holds no service-role key and no database credential. The release pipeline
  talks to a single edge function with a shared secret and uploads through
  short-lived signed URLs.
- Official Expansions are hash-pinned in `Expansions/.trusted-sources`. A hash
  mismatch blocks the install.

## If you are distributing your own version

You may. See `DERIVATIVES.md`. Two security-relevant points from it, repeated here
because they are the ones people miss:

- **Re-point or disable `update_check`.** A derivative that leaves it pointed at
  the upstream repository will have upstream framework files written over the
  derivative's own by any user who follows the update prompt.
- **Delete `Expansions/mypka-cockpit/`** before you distribute. It is separately
  licensed and is not yours to redistribute.

## Safe harbour

If you research in good faith, act only against your own installation, avoid
privacy violations and service disruption, give us reasonable time to fix what you
find, and do not exfiltrate or destroy data, we will not pursue legal action
against you and we will treat your report as authorised.

---

Security reports: `support@myicor.com` (subject line SECURITY), or the GitHub
Security tab. Everything else, including trademark and licensing: `contact@myicor.com`.
