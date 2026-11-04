import os
import tempfile
import unittest
from fastapi.testclient import TestClient
from app.main import app


class FlowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.previous = os.environ.get('APF_DATA_DIR')
        os.environ['APF_DATA_DIR'] = self.tmp.name

    def tearDown(self):
        if self.previous is None:
            os.environ.pop('APF_DATA_DIR', None)
        else:
            os.environ['APF_DATA_DIR'] = self.previous
        self.tmp.cleanup()

    def test_review_survives_restart_and_cannot_be_repeated(self):
        with TestClient(app) as client:
            r = client.post('/api/tasks', json={'title':'Análisis', 'description':'Preparar un caso sintético'})
            self.assertEqual(r.status_code, 201, r.text)
            task = r.json()
            self.assertEqual(task['status'], 'proposed')
            self.assertTrue(task['awaiting_review'])
            self.assertIn('caso sintético', task['proposal'])
            task_id = task['id']
        with TestClient(app) as client:
            self.assertTrue(client.get('/api/tasks/' + task_id).json()['awaiting_review'])
            result = client.post('/api/tasks/' + task_id + '/review', json={'decision':'approve', 'note':'Conforme'})
            self.assertEqual(result.status_code, 200, result.text)
            self.assertEqual(result.json()['status'], 'integrated')
            self.assertEqual(result.json()['review_note'], 'Conforme')
            self.assertEqual(client.post('/api/tasks/' + task_id + '/review', json={'decision':'reject'}).status_code, 409)
        with TestClient(app) as client:
            self.assertEqual(client.get('/api/tasks/' + task_id).json()['status'], 'integrated')

    def test_reject_and_invalid_input(self):
        with TestClient(app) as client:
            self.assertEqual(client.post('/api/tasks', json={'title':' ', 'description':'a'}).status_code, 422)
            self.assertEqual(client.get('/api/tasks/no-existe').status_code, 404)
            task = client.post('/api/tasks', json={'title':'Tarea', 'description':'Texto'}).json()
            result = client.post('/api/tasks/' + task['id'] + '/review', json={'decision':'reject', 'note':'Rehacer'})
            self.assertEqual(result.status_code, 200, result.text)
            self.assertEqual(result.json()['status'], 'rejected')
            self.assertFalse(result.json()['awaiting_review'])
            self.assertEqual(result.json()['review_note'], 'Rehacer')
            self.assertEqual(len(client.get('/api/tasks').json()), 1)


if __name__ == '__main__':
    unittest.main()
