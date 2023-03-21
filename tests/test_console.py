import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models.engine.file_storage import FileStorage

class TestCreateCommand(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.console = HBNBCommand()
        cls.mock_stdout = StringIO()

    def setUp(self):
        FileStorage._FileStorage__objects = {}
        self.console = TestCreateCommand.console
        self.stdout = TestCreateCommand.mock_stdout
        self.patcher = patch('sys.stdout', self.stdout)
        self.patcher.start()

    def tearDown(self):
        self.stdout.seek(0)
        self.stdout.truncate(0)
        self.patcher.stop()

    def test_create_with_params(self):
        # Test creating a new User instance with parameters
        self.console.onecmd("create User email=\"test@example.com\" password=\"test123\" age=30")
        result = self.stdout.getvalue().strip()
        self.assertTrue(len(result) == 36)

    def test_create_with_string_param(self):
        # Test creating a new Place instance with a string parameter
        self.console.onecmd('create Place name="My_little_house" city="San Francisco"')
        result = self.stdout.getvalue().strip()
        self.assertTrue(len(result) == 36)

    def test_create_with_float_param(self):
        # Test creating a new Place instance with a float parameter
        self.console.onecmd("create Place price=100.50 latitude=37.77")
        result = self.stdout.getvalue().strip()
        self.assertTrue(len(result) == 36)

    def test_create_with_invalid_params(self):
        # Test creating a new Place instance with invalid parameters
        self.console.onecmd("create Place city=\"San Francisco\" price=\"not a number\"")
        result = self.stdout.getvalue().strip()
        self.assertTrue(len(result) == 36)

    def test_create_missing_class(self):
        # Test creating an instance with missing class name
        self.console.onecmd("create")
        result = self.stdout.getvalue().strip()
        self.assertEqual(result, "** class name missing **")

    def test_create_invalid_class(self):
        # Test creating an instance with invalid class name
        self.console.onecmd("create SomeClass")
        result = self.stdout.getvalue().strip()
        self.assertEqual(result, "** class doesn't exist **")

