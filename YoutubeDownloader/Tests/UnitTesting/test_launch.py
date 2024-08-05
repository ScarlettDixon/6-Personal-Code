import os
import sys
import unittest
from pathlib import Path
from typing import TYPE_CHECKING


main_directory = Path(__file__).parents[2]
main_file = main_directory / "Scripts"
yaml_path = main_directory / "Configuration" / "Settings.yml"
sys.path.append(str(main_file))
#print(sys.path)

if TYPE_CHECKING:
    from .Scripts import launch
else:
#    import __main__ as MainScript
    import launch
    from launch import include_files 

with open(yaml_path, "r") as file:
    yaml_vars=yaml.safe_load(file)

class LaunchTest(unittest.TestCase):
    def setUp(self):
        self.link=yaml_vars['TESTING']['LINK'] 
        self.playlist=yaml_vars['TESTING']['PLAYLIST']
        self.error_file=yaml_vars['TESTING']['ERROR_FILE']
        self.error_file_location=main_directory / self.error_file
        self.audio_convert=yaml_vars['TESTING']['AUDIO_CONVERT']
        self.audio_convert_location= main_directory / self.audio_convert

        print("---Setup Completed---")

    def tearDown(self):
        print("---TearDown Completed---")

    def test_link_exists(self):
        #print("---Test 1 ---")
        self.assertIsNotNone(self.link)
    
    def test_playlist_exists(self):        
        self.assertIsNotNone(self.playlist)

    def test_error_file_exists(self):        
        self.assertIsNotNone(self.error_file)

    def test_error_file_file(self):
        self.assertTrue(os.path.isfile(self.error_file_location))

    def test_audio_convert_exists(self):        
        self.assertIsNotNone(self.audio_convert)

    def test_audio_convert_file(self):
        self.assertTrue(os.path.isfile(self.audio_convert_location))

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_test(self):
        print(f"Test 1")

def test_all():
    unittest.main()

def test_suite_link():
    suite_link=unittest.TestSuite()
    suite_link.addTest()
    return suite_link


if __name__ == '__main__':
    runner=unittest.TextTestResult()
    runner.run(test_suite_link())
    #test_all()
    


# Test case: An individual unit of testing. It examines the output for a given input set.
# Test suite: A collection of test cases, test suites, or both. They’re grouped and executed as a whole.
# Test fixture: A group of actions required to set up an environment for testing. It also includes the teardown processes after the tests run.
# Test runner: A component that handles the execution of tests and communicates the results to the user.
