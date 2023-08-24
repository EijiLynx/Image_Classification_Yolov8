import unittest
from app import app

class TestIntegration(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_upload_and_classify(self):
        # Simulating image upload and classification
        image_path = 'z.jpg'  # Replace with your test image path
        response = self.app.post('/upload', data={'image': (open(image_path, 'rb'), 'z.jpg')})
        data = response.get_json()
        
        # Check if the response contains the expected keys
        self.assertIn('predictions', data)
        
        # Checking if the predictions are in the expected format
        predictions = data['predictions']
        self.assertTrue(isinstance(predictions, list))
        self.assertTrue(all(isinstance(p, list) and len(p) == 2 for p in predictions))
        
        # Checking if the image filename and predictions match
        for filename, preds in predictions:
            self.assertEqual(filename, 'z.jpg')
            self.assertTrue(isinstance(preds, list))
            # Add more checks for individual predictions if needed

class TestSystem(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_end_to_end_workflow(self):
        # Simulating the entire end-to-end workflow
        image_path = 'z.jpg'  # Replace with your test image path
        
        # Upload and classify image
        response = self.app.post('/upload', data={'image': (open(image_path, 'rb'), 'z.jpg')})
        data = response.get_json()
        
        # Checking if the response contains the expected keys
        self.assertIn('predictions', data)
        
        # Checking if the predictions are in the expected format
        predictions = data['predictions']
        self.assertTrue(isinstance(predictions, list))
        self.assertTrue(all(isinstance(p, list) and len(p) == 2 for p in predictions))
        
        
        
        # Checking if the results page displays correctly
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        

if __name__ == '__main__':
    unittest.main()
