"""Decision-support dashboard. Run from this folder: python -m streamlit run app.py."""
from datetime import date
import json
import math
import pandas as pd
import altair as alt
import streamlit as st
from engine import (BENCH,TICKERS,MIN_VOL,MAX_SHARPE,OPTIMIZERS,RISK_FREE,review,stress_suite,
                    retrospective_diagnostics,chronological_check)

st.set_page_config(page_title='FIN 439 | Five-year ETF committee review',layout='wide')
st.title('Five-year ETF investment committee review')
st.caption('AI disclosure: ChatGPT (GPT-6 family) assisted with research, implementation, calculations and drafting. The investment mandate and pilot decision are the student’s. Educational analysis only; not investment advice. No trades are placed.')
st.info('Frozen November 24, 2026 end-of-day research snapshot. 60 completed monthly total returns from PortfoliosLab, rounded to 0.01 percentage point; current Treasury reference from FRED. No historical vintage or prospective skill is claimed.')
with st.sidebar:
    st.header('Portfolio policy / scenarios')
    asof=st.date_input('Review date (end of day)',date(2026,11,24))
    window=st.selectbox('Monthly return observations',[60,48,36])
    cost=st.number_input('Trading cost per bought or sold dollar (bps)',0.,100.,10.,1.)
    target=st.number_input('Estimated net annual return floor (%)',0.,100.,6.,.5)/100
    reserve=st.number_input('Minimum BIL (%)',0.,100.,5.,1.)/100
    vol=st.number_input('Estimated annual volatility ceiling (%)',0.,100.,15.,1.)/100
    turn=st.number_input('Rolling annual one-way turnover ceiling (%)',0.,100.,25.,1.)/100
    used=st.number_input('Turnover already used (%)',0.,100.,0.,1.)/100
    draw=st.number_input('Current account drawdown (%)',0.,100.,0.,1.)/100
    with st.expander('Estimation assumptions (scenario controls)'):
        rf=st.number_input('Annual Treasury proxy (%)',0.,30.,float(RISK_FREE*100),.1,format='%.2f')/100
        haircut=st.number_input('Annual equity return haircut (percentage points)',0.,50.,0.,1.)/100
        sx=st.number_input('Additional SOXX annual return haircut (percentage points)',0.,50.,0.,1.)/100
        st.caption('Changing a haircut affects estimated mean return, not the covariance or historical returns. Scenario rate changes are not new observed yields.')
    with st.expander('Hypothetical pre-trade holdings',expanded=True):
        st.caption('Default is the 50/40/10 benchmark, not an actual account. Weights must total 100%.')
        current=[st.number_input(f'{t} (%)',0.,100.,float(w*100),1.,key=f'weight_{t}')/100 for t,w in zip(TICKERS,BENCH)]
    st.caption('Monthly review; annual planned rebalancing; separate 15% drawdown and nonpositive VOO signal pauses. No short selling or leverage.')

params=dict(window=window,cost_bps=cost,target=target,reserve=reserve,vol_limit=vol,turnover_limit=turn,
    prior_turnover=used,drawdown=draw,current=current,equity_haircut=haircut,soxx_haircut=sx,
    decision_date=str(asof),risk_free=rf)
try:
    result=review(**params,include_frontier=True)
except (ValueError,OSError,TypeError) as error:
    st.error(f'STOP: {error}. No allocation generated.');st.stop()
if result['stop_reasons']:
    st.error('STOP / NO NEW RISK — '+'; '.join(result['stop_reasons']))
else:
    st.success('PILOT — compare both candidate strategies using simulated capital only')
st.caption('Even a numerical PASS is not a forecast guarantee or authorization to invest. Real capital approved: 0%.')
cols=st.columns(4)
cols[0].metric('Data through',result['data_end'][:7]);cols[1].metric('12-month VOO signal',f"{result['signal_value']:.2%}")
cols[2].metric('Feasible grid candidates',f"{result['feasible_grid_count']:,} / 53,130");cols[3].metric('Live allocation','0%')

def percent(v):return '—' if v is None else f'{v:.2%}'

def summary(rows):
    return pd.DataFrame([{'Portfolio':x['portfolio'],'Net estimate':percent(x['net_estimate']),
        'Annual vol.':percent(x['volatility']),'Estimated Sharpe':f"{x['estimated_sharpe']:.3f}" if x['estimated_sharpe'] is not None else '—',
        'Turnover':percent(x['one_way_turnover']),'Cost':percent(x['trading_cost']),'BIL':percent(x['weights']['BIL']),
        'Verdict':x['verdict'],'Failed rules':'; '.join(x['failed_rules']) or 'None'} for x in rows])

def weight_summary(row):return ', '.join(f'{t} {w:.0%}' for t,w in row['weights'].items() if w>0)

rows={x['portfolio']:x for x in result['rows']}
main,construct,stress,historical,evidence=st.tabs(['Committee decision','Portfolio construction','Stress tests','Historical diagnostics','Data & methods'])
with main:
    st.subheader('Two ways to satisfy the same mandate')
    cards=st.columns(2)
    for box,name,description in zip(cards,OPTIMIZERS,['Lowest estimated volatility above the return floor','Highest estimated excess return per unit of volatility']):
        with box:
            st.markdown(f'**{name}** — {description}')
            if name not in rows: st.warning('No feasible allocation');continue
            x=rows[name]
            a,b,c=st.columns(3);a.metric('Net estimate',percent(x['net_estimate']));b.metric('Volatility',percent(x['volatility']));c.metric('Est. Sharpe',f"{x['estimated_sharpe']:.3f}")
            st.write(weight_summary(x));st.caption(f"Equities {x['equity_weight']:.0%} · BIL {x['weights']['BIL']:.0%} · turnover {x['one_way_turnover']:.0%} · {x['verdict']}")
    st.subheader('Benchmark and baseline verdicts')
    st.dataframe(summary(result['rows']),hide_index=True,use_container_width=True)
    if MIN_VOL in rows and MAX_SHARPE in rows:
        m,s=rows[MIN_VOL],rows[MAX_SHARPE]
        st.markdown(f"**Trade-off:** maximum estimated Sharpe minus minimum volatility = **{(s['net_estimate']-m['net_estimate'])*100:+.2f} pp** estimated net return and **{(s['volatility']-m['volatility'])*100:+.2f} pp** estimated annual volatility. Its volatility headroom is **{(vol-s['volatility'])*100:.2f} pp**. Neither is approved for live trading.")
    st.caption('Intended user: college-aged or early-career investor with a flexible five-year goal, emergency savings outside the portfolio and no scheduled withdrawals during the research horizon. Funds needed on a firm deadline should not rely on an equity forecast.')
with construct:
    st.subheader('Feasible risk–return frontier')
    pts=pd.DataFrame(result['feasible_points']);front=pd.DataFrame(result['frontier'])
    shown_points=len(pts)
    if shown_points>4000: pts=pts.iloc[::math.ceil(shown_points/4000)]
    markers=pd.DataFrame([{'Portfolio':x['portfolio'],'Volatility':x['volatility']*100,'Net return':x['net_estimate']*100,'Verdict':x['verdict'],'Sharpe':x['estimated_sharpe']} for x in result['rows']])
    xenc=alt.X('Volatility:Q',title='Estimated annual volatility (%)',scale=alt.Scale(zero=True))
    yenc=alt.Y('Net return:Q',title='Estimated first-year net return (%)',scale=alt.Scale(zero=True))
    mark=alt.Chart(markers).mark_point(filled=True,size=135,stroke='white',strokeWidth=1).encode(x=xenc,y=yenc,color='Portfolio:N',shape='Verdict:N',tooltip=['Portfolio','Volatility','Net return','Verdict','Sharpe'])
    layers=[mark]
    if not pts.empty:
        pts=pts.rename(columns={'volatility':'Volatility','net_return':'Net return'})*100
        front=front.rename(columns={'volatility':'Volatility','net_return':'Net return'})*100
        cloud=alt.Chart(pts).mark_circle(opacity=.15,size=13,color='#758c9a').encode(x=xenc,y=yenc,tooltip=['Volatility','Net return'])
        line=alt.Chart(front).mark_line(color='#183c65',strokeWidth=2.5).encode(x=xenc,y=yenc)
        layers=[cloud,line,mark]
    st.altair_chart(alt.layer(*layers).properties(height=400),use_container_width=True)
    st.caption(f'Gray points: {len(pts):,} displayed of {shown_points:,} numerically feasible grid points (deterministic display thinning above 4,000). The line connects all non-dominated grid points. Operational stops override numerical feasibility.')
    st.subheader('Allocation comparison')
    aw=pd.DataFrame([{'Portfolio':x['portfolio'],'ETF':t,'Weight (%)':w*100} for x in result['rows'] for t,w in x['weights'].items()])
    st.altair_chart(alt.Chart(aw).mark_bar().encode(y=alt.Y('Portfolio:N',sort=list(rows)),x=alt.X('Weight (%):Q',stack='zero',scale=alt.Scale(domain=[0,100])),color=alt.Color('ETF:N',sort=list(TICKERS)),tooltip=['Portfolio','ETF','Weight (%)']).properties(height=245),use_container_width=True)
    st.dataframe(pd.DataFrame({x['portfolio']:{t:f'{w:.1%}' for t,w in x['weights'].items()} for x in result['rows']}).T,use_container_width=True)
with stress:
    st.subheader('Sensitivity and stop conditions')
    st.caption('Scenarios hold the current sidebar inputs fixed except for the named input. The separate student-locked scenario is not included.')
    if st.button('Run exploratory stress scenarios'):
        cases=stress_suite(**params); data=[]
        for scenario,case in cases.items():
            for name in OPTIMIZERS:
                rr=next((x for x in case['rows'] if x['portfolio']==name),None)
                data.append({'Scenario':scenario,'Optimizer':name,'Feasible':case['feasible_grid_count'],'Net return':rr['net_estimate']*100 if rr else None,'Volatility':rr['volatility']*100 if rr else None,'Sharpe':rr['estimated_sharpe'] if rr else None,'Weights':weight_summary(rr) if rr else 'No feasible allocation','Action':case['recommendation']})
        df=pd.DataFrame(data)
        plot=alt.Chart(df.dropna(subset=['Net return'])).mark_bar().encode(y=alt.Y('Scenario:N',sort=None),x=alt.X('Net return:Q',title='Estimated net return (%)',scale=alt.Scale(zero=True)),color='Optimizer:N',yOffset='Optimizer:N',tooltip=['Scenario','Optimizer','Net return','Volatility','Sharpe','Action'])
        st.altair_chart(plot.properties(height=440),use_container_width=True)
        st.dataframe(df,hide_index=True,use_container_width=True)
        st.download_button('Download exploratory stress JSON',json.dumps(cases,indent=2),'stress-results.json')
with historical:
    st.subheader('Retrospective fixed-target portfolios')
    st.warning('Targets were selected using the full historical sample. This view is hindsight, not a backtest of the decision rule or evidence of predictive skill.')
    diag=retrospective_diagnostics(result);wealth=[];dd=[];hist_summary=[]
    for name,h in diag.items():
        for d,w,x in zip(h['dates'],h['wealth'],h['drawdown']):
            wealth.append({'Date':pd.Timestamp(d),'Portfolio':name,'Value ($)':10000*w});dd.append({'Date':pd.Timestamp(d),'Portfolio':name,'Drawdown (%)':x*100})
        hist_summary.append({'Portfolio':name,'CAGR':percent(h['cagr']),'Annualized realized vol.':percent(h['annualized_realized_volatility']),'Worst month-end drawdown':percent(h['max_month_end_drawdown'])})
    st.line_chart(pd.DataFrame(wealth),x='Date',y='Value ($)',color='Portfolio');st.line_chart(pd.DataFrame(dd),x='Date',y='Drawdown (%)',color='Portfolio')
    st.dataframe(pd.DataFrame(hist_summary),hide_index=True,use_container_width=True)
    st.caption('Hypothetical $10,000, initial transition from pre-trade weights, drift between annual fixed-target rebalances, modeled buys and sells charged; no actual historical trading or policy enforcement. Monthly drawdown may miss intra-month lows.')
    st.subheader('Chronological estimation challenge')
    c=chronological_check()
    st.write('Separate 36-month estimation sample through October 2024; subsequent 24 months evaluated without refitting those targets. Uses a dated October 30, 2024 Treasury proxy, not today’s yield. This is a research diagnostic on revised data, not an untouched holdout.')
    st.dataframe(pd.DataFrame([{'Portfolio':name,'Training allocation':', '.join(f'{t} {w:.0%}' for t,w in c['weights'][name].items() if w>0),'Later annualized return (CAGR)':percent(h['cagr']),'Later max month-end drawdown':percent(h['max_month_end_drawdown'])} for name,h in c['paths'].items()]),hide_index=True,use_container_width=True)
with evidence:
    st.subheader('Dated, auditable inputs')
    st.write('Observed completed return months: November 2021–October 2026; captured November 24, 2026. Last October session: October 30. November’s incomplete return is excluded. Data freshness stops the process after 45 days.')
    st.write(f"Treasury reference: 4.37% DGS3MO observed Nov 23, published Nov 24 at 3:16 pm CST. Active rate {rf:.2%}; {'scenario override' if result['risk_free_scenario'] else 'sourced reference'}.")
    st.markdown('[Monthly returns source: PortfoliosLab](https://portfolioslab.com/symbol/VOO) · [FRED DGS3MO](https://fred.stlouisfed.org/series/DGS3MO/history) · complete six source links and lineage in `docs/data-provenance.md`.')
    st.dataframe(pd.DataFrame({'Asset':TICKERS,'Annual arithmetic mean':[percent(result['asset_annual_arithmetic_means'][t]) for t in TICKERS],'Annual volatility':[percent(result['asset_annual_volatilities'][t]) for t in TICKERS]}),hide_index=True,use_container_width=True)
    st.write('Mean × 12; covariance × 12; volatility = square root of weighted covariance; turnover = half absolute weight changes; cost = full absolute weight changes × bps/10,000; first-year net estimate = (1 − cost) × (1 + gross estimate) − 1; estimated Sharpe = (first-year net estimate − short-term Treasury proxy) / annual volatility. The estimated Sharpe is a forward-looking scoring proxy, not a realized Sharpe statistic.')
    st.write('Risk: short sample, semiconductor concentration, overlap among equity funds, duration risk in BND, reinvestment risk in BIL, rounded/revised provider returns, taxes excluded, no live trading or demonstrated signal alpha. A 15% volatility ceiling does not cap actual losses.')
    st.write('Stop for stale or corrupted data, invalid weights, no feasible allocation, nonpositive 12-month VOO return, or account drawdown ≥15%. Any mandate change or eventual capital allocation requires committee approval.')
    st.code(result['return_file_sha256'],language=None)
    st.download_button('Download current review JSON',json.dumps(result,indent=2),'review.json')
