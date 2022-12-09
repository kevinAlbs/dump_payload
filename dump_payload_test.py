import unittest
import base64
import dump_payload
from io import StringIO
import os
import sys

class TestDump (unittest.TestCase):
    def __init__ (self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName)
        if os.environ.get("REGENERATE_GOLDEN_FILES", None) == "1":
            self.regenGolden = True
            print ("Regenerating golden files")

    def test_dump1 (self):
        with open ("testdata/payload1.b64", "r") as file:
            contents = file.read()
        data = base64.b64decode(contents)
        # Capture stdout.
        capture = StringIO()
        old_stdout = sys.stdout
        sys.stdout = capture
        dump_payload.dump_payload1or2 (data)
        got = capture.getvalue()
        # Restore stdout
        sys.stdout = old_stdout
        if "REGENERATE_GOLDEN_FILES" in os.environ:
            with open ("testdata/payload1.golden", "w") as file:
                file.write(got)
        else:
            with open ("testdata/payload1.golden", "r") as file:
                golden = file.read()
                self.assertEqual (got, golden)

if __name__ == "__main__":
    unittest.main()
