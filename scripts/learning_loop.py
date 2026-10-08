#!/usr/bin/env python3
"""Measurement tasks and metadata on existing objects; never collects or promotes rules."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import math
import re
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WINDOWS = {'1h': 3600, '3h': 10800, '6h': 21600, '12h': 43200, '24h': 86400,
           '72h': 259200, '7d': 604800, '14d': 1209600, '28d': 2419200}
STAGES = {'OBSERVATION', 'CASE', 'HYPOTHESIS', 'EVIDENCE', 'VALIDATION', 'RULE_CANDIDATE'}
PHASES = {'INITIAL_DISTRIBUTION', 'STAGNATION', 'REACTIVATION', 'LONG_TAIL', 'UNKNOWN'}
TRACKS = {'DISTRIBUTION', 'MONETIZATION', 'MEASUREMENT'}
MISSING = {'', 'UNKNOWN', 'NA', 'N/A', 'NULL'}
META = 'data/learning_loop_metadata.json'
VELOCITY = 'data/distribution_velocity_snapshots.csv'
EXTRA_FIELDS = ['production_id', 'target_window', 'due_at', 'observed_at', 'actual_age',
                'timing_delta', 'timing_status', 'measurement_source', 'measurement_status',
                'measurement_id', 'evidence_reference', 'measurement_window_start',
                'measurement_window_end', 'earnings_window_start', 'earnings_window_end',
                'earnings_match_status', 'attribution_status']
# Existing production surfaces only; this infrastructure protocol is not a content rule.
PROTECTED_EXCEPTIONS = {'docs/Measurement_Learning_Loop.md'}
PROTECTED_EXACT = {'production_variable_library.md', 'data/production_reference.md',
                   'scripts/release_runtime.py', 'scripts/validate_runtime_consistency.py',
                   'scripts/learning_loop.py', '.githooks/pre-commit'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def timestamp(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?(?:Z|[+-]\d\d:\d\d)', value):
        raise ValueError('exact timezone-aware timestamp required')
    return datetime.fromisoformat(value.replace('Z', '+00:00'))


def number(value):
    if str(value).strip().upper() in MISSING:
        return None
    n = float(value)
    if not math.isfinite(n) or n < 0:
        raise ValueError('metric must be finite and nonnegative')
    return n


def read_csv(root, path):
    with (root / path).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def load_meta(root):
    return json.loads((root / META).read_text(encoding='utf-8'))


def write_json(root, path, value):
    dest = root / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    temp = dest.with_suffix(dest.suffix + '.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temp.replace(dest)


def require(record, fields):
    for key in fields:
        if str(record.get(key, '')).strip().upper() in MISSING:
            raise ValueError(f'missing {key}')


def references(root, refs):
    if not isinstance(refs, list) or not refs:
        raise ValueError('nonempty evidence reference list required')
    for ref in refs:
        path = (root / ref.split('#', 1)[0]).resolve()
        if not path.is_relative_to(root.resolve()) or not path.is_file():
            raise ValueError(f'evidence not found: {ref}')


def publications(root):
    rows = read_csv(root, 'data/production_article_map.csv')
    overrides = {r['article_id']: r for r in load_meta(root)['publication_metadata']}
    seen = set()
    for row in rows:
        aid = row['article_id']
        if aid in seen:
            raise ValueError(f'duplicate publication mapping: {aid}')
        seen.add(aid)
        override = overrides.get(aid)
        if override:
            if override['production_id'] != row['production_id']:
                raise ValueError('publication metadata identity mismatch')
            references(root, override['evidence_reference'])
            row = dict(row, published_at=override['published_at'])
        try:
            pub = timestamp(row['published_at'])
            if not row.get('source') or (override and override['status'] != 'CONFIRMED'):
                pub = None
        except ValueError:
            pub = None
        yield row, pub


def timing(pub, observed, window):
    due = pub + timedelta(seconds=WINDOWS[window])
    delta = (observed - due).total_seconds()
    return {'due_at': due.isoformat(), 'actual_age': (observed-pub).total_seconds(),
            'timing_delta': delta, 'timing_status': 'ON_TIME' if delta == 0 else ('LATE' if delta > 0 else 'EARLY')}


def normalize_measurement(root, record):
    r = dict(record)
    require(r, ['article_id', 'production_id', 'observed_at', 'target_window', 'measurement_source', 'measurement_id'])
    if r['target_window'] not in {*WINDOWS, 'REVIEW_DAY', 'HISTORICAL_BACKFILL'}:
        raise ValueError('unsupported fixed window')
    if r.get('data_window') in {'REVIEW_DAY', 'HISTORICAL_BACKFILL'} and r['target_window'] in WINDOWS:
        raise ValueError('historical/review snapshots cannot be ingested as fixed windows')
    references(root, r.get('evidence_reference'))
    observed = timestamp(r['observed_at'])
    matches = [(p, t) for p, t in publications(root) if p['article_id'] == r['article_id']]
    if len(matches) != 1 or matches[0][0]['production_id'] != r['production_id']:
        raise ValueError('publication identity mapping required')
    p, pub = matches[0]
    r['published_at'] = p['published_at']
    for field in ['views', 'likes', 'comments', 'favorites', 'earnings']:
        number(r.get(field, 'UNKNOWN'))
        r[field] = r.get(field, 'UNKNOWN')
    if pub:
        if observed < pub:
            raise ValueError('observation precedes publication')
        if r['target_window'] in WINDOWS:
            r.update(timing(pub, observed, r['target_window']))
            r['measurement_status'] = 'OBSERVED' if r['timing_status'] == 'ON_TIME' else 'OBSERVED_OFF_WINDOW'
        else:
            r.update(due_at='UNKNOWN', actual_age=(observed-pub).total_seconds(), timing_delta='UNKNOWN',
                     timing_status='HISTORICAL_BACKFILL' if r['target_window'] == 'HISTORICAL_BACKFILL' else 'UNKNOWN',
                     measurement_status=r['target_window'])
    else:
        r.update(due_at='UNKNOWN', actual_age='UNKNOWN', timing_delta='UNKNOWN',
                 timing_status='PUBLISH_TIME_UNCERTAIN', measurement_status='PUBLISH_TIME_UNCERTAIN')
    r['attribution_status'] = 'ATTRIBUTION_UNKNOWN'
    if number(r['earnings']) is not None:
        require(r, ['measurement_window_start', 'measurement_window_end', 'earnings_window_start', 'earnings_window_end', 'earnings_match_status'])
        boundaries = [timestamp(r[f]) for f in ['measurement_window_start', 'measurement_window_end', 'earnings_window_start', 'earnings_window_end']]
        if not pub or boundaries != [pub, observed, pub, observed] or r['earnings_match_status'] != 'MATCH_BY_ARTICLE_ID':
            raise ValueError('earnings require verified identity and identical effective cumulative windows')
        r['attribution_status'] = 'WINDOW_ALIGNED_CAUSAL_ATTRIBUTION_UNKNOWN'
    r.update(checkpoint=r['target_window'], collected_at=r['observed_at'], source=r['measurement_source'])
    r['evidence_reference'] = json.dumps(r['evidence_reference'], ensure_ascii=False)
    return r


def ingest(root, batch):
    # Validate whole batch before any write; repeated IDs must be identical, never overwritten.
    normalized = [normalize_measurement(root, r) for r in batch]
    dest = root / VELOCITY
    with dest.open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        fields = list(reader.fieldnames)
        old = list(reader)
    fields += [f for f in EXTRA_FIELDS if f not in fields]
    index = {r.get('measurement_id'): r for r in old if r.get('measurement_id')}
    added = []
    for r in normalized:
        projected = {f: str(r.get(f, '')) for f in fields}
        prior = index.get(r['measurement_id'])
        if prior:
            if any(str(prior.get(f, '')) != projected[f] for f in fields):
                raise ValueError('measurement_id already exists with different data')
            continue
        index[r['measurement_id']] = projected
        added.append(projected)
    temp = dest.with_suffix('.csv.tmp')
    with temp.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(old + added)
    temp.replace(dest)
    return len(added)


def tasks(root, now):
    measurements = read_csv(root, VELOCITY)
    output = []
    for p, pub in publications(root):
        for window, seconds in WINDOWS.items():
            samples = [r for r in measurements if r.get('article_id') == p['article_id'] and r.get('target_window') == window]
            valid = [r for r in samples if r.get('timing_status') == 'ON_TIME' and r.get('measurement_status') == 'OBSERVED' and number(r.get('views', 'UNKNOWN')) is not None]
            due = pub + timedelta(seconds=seconds) if pub else None
            status = 'PUBLISH_TIME_UNCERTAIN' if not due else ('CAPTURED' if valid else ('OVERDUE_MISSING_WINDOW' if now > due else 'DUE' if now == due else 'SCHEDULED'))
            output.append({'task_id': p['article_id'] + ':' + window, 'article_id': p['article_id'],
                           'production_id': p['production_id'], 'published_at': p['published_at'],
                           'target_window': window, 'due_at': due.isoformat() if due else 'UNKNOWN',
                           'task_status': status, 'overdue_seconds': (now-due).total_seconds() if due and now > due and not valid else 0,
                           'sample_count': len(samples), 'historical_recovery': 'DO_NOT_BACKFILL_WITH_CURRENT_TOTALS'})
    return output


def deltas(root):
    groups = {}
    for row in read_csv(root, VELOCITY):
        if row.get('measurement_id') and row.get('observed_at'):
            groups.setdefault((row['article_id'], row.get('measurement_source')), []).append(row)
    out = []
    for (aid, source), rows in groups.items():
        rows.sort(key=lambda r: timestamp(r['observed_at']))
        for a, b in zip(rows, rows[1:]):
            duration = (timestamp(b['observed_at'])-timestamp(a['observed_at'])).total_seconds()
            av, bv = number(a.get('views', 'UNKNOWN')), number(b.get('views', 'UNKNOWN'))
            delta = bv-av if av is not None and bv is not None else None
            status = 'COMPARABLE_CUMULATIVE_ENDPOINTS' if duration > 0 and delta is not None and delta >= 0 else 'UNKNOWN_OR_COUNTER_REVISION'
            out.append({'article_id': aid, 'measurement_source': source, 'from_measurement': a['measurement_id'], 'to_measurement': b['measurement_id'],
                        'elapsed_seconds': duration, 'views_delta': delta if delta is not None else 'UNKNOWN',
                        'velocity_per_hour': delta*3600/duration if status == 'COMPARABLE_CUMULATIVE_ENDPOINTS' else 'UNKNOWN',
                        'comparison_status': status, 'phase': 'UNKNOWN', 'review_status': 'HUMAN_REVIEW_REQUIRED'})
    return out


def validate_metadata(root, meta):
    for r in meta['research_stage_records']:
        require(r, ['source_object', 'source_object_id', 'research_stage', 'transition_reason', 'transition_at', 'transition_by', 'track'])
        if r['research_stage'] not in STAGES or r['track'] not in TRACKS or r['source_object'] not in {'Observation', 'Parameter', 'Case', 'Experiment'}:
            raise ValueError('invalid research stage/object/track')
        timestamp(r['transition_at'])
        references(root, r['evidence_reference'])
        references(root, [r['source_reference']])
        if r['research_stage'] in {'VALIDATION', 'RULE_CANDIDATE'}:
            if r.get('validation_result') not in {'PASSED', 'FAILED', 'INCONCLUSIVE'} or r.get('counterexample_check') not in {'PASSED', 'FAILED', 'INCONCLUSIVE'}:
                raise ValueError('validation stage requires result and counterexample check')
        if r['research_stage'] == 'RULE_CANDIDATE' and r.get('validation_result') != 'PASSED':
            raise ValueError('failed/inconclusive validation cannot become rule candidate')
    for r in meta['lifecycle_observations']:
        require(r, ['article_id', 'evidence_reference', 'status', 'review_status'])
        if 'confidence' not in r:
            raise ValueError('confidence key required; UNKNOWN is allowed')
        if r.get('phase') not in PHASES or r['review_status'] not in {'PENDING', 'APPROVED', 'REJECTED'}:
            raise ValueError('invalid lifecycle observation')
        references(root, r['evidence_reference'])
        for k in ['phase_start', 'phase_end']:
            if r.get(k, 'UNKNOWN') != 'UNKNOWN':
                timestamp(r[k])
        if r.get('phase_start', 'UNKNOWN') != 'UNKNOWN' and r.get('phase_end', 'UNKNOWN') != 'UNKNOWN' and timestamp(r['phase_end']) < timestamp(r['phase_start']):
            raise ValueError('phase end precedes start')
        if r['review_status'] == 'APPROVED':
            require(r, ['reviewed_by', 'reviewed_at'])
            timestamp(r['reviewed_at'])
    for r in meta['promotion_approvals']:
        require(r, ['research_object', 'research_object_id', 'research_reference', 'validated_claim', 'validation_result',
                    'counterexample_check', 'target_file', 'target_section', 'proposed_change', 'change_version',
                    'approval_scope', 'approval_status', 'before_sha256', 'after_sha256', 'diff_sha256'])
        references(root, r['evidence_references'])
        references(root, [r['research_reference']])
        if r['approval_status'] not in {'PENDING', 'APPROVED', 'REJECTED'}:
            raise ValueError('invalid approval status')
        if r['approval_status'] == 'APPROVED':
            require(r, ['approved_by', 'approved_at', 'promotion_timestamp', 'human_approval_reference'])
            references(root, [r['human_approval_reference']])
            if timestamp(r['promotion_timestamp']) < timestamp(r['approved_at']):
                raise ValueError('promotion cannot precede approval')
            timestamp(r['approved_at']); timestamp(r['promotion_timestamp'])
            matching = [s for s in meta['research_stage_records'] if s['source_object'] == r['research_object'] and s['source_object_id'] == r['research_object_id']]
            if not matching or matching[-1]['research_stage'] not in {'VALIDATION', 'RULE_CANDIDATE'} or matching[-1].get('validation_result') != 'PASSED':
                raise ValueError('approval without passed validation')
            if matching[-1].get('counterexample_check') != 'PASSED' or timestamp(matching[-1]['transition_at']) > timestamp(r['approved_at']):
                raise ValueError('approval precedes validation or ignores failed counterexample check')
            if not set(matching[-1]['evidence_reference']).issubset(set(r['evidence_references'])):
                raise ValueError('approval omits validation evidence')
            if r['validation_result'] != 'PASSED' or r['counterexample_check'] != 'PASSED':
                raise ValueError('promotion requires passed validation and counterexample check')
            if r['research_object_id'].startswith('EXP008') or any('EXP008' in x.upper() or 'exp008' in x.lower() for x in r['evidence_references'] + [r['research_reference']]):
                raise ValueError('EXP008 promotions frozen in this implementation')
            evidence_hashes = r.get('evidence_sha256', {})
            for ref in r['evidence_references'] + [r['research_reference'], r['human_approval_reference']]:
                refpath = ref.split('#', 1)[0]
                if evidence_hashes.get(refpath) != digest((root/refpath).read_bytes()):
                    raise ValueError('reviewed evidence changed or lacks hash: ' + refpath)
            for key in ['before_sha256', 'after_sha256', 'diff_sha256']:
                if not re.fullmatch('[a-f0-9]{64}', r[key]):
                    raise ValueError('invalid change digest')
            if r['approval_scope'] not in {'Topic Selection', 'Topic Investment', 'Compiler', 'Prompt', 'ACTIVE Variable', 'Production Protocol'}:
                raise ValueError('invalid production approval scope')
            allowed = scope_for(r['target_file'])
            if r['approval_scope'] not in allowed:
                raise ValueError('approval scope does not cover target surface')


def validate_reference_changes(root, meta):
    records = meta.get('production_reference_records', [])
    for r in records:
        if r.get('reference_status') not in {'RESEARCH_ONLY', 'PRODUCTION_REFERENCE', 'VALIDATED_RULE'}:
            raise ValueError('invalid reference eligibility')
        references(root, [r['source_reference']])
        if r['reference_status'] == 'PRODUCTION_REFERENCE':
            require(r, ['accepted_by', 'accepted_at', 'acceptance_reference', 'scope'])
            if r.get('finding_kind') != 'DATA_FINDING':
                raise ValueError('candidate mechanisms are not production references')
            timestamp(r['accepted_at'])
            references(root, [r['acceptance_reference']])
        if r['reference_status'] == 'VALIDATED_RULE':
            matching = [x for x in meta['research_stage_records'] if x['source_object_id'] == r['source_object_id']]
            if not matching or matching[-1]['research_stage'] not in {'VALIDATION', 'RULE_CANDIDATE'} or matching[-1].get('validation_result') != 'PASSED' or matching[-1].get('counterexample_check') != 'PASSED':
                raise ValueError('validated rule label without validation')
    for r in meta.get('reference_change_approvals', []):
        # A reference is not a broad permission to change the production system.
        if r.get('approval_status') != 'APPROVED' or r.get('approval_kind') != 'REFERENCE_INTERFACE_REPAIR' or r.get('target_file') not in {
            'docs/Codex选题采集协议.md', 'data/production_reference.md'}:
            raise ValueError('reference approval exceeds interface scope')
        require(r, ['approved_by', 'approved_at', 'human_approval_reference', 'proposed_change'])
        timestamp(r['approved_at'])
        references(root, r['evidence_references'] + [r['human_approval_reference']])
        eligible = {x['reference_id'] for x in records if x['reference_status'] == 'PRODUCTION_REFERENCE'}
        if not r.get('reference_ids') or not set(r['reference_ids']).issubset(eligible):
            raise ValueError('unaccepted findings in reference change')
        for ref in r['evidence_references'] + [r['human_approval_reference']]:
            path = ref.split('#', 1)[0]
            if r.get('evidence_sha256', {}).get(path) != digest((root/path).read_bytes()):
                raise ValueError('reference acceptance evidence changed')
        for key in ['before_sha256', 'after_sha256', 'diff_sha256']:
            if not re.fullmatch('[a-f0-9]{64}', r.get(key, '')):
                raise ValueError('reference change digest required')


def scope_for(path):
    if path == 'production_variable_library.md' or path == 'runtime/production_variable_snapshot.md':
        return {'ACTIVE Variable'}
    if 'Compiler' in path:
        return {'Compiler'}
    if 'Prompt' in path or '正文生产Prompt' in path:
        return {'Prompt'}
    if path in {'docs/Codex选题采集协议.md', 'data/Topic_Pool.md'}:
        return {'Topic Selection', 'Topic Investment'}
    return {'Production Protocol'}


def protected(path):
    return path not in PROTECTED_EXCEPTIONS and (path in PROTECTED_EXACT or path.startswith(('docs/', 'templates/', 'skills/')) or (path.startswith('runtime/') and not path.startswith('runtime/logs/')))


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args])


def check_promotion(root, base='HEAD', staged=False):
    # Staged data and code are read from the index by the hook, not unstaged approval edits.
    raw = git(root, 'show', ':' + META) if staged else (root / META).read_bytes()
    meta = json.loads(raw)
    validate_metadata(root, meta)
    validate_reference_changes(root, meta)
    options = ['--cached'] if staged else []
    names = git(root, 'diff', *options, '--name-only', '-z', base).decode().split('\0')
    blocked = []
    for path in filter(protected, filter(None, names)):
        existed = subprocess.run(['git', '-C', str(root), 'cat-file', '-e', base + ':' + path], capture_output=True).returncode == 0
        before = git(root, 'show', base + ':' + path) if existed else b''
        if not existed and path in {'scripts/learning_loop.py', '.githooks/pre-commit'}:
            continue  # First installation only; later modifications require scoped approval.
        try:
            after = git(root, 'show', ':' + path) if staged else (root/path).read_bytes()
        except (subprocess.CalledProcessError, FileNotFoundError):
            after = b''
        diff = git(root, 'diff', *options, '--binary', base, '--', path)
        matches = [r for r in meta['promotion_approvals'] if r['approval_status'] == 'APPROVED' and r['target_file'] == path and
                   r['before_sha256'] == digest(before) and r['after_sha256'] == digest(after) and r['diff_sha256'] == digest(diff)]
        if not matches:
            matches = [r for r in meta.get('reference_change_approvals', []) if r['target_file'] == path and
                       r['before_sha256'] == digest(before) and r['after_sha256'] == digest(after) and r['diff_sha256'] == digest(diff)]
        if not matches:
            blocked.append(path)
        elif staged:
            # Approval and validation artifacts must themselves exist in the index.
            for ref in matches[0]['evidence_references'] + [matches[0]['human_approval_reference']] + ([matches[0]['research_reference']] if 'research_reference' in matches[0] else []):
                reference_path = ref.split('#', 1)[0]
                if git(root, 'show', ':' + reference_path) != (root/reference_path).read_bytes():
                    raise ValueError('staged evidence differs from reviewed evidence: ' + reference_path)
    if blocked:
        raise ValueError('unapproved scoped production changes: ' + ', '.join(blocked))


def validate_measurements(root):
    seen = set()
    for row in read_csv(root, VELOCITY):
        if not row.get('measurement_id'):
            continue
        if row['measurement_id'] in seen:
            raise ValueError('duplicate measurement_id')
        seen.add(row['measurement_id'])
        raw = dict(row, evidence_reference=json.loads(row['evidence_reference']))
        normalized = normalize_measurement(root, raw)
        for field in ['due_at', 'timing_status', 'measurement_status', 'attribution_status', 'published_at']:
            if str(row.get(field)) != str(normalized[field]):
                raise ValueError(f'tampered measurement field: {field}')
        for field in ['actual_age', 'timing_delta']:
            if str(row.get(field)) != str(normalized[field]):
                raise ValueError(f'tampered timing: {field}')


def refresh(root, now):
    meta = load_meta(root)
    validate_metadata(root, meta)
    validate_reference_changes(root, meta)
    validate_measurements(root)
    mapped = {p['article_id'] for p, _ in publications(root)}
    unmapped = sorted({r['article_id'] for r in read_csv(root, 'data/l0_content_assets.csv')} - mapped)
    write_json(root, 'reports/measurement_due_tasks.json', {'generated_at': now.isoformat(), 'deployment_status': 'DEPLOYMENT_GAP_NO_SCHEDULER_OR_PERSISTENT_COLLECTOR', 'mapping_gaps': [{'article_id': aid, 'status': 'MAPPING_REQUIRED', 'production_id': 'UNKNOWN'} for aid in unmapped], 'tasks': tasks(root, now)})
    write_json(root, 'reports/lifecycle_numeric_deltas.json', deltas(root))
    inputs = []
    mapping = read_csv(root, 'data/distribution_text_annotations_blind_map.csv')
    pair_ids = {r['blind_id'] for r in mapping if r.get('pair_id') == 'PAIR-02'}
    for r in read_csv(root, 'data/distribution_text_annotations_blind.csv'):
        if r['blind_id'] in pair_ids:
            inputs.append({k: r.get(k, 'UNKNOWN') for k in ['blind_id', 'answer_text', 'text_source_status']})
    write_json(root, 'reports/exp008_pair02_blind_input.json', {'version_at_publish': 'UNKNOWN', 'independent_unexposed_reviewer_required': True, 'records': inputs})
    queue = [
        {'task_id':'EXP008-P0-ALIGNMENT', 'priority':'P0', 'task':'Revenue Attribution Measurement Alignment', 'track':'MEASUREMENT', 'status':'OPEN', 'requires_human_review':True, 'input_reference':'reports/exp008_research_update_20261008.md#5', 'acceptance':'Same article and effective single-day read/revenue windows; missing is not zero; inaccessible history stays UNKNOWN'},
        {'task_id':'EXP008-P1-LIFECYCLE', 'priority':'P1', 'task':'Reactivation / Lifecycle Case-Control Evidence', 'track':'DISTRIBUTION', 'status':'OPEN', 'requires_human_review':True, 'input_reference':'reports/exp008_lifecycle_evidence_20261008.csv', 'acceptance':'Daily endpoints and sources for 老实人/性格适合领导/心腹异性/劳务派遣; never infer phases automatically'},
        {'task_id':'EXP008-P1-PAIR02', 'priority':'P1', 'task':'PAIR-02 Independent Blind Annotation', 'track':'DISTRIBUTION', 'status':'PENDING_INDEPENDENT_HUMAN', 'requires_human_review':True, 'blind_input':'reports/exp008_pair02_blind_input.json', 'acceptance':'Unexposed reviewer; establish version; lock annotation before outcome join; partial entry is not full text'}]
    # Queue is a derived view; completions and human decisions belong to source objects.
    write_json(root, 'reports/exp008_evidence_collection_queue.json', {'source_object':'Experiment', 'source_object_id':'EXP008', 'promotion_allowed':False, 'tasks':queue})
    historical = read_csv(root, 'data/review_data_snapshots.csv')
    write_json(root, 'reports/measurement_historical_metadata.json', {'classification_only':True, 'records':[
        {'source_reference':f'data/review_data_snapshots.csv#line-{i+2}', 'article_id':r['article_id'], 'production_id':r.get('production_id') or 'UNKNOWN',
         'data_window':r.get('data_window') or 'WINDOW_UNKNOWN', 'fixed_window_status':'HISTORICAL_BACKFILL',
         'publish_time_status':'PUBLISH_TIME_UNCERTAIN', 'attribution_status':'ATTRIBUTION_UNKNOWN', 'source_row_sha256':digest(json.dumps(r,sort_keys=True,ensure_ascii=False).encode())}
        for i,r in enumerate(historical)]})
    return len(tasks(root, now))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['refresh', 'validate', 'ingest', 'promotion-check'])
    parser.add_argument('--at', help='exact timestamp; defaults to current UTC')
    parser.add_argument('--input', type=Path, help='acquired JSON measurement batch; no network collection')
    parser.add_argument('--base', default='HEAD')
    parser.add_argument('--staged', action='store_true')
    args = parser.parse_args()
    try:
        if args.command == 'refresh':
            print(f'Generated {refresh(ROOT, timestamp(args.at) if args.at else datetime.now(timezone.utc))} measurement tasks; deployment gap remains')
        elif args.command == 'ingest':
            if not args.input:
                raise ValueError('--input required')
            print(f'Ingested {ingest(ROOT, json.loads(args.input.read_text(encoding="utf-8")))} measurements')
        elif args.command == 'promotion-check':
            check_promotion(ROOT, args.base, args.staged)
            print('Scoped promotion gate: PASS (no automatic promotion)')
        else:
            validate_metadata(ROOT, load_meta(ROOT))
            validate_reference_changes(ROOT, load_meta(ROOT))
            validate_measurements(ROOT)
            print('Learning metadata / acquired measurement validation: PASS')
    except (ValueError, KeyError, TypeError, OSError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f'FAIL: {exc}\n')

if __name__ == '__main__':
    main()
