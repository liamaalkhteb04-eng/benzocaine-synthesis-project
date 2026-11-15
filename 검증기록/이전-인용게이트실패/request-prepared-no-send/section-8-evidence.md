Section 8 evidence only

Replace only the opening paragraph under the existing section 8 heading. Cite [D10]. Use the separately recomputed artifact `evidence-run/rerun/benzocaine-live-repro-20261105-01/reproduction-validation-corrected.json` and its input files.

Run relationship:
- benzocaine-live-20261031-03 is the original successful AiZynthFinder route run.
- benzocaine-live-20261031-04 is the earlier representative result bundle. Its routes.json is byte-identical to -03, SHA-256 a5256cab92771f695bff3b594e7a29ff0193f343923a51090e9df6da7dab6e63. The successful Parrot conditions and Yield-BERT predictions used as representative evidence are in -04. The -03 Parrot conditions file failed and is not the successful condition reference.
- benzocaine-live-repro-20261105-01 is the same-PC full rerun using submission code. Compare its routes to -03; compare its Parrot conditions and Yield-BERT outputs to -04.

Asset hashes match between the route runs: ONNX model uspto_model.onnx SHA-256 bd0a3cb74cd7068de474c8fb789a00a66bc42c75636d66510ccac585ebe928f8; compressed reaction-template archive uspto_templates.csv.gz SHA-256 a4f1945e90cfa195538320833d68aed38f14e2fcc2f8afb5d958bc920edcafbe; ZINC source SHA-256 99d39a6f807c3e815487500bafc2b4a9dc66a31af189e3b1776874fb0d4a188d; and all 26 derived stock bucket size/hash entries. The materialized configuration JSON byte hashes differ: -03 ef98c6f2fa1540fb59b41837afc33b550d7c5800fa16e71e50ebc3ec7edfc6bd, -05 9cf3ea6f9da7d0e1c5bfd942c74fa551a87eb70ea36bc7b48662a9e4d31d2563. Recorded configuration objects match after path-separator normalization. The historical temporary JSON is not preserved, so the exact byte-level cause is unresolved. Historical config-template hash was not recorded and is not comparable.

The original reproduction-validation.json has two false hash flags contradicted by raw assets. Preserve that original; a separate corrected validation was recomputed from raw evidence and passed. Keep prediction equality separate from asset-hash equality. The rerun covers the same molecule on the same PC only; no other molecule or PC was tested. Do not speculate about the config hash cause, overstate portability, or mention other reaction condition slots.
