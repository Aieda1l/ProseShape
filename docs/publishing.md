# Publishing ProseShape

How a ProseShape release reaches people, and how to list it in Anthropic's directory. The install commands for users are in the [README](../README.md#install).

## Where ProseShape is available

| Channel | How people get it | What you do |
|---|---|---|
| This repository's marketplace | Claude Code: `/plugin marketplace add Aieda1l/ProseShape`, then `/plugin install proseshape@proseshape`. claude.ai: add the same marketplace under **Customize > Plugins**. Codex: `codex plugin marketplace add Aieda1l/ProseShape`, then `codex plugin add proseshape@proseshape`. | Merge to `main`. |
| GitHub release zip | Upload under **Customize > Skills** on claude.ai, or unzip into another tool's skills folder. | Push a `vX.Y.Z` tag. The release workflow builds and attaches `proseshape-X.Y.Z.zip`. |
| Anthropic's directory | Browse and add on claude.ai and in Cowork. It then loads in Claude Code too. | Submit once from the developer portal (below), then publish each new version there. |
| OpenAI's plugin directory | Browse and add in Codex and ChatGPT. | Submit from the OpenAI Platform (below). |

Anthropic's preinstalled `claude-plugins-official` marketplace doesn't take submissions; it lists plugins from Anthropic and its partners. The directory is the route open to independent authors.

## Release checklist

1. **Version.** Set the same version in three places: `plugins/proseshape/.claude-plugin/plugin.json` (Claude), `plugins/proseshape/plugin.json` (portable, read by Codex), and `SKILL.md` (`metadata.version`). Users of a marketplace receive an update only when `version` changes.
2. **Changelog.** Add a `## X.Y.Z` section to `CHANGELOG.md`. The release workflow uses it as the release notes.
3. **Evidence.** If `SKILL.md` or any reference file the skill loads changed, follow the evaluation rules in [`evals/harness/README.md`](../evals/harness/README.md). Freeze a new held-out corpus before editing, iterate on development data, validate once, and record the result whatever it is. `references/prompt-engineering-notes.md` is for maintainers only and doesn't need this.
4. **Checks.** Run:
   ```bash
   python3 -m unittest discover -s scripts/tests
   python3 scripts/package_skill.py --check
   claude plugin validate --strict plugins/proseshape
   claude plugin validate .
   ```
   `package_skill.py` checks the things the directory and claude.ai care about:
   - the skill name matches its folder, and the description is at most 1,024 characters (it is 1,000 now);
   - every reference file `SKILL.md` mentions exists;
   - the versions agree across both manifests and `SKILL.md`;
   - both marketplace files list the plugin, and the Codex entry has a valid `policy` and `category`;
   - Codex's display fields stay within OpenAI's limits, and the icon is square;
   - the README has at least 40 words;
   - the license copies match the root files;
   - every file is under 256 KiB, with no system files.
5. **Merge to `main`.** Marketplace users can now run `claude plugin update proseshape@proseshape`.
6. **Tag.** Push `git tag vX.Y.Z && git push origin vX.Y.Z`. The workflow refuses a tag that doesn't match `plugin.json`.
7. **Directory.** Publish the new version from the developer portal ([Update a published plugin](https://claude.com/docs/plugins/submit#update-a-published-plugin)).

## Submit to Anthropic's directory

You need a paid claude.ai plan. On Pro or Max you submit from your own account. On Team or Enterprise, an Owner submits.

1. Make sure the version you want listed is on `main`.
2. Open the developer portal at [claude.ai/directory/manage](https://claude.ai/directory/manage), select **Submit new**, then **Plugin bundle**.
3. On the **Source** step, enter the repository `Aieda1l/ProseShape` and the plugin folder `plugins/proseshape`, spelled exactly like that.
4. Select **Validate**. Fix anything marked **Blocking**, push, and select **Re-validate**.
5. Submit. Every version goes through an automated scan and Anthropic's review against the [Software Directory Policy](https://support.claude.com/en/articles/13145358-anthropic-software-directory-policy). The portal shows the status.

What to expect for ProseShape:

- **Validation.** The plugin passes `claude plugin validate --strict`. The portal runs extra checks, such as README length, license, name collisions and file limits, which `package_skill.py` mirrors where it can.
- **Security scan.** The plugin contains only Markdown instructions. It runs no code, starts no servers and makes no network requests, and its README says so.
- **Surfaces.** Skills load in claude.ai chat, Cowork and Claude Code.
- **Approval.** It isn't guaranteed. The directory's [pre-submission checklist](https://claude.com/docs/plugins/pre-submission-checklist) lists every automated check.

## Submit to OpenAI's plugin directory

Submit at [platform.openai.com/plugins](https://platform.openai.com/plugins) with **Upload new or existing plugin**. Organization owners can submit; other members need **Apps Management Write**. To publish under your own name or a company's, finish individual or business verification in the organization settings first. The full process is in [Submit plugins](https://developers.openai.com/plugins/deploy/submission).

For a plugin that has only skills, like ProseShape:

- **What review needs.** It doesn't need MCP review cases or a demo recording.
- **Where the display details live.** They are in `plugins/proseshape/plugin.json` under `extensions` → `com.openai` → `interface`:
  - display name and short description, 30 characters at most each;
  - a long description;
  - developer name;
  - category;
  - capabilities, which is empty because the plugin reads and writes no outside data;
  - example prompts;
  - brand color.
- **Icons.** `composerIcon` and `logo` both point to `assets/icon.svg`, a square SVG. OpenAI accepts PNG, JPEG, WebP or SVG, square and at least 48 by 48.

Codex reads this portable `plugin.json`. Claude reads `.claude-plugin/plugin.json`. Each ignores the other's file, so keep them in agreement. `package_skill.py` fails when their names or versions differ.

## Rules that keep installs working

- **Never rename the plugin.** Installs are recorded as `proseshape@proseshape` in both Claude Code and Codex. To change the label people see, edit `displayName` in both manifests.
- **Keep the copies in sync.** `plugins/proseshape/LICENSE` and `plugins/proseshape/THIRD_PARTY_NOTICES.md` must match the root files, because users receive only the plugin folder and Humanizer's MIT notice has to travel with every copy. After editing either root file, run `cp LICENSE THIRD_PARTY_NOTICES.md plugins/proseshape/`.
- **Keep the plugin folder small.** Evaluation data and research stay outside `plugins/proseshape/`, so people don't download them.
- **Leave the evaluation harness pointed at the plugin.** It reads the skill from `plugins/proseshape/skills/proseshape/`. For commits from before the move, it falls back to the old root location, so `build_arm.py --rev` still rebuilds every earlier version exactly.
