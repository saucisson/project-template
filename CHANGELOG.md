# Changelog

## [0.2.0](https://github.com/saucisson/project-template/compare/v0.1.0...v0.2.0) (2026-11-25)


### Features

* actively wait for ci ([a6eb74a](https://github.com/saucisson/project-template/commit/a6eb74a8e60f1090916946572a2cabc2f4c27ed3))
* add script to synchronize daily from main ([8401400](https://github.com/saucisson/project-template/commit/8401400f9a3282b53c0e73103b0057504948ab9c))
* agent-written worklog audited at the daily merge ([d6379b4](https://github.com/saucisson/project-template/commit/d6379b4d9000a1bd5527e1831295b2393d534320))
* **G4/N4:** the english-only front and the commit-subject hook (ADR-0008) ([b054178](https://github.com/saucisson/project-template/commit/b05417853755d85c9fffcbebce4830d3574d5b58))
* **H1:** the engineering rules in the review bundle (ADR-0008) ([58f1eab](https://github.com/saucisson/project-template/commit/58f1eabb771a1b5ac3b568b211fff5987c5a54d6))
* initial commit ([5b04128](https://github.com/saucisson/project-template/commit/5b04128e0126225cee490f3c54bd74d9f6e2c14e))
* milestone filter for the night loop ([0030b3e](https://github.com/saucisson/project-template/commit/0030b3e86f73469133c772420265d61d79209b2b))
* more output during night session ([9e8dcce](https://github.com/saucisson/project-template/commit/9e8dcce1d88d6e092bbe8c70320ec93afb12aa6d))
* **N2:** dependency admission by argued evidence, license gate and audit (ADR-0008) ([b083761](https://github.com/saucisson/project-template/commit/b083761204805ed8e4b3c544b8b68c6398959eaa))
* **N3:** the staging and release deployment channels (ADR-0008) ([b01b4c2](https://github.com/saucisson/project-template/commit/b01b4c25348577a93f717d7ad8d843d33bf5fa66))
* night autonomy trace and PR body updates ([d43d8a6](https://github.com/saucisson/project-template/commit/d43d8a6e81c0a28bf8ec8ee82d843490a39d176b))
* one session context per pull request ([b4c32c0](https://github.com/saucisson/project-template/commit/b4c32c0c33e98b1128acbf8d835e3335c494976d))
* probe-merge, the per-commit greenness dry run (ADR-0008 N5/H5) ([f5a80f7](https://github.com/saucisson/project-template/commit/f5a80f7df5ec99446551b3cbfe8ad75e4172ec17))
* recover PRs during autonomous work ([47eadf4](https://github.com/saucisson/project-template/commit/47eadf443dcc45a38abc94ae9961b4aa904f488c))
* unattended night loop ([3463aea](https://github.com/saucisson/project-template/commit/3463aead9e6b6065f162170783549affc309281c))
* worklog v2 per-record files, pulls network error handling, PR budget back to ~500 ([7602002](https://github.com/saucisson/project-template/commit/7602002af88f8cc005a9a69a329302e083020961))


### Bug Fixes

* align tooling on ruff 0.17 and mypy 2.4, pass gitleaks PR token ([9181e72](https://github.com/saucisson/project-template/commit/9181e72238b44216b59e55497ce27b1f420d8945))
* annotate the local check_runs variables for mypy invariance ([d8c8e9e](https://github.com/saucisson/project-template/commit/d8c8e9ed8e6800c50f909e18ed7a57f07b8332ae))
* apply dispatch keyword-arg fix and raise PR size budget to ~1000 lines ([e2c26a3](https://github.com/saucisson/project-template/commit/e2c26a39628e2e398de7d65664750e7d053847ff))
* correct structlog import paths, explicit Any usage and pip-audit export ([c0991f7](https://github.com/saucisson/project-template/commit/c0991f7da0e30d78c21641955b9414b10b91ef69))
* force root handler installation in configure_logging ([aceb240](https://github.com/saucisson/project-template/commit/aceb240dce67c0257e4fe7515a3f926e2d5350e0))
* install uv in the security job for pip-audit ([a223f09](https://github.com/saucisson/project-template/commit/a223f091465952980edcb278dfc4323718550713))
* linear merge prefers rebase, squash in the branch (I3) ([7047066](https://github.com/saucisson/project-template/commit/7047066e288a8b605c04f2843f61eeaa53c3ef52))
* load documented uppercase env vars, type the webhook as SecretStr in tests ([d446762](https://github.com/saucisson/project-template/commit/d446762e0787a2349ec70353c2c32d9a21a91faa))
* make the review the last gate, negotiate the merge method ([53b7eb7](https://github.com/saucisson/project-template/commit/53b7eb752040e36a72173ba9c447b823450d8e4a))
* **N2:** license gate as a driver subcommand, atomic SPDX evaluation ([d3a00d1](https://github.com/saucisson/project-template/commit/d3a00d1682f679de6e2fca37b274841847adc385))
* **N2:** pytest moved into TYPE_CHECKING, annotation-only import (TC002) ([febdc69](https://github.com/saucisson/project-template/commit/febdc695cfb13e531e4418256242450477b3489c))
* parameterize _SubParsersAction and drop explicit Any in dispatcher ([2aa4d27](https://github.com/saucisson/project-template/commit/2aa4d27a160b953104806dad426cfec11146fdb2))
* probe ruff findings (invalid string literal, PLW0108 lambda, pytest TC004) ([a3d9934](https://github.com/saucisson/project-template/commit/a3d99341a9638099ac033eab53c039791d972b8e))
* probe ruff findings (TC003 argparse, F541 placeholderless f-string) ([cc446b0](https://github.com/saucisson/project-template/commit/cc446b0e50f1f2c57feb074ebf95c0569572bdce))
* rename reused offender variable for mypy ([a0b8c15](https://github.com/saucisson/project-template/commit/a0b8c152861c5a55784343735978c6aaa620b7d5))
* repair character-duplication corruption in scripts/review.py (bareest) ([7b983ce](https://github.com/saucisson/project-template/commit/7b983ce847b5efd7b557e14ff061454fdaad4ad3))
* repair line-break corruption in the documents ([69f6312](https://github.com/saucisson/project-template/commit/69f6312fb1e4470bb4b2fd0bdbf1a7066afa4e6e))
* repair notify example imports, lockfile wording and mutation gate ([a4a6d54](https://github.com/saucisson/project-template/commit/a4a6d54c83cbbb7c9cbe85818c08494e544806f9))
* repair the bareest duplication in the day driver docstring ([be47f99](https://github.com/saucisson/project-template/commit/be47f9956ff40795e8d8c54cb1133bf045a7d9a1))
* repair the remaining line-break corruptions in the documents ([3a3ab60](https://github.com/saucisson/project-template/commit/3a3ab604c321d42223382b2e05fb92c31381e882))
* repair the two residual line-break corruptions in rules.md ([e6a44e6](https://github.com/saucisson/project-template/commit/e6a44e60b92136d067d9077408e63bbe635612ba))
* restore typed runner call in dispatcher ([39b1589](https://github.com/saucisson/project-template/commit/39b158960027ddf01055dccdc262ee1835287778))
* run night sessions with --output text ([02f59c2](https://github.com/saucisson/project-template/commit/02f59c215b29c2f601600cb96b5e0dbd26197362))
* TC004 Path runtime import and overlong dispatch lines ([21757d8](https://github.com/saucisson/project-template/commit/21757d8858a21fb5aa76311821af37c5ac037cc3))
* the merge driver merges into daily only ([c0a636b](https://github.com/saucisson/project-template/commit/c0a636b30b2b76b96587d120c8e1d3f861711e2b))
* unquoted Path annotations in test_review (UP037, PEP 649 lazy annotations) ([65e1ccb](https://github.com/saucisson/project-template/commit/65e1ccbf87479c085aade247ad29b2be33306d9d))


### Documentation

* **ADR-0008:** adopt agent-era engineering rules and the night-acceptance loop ([149608e](https://github.com/saucisson/project-template/commit/149608e3e03f5afd011410ed354a2812047986be))
* **ADR-0008:** wire the new document into AGENTS.md and docs/rules.md ([2837733](https://github.com/saucisson/project-template/commit/283773398b42f01f88f8c66f2b00d2230f2a5154))
* ask for Closes #n in the pull request template ([e7a78a7](https://github.com/saucisson/project-template/commit/e7a78a740f5437337494caa9f05064b050b71935))
* consolidate template documentation (patches 01-05) ([f9190bb](https://github.com/saucisson/project-template/commit/f9190bbfed9fb69ed00300d408629a62851f73a9))
* H5 - review is sequential, per commit ([046efb7](https://github.com/saucisson/project-template/commit/046efb70979fd4a6719430be208af2ad7263ed19))
* I3 - merges are rebase-only, squash in the branch ([e2f20d7](https://github.com/saucisson/project-template/commit/e2f20d7ebb96855a2a5ddc13c396178ed0fb1b01))
* **N2:** worklog records the format-helper iteration ([d451bf2](https://github.com/saucisson/project-template/commit/d451bf2c1c5c78736f5d4213f3e293ec717e0a27))
* record the mypy diagnostic detour in the pr-27 card ([3f4952b](https://github.com/saucisson/project-template/commit/3f4952b2fa18f6a6be4d2299938b16f0bfd76a7c))
* restore exact characters in the untouched parts of docs/rules.md ([e3f5e59](https://github.com/saucisson/project-template/commit/e3f5e59440501d63a84370ee0e371dc5e77a6fa9))
* the release pipeline publishes the worked example, not the template ([d85a507](https://github.com/saucisson/project-template/commit/d85a507ede45695bbf5167f97d9c789769630a01))
* the unparenthesized except clauses need Python 3.14+ ([7a11dea](https://github.com/saucisson/project-template/commit/7a11dea655bc5690c9a46029005f10916522a406))
* worklog records the format helper run ([f3ca451](https://github.com/saucisson/project-template/commit/f3ca4514b4ea8facb59098dc35b8d3167adb1b21))
* worklog records the rules.md residual corruption repair ([7deb351](https://github.com/saucisson/project-template/commit/7deb3514221594f5e107b3d82a502c421c70bdc1))
