# Third-party notices and research attribution

## Humanizer

ProseShape adapts ideas and material from **Humanizer** by Siqi Chen (`blader/humanizer`), released under the MIT License.

Source: https://github.com/blader/humanizer

Original license notice:

> MIT License  
> Copyright (c) 2025 Siqi Chen
>
> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all
> copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
> SOFTWARE.

## StoryScope

ProseShape also draws on findings reported in:

Jenna Russell, Rishanth Rajendhran, Chau Minh Pham, Mohit Iyyer, and John Wieting. **StoryScope: Investigating idiosyncrasies in AI fiction.** 2026. arXiv:2604.03136.

Paper: https://arxiv.org/abs/2604.03136  
Code: https://github.com/jenna-russell/storyscope

The StoryScope authors are not presented as authors, maintainers, or endorsers of ProseShape. References to StoryScope in this repository describe the research source for narrative-level observations.

## HumanScope

ProseShape 1.4.2's rule that writing patterns count as evidence only in clusters, and that a change to text a person wrote needs a fault that can be named for the reader, adapts the evidence-before-edit idea of **HumanScope** (`Anson-Saju-George/HumanScope`), released under the MIT License. No text from HumanScope is included.

Source: https://github.com/Anson-Saju-George/HumanScope

## Wikipedia: Signs of AI writing

Many of the sentence-level patterns in the skill's `references/humanizer-rules.md` come, through Humanizer, from the Wikipedia project page **"Wikipedia:Signs of AI writing"**, written by WikiProject AI Cleanup and other Wikipedia contributors. Wikipedia text is available under the Creative Commons Attribution-ShareAlike 4.0 License. ProseShape credits the page as a source of its pattern categories. It does not reproduce the page.

Page: https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing  
License: https://creativecommons.org/licenses/by-sa/4.0/

## Evaluation corpora

These files are in the source repository (https://github.com/Aieda1l/ProseShape), not in the installed skill. The evaluation corpora are synthetic apart from the following excerpts, which are included for testing only:

- `evals/heldout/h10_human_rust.md`: from *The Rust Programming Language*, Introduction, by Steve Klabnik, Carol Nichols, and contributors (https://github.com/rust-lang/book). Copyright (c) 2010 The Rust Project Developers. Licensed under the MIT License or the Apache License 2.0, at your option.
- `evals/heldout/h11_human_twain.md`: from Mark Twain, *Roughing It* (1872). Public domain (Project Gutenberg #3177).
- `evals/heldout2/k13_human_austen.md`: from Jane Austen, *Pride and Prejudice* (1813), chapter 13. Public domain (Project Gutenberg #1342).
- `evals/heldout2/k14_human_go_blog.md`: from Rob Pike, "Errors are values", The Go Blog, 12 January 2015 (https://go.dev/blog/errors-are-values). Text licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), code under the Go BSD license. Converted from HTML to Markdown.
- `evals/heldout2/k15_human_doctorow.md`: from Cory Doctorow, "Tiktok's enshittification", *Pluralistic*, 21 January 2023 (https://pluralistic.net/2023/01/21/potemkin-ai/). Licensed under CC BY 4.0. First four paragraphs, converted to plain text.
- `evals/heldout3/m11_human_thoreau.md`: from Henry David Thoreau, *Walden* (1854), "The Pond in Winter". Public domain (Project Gutenberg #205).
- `evals/heldout3/m12_human_chesterton.md`: from G. K. Chesterton, "On Running After One's Hat", *All Things Considered* (1908). Public domain (Project Gutenberg #11505).
- `evals/heldout3/m13_human_lincoln.md`: Abraham Lincoln, letter to Horace Greeley, 22 August 1862. Public domain (Project Gutenberg #14721).
- `evals/heldout3/m14_human_eisenhower.md`: from Dwight D. Eisenhower's Farewell Address, 17 January 1961. A work of the US government, public domain (transcript from the National Archives).
- `evals/heldout3/m15_human_kubernetes.md`: from the Kubernetes documentation, "Overview" (https://kubernetes.io/docs/concepts/overview/). © The Kubernetes Authors, licensed under CC BY 4.0. Converted from HTML to Markdown.
- `evals/heldout3/m16_human_go_errors.md`: from Damien Neil and Jonathan Amsterdam, "Working with Errors in Go 1.13", The Go Blog, 17 October 2019 (https://go.dev/blog/go1.13-errors). Text licensed under CC BY 4.0, code under the Go BSD license. Converted from HTML to Markdown.
- `docs/research/experiment-2026-09/corpus/s10_human_tech.md`: from the Python Tutorial, "Whetting Your Appetite". © Python Software Foundation, used under the PSF License Agreement.
- `docs/research/experiment-2026-09/corpus/s11_human_voice.md`: from Jerome K. Jerome, *Three Men in a Boat* (1889). Public domain (Project Gutenberg #308).

`h05_oped.md` cites a published California Air Resources Board comparison (leaf-blower emissions against car miles). Every other name, organization, figure and quotation in the synthetic samples is fictional.

## Banner and icon lettering

The pilcrow in the icon (`plugins/proseshape/assets/icon.svg`, and the source repository's `assets/icon*`) and the lettering in the source repository's `assets/banner.svg`, `assets/banner-dark.svg` and `assets/social-preview.png` are set in **Instrument Serif** (Copyright 2022 The Instrument Serif Project Authors, https://github.com/Instrument/instrument-serif) and converted to outlines. The font is licensed under the SIL Open Font License 1.1 (https://openfontlicense.org). The font files themselves are not included in this repository.
