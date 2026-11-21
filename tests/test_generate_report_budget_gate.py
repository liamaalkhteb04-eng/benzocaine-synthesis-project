import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import generate_report
import unittest
from datetime import datetime, timezone, timedelta

class ReportBudgetGateTests(unittest.TestCase):
    def snapshot(self, **changes):
        value = {
            'verified': True,
            'free_credit_only_confirmed': True,
            'project_cumulative_usd': 1.0,
            'project_cap_usd': 1.2,
            'as_of_utc': datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),
            'verification_source': 'unit-test fixture; no external account check',
        }
        value.update(changes)
        return value

    def plan(self, snapshot):
        return {'paid_calls_authorized': True, 'report_generation_authorized': True, 'live_budget_snapshot': snapshot}

    def test_missing_snapshot_rejected(self):
        with self.assertRaises(ValueError): generate_report.verified_budget(self.plan(None))

    def test_unverified_or_paid_credit_snapshot_rejected(self):
        with self.assertRaises(ValueError): generate_report.verified_budget(self.plan(self.snapshot(verified=False)))
        with self.assertRaises(ValueError): generate_report.verified_budget(self.plan(self.snapshot(free_credit_only_confirmed=False)))

    def test_stale_snapshot_rejected(self):
        stamp=(datetime.now(timezone.utc)-timedelta(hours=25)).isoformat().replace('+00:00','Z')
        with self.assertRaises(ValueError): generate_report.verified_budget(self.plan(self.snapshot(as_of_utc=stamp)))

    def test_worst_case_reservation_over_cap_rejected(self):
        with self.assertRaises(ValueError): generate_report.verified_budget(self.plan(self.snapshot(project_cumulative_usd=1.19,project_cap_usd=1.20)))

    def test_current_credit_only_snapshot_accepted_when_reservation_fits(self):
        _,baseline,cap=generate_report.verified_budget(self.plan(self.snapshot(project_cumulative_usd=0.5,project_cap_usd=1.2)))
        self.assertEqual((baseline,cap),(0.5,1.2))

    def test_local_profile_paths_are_redacted_before_prompt(self):
        local_path = 'C:' + chr(92) + chr(92).join(['Users', 'Student', 'project', 'scripts', 'run.py'])
        value={'command':local_path,'relative':'reports/run-01'}
        cleaned,count=generate_report.redact_local_paths(value)
        self.assertEqual(count,1)
        self.assertEqual(cleaned['command'],'<LOCAL_PATH>')
        self.assertEqual(cleaned['relative'],'reports/run-01')

    def test_token_and_single_call_guards(self):
        req={'model':generate_report.MODEL_ID,'temperature':0,'reasoning_effort':'none','max_tokens':35000,'n':1,'stream':False,'messages':[{'role':'system','content':'s'},{'role':'user','content':'u'}]}
        self.assertEqual(generate_report.validate_request(req),2)
        bad={**req,'max_tokens':35001}
        with self.assertRaises(ValueError): generate_report.validate_request(bad)
        bad={**req,'n':2}
        with self.assertRaises(ValueError): generate_report.validate_request(bad)

if __name__=='__main__': unittest.main(verbosity=2)
