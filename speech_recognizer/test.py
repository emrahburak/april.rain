import unittest
import subprocess
import dataset
import os
from app import FileQueue


class TestFileQueue(unittest.TestCas):
    def __init__(self):
        self.args = subprocess.run(["python", "app.py", "güncelleme 18a.mp3", "test ses kaydi.mp3"])


    def setUp(self):
        self.file_queue = FileQueue()

    def test_populate_queue(self):
        self.file_queue.populate_queue()
        self.assertIsNotNone(self.file_queue.queue)

    def test_process_queue(self):
        self.file_queue.process_queue()
        self.assertNotEqual(self.file_queue.whole_text, '')


    def test_to_db(self):
        ...









