import unittest
import base64
import dump_payload
from io import StringIO
import os
import sys


class TestDump (unittest.TestCase):
    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName)
        if os.environ.get("REGENERATE_GOLDEN_FILES", None) == "1":
            self.regenGolden = True
            print("Regenerating golden files")

    def test_dump(self):
        filenames = [
            "payload0",
            "payload1",
            "payload2",
            "payload3",
            "payload4",
            "payload5",
            "payload6",
            "payload7",
            "payload9",
        ]
        for filename in filenames:
            with open(f"testdata/{filename}.b64", "r") as file:
                contents = file.read()
            # Capture stdout.
            capture = StringIO()
            old_stdout = sys.stdout
            sys.stdout = capture
            dump_payload.dump_payload(contents)
            got = capture.getvalue()
            # Restore stdout
            sys.stdout = old_stdout
            if "REGENERATE_GOLDEN_FILES" in os.environ:
                with open(f"testdata/{filename}.golden", "w") as file:
                    file.write(got)
            else:
                with open(f"testdata/{filename}.golden", "r") as file:
                    golden = file.read()
                    self.assertEqual(
                        got, golden, msg=f"Failed to match: {filename}")


if __name__ == "__main__":
    unittest.main()
