import {test} from 'node:test';
import assert from 'node:assert/strict';
import {dashboardMetrics} from './metrics.js';
test('Monday boundaries, future exclusion, duration × RPE and missing sleep',()=>{
 const data={training:[{date:'2026-10-04',duration_minutes:100,rpe:10},{date:'2026-10-05',duration_minutes:30,rpe:6},{date:'2026-10-10',duration_minutes:45,rpe:4},{date:'2026-10-11',duration_minutes:100,rpe:10}],wellness:[{date:'2026-10-05',sleep_hours:7,soreness:2,stress:4},{date:'2026-10-10',sleep_hours:9,soreness:4,stress:6}],pt:[]};
 const m=dashboardMetrics(data,'2026-10-10');assert.equal(m.load,360);assert.equal(m.duration,75);assert.equal(m.soreness,3);assert.equal(m.stress,5);assert.equal(m.days.length,14);assert.equal(m.days.at(-1).sleep,9);assert.equal(m.days.at(-2).sleep,null);
});
test('empty wellness is unknown, empty training is zero',()=>{const m=dashboardMetrics({training:[],wellness:[],pt:[]},'2026-10-10');assert.equal(m.soreness,null);assert.equal(m.load,0);});
