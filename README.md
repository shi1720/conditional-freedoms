# What Did Release Release?

**Service, Surety, and Conditional Freedoms in England, 1349–1358**  
Shivam Gupta, Independent Researcher · 16 October 2026

This repository accompanies a historical research manuscript examining recruitment, departure, seasonal movement, release on service surety, and acquittal. Its contribution is an interpretive synthesis supported by a source register and a transparent partial reconstruction. It does not claim a newly discovered archive, a new general theory of freedom, or a complete model of medieval law.

Read the [paper](paper/What_Did_Release_Release_Shivam_Gupta.pdf) or its [editable source](paper/manuscript.txt).

## Reproduce the analysis

Python 3.9 or newer; analysis and tests require only the standard library. From the repository root:

```sh
python3 -m src.verify
python3 -m src.register
python3 -m src.analyze
python3 -m unittest discover -s tests -v
```

These commands check all 22 source anchors, generate the exhaustive logical assignments and summary in `results/`, and run nine regression tests. The enumeration domains are 512 recruitment rows (256 profiles × two status labels), eight departure rows, twelve seasonal rows (including unknown custom), and 64 combined rows. They are logical configurations, **not historical observations or prevalence estimates**.

To regenerate the figures and PDF:

```sh
python3 -m pip install -r requirements.txt
python3 -m src.figures
python3 -m src.build_pdf
```

The figure PNGs are embedded in the PDF; individual vector PDF figures are also supplied. All analysis runs locally without accounts or external inference services.

## Repository contents

| Path | Purpose |
|---|---|
| `data/source_units.json` | 22 manually curated units with printed page references, searchable anchors, interpretation, date and evidence type |
| `data/manifest.json` | Download URLs, access date, byte counts and SHA-256 hashes |
| `data/*_ocr.txt` | Pinned OCR of the historical editions; not diplomatic transcriptions |
| `src/model.py` | Separate recruitment, departure, mobility and release functions |
| `src/register.py` | Source-register definition and anchor verification |
| `src/analyze.py` | Exhaustive enumeration and constructed reading mutations |
| `tests/test_model.py` | Source-motivated regression cases and uncertainty checks |
| `results/` | Reproducible assignment-level CSVs and summary JSON |
| `figures/` | Three original figures, in PNG and vector PDF |
| `paper/` | Manuscript PDF and editable text |

## How to interpret the outputs

`True` means that the **specified provision's trigger** is present, not that a historical person was convicted. `False` means that this trigger is absent, not that an act was legally authorized under every applicable rule. `None` is an unresolved historical predicate or result. In CSVs it appears as an empty field; Boolean values appear as `True` or `False`.

Reasonable cause is an adjudicated input, not an automatic classification of a person's assertion. Protected customary movement is likewise an input: the code does not make the named counties into a closed eligibility list. The seasonal rule assumes an otherwise in-scope servant contemplating summer service away; local service means service at the stipulated terms. The combination of early-departure and seasonal restrictions is explicitly a **cumulative reading**, not an established judicial resolution of their precedence.

Release on service surety is kept distinct from the Cornwall acquittal. The latter does not fill unknown service or status facts. The commission function records the conjunction singled out for inquiry, rather than treating its complement as a lawful-release rule.

The deliberately defective readings in `results/mutations.csv` are constructed sensitivity cases. They are not attributed to named historians and were not measured as errors in a sample of publications. The tests verify implementation fidelity; historical interpretation remains open to source-based criticism.

## Sources and scope

The main documentary witnesses are White and Notestein (1915), pp. 141–157, and Putnam (1908), Appendix, pp. 24–25 and 152–154. The study uses published editions and does not claim inspection of the original manuscript rolls. Scans of Putnam's Appendix pp. 25 and 154 and White and Notestein's pp. 142 and 149 were visually checked and are retained in `data/scans/` with provenance in the manifest. The printed editions abridge material, and their selections cannot support national enforcement or acquittal rates.

The bibliography engages Bennett (2010), Cohn (2007), Whittle (2023), and Bailey (2023, 2025). Coercion within wage labour, harvest mobility exceptions, and the limitations of legislative inference are existing scholarship. The paper's proposed contribution is the coordinated analysis of the **objects and temporal effects of release**, plus the inspectable reconstruction. It makes no absolute priority or exhaustive novelty claim.

## Reuse

Original code: MIT licence. Original manuscript, figures and annotations: copyright Shivam Gupta, 2026; all rights reserved unless separately authorized. The historical editions are public domain in the United States and remain separately attributed. No licence over modern publisher material or archive website design is asserted. Bibliographic links identify modern scholarship; its full text is not redistributed here.

## Potential application

The register offers a prototype data model for scholarly editions and research tools that need to distinguish an exception from general permission, and discharge from a continuing obligation. A product could expose passage-level scope and uncertainty to readers. No market-size estimate, customer validation, patentability assessment or commercial-performance result is claimed.
