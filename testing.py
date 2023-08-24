import unittest
import json
from unittest.mock import patch
from app import app, wriylop

class TestApp(unittest.TestCase):

    @patch('app.YOLO')
    def test_wriylop(self, mock_yolo):
       
        mock_yolo_instance = mock_yolo.return_value
        mock_result = mock_yolo_instance.return_value
        mock_result.boxes.xyxy = [[10, 20, 30, 40]]
        mock_result.path = "z.jpg"

        
        mock_model = mock_yolo_instance.return_value
        mock_model.names = ["birds,cats,dogs,persons"]  

        # Perform testing
        with patch('app.model', return_value=mock_model):
            expected_json = {
                "Name": "z.jpg",
                "image_width": 269,  
                "image_height": 180,  
                "objects": [
                    
                ]
            }

            json_str = wriylop(mock_result)
            self.assertDictEqual(json.loads(json_str), expected_json)

if __name__ == '__main__':
    unittest.main()
