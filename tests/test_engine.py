import hashlib, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
import pandas as pd
from engine import (BENCH,TICKERS,ROOT,RETURN_HASH,MIN_VOL,MAX_SHARPE,RISK_FREE,OPTIMIZERS,grid,load_returns,load_rf,validate_returns,metrics,review,stress_suite,estimate_from,chronological_check,historical_path)
from build_data import build

class EngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base=review(include_frontier=True)
        cls.rows={x['portfolio']:x for x in cls.base['rows']}
        cls.r=load_returns()
    def test_annual_source_reconciliation(self):
        from audit_data import audit
        a=audit();self.assertTrue(all(x['within_rounding_tolerance'] for x in a['annual_checks']))
        self.assertEqual(len(a['annual_checks']),24)
        self.assertTrue(all(abs(x['difference_pp'])<=.05 for x in a['independent_publisher_checks']))
    def test_rebuild_exact_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            f=Path(tmp)/'copy.csv';self.assertEqual(build(f),RETURN_HASH)
            self.assertEqual(f.read_bytes(),(ROOT/'data/monthly_returns_pct.csv').read_bytes())
    def test_source_window_and_last_month(self):
        self.assertEqual(self.r.shape,(60,6));self.assertEqual(str(self.r.index[0].date()),'2021-11-30');self.assertEqual(str(self.r.index[-1].date()),'2026-10-31')
        np.testing.assert_allclose(self.r.iloc[-1],[-.0086,-.0666,-.1708,.0999,.0035,.0237])
    def test_source_checksum_fails_loudly(self):
        with tempfile.TemporaryDirectory() as tmp:
            f=Path(tmp)/'corrupted.csv';f.write_bytes((ROOT/'data/monthly_returns_pct.csv').read_bytes()+b'\n')
            with self.assertRaisesRegex(ValueError,'checksum'):load_returns(f)
    def test_data_schema_missing_and_duplicates(self):
        for bad in [self.r.iloc[:-1]*100,self.r.assign(VOO=np.nan)*100,self.r.set_axis([self.r.index[0]]*60)*100,self.r.assign(SOXX=-100)*100]:
            with self.assertRaises(ValueError):validate_returns(bad)
    def test_source_rf_and_vintage_gate(self):
        rf=load_rf();self.assertEqual(rf['observation_date'],'2026-11-23');self.assertEqual(rf['published_at'],'2026-11-24T15:16:00-06:00');self.assertAlmostEqual(rf['annual_percent']/100,RISK_FREE)
        with self.assertRaises(ValueError):review(decision_date='2026-11-23')
    def test_grid(self):
        w=grid();self.assertEqual(w.shape,(53130,6));self.assertTrue(np.all(w>=0));self.assertTrue(np.allclose(w.sum(1),1))
        self.assertEqual(len(np.unique(w,axis=0)),len(w))
    def test_independent_two_asset_known_answer(self):
        g,n,v,t,c=[float(z[0]) for z in metrics([.6,.4],np.array([.08,.04]),np.diag([.04,.01]),[.5,.5],10)]
        self.assertAlmostEqual(g,.064);self.assertAlmostEqual(t,.1);self.assertAlmostEqual(c,.0002)
        self.assertAlmostEqual(n,.0637872);self.assertAlmostEqual(v,np.sqrt(.016))
    def test_independent_weighted_monthly_returns(self):
        # Verify both portfolio volatility and gross mean directly from monthly portfolio returns,
        # rather than reusing the covariance implementation. Net/cost checked separately.
        for name in ('Benchmark',*OPTIMIZERS):
            x=self.rows[name];w=np.array(list(x['weights'].values()));pr=self.r.to_numpy()@w
            self.assertAlmostEqual(x['gross_estimate'],float(pr.mean()*12),places=12)
            self.assertAlmostEqual(x['volatility'],float(pr.std(ddof=1)*np.sqrt(12)),places=12)
            traded=sum(abs(a-b) for a,b in zip(w,BENCH));self.assertAlmostEqual(x['one_way_turnover'],traded/2)
            cost=traded*.001;self.assertAlmostEqual(x['net_estimate'],(1-cost)*(1+pr.mean()*12)-1)
            self.assertAlmostEqual(x['estimated_sharpe'],(x['net_estimate']-RISK_FREE)/x['volatility'])
    def test_optimizer_global_grid_winners(self):
        # Alternate direct monthly-return calculation across all grid portfolios.
        w=grid();pr=self.r.to_numpy()@w.T;g=pr.mean(0)*12;v=pr.std(0,ddof=1)*np.sqrt(12)
        t=np.abs(w-BENCH).sum(1)/2;n=(1-2*t*.001)*(1+g)-1
        ok=(n>=.06-1e-10)&(w[:,4]>=.05-1e-10)&(v<=.15+1e-10)&(t<=.25+1e-10)
        self.assertEqual(ok.sum(),self.base['feasible_grid_count']);self.assertAlmostEqual(self.rows[MIN_VOL]['volatility'],v[ok].min(),places=12)
        self.assertAlmostEqual(self.rows[MAX_SHARPE]['estimated_sharpe'],((n[ok]-RISK_FREE)/v[ok]).max(),places=12)
    def test_baseline_verdicts_and_selection(self):
        self.assertEqual(self.rows['Benchmark']['verdict'],'PASS');self.assertIn('Rolling turnover ceiling',self.rows['Equal weight']['failed_rules'])
        self.assertIn('Net return target',self.rows['Inverse volatility']['failed_rules'])
        self.assertEqual(self.rows[MIN_VOL]['weights'],dict(zip(TICKERS,[.4,0,0,0,.35,.25])))
        self.assertEqual(self.rows[MAX_SHARPE]['weights'],dict(zip(TICKERS,[.5,0,.15,.1,.1,.15])))
        for name in OPTIMIZERS:self.assertEqual(self.rows[name]['verdict'],'PASS')
    def test_frontier_is_nondominated(self):
        f=self.base['frontier'];v=np.array([x['volatility'] for x in f]);n=np.array([x['net_return'] for x in f])
        self.assertTrue(np.all(np.diff(v)>=0));self.assertTrue(np.all(np.diff(n)>0))
        for p in f:
            self.assertFalse(any(q['volatility']<p['volatility']-1e-10 and q['net_return']>=p['net_return']-1e-10 for q in self.base['feasible_points']))
    def test_30bps_cost_direction_both(self):
        higher={x['portfolio']:x for x in review(cost_bps=30)['rows']}
        for name in OPTIMIZERS:
            self.assertEqual(self.rows[name]['weights'],higher[name]['weights']);self.assertLess(higher[name]['net_estimate'],self.rows[name]['net_estimate']);self.assertAlmostEqual(higher[name]['volatility'],self.rows[name]['volatility'])
    def test_drawdown_boundary(self):
        self.assertFalse(review(drawdown=.1499)['paused']);self.assertTrue(review(drawdown=.15)['paused']);self.assertIn('STOP',review(drawdown=.15)['recommendation'])
    def test_signal_pause(self):
        bad=self.r.copy();bad.loc[bad.index[-12:],'VOO']=-.02
        with patch('engine.load_returns',return_value=bad):
            x=review();self.assertLess(x['signal_value'],0);self.assertTrue(x['paused']);self.assertIn('STOP',x['recommendation'])
    def test_data_freshness_boundary(self):
        self.assertFalse(review(decision_date='2026-12-14')['stale']);self.assertTrue(review(decision_date='2026-12-15')['stale'])
        self.assertTrue(all('Stale data' in x['failed_rules'] for x in review(decision_date='2026-12-15')['rows']))
    def test_bad_holdings_and_params(self):
        for v in [np.zeros(6),np.full(6,np.nan),np.array([-.1,.1,0,0,0,1])]:
            with self.assertRaises(ValueError):review(current=v)
        with self.assertRaises(ValueError):review(cost_bps=-1)
        with self.assertRaises(ValueError):review(window=59)
    def test_consumed_turnover(self):
        x=review(prior_turnover=.25);self.assertTrue(all(p['one_way_turnover']<1e-9 for p in x['rows'] if p['numerical_verdict']=='PASS'))
    def test_infeasible_rule(self):
        x=review(target=.90);self.assertEqual(x['feasible_grid_count'],0);self.assertIn('STOP',x['recommendation']);self.assertFalse(any(p['portfolio'] in OPTIMIZERS for p in x['rows']))
    def test_sensitivity_suite(self):
        cases=stress_suite();self.assertEqual(cases['Volatility ceiling 5%']['feasible_grid_count'],0);self.assertEqual(cases['Drawdown 15%']['recommendation'],'STOP / NO NEW RISK');self.assertGreater(cases['Base']['feasible_grid_count'],0)
        self.assertTrue(all(c['soxx_haircut']==0 for c in cases.values()))
    def test_historical_drift_and_cost(self):
        idx=pd.date_range('2025-01-31',periods=2,freq=pd.offsets.MonthEnd());r=pd.DataFrame([[.10,0,0,0,0,0],[.10,0,0,0,0,0]],index=idx,columns=TICKERS)
        # 50/40/10 buy and hold for two months: 50% grows 21%, remainder flat.
        x=historical_path(r,BENCH);self.assertAlmostEqual(x['wealth'][-1],1.105);self.assertAlmostEqual(x['max_month_end_drawdown'],0)
        y=historical_path(r,[1,0,0,0,0,0]);self.assertAlmostEqual(y['wealth'][-1],1.21*.999)
    def test_chronological_split(self):
        c=chronological_check();self.assertEqual(c['training_end'],'2024-10-31');self.assertEqual(c['evaluation_start'],'2024-11-30')
        self.assertTrue(all(len(p['wealth'])==25 for p in c['paths'].values()))

if __name__=='__main__':unittest.main()
