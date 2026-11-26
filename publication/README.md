# Publishing the two reading editions

The editable overview is [manuscript/overview.md](../manuscript/overview.md). The [detailed edition builder](full/build.py) selects the source chapters for the longer book. Both editions use the same title and identify their edition, source revision and scope. The [coverage register](audit/completeness.md) records where a proof-specific input still relies on an external account.

The detailed build checks the registered manuscript claim ranges, dependency links and review digests before assembling the text. The research guide gives the command for checking the pinned upstream excerpts as well. [Current Galois claim records](../research/modules/galois/polarized_galois_attachment/) · [Research guide](../research/README.md)

When expanding the detailed edition, add the derivation to the appropriate source chapter and include that chapter in the [book contents](full/contents.json). For a published result, identify the paper and theorem and match its hypotheses. For an argument adapted from a preprint, webpage or Git repository, credit the author and give the version and location. Update the coverage register when the manuscript supplies the missing argument.

## Build

From a clean checkout of the desired revision, use Python 3.10 or later, Pandoc 3, and pdfLaTeX. On Ubuntu 24.04 the typesetting packages are `pandoc`, `lmodern`, `texlive-latex-extra` and `texlive-fonts-recommended`. Run

```sh
python3 research/register/verify_selected_family.py
python3 publication/build.py --edition "$(cat publication/edition.txt)"
```

The generated files are under `publication/build/`. Open `index.html` for the reading page, `overview.pdf` for the short account or `full.pdf` for the detailed account. The browser edition of the overview displays mathematics with native MathML. To rebuild only the short edition, add `--overview-only`. Use `--output DIRECTORY` to stage the files elsewhere.

The portable `proof-source.zip` contains `overview.tex`, `full.tex` and typesetting instructions. A reader can compile either TeX document on its own. Citations to repository files point to the source commit. The editable sources remain in Git. Generated publication files are excluded from the working tree.

## Update the reading site

A successful push to `main` builds the current reading copy. To enable the site select **Settings → Pages → Build and deployment → Source → GitHub Actions**. The [publication workflow](../.github/workflows/manuscript.yml) then deploys the generated files at the project’s Pages address. The same workflow can be run manually on `main`. Versioned manuscript releases work independently of the Pages setting.

## Publish a numbered edition

For an edition intended for citation, change [edition.txt](edition.txt) on `main` to a new name such as `edition-6`, and describe the changes in `publication/editions/edition-6.md`. On that push the workflow creates a draft release for the exact commit, attaches the two PDFs and TeX archive produced by its build, and publishes the release. A change to any other manuscript file updates the reading copy. Pushing an explicit `edition-*` tag also builds and releases that tag. A manual workflow on `main` can publish the edition named in the file.

Every release uses the same asset names. In a README, `releases/latest/download/overview.pdf` or `releases/latest/download/full.pdf` on the GitHub repository URL opens the latest released file. For a fixed edition use `releases/download/edition-5/full.pdf`. The source archive is `proof-source.zip` alongside the PDFs. Create a new edition for a correction to a published file. GitHub's optional immutable releases setting can lock the tag and assets after publication.

[GitHub Pages publication](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) · [Release URLs](https://docs.github.com/en/repositories/releasing-projects-on-github/linking-to-releases) · [Immutable release settings](https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases)
