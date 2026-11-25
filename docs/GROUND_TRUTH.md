# Ground truth: conventions and known issues

## Conventions

Transcription is **literal**: what is seen on the page, in the original orthography.

- No modernisation of spelling and no expansion of abbreviations.
- `[?]` marks a doubtful reading.
- Line-end hyphenation is kept as written.
- A short filler stroke at the end of a line is not transcribed as a hyphen.
- Initial *Y/I* with a curl is transcribed *Y* (e.g. "Ysla").
- The small mark over the *o* in *-cion* is the displaced dot of the *i*, not an accent.
- The graphs for *x* (a *p* with a long stroke) and the near-identical *r* / *v* are read from context.

Some conventions were refined while working through folios 4962–4971; earlier folios were typed before that
refinement, so the training ground truth is not fully uniform.

## Known issues (candidate errors, not yet checked against the originals)

A comparison of V4 readings with the training ground truth turned up systematic differences that are likely
to be ground-truth inconsistencies rather than model errors:

- **Abbreviations.** Some folios have expanded abbreviations (e.g. *dho* written as *dicho*), others do not.
- **Accents.** Used inconsistently across folios.
- **Isolated words** that look like typing or reading errors and should be checked against the page, for example
  "enomeser", "Eperculata", "Gaviente", "desucbrio", "ey" and "informare"; and "Capital" where the context
  suggests "Capitan" (folio 4975).

Effect: part of the apparent model error in the evaluation may come from the reference, so the CER values in
`results/RESULTS.md` are estimates with this uncertainty in addition to the small sample size. A pass of human
verification of the ground truth against the images is the first item of the roadmap.
