# Models

`tenerife_V4_best.mlmodel` — Kraken recognition model, fine-tuned from `McCATMuS_nfd_nofix_V1` on 58
manually aligned folios (see `../docs/METHODS.md`). Trained with Kraken 5.2.9:

```bash
ketos train -i McCATMuS_nfd_nofix_V1.mlmodel -f alto --resize add --workers 0 -o tenerife_V4 <aligned ALTO files>
```

Use:

```bash
kraken -a -i page.png page.xml segment -bl ocr -m models/tenerife_V4_best.mlmodel
```

(on a binarized image, as in section 7 of the notebook). The base model is not redistributed.
