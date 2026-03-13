# WeChat Layout Rules

Use these rules to make an article look better inside 微信公众号草稿箱, not just to make HTML technically valid.

## Main Goal

Optimize for mobile reading in WeChat:

- clear first screen
- stable Chinese typography
- obvious but restrained section hierarchy
- comfortable spacing
- balanced image rhythm

## Style Presets

### bold

- stronger heading blocks
- more obvious emphasis
- suitable for tutorials, announcements, and highly structured content

### minimal-cn

- closer to Chinese long-form column writing
- less card-like decoration
- cleaner text-first reading experience
- suitable for观点文、专栏、知识型长文

### tech-editorial

- closer to Chinese tech media / industry analysis style
- stronger title deck and more media-like hierarchy
- cooler visual tone and more explicit section breaks
- suitable for AI、产品、产业观察、技术媒体文章

## Auto Recommendation

- `essay` -> `tech-editorial`
- `tutorial` -> `bold`
- `brief` -> `minimal-cn`

Use `--compare-styles` when the article sits between categories or when the opening visual tone matters a lot.

## First Screen Rules

- The title should not be repeated as the first body heading.
- Keep the opening paragraph short enough to read comfortably on mobile.
- Avoid placing a heavy banner-style section heading immediately after the opening unless the article is a tutorial.
- If the article starts with an image, confirm that it improves the opening rather than pushing the value below the fold.

## Heading Rules

- H2 should be visually stronger than body text, but avoid oversized colored banners by default.
- H3 should behave like a section marker, not a mini-title card.
- Do not use more than three visible heading levels in most WeChat articles.
- If the source Markdown overuses headings, merge weak sections instead of rendering all of them.

## Paragraph Rules

- Prefer short to medium paragraphs for Chinese articles.
- Break paragraphs that carry multiple claims or examples.
- Avoid consecutive one-line paragraphs unless they are used intentionally for rhythm.
- Avoid giant text walls longer than roughly 5-6 mobile lines.

## List Rules

- Lists should feel editorial, not like raw Markdown output.
- Ordered lists are preferred for process/tutorial content.
- Unordered lists work best for short takeaways, comparisons, or principles.
- If a list item becomes a full paragraph, consider promoting it into a subsection.

## Quote and Callout Rules

- Use blockquotes for insight, caution, or emphasis, not for large chunks of ordinary text.
- Quote styling should be calm: left border, subtle background, readable text color.
- Strong callouts should be rare. One or two per article is usually enough.

## Code Rules

- Keep code blocks only when they help the target audience.
- For creator or essay articles, prefer explanations over long code dumps.
- For technical tutorials, keep code styling minimal and readable.
- If code blocks are too frequent, the article likely needs segmentation or screenshots.

## Image Rules

- Do not cluster too many images without explanatory text between them.
- Give hero screenshots and diagrams more breathing room than inline decorative images.
- Prefer a consistent max width and centered layout.
- When multiple images appear in sequence, consider whether one should be removed or turned into cover.

## Article Type Presets

### essay

- More whitespace
- Fewer decorative boxes
- Stronger paragraph rhythm
- H2 emphasis without heavy backgrounds

### tutorial

- Clear steps
- Stronger H2/H3 hierarchy
- Better numbering
- More obvious callouts for warnings and tips

### brief

- Compact spacing
- Strong opening summary
- Limited number of sections
- Quick scanability

## Common Failure Modes

- Markdown looks like a generic docs renderer
- H2 blocks are too visually loud
- Chinese text spacing feels cramped
- Lists and quotes look misaligned
- Images interrupt the argument instead of supporting it
- The draft box preview looks fine on desktop but crowded on mobile

When in doubt, choose readability over ornament.
