import {test} from 'node:test';
import assert from 'node:assert/strict';
import {fetchWhoopRecovery} from './whoop.js';
const sample={date:'2026-10-11T14:36:29.761Z',recovery_score:82,hrv_rmssd_milli:146.68684,resting_heart_rate:58,spo2_percentage:96.68421,skin_temp_celsius:33.919};
function mock(t,body,status=200){t.mock.method(globalThis,'fetch',async()=>new Response(JSON.stringify(body),{status}));}
test('fetches the same-origin endpoint and whitelists metric fields',async t=>{mock(t,{...sample,access_token:'must-not-be-returned'});assert.deepEqual(await fetchWhoopRecovery(),sample);assert.equal(fetch.mock.calls[0].arguments[0],'/api/whoop/recovery');assert.equal(fetch.mock.calls[0].arguments[1].cache,'no-store');});
for(const [detail,kind] of [['WHOOP is not connected','disconnected'],['WHOOP access token is missing','disconnected'],['WHOOP access token expired; refresh is needed','expired'],['Unauthorized','expired']]) test(detail,async t=>{mock(t,{detail},401);await assert.rejects(fetchWhoopRecovery(),e=>e.kind===kind);});
test('empty recovery response',async t=>{mock(t,{message:'No WHOOP recovery data available'});assert.equal(await fetchWhoopRecovery(),null);});
test('partial data preserves zero and marks missing or invalid values unavailable',async t=>{mock(t,{recovery_score:0,date:'invalid',hrv_rmssd_milli:'12'});assert.deepEqual(await fetchWhoopRecovery(),{date:null,recovery_score:0,hrv_rmssd_milli:null,resting_heart_rate:null,spo2_percentage:null,skin_temp_celsius:null});});
test('upstream failures expose no raw error details',async t=>{mock(t,{detail:'private upstream information'},502);await assert.rejects(fetchWhoopRecovery(),e=>e.kind==='error'&&!e.message.includes('private'));});
test('HTML and malformed payloads fail safely',async t=>{t.mock.method(globalThis,'fetch',async()=>new Response('<html>wrong route</html>'));await assert.rejects(fetchWhoopRecovery(),e=>e.kind==='error');});
test('network failures are recoverable errors',async t=>{t.mock.method(globalThis,'fetch',async()=>{throw new TypeError('Failed to fetch')});await assert.rejects(fetchWhoopRecovery(),e=>e.kind==='error');});
test('unmount cancellation propagates without retry',async t=>{t.mock.method(globalThis,'fetch',async(_url,{signal})=>{signal.throwIfAborted()});const controller=new AbortController();controller.abort();await assert.rejects(fetchWhoopRecovery({signal:controller.signal}),e=>e.name==='AbortError');assert.equal(fetch.mock.calls.length,1);});
