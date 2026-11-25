# Methods

## 1. Material and image preparation

The source is a photographed archival dossier of 248 folios (IMG_4954–IMG_5200). Every folio was rotated and
cropped by hand. The script then applies:

- grayscale conversion;
- CLAHE with `clipLimit = 1.5` and `tileGridSize = (4, 4)`. An earlier setting (3.0, 8×8) amplified the ink
  that shows through from the reverse side and the paper texture, and made the segmenter split lines wrongly;
- for the V4 round and for inference, binarization with `kraken binarize`, saved as a persistent PNG.

## 2. Segmentation

`kraken -a -i <image> <out.xml> segment -bl` (baseline segmentation, no recognition). The output ALTO XML is
the input of the alignment tool.

## 3. Ground-truth construction

The alignment tool (notebook, section 3) crops every detected line from the page image, displays it, and
asks for its text. The text is written into the `CONTENT` attribute of the line's `String` element. A blank
answer removes the line from the output, since lines without text are useless for training. Text is typed
directly from the crop; the conventions followed are in `GROUND_TRUTH.md`.

Training uses ALTO XML directly (`ketos train -f alto`).

## 4. Training

| | V3 | V4 |
|---|---|---|
| Base model | McCATMuS_nfd_nofix_V1 | McCATMuS_nfd_nofix_V1 |
| Training folios | 23 | 58 (the 23 of V3 re-processed + 35 new) |
| Command | `ketos train -i BASE -f alto --resize add --workers 0 -o NAME files...` | same |

Each round restarts from the base model; V4 is not fine-tuned from V3. `--resize add` extends the output
alphabet with characters that are in the ground truth but not in the base model. `--workers 0` avoids a
race condition on temporary files with multi-process data loading.

The 35 additional V4 folios were chosen for variety (inventory register, strong show-through, other hands),
not for order in the dossier.

`ketos` holds out part of the training folios for its internal validation. The validation accuracy reached
about 0.83 for V4. That figure comes from folios of the same pool as the training data and says little about
generalisation, which is why a separate test set was built.

## 5. Evaluation

**Held-out test set.** Five folios (5068, 5092, 5101, 5125, 5153) were aligned in a separate folder that the
training cell never reads, and were never used to train V4. V3 and V4 were both evaluated on them with
`ketos test -f alto -m <model> <files>`.

**Why it matters.** When only the training folios were available, the first dossier-wide triage flagged 23
of 26 "legible" folios that turned out to be exactly the 23 training folios: the model reads what it
memorised. Evaluating on training folios, as section 5 of the notebook does for the V3 checkpoints, is therefore
optimistic and is labelled as such there.

**Line-level metrics.** `scripts/evaluate_alto.py` compares reference and hypothesis ALTO per folio:

- *strict CER*: Levenshtein distance over characters, after removing whitespace and line-end hyphens; case,
  accents and punctuation count;
- *lax CER*: additionally ignores case, accents and punctuation (are the same letters read?);
- *exact words*: share of reference words (lax form) matched, in order, by the hypothesis.

The total CER weights each folio by its number of reference characters. Folio 5125 (a columnar table of timber
species) is not in this table: line order in columns does not reflect reading order, so a line-by-line
comparison would not be meaningful.

## 6. Application to the dossier and triage

V4 is applied to the 248 folios (binarize → baseline segmentation → recognition). As a rough, reference-free
indicator, the notebook computes for each folio the share of words (length ≥ 3) that appear in a modern Spanish
dictionary (`pyspellchecker`). This is **not a quality measure**: 18th-century orthography ("qual", "Ysla"),
Latin binomials, abbreviations and names count as unknown words, and printed or typed pages (5170–5200) score
lower for such reasons. It is used only to prioritise folios for human review. Across the dossier the median ratio is
0.45 (182 of 248 folios reach the working threshold of 0.35); the threshold was set by inspecting a handful of
folios by eye and is not validated.

## 7. Text extraction

The plain-text version reads the ALTO `TextLine` elements and joins the `String` words of each line, preserving
the line structure of the manuscript.

## 8. Software

Kraken 5.2.9, Python 3.10, OpenCV (CLAHE), lxml, rapidfuzz, pyspellchecker.
