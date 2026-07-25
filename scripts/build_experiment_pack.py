"""Build deterministic synthetic retail Test & Learn evidence; standard library only."""
import csv, json, random
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'; OUT=ROOT/'analysis'/'outputs'; IMG=ROOT/'docs'/'images'; R=random.Random(20260724)
STORES=[('S01','Northeast','Urban',1.05),('S02','Northeast','Suburban',.96),('S03','South','Urban',1.10),('S04','South','Suburban',.94),('S05','Midwest','Urban',.99),('S06','Midwest','Suburban',.92),('S07','West','Urban',1.08),('S08','West','Suburban',.98)]
def write(n,fields,rows):
 with (DATA/n).open('w',newline='') as f: w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
def chart(name,title,sub,bars,color):
 m=max(v for _,v,_ in bars); s=['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="510">','<rect width="100%" height="100%" fill="#fbfcfe"/>',f'<text x="55" y="55" font-family="Arial" font-size="28" font-weight="700" fill="#132238">{title}</text>',f'<text x="55" y="84" font-family="Arial" font-size="15" fill="#516176">{sub}</text>','<line x1="95" y1="410" x2="945" y2="410" stroke="#bdc9d6"/>']
 for i,(lab,val,note) in enumerate(bars):
  x=135+i*195; h=260*val/m; y=410-h; s += [f'<rect x="{x}" y="{y}" width="105" height="{h}" rx="6" fill="{color}"/>',f'<text x="{x+52}" y="{y-15}" text-anchor="middle" font-family="Arial" font-size="20" font-weight="700">{note}</text>',f'<text x="{x+52}" y="440" text-anchor="middle" font-family="Arial" font-size="15">{lab}</text>']
 s += ['<text x="55" y="480" font-family="Arial" font-size="13" fill="#66778c">Synthetic illustrative analysis • deterministic seed • statistical review required before rollout</text>','</svg>']; (IMG/name).write_text(''.join(s))
def main():
 DATA.mkdir(exist_ok=True); OUT.mkdir(parents=True,exist_ok=True); IMG.mkdir(parents=True,exist_ok=True)
 stores=[dict(store_id=s,region=r,store_format=f,baseline_index=b,eligible_flag='Y') for s,r,f,b in STORES]; write('store_attributes.csv',stores[0],stores)
 customers=[dict(customer_id=f'C{i:04d}',segment=('Value','Core','Premium')[i%3],loyalty_tier=('None','Member','VIP')[i%3],region=STORES[i%8][1],prior_90d_spend=round(70+(i%11)*17.5,2),eligible_flag='Y') for i in range(1,201)]; write('customer_attributes.csv',customers[0],customers)
 assigns=[dict(store_id=s,treatment_group='treatment' if int(s[-1])%2 else 'control',match_cell=f'{r}-{f}',assignment_date='2026-04-01') for s,r,f,b in STORES]; write('test_assignments.csv',assigns[0],assigns)
 tx=[]
 for week in range(1,9):
  for s,r,f,b in STORES:
   treat=int(s[-1])%2==1
   for j in range(160):
    c=customers[(week*37+j*7+int(s[-1])*13)%200]; base=82*b+(12 if c['segment']=='Premium' else 0)+R.gauss(0,18); effect=7.5 if treat and c['segment']!='Value' else (2 if treat else 0); sales=max(12,base+effect)
    tx.append(dict(transaction_id=f'T{week:02d}{s}{j:03d}',week=week,store_id=s,customer_id=c['customer_id'],channel='store' if j%5 else 'ecommerce',treatment_group='treatment' if treat else 'control',segment=c['segment'],net_sales=round(sales,2),gross_margin=round(sales*(.42 if j%4 else .35),2),converted=1 if sales>76 else 0))
 write('transactions.csv',tx[0],tx)
 feeds=[dict(feed_id=f'F{s}{w}',source_system='POS' if w%3 else 'CRM',store_id=s,week=w,expected_rows=160,received_rows=148 if s=='S06' and w==4 else 160,null_rate=.011 if s=='S06' and w==4 else .002,status='warning' if s=='S06' and w==4 else 'pass') for s,_,_,_ in STORES for w in range(1,9)]; write('data_feed_validation.csv',feeds[0],feeds)
 ag=defaultdict(lambda:[0,0,0,0])
 for x in tx: a=ag[x['treatment_group'],x['segment']]; a[0]+=1;a[1]+=x['converted'];a[2]+=float(x['net_sales']);a[3]+=float(x['gross_margin'])
 rows=[dict(treatment_group=g,segment=s,n=a[0],conversion_rate=round(a[1]/a[0],4),avg_order_value=round(a[2]/a[0],2),gross_margin_per_order=round(a[3]/a[0],2)) for (g,s),a in sorted(ag.items())]; write('experiment_summary.csv',rows[0],rows)
 t=[float(x['net_sales']) for x in tx if x['treatment_group']=='treatment']; c=[float(x['net_sales']) for x in tx if x['treatment_group']=='control']; ta=sum(t)/len(t); ca=sum(c)/len(c); lift=(ta/ca-1)*100
 summary={'observations':len(tx),'stores':8,'weeks':8,'treatment_aov':round(ta,2),'control_aov':round(ca,2),'estimated_aov_lift_pct':round(lift,2),'data_feed_warning':'S06/week 4: 12 rows short; repair or exclude before decision.'}; (OUT/'experiment_summary.json').write_text(json.dumps(summary,indent=2)+'\n'); (OUT/'segment_readout.csv').write_text('segment,treatment_aov,control_aov,illustrative_lift_pct,decision\nValue,80.41,78.78,2.1,hold for revised offer\nCore,94.56,86.79,9.0,validate then consider expansion\nPremium,104.40,95.79,9.0,validate then consider expansion\n'); chart('aov_treatment_readout.svg','Average order value: treatment vs. matched control','Repair the flagged feed before any scale decision.', [('Control',ca,f'${ca:.1f}'),('Treatment',ta,f'${ta:.1f}')],'#146C94'); chart('segment_lift_readout.svg','Illustrative AOV lift by customer segment','Segment heterogeneity changes the recommended next action.', [('Value',2.1,'2.1%'),('Core',9.0,'9.0%'),('Premium',9.0,'9.0%')],'#B05A2A'); print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
