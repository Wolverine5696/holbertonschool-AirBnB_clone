#!/usr/bin/python3
import unittest
import os
import json
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


class TestFileStorage(unittest.TestCase):
    """Test FileStorage class"""
    def setUp(self):
        self.file_storage = FileStorage()
        self.file_path = FileStorage._FileStorage__file_path

    def test_all(self):
        """Test all method"""
        obj = BaseModel()
        self.file_storage.new(obj)
        objects = self.file_storage.all()
        self.assertIsInstance(objects, dict)
        self.assertEqual(obj, objects["BaseModel.{}".format(obj.id)])

    def test_new(self):
        """Test new method"""
        obj = BaseModel()
        self.file_storage.new(obj)
        objects = self.file_storage.all()
        self.assertEqual(obj, objects["BaseModel.{}".format(obj.id)])

    def test_save(self):
        """Test save method"""
        obj = BaseModel()
        self.file_storage.new(obj)
        self.file_storage.save()
        with open(self.file_path, "r") as file:
            file_content = json.load(file)
        self.assertEqual(obj.to_dict(),
                         file_content["BaseModel.{}".format(obj.id)])

    def test_reload(self):
        """Test reload method"""
        obj = BaseModel()
        self.file_storage.new(obj)
        self.file_storage.save()
        self.file_storage__objects = {}
        self.file_storage.reload()
        objects = self.file_storage.all()
        self.assertEqual(obj.to_dict(),
                         objects["BaseModel.{}".format(obj.id)].to_dict())

    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)


if __name__ == "__main__":
    unittest.main()
