#!/usr/bin/env python3
import copy
import csv
import json
import subprocess
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
import learning_loop as ll
from validate_l0_assets import parse_number


class LearningLoopTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root/'data').mkdir()
        (self.root/'reports').mkdir()
        (self.root/'docs').mkdir()
        (self.root/'reports/evidence.md').write_text('Evidence and human review fixture')
        self.meta = {'publication_metadata':[], 'research_stage_records':[], 'lifecycle_observations':[], 'promotion_approvals':[]}
        self.save()
        self.write_csv('data/production_article_map.csv', ['article_id','production_id','published_at','source'], [{'article_id':'a','production_id':'p','published_at':'2026-10-01T00:00:00+00:00','source':'verified publish result'}])
        self.write_csv(ll.VELOCITY, ['article_id','title','published_at','checkpoint','collected_at','views','likes','comments','favorites','thanks','earnings','source','notes'], [])
        self.record = {'article_id':'a','production_id':'p','target_window':'24h','observed_at':'2026-10-02T00:00:00+00:00','measurement_source':'content management cumulative','measurement_id':'m1','evidence_reference':['reports/evidence.md'],'views':20,'likes':1,'comments':0,'favorites':2,'earnings':'UNKNOWN'}

    def save(self):
        (self.root/ll.META).write_text(json.dumps(self.meta))

    def write_csv(self, path, fields, rows):
        with (self.root/path).open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

    def test_missing_markers_are_not_zero(self):
        for value in ['', 'UNKNOWN', 'unknown', 'NA', 'N/A', 'NULL', '  ']:
            self.assertIsNone(parse_number(value))
        self.assertEqual(parse_number('0'),0)
        self.assertEqual(parse_number('1.2万'),12000)
        for value in ['wrong','nan','inf']:
            with self.assertRaises(ValueError):parse_number(value)

    def test_30h_is_late_not_24h(self):
        r=ll.normalize_measurement(self.root,dict(self.record,observed_at='2026-10-02T06:00:00+00:00'))
        self.assertEqual(r['actual_age'],108000)
        self.assertEqual(r['timing_delta'],21600)
        self.assertEqual(r['timing_status'],'LATE')
        ll.ingest(self.root,[dict(self.record,observed_at='2026-10-02T06:00:00+00:00')])
        t=next(r for r in ll.tasks(self.root,ll.timestamp('2026-10-03T00:00:00Z')) if r['target_window']=='24h')
        self.assertEqual(t['task_status'],'OVERDUE_MISSING_WINDOW')

    def test_exact_and_early_window(self):
        self.assertEqual(ll.normalize_measurement(self.root,self.record)['timing_status'],'ON_TIME')
        self.assertEqual(ll.normalize_measurement(self.root,dict(self.record,observed_at='2026-10-01T23:00:00Z'))['timing_status'],'EARLY')
        ll.ingest(self.root,[self.record])
        t=next(r for r in ll.tasks(self.root,ll.timestamp('2026-10-03T00:00:00Z')) if r['target_window']=='24h')
        self.assertEqual(t['task_status'],'CAPTURED')

    def test_uncertain_publication_no_precision(self):
        self.write_csv('data/production_article_map.csv',['article_id','production_id','published_at','source'],[{'article_id':'a','production_id':'p','published_at':'2026-10-01 约 11:35 +03:00','source':'screenshot'}])
        r=ll.normalize_measurement(self.root,self.record)
        self.assertEqual(r['due_at'],'UNKNOWN')
        self.assertEqual(r['actual_age'],'UNKNOWN')
        self.assertEqual(r['timing_status'],'PUBLISH_TIME_UNCERTAIN')

    def test_daily_review_keeps_unknown_window(self):
        r=ll.normalize_measurement(self.root,dict(self.record,target_window='REVIEW_DAY',data_window='REVIEW_DAY'))
        self.assertEqual(r['due_at'],'UNKNOWN')
        self.assertEqual(r['measurement_status'],'REVIEW_DAY')

    def test_historical_and_wrong_identity_rejected(self):
        for r in [dict(self.record,data_window='REVIEW_DAY'),dict(self.record,data_window='HISTORICAL_BACKFILL'),dict(self.record,production_id='wrong'),dict(self.record,observed_at='2026-09-30T00:00:00Z')]:
            with self.assertRaises(ValueError):ll.normalize_measurement(self.root,r)

    def test_earnings_windows_require_alignment(self):
        aligned=dict(self.record,earnings=3,measurement_window_start='2026-10-01T00:00:00Z',measurement_window_end='2026-10-02T00:00:00Z',earnings_window_start='2026-10-01T00:00:00Z',earnings_window_end='2026-10-02T00:00:00Z',earnings_match_status='MATCH_BY_ARTICLE_ID')
        self.assertEqual(ll.normalize_measurement(self.root,aligned)['attribution_status'],'WINDOW_ALIGNED_CAUSAL_ATTRIBUTION_UNKNOWN')
        for r in [dict(self.record,earnings=3),dict(aligned,earnings_window_end='2026-10-01T23:00:00Z'),dict(aligned,earnings_match_status='MATCH_BY_TITLE_DATE')]:
            with self.assertRaises(ValueError):ll.normalize_measurement(self.root,r)

    def test_batch_atomic_idempotent_no_overwrite(self):
        before=(self.root/ll.VELOCITY).read_bytes()
        with self.assertRaises(ValueError):ll.ingest(self.root,[self.record,dict(self.record,measurement_id='m2',views=-1)])
        self.assertEqual(before,(self.root/ll.VELOCITY).read_bytes())
        self.assertEqual(ll.ingest(self.root,[self.record]),1)
        self.assertEqual(ll.ingest(self.root,[self.record]),0)
        with self.assertRaises(ValueError):ll.ingest(self.root,[dict(self.record,views=99)])

    def test_deltas_do_not_classify_phase(self):
        ll.ingest(self.root,[self.record,dict(self.record,measurement_id='m2',target_window='72h',observed_at='2026-10-04T00:00:00Z',views=100)])
        row=ll.deltas(self.root)[0]
        self.assertEqual(row['views_delta'],80)
        self.assertEqual(row['phase'],'UNKNOWN')
        self.assertEqual(row['review_status'],'HUMAN_REVIEW_REQUIRED')

    def test_lifecycle_repeated_overlap_allowed_human_approval_required(self):
        r={'article_id':'a','phase':'REACTIVATION','phase_start':'UNKNOWN','phase_end':'UNKNOWN','evidence_reference':['reports/evidence.md'],'confidence':'UNKNOWN','status':'PROPOSED','review_status':'PENDING'}
        self.meta['lifecycle_observations']=[r,copy.deepcopy(r),dict(r,phase='UNKNOWN')]
        ll.validate_metadata(self.root,self.meta)
        self.meta['lifecycle_observations'][0]['review_status']='APPROVED'
        with self.assertRaises(ValueError):ll.validate_metadata(self.root,self.meta)

    def stage(self,result='PASSED',oid='case1'):
        return {'source_object':'Case','source_object_id':oid,'source_reference':'reports/evidence.md','research_stage':'VALIDATION','track':'DISTRIBUTION','evidence_reference':['reports/evidence.md'],'transition_reason':'reviewed results','transition_at':'2026-10-08T00:00:00Z','transition_by':'human fixture','validation_result':result,'counterexample_check':'PASSED'}

    def test_stage_failed_validation_cannot_be_rule(self):
        s=self.stage('FAILED');self.meta['research_stage_records']=[s]
        ll.validate_metadata(self.root,self.meta)
        s['research_stage']='RULE_CANDIDATE'
        with self.assertRaises(ValueError):ll.validate_metadata(self.root,self.meta)

    def setup_git(self):
        self.run_git('init','-q');self.run_git('config','user.email','test@example.invalid');self.run_git('config','user.name','Test')
        (self.root/'docs/content.md').write_text('old rule')
        self.run_git('add','.');self.run_git('commit','-qm','baseline')
        (self.root/'docs/content.md').write_text('new rule')

    def run_git(self,*args):
        return subprocess.check_output(['git','-C',str(self.root),*args],stderr=subprocess.STDOUT)

    def approval(self):
        return {'research_object':'Case','research_object_id':'case1','research_reference':'reports/evidence.md','validated_claim':'test claim','validation_result':'PASSED','counterexample_check':'PASSED','evidence_references':['reports/evidence.md'],'target_file':'docs/content.md','target_section':'rule','proposed_change':'old to new','change_version':'v1','evidence_sha256':{'reports/evidence.md':ll.digest((self.root/'reports/evidence.md').read_bytes())},'human_approval_reference':'reports/evidence.md','approved_by':'human test fixture','approved_at':'2026-10-08T00:00:00Z','promotion_timestamp':'2026-10-08T00:00:00Z','approval_scope':'Production Protocol','approval_status':'APPROVED','before_sha256':ll.digest(b'old rule'),'after_sha256':ll.digest(b'new rule'),'diff_sha256':ll.digest(self.run_git('diff','--binary','HEAD','--','docs/content.md'))}

    def test_gate_blocks_unapproved_allows_exact_approved_change(self):
        self.setup_git()
        with self.assertRaises(ValueError):ll.check_promotion(self.root)
        self.meta['research_stage_records']=[self.stage()]
        self.meta['promotion_approvals']=[self.approval()];self.save()
        ll.check_promotion(self.root)
        (self.root/'docs/content.md').write_text('different unapproved rule')
        with self.assertRaises(ValueError):ll.check_promotion(self.root)

    def test_failed_validation_and_exp008_cannot_promote(self):
        self.setup_git();self.meta['research_stage_records']=[self.stage('FAILED')]
        self.meta['promotion_approvals']=[self.approval()]
        with self.assertRaises(ValueError):ll.validate_metadata(self.root,self.meta)
        self.meta['research_stage_records']=[self.stage(oid='EXP008-case')]
        self.meta['promotion_approvals'][0]['research_object_id']='EXP008-case'
        with self.assertRaises(ValueError):ll.validate_metadata(self.root,self.meta)

    def test_tampered_timing_is_rejected(self):
        ll.ingest(self.root,[self.record])
        path=self.root/ll.VELOCITY
        with path.open(newline='') as f:
            reader=csv.DictReader(f);fields=reader.fieldnames;rows=list(reader)
        rows[0]['timing_delta']='999'
        self.write_csv(ll.VELOCITY,fields,rows)
        with self.assertRaises(ValueError):ll.validate_measurements(self.root)

    def test_wrong_promotion_scope_rejected(self):
        self.setup_git();self.meta['research_stage_records']=[self.stage()]
        self.meta['promotion_approvals']=[dict(self.approval(),target_file='production_variable_library.md',approval_scope='Compiler')]
        with self.assertRaises(ValueError):ll.validate_metadata(self.root,self.meta)

    def test_approved_staged_change_and_hook_blocks_future_change(self):
        self.setup_git();self.meta['research_stage_records']=[self.stage()]
        self.meta['promotion_approvals']=[self.approval()];self.save()
        self.run_git('add','.')
        ll.check_promotion(self.root,staged=True)
        (self.root/'docs/content.md').write_text('other rule')
        self.run_git('add','docs/content.md')
        with self.assertRaises(ValueError):ll.check_promotion(self.root,staged=True)

    def test_failed_counterexample_and_changed_evidence_block_promotion(self):
        self.setup_git();self.meta['research_stage_records']=[self.stage()]
        self.meta['promotion_approvals']=[self.approval()]
        self.meta['research_stage_records'][0]['counterexample_check']='FAILED'
        with self.assertRaises(ValueError):ll.validate_metadata(self.root,self.meta)
        self.meta['research_stage_records'][0]['counterexample_check']='PASSED'
        (self.root/'reports/evidence.md').write_text('Changed after approval')
        with self.assertRaises(ValueError):ll.validate_metadata(self.root,self.meta)

    def test_operational_records_not_treated_as_rule_changes(self):
        self.assertFalse(ll.protected('data/Topic_Pool.md'))
        self.assertFalse(ll.protected('data/Publish_Queue.md'))
        self.assertFalse(ll.protected('runtime/logs/production_runs.jsonl'))
        self.assertTrue(ll.protected('docs/Codex选题采集协议.md'))
        self.assertTrue(ll.protected('production_variable_library.md'))

    def test_reference_eligibility_requires_human_acceptance(self):
        r={'reference_id':'r1','source_object_id':'EXP008','source_reference':'reports/evidence.md','reference_status':'PRODUCTION_REFERENCE'}
        self.meta['production_reference_records']=[r]
        with self.assertRaises(ValueError):ll.validate_reference_changes(self.root,self.meta)
        r.update(finding_kind='DATA_FINDING',accepted_by='User',accepted_at='2026-10-09T00:00:00Z',acceptance_reference='reports/evidence.md',scope='manual selection only')
        ll.validate_reference_changes(self.root,self.meta)
        r['reference_status']='VALIDATED_RULE'
        with self.assertRaises(ValueError):ll.validate_reference_changes(self.root,self.meta)

    def test_reference_permission_cannot_touch_prompt_or_active(self):
        self.meta['reference_change_approvals']=[{'approval_kind':'REFERENCE_INTERFACE_REPAIR','approval_status':'APPROVED','target_file':'templates/Claude正文生产Prompt.md'}]
        with self.assertRaises(ValueError):ll.validate_reference_changes(self.root,self.meta)
        self.meta['reference_change_approvals'][0]['target_file']='production_variable_library.md'
        with self.assertRaises(ValueError):ll.validate_reference_changes(self.root,self.meta)

    def test_reference_bridge_allows_exact_change_without_causal_validation(self):
        self.setup_git()
        (self.root/'docs/content.md').write_text('old rule')
        path='docs/Codex选题采集协议.md'
        (self.root/path).write_text('old reference interface')
        self.run_git('add','.');self.run_git('commit','-qm','interface baseline')
        (self.root/path).write_text('new reference interface')
        self.meta['production_reference_records']=[{'reference_id':'r1','source_object_id':'EXP008','source_reference':'reports/evidence.md','reference_status':'PRODUCTION_REFERENCE','finding_kind':'DATA_FINDING','accepted_by':'User','accepted_at':'2026-10-09T00:00:00Z','acceptance_reference':'reports/evidence.md','scope':'manual selection only'}]
        self.meta['reference_change_approvals']=[{'approval_kind':'REFERENCE_INTERFACE_REPAIR','approval_status':'APPROVED','target_file':path,'approved_by':'User','approved_at':'2026-10-09T00:00:00Z','human_approval_reference':'reports/evidence.md','proposed_change':'reference interface only','reference_ids':['r1'],'evidence_references':['reports/evidence.md'],'evidence_sha256':{'reports/evidence.md':ll.digest((self.root/'reports/evidence.md').read_bytes())},'before_sha256':ll.digest(b'old reference interface'),'after_sha256':ll.digest(b'new reference interface'),'diff_sha256':ll.digest(self.run_git('diff','--binary','HEAD','--',path))}]
        self.save();ll.check_promotion(self.root)
        self.assertEqual(self.meta['research_stage_records'],[])
        (self.root/path).write_text('unapproved expanded rule')
        with self.assertRaises(ValueError):ll.check_promotion(self.root)

    def test_reference_permission_cannot_rewrite_gate_or_compiler(self):
        for path in ['scripts/learning_loop.py', 'docs/知乎OS Compiler V1.md']:
            self.meta['reference_change_approvals']=[{'approval_kind':'REFERENCE_INTERFACE_REPAIR','approval_status':'APPROVED','target_file':path}]
            with self.assertRaises(ValueError):ll.validate_reference_changes(self.root,self.meta)

    def test_accepted_candidate_mechanism_cannot_be_data_finding(self):
        self.meta['production_reference_records']=[{'reference_id':'candidate','source_object_id':'EXP008','source_reference':'reports/evidence.md','reference_status':'PRODUCTION_REFERENCE','finding_kind':'CANDIDATE_MECHANISM','accepted_by':'User','accepted_at':'2026-10-09T00:00:00Z','acceptance_reference':'reports/evidence.md','scope':'manual selection only'}]
        with self.assertRaises(ValueError):ll.validate_reference_changes(self.root,self.meta)

    def test_index_gate_ignores_unstaged_approval(self):
        self.setup_git();self.run_git('add','docs/content.md')
        self.meta['research_stage_records']=[self.stage()];self.meta['promotion_approvals']=[self.approval()];self.save()
        with self.assertRaises(ValueError):ll.check_promotion(self.root,staged=True)


if __name__=='__main__':unittest.main()
