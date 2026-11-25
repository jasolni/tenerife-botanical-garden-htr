# Handwritten text recognition for an 18th–19th-century Spanish archival dossier

Kraken-based HTR pipeline, trained models and a full machine transcription of
*Indiferente General 1544* (Archivo General de Indias, Seville): the dossier on the
Botanical Garden of Tenerife, documents from the late 18th and early 19th century (up to about 1806).

**Status: work in progress.** The pipeline and the V4 model are operational and the whole dossier
(248 folios) has been transcribed, but the transcription is raw model output: it contains errors
and has not yet been systematically corrected. Read the *Limitations* section before using the text.

## What is in this repository

| Path | Content |
|---|---|
| `notebooks/kraken_htr_pipeline.ipynb` | The complete workflow: preprocessing, segmentation, line-by-line ground-truth alignment, V3 and V4 training, held-out evaluation, application to the whole dossier, triage, text extraction (outputs cleared) |
| `models/tenerife_V4_best.mlmodel` | Kraken recognition model V4 (fine-tuned from a CATMuS-based model) |
| `data/ground_truth/train/` | 58 manually aligned folios (ALTO XML) used to train V4 |
| `data/ground_truth/test/` | 5 manually aligned folios (ALTO XML) never used for training: the held-out test set |
| `data/transcription_v4/alto_v4.zip` | V4 output for all 248 folios, ALTO XML with line coordinates |
| `data/transcription_v4/dossier_v4.txt` | The same output as plain text, one line per manuscript line, with a header per folio |
| `scripts/evaluate_alto.py` | Standalone evaluation of ALTO transcriptions against a reference (strict and lax CER, exact words) |
| `results/` | Evaluation results and their interpretation |
| `docs/METHODS.md` | Data preparation, training and evaluation in detail |
| `docs/GROUND_TRUTH.md` | Transcription conventions and known issues in the ground truth |

The page images are **not** included (see *Data and rights*).

## The material

The dossier is a mixed archival file, which is what makes it a demanding HTR target. Approximate
composition, from the folio numbering (IMG_4954–IMG_5200):

| Folios (approx.) | Type |
|---|---|
| majority | Manuscript letters, memorials and reports in several hands, with strong ink show-through |
| 5124–5129 | Tables of Philippine timber species (columnar layout) |
| various | Seed and plant lists with Latin binomials |
| 5172–5173 | Typed cards |
| 5174–5189 | Printed 18th-century material |

## Results

Evaluation on the held-out test set (5 folios that no model saw during training):

| Model | Character accuracy | Word accuracy |
|---|---|---|
| V3 (23 training folios) | 50.99 % | 4.40 % |
| V4 (58 training folios) | **85.23 %** | **53.30 %** |

(`ketos test`, Kraken 5.2.9. Details and caveats in [`results/RESULTS.md`](results/RESULTS.md).)

A finer-grained comparison of V4 against the reference on the four continuous-text test folios, produced
by `scripts/evaluate_alto.py`:

| Metric | Value |
|---|---|
| CER, strict (case, accents and punctuation count) | 11.3 % |
| CER, lax (only letters count) | 8.7 % |
| Words read exactly (lax form, in order) | 65.4 % |

Reproduce it with:

```bash
python scripts/evaluate_alto.py \
    --reference data/ground_truth/test \
    --hypothesis <folder with the unzipped alto_v4.zip> \
    --pages 5068,5092,5101,5153
```

**These figures come from a very small test set (5 folios, 4 for the CER table) and should be read as
indicative, not as a benchmark.** They are also not directly comparable with the `ketos test` figures
above, which use a different counting scheme.

## Method in brief

1. Folios are rotated and cropped by hand, then converted to grayscale with mild CLAHE
   (clip limit 1.5, 4×4 tiles). A stronger setting amplified show-through and made the segmenter over-split lines.
2. Lines are detected with Kraken's baseline segmenter.
3. Ground truth is produced by showing each detected line as an image crop and typing its text
   (a small tool in the notebook, section 3). Lines left blank are dropped.
4. Each training round restarts from the base model rather than chaining models, and the
   ground truth is kept as ALTO XML.
5. V4 adds 35 folios chosen for variety (register, hand, degradation) to the 23 of V3, and is evaluated on a
   separate set that the training cell never reads.
6. The model is applied to all 248 folios; a dictionary-based legibility ratio is used for rough triage.

See [`docs/METHODS.md`](docs/METHODS.md).

## Limitations

- **The transcription is not corrected.** Expect misread letters, split or merged words, and
  non-words. On the four text test folios roughly one word in three is not read exactly.
- **Small evaluation set.** Five held-out folios; the figures have wide uncertainty and the hands and
  document types in the test set do not cover the whole dossier.
- **Heterogeneous material.** Tables, seed lists, typed cards and printed pages are handled by a model trained
  mainly on manuscript letters; performance on these types has not been measured separately.
- **Ground truth is itself imperfect** and partly inconsistent (see `docs/GROUND_TRUTH.md`).
- **Line-level output only.** Reading order in columnar pages is not reliable, and no layout or
  region analysis has been done.
- **Literal transcription.** Original spelling, abbreviations and line-end hyphenation are kept; nothing is expanded or modernised.

## Roadmap

- Systematic human verification of a sample, to replace the current small test set with a larger one.
- A V5 round with more ground truth for the weakest document types.
- Comparison with transformer-based HTR / vision-language models on the same held-out folios.
- A documented LLM-assisted workflow for checking ground truth and proposing corrections, to be
  evaluated against human verification before any use (not included in this repository yet).

## Requirements

Kraken 5.2.9, Python 3.10 (see `requirements.txt`). Training starts from a public CATMuS-based Kraken model
(`McCATMuS_nfd_nofix_V1`), which is not redistributed here; obtain it from the CATMuS / Kraken model repositories.
Paths are configured in section 0 of the notebook (`HTR_BASE_DIR`).

## Data and rights

Page images are not distributed here. The images belong to the Archivo General de Indias; check its
reuse conditions before redistributing them. The transcriptions, ground truth and model in this repository are
the author's work product.

## Provenance and tooling

The V1–V4 models, the training pages and the manual line-by-line ground truth were produced by the author
with the workflow in the notebook. The evaluation script and the documentation in this repository were
drafted with AI assistance and reviewed by the author.

## Licence

To be decided before the first public release (proposal: MIT for code, CC BY 4.0 for transcriptions and ground truth).

## Author

Juan Alberto Salazar Rebolledo · GitHub: [jasolni](https://github.com/jasolni)
