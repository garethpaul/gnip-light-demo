import io
import os
import unittest


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class BaselineContractTest(unittest.TestCase):

    def test_python2_verification_is_syntax_only(self):
        checker_path = os.path.join(ROOT, "scripts", "check-baseline.py")
        with io.open(checker_path, "r", encoding="utf-8") as checker_file:
            checker = checker_file.read()

        self.assertIn('[python2, "-c", syntax_check] + py_files', checker)
        self.assertNotIn('[python2, "-m", "unittest"', checker)


if __name__ == "__main__":
    unittest.main()
