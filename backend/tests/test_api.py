"""Integration tests always use a disposable database, never athlete records."""
import os
import tempfile
import unittest
from pathlib import Path

temporary = tempfile.TemporaryDirectory()
os.environ['DATABASE_URL'] = f"sqlite:///{Path(temporary.name) / 'test.db'}"
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import engine

class TrackerTests(unittest.TestCase):
    def test_crud_and_stable_ids(self):
        payloads = {
            'training': dict(date='2026-10-10', session_type='Run', duration_minutes=30, rpe=6, notes='Easy'),
            'wellness': dict(date='2026-10-10', sleep_hours=7.5, sleep_quality=8, soreness=3, stress=4, pain=0),
            'pt': dict(date='2026-10-10', exercise='Heel raises', sets=3, reps=12, duration_minutes=10, pain=1),
        }
        with TestClient(app) as client:
            for resource, payload in payloads.items():
                with self.subTest(resource=resource):
                    first = client.post(f'/{resource}/', json=payload)
                    self.assertEqual(first.status_code, 201)
                    record = first.json()
                    second = client.post(f'/api/{resource}/', json=payload).json()
                    self.assertNotEqual(record['id'], second['id'])
                    self.assertEqual(client.get(f'/{resource}/{record["id"]}').json(), record)
                    self.assertIn(record, client.get(f'/api/{resource}/').json())
                    updated = client.put(f'/{resource}/{record["id"]}', json={**payload, 'notes':'Updated'})
                    self.assertEqual(updated.json()['id'], record['id'])
                    self.assertEqual(updated.json()['notes'], 'Updated')
                    self.assertEqual(client.delete(f'/{resource}/{record["id"]}').status_code, 204)
                    self.assertEqual(client.get(f'/{resource}/{record["id"]}').status_code, 404)
                    self.assertEqual(client.put(f'/{resource}/{record["id"]}', json=payload).status_code, 404)
                    self.assertEqual(client.delete(f'/{resource}/{record["id"]}').status_code, 404)
                    self.assertEqual(client.get(f'/{resource}/{second["id"]}').json()['id'], second['id'])
                    invalid = {**payload, 'date':'not-a-date'}
                    self.assertEqual(client.post(f'/{resource}/', json=invalid).status_code, 422)
            for change in ({'rpe':11}, {'duration_minutes':0}, {'session_type':'  '}):
                self.assertEqual(client.post('/training/', json={**payloads['training'], **change}).status_code,422)
            self.assertEqual(client.post('/wellness/',json={**payloads['wellness'],'sleep_hours':25}).status_code,422)
            self.assertEqual(client.post('/pt/',json={**payloads['pt'],'sets':0}).status_code,422)
        # A new app lifespan sees the same saved records.
        with TestClient(app) as client:
            self.assertEqual(len(client.get('/wellness/').json()),1)
            self.assertEqual(client.get('/health').json(), {'status':'ok'})

if __name__ == '__main__':
    try:
        unittest.main()
    finally:
        engine.dispose()
        temporary.cleanup()
