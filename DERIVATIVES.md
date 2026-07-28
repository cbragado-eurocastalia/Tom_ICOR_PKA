# Building your own version of myPKA

You may build and distribute your own version of the myPKA scaffold. You do not
need our permission, you do not need a separate licence, and you do not owe us a
share of anything you earn from it. The published licence already permits it.

This page exists because there are five places where a derivative can go wrong
quietly, and four of them are invisible until somebody downstream is already
stuck. Everything below is a general rule. It applies to everyone equally, and
nothing on this page is granted or withheld case by case.

Read this alongside `LICENSE`, `LICENSE-MAP.md`, `NOTICE.md`, and `TRADEMARK.md`.
Where this page and any licence file differ, the licence file wins. The Cockpit
and the myICOR member content sit under their own instruments, named in sections
3 and 4, and those govern their own subjects.

---

## 1. Start from v5.3.0 or later. This is the one that cannot be undone.

**Derive from a fresh copy of v5.3.0 or later, taken from
https://github.com/myICOR/myPKA. Do not fork the copy you have been running.**

Releases before v5.3.0 were published under **CC BY-NC-SA 4.0**. Creative Commons
licences are irrevocable, so those copies stay under those terms forever. Nothing
is withdrawn from anyone, and if you hold an older copy you keep it.

The problem is what happens when you *adapt* one. CC BY-NC-SA 4.0 Section 3(b)(1)
requires your adaptation to carry a Creative Commons licence with **the same
licence elements**, which means the NonCommercial term comes with it. Creative
Commons has designated **no compatible licences for CC BY-NC-SA 4.0**. There is
no list and there is no exit.

So a derivative built on a pre-v5.3.0 copy is locked to NonCommercial
permanently:

- Everyone you hand it to receives a NonCommercial-encumbered copy and cannot use
  it in their own paid work.
- You cannot relicense your way out later, because ShareAlike has already bound
  the derivative.
- Once you have distributed it, those downstream copies are NonCommercial
  permanently too, because the licence they received is irrevocable.

None of that is recoverable. A fresh clone before you start costs one command.

**How to confirm you are on the right base:** `LICENSE` reads
"Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)", `TRADEMARK.md`
is present at the root, and `manifest.json` reports `scaffold_version` 5.3.0 or
higher. Those three facts together are the fingerprint.

If you have already built work on an older copy, your own additions are your own
copyright and you may recombine them onto a v5.3.0 base. Rebase the base, keep
your work.

---

## 2. What you must do

Six obligations, from CC BY-SA 4.0 Sections 3(a) and 3(b) plus `NOTICE.md`. All
of them are cheap.

1. **Keep the attribution package.** Retain `NOTICE.md` and `LICENSE` intact.
   Between them they carry the creator identification, the copyright notice, the
   licence notice, the warranty disclaimer, and the link back to the source, which
   is the whole of Section 3(a)(1)(A) discharged in one move. `NOTICE.md` is the
   licensor's supplied attribution form, so it is not optional decoration.

2. **Ship the required README block.** `NOTICE.md` specifies it verbatim:

   > Built on the myPKA™ Scaffold by Paperless Movement® / ICOR®.
   > Source: https://github.com/myICOR/myPKA
   > Licensed under CC BY-SA 4.0.

   Put it where a reader will actually see it, not in a legal footer.

3. **Indicate that you changed things.** Section 3(a)(1)(B). A short "what I
   changed" section or a CHANGELOG is the honest form. If the material you started
   from carried indications of previous modification, retain those too.

4. **Licence your version under CC BY-SA 4.0** and include the licence text or a
   URI to it. Sections 3(b)(1) and 3(b)(2). A later version of BY-SA, or a
   designated BY-SA Compatible Licence, also satisfies this; in practice CC BY-SA
   4.0 is the answer.

5. **Replace the `LICENSE` file if you carried one over.** Publishing a
   BY-SA derivative with a BY-NC-SA `LICENSE` file inside it is a false licence
   statement about your own work, and it misleads everyone downstream about which
   terms they actually hold.

6. **Impose no additional restrictions.** Section 2(a)(5)(C) and Section 3(b)(3).
   See section 5 below, because this is the one people breach by accident.

**A note on renaming.** You may rename every agent, rewrite every SOP, Guideline
and skill, and restructure as you like. The agent names are not trademarks and
renaming needs no permission from us. Distinct names are genuinely better for
everyone, because they reduce confusion about who made what. Renaming does not
reduce any of the six obligations above, and it is precisely the moment people
forget them.

---

## 3. What you must remove before you distribute

**Delete `Expansions/mypka-cockpit/` from any derivative you distribute.**

The Cockpit is in this repository but it is not under Creative Commons. It
carries the **myICOR Cockpit Personal-Use License** (based on PolyForm
Noncommercial 1.0.0), which prohibits redistributing it, or any derivative of it,
as part of or in connection with a commercial product or service, and prohibits
use directed toward commercial advantage or monetary compensation.

That is not a restriction we add to derivatives. It is a different licence on a
different subtree, and `LICENSE-MAP.md` has always said so. The CC BY-SA grant
never reached it.

This rule is general. We do not grant Cockpit carve-outs to individual projects,
programmes, or people, and asking for one will get you this paragraph. Anyone who
wants the Cockpit takes it themselves, from us, under its own terms. If the
Cockpit ever carries commercial terms, they will be published terms open to
everyone on the same basis, never a private arrangement with anyone. If you are
teaching or supporting others, point them at the source rather than bundling it.

Everything else in `Expansions/` at v5.3.0 and later is documentation. The
official Expansion Packs are not part of this repository, so a clean fork will not
carry them accidentally.

---

## 4. What is outside the scaffold licence entirely

Three things, and only the first is obvious.

**Trademarks.** CC BY-SA 4.0 Section 2(b)(2) grants no trademark rights, and
`LICENSE` restates it. PAPERLESS MOVEMENT®, ICOR®, myICOR™ and myPKA™ are not
licensed to you. The published one-sentence test is:

> **Use the marks to say what your work is built on. Do not use them to say who
> your work is by.**

Full guidance, including the worked good and bad examples, is in `TRADEMARK.md`.
Naming your product after ours, using the marks as your branding or domain, or
claiming an endorsement, partnership or certification that does not exist all
need written permission and are usually refused.

**The ICOR® methodology and the myICOR member content.** The scaffold on GitHub
and the myICOR membership product are two different bodies of work under two
different instruments. The methodology, the courses, the lessons, the videos, the
transcripts, and the framework diagrams are **not** under Creative Commons and
never were. They are governed by the myICOR Terms of Use, which reserve them and
prohibit reselling, sublicensing, redistributing, or publicly sharing them.

The line is ideas versus expression. Copyright does not protect a method or a
system, so teaching the concepts in your own words is fine and always was.
Reproducing our expression is not. Two riders. If you are a myICOR member,
holding a CC BY-SA licence on the scaffold gives you no cover on the member
content. And the Terms of Use are a contract, so they can reach further than
copyright does: what they reach is our material, not your understanding of it,
and they keep applying to you as a member whatever licence you hold on the
scaffold.

**Other people's assets that we merely bundle.** The weekly-report deck ships four
webfonts under the SIL Open Font License 1.1. If you ship those assets, keep
`FONT-LICENSES.md` and honour the OFL for those files. The OFL governs the font
binaries only and changes nothing about the scaffold licence.

---

## 5. The platform-terms trap

This is the likeliest accidental breach in an otherwise clean derivative, and
almost nobody sees it coming.

CC BY-SA 4.0 Section 2(a)(5)(C) says you may not offer or impose additional or
different terms on the licensed material if doing so restricts your recipients
from exercising their licensed rights. Section 3(b)(3) repeats it for adapted
material. Under Section 6(a) your licence terminates **automatically** if you
breach it. Section 6(b)(1) reinstates it as of the date you cure the breach,
provided you cure within 30 days of discovering it, and those 30 days run from
your own discovery rather than from any notice by us. Reinstatement restores the
licence going forward; Section 6(b) says expressly that it does not affect any
remedy we may have for the period of the breach.

Course platforms, membership sites, and private repositories behind a member
agreement almost all ship default terms of the form "these materials are for your
personal use, do not copy, do not share, do not redistribute". The moment your
CC BY-SA derivative sits inside terms that say that, you have imposed an
additional restriction on your recipients, and your own licence to the material
terminates automatically. It does not lapse gradually, and it does not wait for
us to notice.

The distinction is sharp:

- **A login wall is fine.** Limiting who gets access, including by requiring a
  username and password, is permitted, as long as the people who do get access can
  still exercise every licensed right afterwards.
- **An anti-sharing clause is not fine.** It is the clause that breaches, not the
  wall.

Two lines of mitigation, both cheap:

1. Publish the derivative at a plain public URL. A public repository is the clean
   instrument, and it discharges obligations 1 to 4 in section 2 at the same time.
2. If a copy also lives inside a platform, add an explicit carve-out stating that
   these files are licensed CC BY-SA 4.0 and that the platform's no-sharing terms
   do not apply to them.

---

## 6. Re-point or turn off the update check

**If you distribute a derivative, you must either set
`update_check.enabled` to `false` in `manifest.json`, or re-point both
`update_check.upstream_repo` and `update_check.remote_version_url` at your own
release.** The two must agree with each other and with `distribution.id`.

This is the one hard technical condition, and it is a two-line edit.

`manifest.json` ships the boot-time update check enabled, pointed at the official
myPKA `VERSION` file. On a derivative that leaves it untouched, every one of your
users is told on every boot that a "myPKA update" is available, aimed at our
release rather than yours.

The consequence is worse than a stray notification. The scaffold updater applies
whatever framework files the bundle it is given contains. A user who follows that
prompt gets our agents, our SOPs and our Guidelines written back over your renamed
team and your own material, with your edits backed up but your product's identity
gone. The support request that follows arrives at us, about a product we did not
build.

While you are in `manifest.json`, set the `distribution` block to identify your
release rather than ours: your own `id`, `is_official_myicor_release: false`, and
the upstream version you derived from in `derived_from`. That block is how a
provenance check, and any human reading the folder, can tell whose release this
is. Declaring yourself there costs nothing and it is the record that settles the
question later.

---

## 7. Official Expansion Packs do not work on a renamed derivative

Official myICOR Expansion Packs declare their dependencies with `requires_agents`,
naming the canonical scaffold specialists (Larry, Nolan, Pax, Penn, Mack, Silas).
The install workstream blocks the install when a named agent is not present in
`Team/agent-index.md`.

If you rename the team, those packs will refuse to install, and that is correct
behaviour rather than a bug. **Official packs target the canonical agent names and
are not supported on renamed derivatives.** We do not maintain compatibility
shims, alias maps, or per-derivative pack builds, and we do not troubleshoot pack
installs against a renamed team.

Renaming is fully permitted and we encourage it. This is simply the trade that
comes with it: your derivative, your team names, your Expansion story.

---

## 8. What we do not ask for

Stated plainly, because people keep offering:

- **No revenue share.** Charge whatever you like for whatever you build.
- **No approval rights.** We do not review, approve, or sign off your curriculum,
  your product, or your changes.
- **No separate licence.** The published licence is the whole grant. There is
  nothing extra to negotiate and asking will get you this page.
- **No case-by-case permissions under the scaffold licence.** We do not issue
  bespoke grants, private exceptions, or individual carve-outs to what CC BY-SA
  4.0 already gives you. Everything anyone may do with the scaffold is written
  down here and in the licence files, identically for everyone. Trademark
  permission, OEM licensing, and branded redistribution are separate instruments
  rather than exceptions to this one, and they are answered on published terms
  rather than as personal favours. They are the address at the foot of this page.
- **No partnership, certification, or affiliation.** Not on offer, and claiming one
  is a trademark problem rather than a licence problem. See `TRADEMARK.md`.

What we do ask, as a request rather than a condition, is the sentence in
`TRADEMARK.md` under "Modified versions": make it clear that your version is
yours and not ours, so nobody is misled about who maintains it and who supports
it.

---

## 9. Checklist

Before you publish a derivative:

- [ ] Built from a fresh v5.3.0 or later copy, not from an older running folder.
- [ ] `LICENSE` in your distribution reads CC BY-SA 4.0 and matches what you are
      actually publishing.
- [ ] `NOTICE.md` retained.
- [ ] The required attribution block is in your README, above the fold.
- [ ] Changes indicated (a "what I changed" section or a CHANGELOG).
- [ ] `Expansions/mypka-cockpit/` deleted.
- [ ] No myICOR member content, lesson text, slides, video, transcripts, or
      framework diagrams reproduced.
- [ ] No platform terms sitting over the files that stop recipients sharing them.
- [ ] `update_check` disabled or re-pointed, and `distribution` set to identify
      your release.
- [ ] Your product is not named after ours and claims no endorsement.

---

Questions this page does not answer, plus trademark permission, OEM licensing, and
branded redistribution: **contact@myicor.com**.

This page is a plain-language summary of our own licence terms, written to be
useful rather than exhaustive. It is not legal advice. Where it differs from
`LICENSE`, `LICENSE-MAP.md`, `NOTICE.md`, `TRADEMARK.md`, the myICOR Terms of
Use, or the licence file of a subtree, those documents win. If your situation
turns on the detail, take the licence text to your own lawyer.
