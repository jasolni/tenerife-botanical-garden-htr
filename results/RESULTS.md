# Results

## 1. Held-out evaluation (`ketos test`)

Five folios (5068, 5092, 5101, 5125, 5153) never used in training; Kraken 5.2.9; same files for both models.

| Model | Training folios | Character accuracy | Word accuracy |
|---|---|---|---|
| V3 | 23 | 50.99 % | 4.40 % |
| V4 | 58 | 85.23 % | 53.30 % |

The gain comes from more and more varied ground truth and from a consistent preprocessing recipe, but this
experiment does not separate those two factors.

## 2. Line-level CER on four text folios (`scripts/evaluate_alto.py`)

V4 against the manual ground truth of the held-out set (folio 5125, a columnar table, is excluded).

| Folio | Reference chars | CER strict | CER lax | Exact words |
|---|---|---|---|---|
| 5068 | 767 | 10.6 % | 8.9 % | 67.7 % |
| 5092 | 732 | 9.3 % | 6.0 % | 52.0 % |
| 5101 | 1243 | 13.6 % | 10.5 % | 72.1 % |
| 5153 | 1050 | 10.6 % | 8.3 % | 69.7 % |
| **Total** | **3792** | **11.3 %** | **8.7 %** | **65.4 %** |

Strict CER ignores whitespace and end-of-line hyphens but counts case, accents and punctuation; lax CER
also ignores those. The `ketos test` accuracies above use a different counting scheme and are not the
complement of these CER values.

Reproduce:

```bash
unzip data/transcription_v4/alto_v4.zip -d /tmp/alto_v4
python scripts/evaluate_alto.py --reference data/ground_truth/test \
    --hypothesis /tmp/alto_v4 --pages 5068,5092,5101,5153
```

## 3. How to read these numbers

- Test set size: 5 folios (4 in the CER table, 3,792 reference characters). Differences between folios (6.0 % to
  10.5 % lax CER) show that the estimate is unstable.
- The reference is itself imperfect (`docs/GROUND_TRUTH.md`); some measured errors may be reference errors.
- Only manuscript text folios are in the CER table. Performance on printed pages, typed cards, tables and
  seed lists is not measured.
- At about 65 % exact words, roughly one word in three needs correction: the output is suitable for search,
  prioritisation and as a first draft for verification, not as a citable text.

## 4. Reference-free triage across the dossier

Mean share of dictionary-valid words per block of folios (indicator only; see `docs/METHODS.md`, section 6):

| Folios | Number | Mean ratio |
|---|---|---|
| 4954–4977 | 24 | 0.50 |
| 4978–5100 | 127 | 0.42 |
| 5101–5169 | 66 | 0.45 |
| 5170–5200 | 31 | 0.28 |

The last block contains the typed and printed pages, where a modern Spanish dictionary is a poor yardstick,
so the lower value does not by itself indicate worse recognition.
