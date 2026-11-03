#!/usr/bin/env python3
"""Check that all prepared policy CSVs activate exactly the intended constraints.

This test deliberately follows the original src/japan9cewg2.py parsing order:
seeing a co2_intensity_tco2_per_mwh key turns the CO2 constraint ON.
"""
import csv, json, tempfile
from pathlib import Path
from run_case import prepare

ROOT = Path(__file__).resolve().parents[1]
CASES = json.loads((ROOT / 'cases.json').read_text(encoding='utf-8'))['cases']

def read_policy(path):
    with path.open(encoding='utf-8', newline='') as f:
        return {row['parameter']: row['value'] for row in csv.DictReader(f)}

def original_code_effective_co2_flag(p):
    active = p.get('use_co2_intensity_constraint', '').strip().lower() in {'1','true','yes','y','on'}
    if 'co2_intensity_tco2_per_mwh' in p or 'co2_intensity_kgco2_per_kwh' in p:
        active = True
    return active

def assert_policy(p, case, expected_co2, expected_sep):
    actual_co2 = original_code_effective_co2_flag(p)
    actual_sep = p.get('use_basic_mix_constraint', '').strip().lower() in {'1','true','yes','y','on'}
    assert actual_co2 == expected_co2, f'{case}: effective CO2={actual_co2}; expected {expected_co2}'
    assert actual_sep == expected_sep, f'{case}: SEP={actual_sep}; expected {expected_sep}'
    assert float(p.get('carbon_price', 0)) == 0, f'{case}: wrong carbon price'
    if expected_co2:
        assert float(p['co2_intensity_tco2_per_mwh']) == .04, f'{case}: wrong CO2 intensity'
    else:
        assert 'co2_intensity_tco2_per_mwh' not in p, f'{case}: unwanted intensity parameter'

assert_policy(read_policy(ROOT/'input'/'policy_2040.csv'), 'base input', False, False)
with tempfile.TemporaryDirectory(prefix='pypsa_policy_test_') as directory:
    for name,c in CASES.items():
        staged = prepare(name,Path(directory))
        p = read_policy(staged/'input'/'policy_2040.csv')
        assert_policy(p,name,c['co2_intensity_constraint'],c['basic_mix_constraint'])
        print(f'PASS {name}: CO2={c["co2_intensity_constraint"]}, SEP={c["basic_mix_constraint"]}')
print('PASS: all six effective policy flags and neutral base input')
