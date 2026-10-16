"""Exhaustive logical sensitivity analyses; no synthetic row is a historical person."""
import csv, json
from itertools import product
from pathlib import Path
from src.model import *

ROOT = Path(__file__).resolve().parents[1]

def write_csv(name, rows):
    with (ROOT/'results'/name).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

def run():
    rows=[]
    for bits in product((False,True), repeat=8):
        for status in ('free','bond'):
            p=Recruitment(*bits,status=status)
            rows.append({**p.__dict__, 'trigger':recruitment_trigger(p)})
    write_csv('recruitment.csv', rows)
    departures=[]
    for term,licence,cause in product((False,True),repeat=3):
        correct=early_departure_trigger(term,licence,cause)
        departures.append(dict(term=term,licence=licence,cause=cause,trigger=correct,
                               licence_only=term and not licence,
                               both_required=term and not (licence and cause),
                               no_exception=term))
    write_csv('departure.csv',departures)
    seasonal=[]
    for local,august in product((False,True),repeat=2):
        for protected in (False,True,None):
            seasonal.append(dict(local_service_at_rate=local,august=august,
                protected_custom=protected,restriction=seasonal_restriction(local,august,protected)))
    write_csv('seasonal.csv',seasonal)
    combinations=[]
    for bits in product((False,True),repeat=6):
        term,licence,cause,local,august,custom=bits
        d=early_departure_trigger(term,licence,cause)
        m=seasonal_restriction(local,august,custom)
        combinations.append(dict(term=term,licence=licence,cause=cause,local=local,
            august=august,custom=custom,term_bar=d,mobility_bar=m,cumulative_bar=d or m))
    write_csv('combined.csv',combinations)
    # Explicitly constructed bad readings, not measured errors in existing scholarship.
    mutation_rows=[]
    for field in ('licence_only','both_required','no_exception'):
        mismatch=sum(r['trigger']!=r[field] for r in departures)
        mutation_rows.append(dict(reading=field,disagreements=mismatch,domain=8))
    seasonal_bool=[r for r in seasonal if r['protected_custom'] is not None]
    for name,fn in [('blanket_geographical_ban',lambda r:True),
                    ('omit_customary_saving',lambda r:r['local_service_at_rate'])]:
        mutation_rows.append(dict(reading=name,disagreements=sum(
            r['restriction']!=fn(r) for r in seasonal_bool),domain=len(seasonal_bool)))
    write_csv('mutations.csv',mutation_rows)
    # All counts have declared finite domains. No prevalence estimates or p-values.
    out=dict(recruitment_rows=len(rows),recruitment_trigger_rows=sum(r['trigger'] for r in rows),
        departure_rows=len(departures),departure_trigger_rows=sum(r['trigger'] for r in departures),
        seasonal_rows=len(seasonal),seasonal_unresolved=sum(r['restriction'] is None for r in seasonal),
        combined_rows=len(combinations),
        seasonal_clear_but_term_bar=sum(not r['mobility_bar'] and r['term_bar'] for r in combinations),
        source_units=len(json.loads((ROOT/'data'/'source_units.json').read_text())),
        mutations=mutation_rows)
    (ROOT/'results'/'summary.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':run()
