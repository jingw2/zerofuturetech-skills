# Anti-Patterns Catalog

Read this file when assessing content quality in step 4 of the review workflow. For each anti-pattern, check whether evidence exists in the skill being reviewed. Cite specific sections when flagging.

---

## Anti-Pattern 1: Stating the Obvious

**Definition**: Explaining concepts Claude already knows without adding skill-specific constraints.

**How to detect**: Ask "Would Claude get this right without the instruction, given its general knowledge?" If yes, the instruction may be stating the obvious.

**Important caveat**: Not all basic content is obvious. If the instruction corrects a known model weakness in a specific domain (e.g., WeChat's non-standard image URL requirements), it is not obvious even if the underlying concept is basic.

**Examples of stating the obvious**:
- "Python uses indentation for code blocks."
- "JSON must be valid before parsing."
- "Git commits should have descriptive messages."

**Examples that look obvious but are not**:
- "WeChat does not accept image URLs from external sources during draft creation — images must be uploaded to WeChat's servers first." (Domain-specific constraint Claude would not infer.)
- "This CLI's `--format` flag accepts `yaml` but not `json`, despite the docs saying otherwise." (Contradicts documentation — non-obvious.)

**Severity**: Nice-to-have to Important (depends on proportion of obvious content)

---

## Anti-Pattern 2: Railroading

**Definition**: Over-constraining Claude with exact implementation details rather than outcomes, reducing its ability to adapt.

**How to detect**: Look for workflow steps that specify exactly which command to run, exactly how many lines to write, or exactly which file to modify — when the outcome could be achieved multiple ways.

**Examples of railroading**:
- "Run `git log --oneline -20 | head -5` to get the recent commits."
- "The output must be exactly 3 paragraphs."
- "You must use the requests library to make the API call."

**Examples that are NOT railroading** (appropriate specificity):
- "Fetch the last 20 commits and summarize the theme." (outcome, not command)
- "Keep the output concise — under 5 paragraphs." (constraint, not prescription)
- "Use the WeChat draft API endpoint, not the publish endpoint." (domain-specific constraint)

**Severity**: Important

---

## Anti-Pattern 3: Empty Gotchas

**Definition**: A Gotchas section that exists structurally but contains no real failure modes — only placeholders, generic warnings, or skeleton entries.

**How to detect**: Look for TODO markers, entries that say "be careful" without specifics, or entries copied from a template without customization.

**Examples of empty gotchas**:
- `- **TODO gotcha**: explanation and resolution.`
- `- **Edge cases**: Be careful with edge cases in this skill.`
- `- **Errors**: Handle errors appropriately.`

**Examples of real gotchas**:
- `- **Access token expiration**: WeChat tokens expire every 2 hours. If more than 2 hours pass between prepare_article.py and publish_wechat.py, re-fetch the token before publishing.`
- `- **Image path resolution**: Paths in the Markdown must be relative to the article file, not the working directory. Running prepare_article.py from a different directory will break image references.`

**Severity**: Critical if Gotchas is entirely empty or all entries are placeholders. Important if some entries are real but the section is thin.

---

## Anti-Pattern 4: Monolithic SKILL.md

**Definition**: Putting all reference content inline in SKILL.md instead of using progressive disclosure via reference files.

**How to detect**: Look for sections exceeding ~30 lines of dense prose, tables of API endpoints, or large code snippets embedded inline. Check whether references/ is empty or unused.

**Examples of monolithic patterns**:
- A Workflow section with 50 lines of inline API documentation
- A Frontmatter Contract section listing all 20 possible fields with full descriptions inline
- A Quality Bar section containing a full rubric table instead of linking to a rubric reference file

**The fix**: Move the detailed content to a references/ file and replace the inline content with a link: "Read [references/api-reference.md](references/api-reference.md) for the full endpoint list."

**Severity**: Important

---

## Anti-Pattern 5: Summary-as-Description

**Definition**: The description field reads like a human-facing README summary rather than a model-facing trigger condition.

**How to detect**: Check if the description starts with "This skill", is a noun phrase, lists features without trigger conditions, or omits "Use when".

**Examples of summary-as-description**:
- `"This skill handles WeChat publishing and supports multiple styles."`
- `"Features: Markdown cleanup, style selection, image upload, API publishing."`
- `"A comprehensive tool for creating illustrated articles with HTML output."`

**Examples of trigger-oriented descriptions**:
- `"Prepare polished WeChat-draft-ready articles from Markdown and image assets... Use when Codex receives a Markdown article and needs to optimize typography and publish to 微信公众号草稿箱."`

**Severity**: Critical (the model cannot decide when to trigger the skill)

---

## Anti-Pattern 6: Missing Trigger Conditions

**Definition**: The description has no "Use when" clause, or the clause is too broad to be useful.

**How to detect**: Search the description for "Use when". If absent, flag as critical. If present but followed by a vague condition ("when the user wants to write something"), flag as important.

**Examples of missing or too-broad triggers**:
- No "Use when" at all
- `"Use when the user wants help."`
- `"Use when writing content."`

**Examples of specific triggers**:
- `"Use when Codex receives raw notes, prompts, outlines, or half-formed arguments and needs to turn them into a long-form essay."`
- `"Use when a user says 'review this skill', 'audit my skill', or 'how good is this skill'."`

**Severity**: Critical if absent. Important if present but too broad.

---

## Anti-Pattern 7: Generic Quality Bar

**Definition**: Quality Bar entries are vague or could apply to any skill, not just this one.

**How to detect**: Read each Quality Bar entry. If replacing the skill name with a different skill's name would leave the entry equally applicable, it is too generic.

**Examples of generic quality bar entries**:
- `"Make sure the output is correct."`
- `"Ensure quality before delivering."`
- `"Check that all steps completed successfully."`

**Examples of specific quality bar entries**:
- `"The cover image path resolves from the article's directory, not the working directory."`
- `"The generated HTML passes validation with no unclosed tags."`
- `"All inline images have been uploaded to WeChat servers and URLs rewritten."`

**Severity**: Nice-to-have

---

## Anti-Pattern 8: Orphaned Reference Files

**Definition**: Files exist in references/ but are not linked from the Overview section, so Claude does not know to read them.

**How to detect**: List all files in references/. For each file, check whether its path appears as a link in the SKILL.md body (specifically the Overview section). Any unlinked file is orphaned.

**The fix**: Add a link in the Overview: "Read [references/filename.md](references/filename.md) for [purpose]."

**Severity**: Important (the file exists but is unreachable in practice)
