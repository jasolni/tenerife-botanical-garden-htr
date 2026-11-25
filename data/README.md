# Data

- `ground_truth/train/` — 58 ALTO XML files, manually aligned (training set of V4). Folio numbers 4955–5194.
- `ground_truth/test/` — 5 ALTO XML files: 5068, 5092, 5101, 5125, 5153. Never used for training.
- `transcription_v4/alto_v4.zip` — V4 ALTO XML for the 248 folios (IMG_4954–IMG_5200), unedited model output.
- `transcription_v4/dossier_v4.txt` — plain text of the same output (36,026 words in 6,305 lines).

The `<fileName>` element of every XML file holds only the image's base name. Page images are not included.
File names follow the pattern `clean_IMG_<number>`, where the number is the folio's photograph number.
