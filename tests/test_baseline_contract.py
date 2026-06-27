import io
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASELINE_CHECKER = os.path.join(ROOT, "scripts", "check-baseline.py")
PYTHON3_PREFLIGHT = os.path.join(ROOT, "scripts", "check-python3.sh")


class BaselineContractTest(unittest.TestCase):

    def run_python3_preflight(self, python_command):
        env = dict(os.environ)
        env["PYTHON"] = python_command
        process = subprocess.Popen(
            ["sh", PYTHON3_PREFLIGHT],
            cwd=ROOT,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        stdout, stderr = process.communicate()
        return process.returncode, stdout, stderr

    def test_missing_python3_command_fails_closed(self):
        command = "gnip-python-command-that-does-not-exist"
        returncode, stdout, stderr = self.run_python3_preflight(command)

        self.assertNotEqual(0, returncode)
        self.assertEqual("", stdout)
        self.assertIn("Python command not found: %s" % command, stderr)

    def test_non_python3_command_fails_closed(self):
        returncode, stdout, stderr = self.run_python3_preflight("true")

        self.assertNotEqual(0, returncode)
        self.assertEqual("", stdout)
        self.assertIn("Python 3 is required: true", stderr)

    def test_absolute_makefile_path_with_spaces_runs_full_gate(self):
        if os.environ.get("GNIP_BASELINE_CONTRACT_CHILD") == "1":
            return

        temp_dir = tempfile.mkdtemp(prefix="gnip-make-space-contract-")
        try:
            copied_root = os.path.join(temp_dir, "repository with spaces")
            caller_root = os.path.join(temp_dir, "external caller")
            shutil.copytree(
                ROOT,
                copied_root,
                ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc", "*.pyo"),
            )
            os.mkdir(caller_root)

            env = dict(os.environ)
            env["GNIP_BASELINE_CONTRACT_CHILD"] = "1"
            process = subprocess.Popen(
                ["make", "-f", os.path.join(copied_root, "Makefile"), "check"],
                cwd=caller_root,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
            stdout, stderr = process.communicate()

            self.assertEqual(0, process.returncode, stderr)
            self.assertIn("GNIP light demo baseline checks passed.", stdout)
        finally:
            shutil.rmtree(temp_dir)

    def test_python2_probe_invokes_only_syntax_compilation(self):
        if os.environ.get("GNIP_BASELINE_CONTRACT_CHILD") == "1":
            return

        temp_dir = tempfile.mkdtemp(prefix="gnip-python2-contract-")
        try:
            invocation_log = os.path.join(temp_dir, "python2-invocations.log")
            fake_python2 = os.path.join(temp_dir, "python2")
            with io.open(fake_python2, "w", encoding="utf-8") as fake_file:
                fake_file.write(
                    "#!/bin/sh\n"
                    "case \"$2\" in\n"
                    "  *platform.python_implementation*)\n"
                    "    printf '2\\tFakePython\\t2.7.18'\n"
                    "    exit 0\n"
                    "    ;;\n"
                    "esac\n"
                    "case \"$2\" in\n"
                    "  *compile\\(open\\(filename*) invocation=syntax ;;\n"
                    "  *) invocation=other ;;\n"
                    "esac\n"
                    "printf '%s\\n' \"$invocation\" >> \"$GNIP_FAKE_PYTHON2_LOG\"\n"
                )
            os.chmod(fake_python2, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)

            env = dict(os.environ)
            env["GNIP_BASELINE_CONTRACT_CHILD"] = "1"
            env["GNIP_FAKE_PYTHON2_LOG"] = invocation_log
            env["PATH"] = temp_dir + os.pathsep + env.get("PATH", "")
            process = subprocess.Popen(
                [sys.executable, BASELINE_CHECKER],
                cwd=ROOT,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
            stdout, stderr = process.communicate()

            with io.open(invocation_log, "r", encoding="utf-8") as log_file:
                invocations = [line.strip() for line in log_file if line.strip()]

            self.assertEqual(0, process.returncode, stderr)
            self.assertIn(
                "Python 2 syntax compiler: %s (FakePython 2.7.18)" % fake_python2,
                stdout,
            )
            self.assertEqual(["syntax"], invocations)
        finally:
            shutil.rmtree(temp_dir)

    def test_python2_alias_to_python3_fails_closed(self):
        if os.environ.get("GNIP_BASELINE_CONTRACT_CHILD") == "1":
            return

        temp_dir = tempfile.mkdtemp(prefix="gnip-python2-major-contract-")
        try:
            fake_python2 = os.path.join(temp_dir, "python2")
            with io.open(fake_python2, "w", encoding="utf-8") as fake_file:
                fake_file.write(
                    "#!/bin/sh\n"
                    "printf '3\\tFakePython\\t3.14.0'\n"
                )
            os.chmod(fake_python2, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)

            env = dict(os.environ)
            env["GNIP_BASELINE_CONTRACT_CHILD"] = "1"
            env["PATH"] = temp_dir + os.pathsep + env.get("PATH", "")
            process = subprocess.Popen(
                [sys.executable, BASELINE_CHECKER],
                cwd=ROOT,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
            stdout, stderr = process.communicate()

            self.assertNotEqual(0, process.returncode)
            self.assertIn(
                "python2 command must identify itself as a Python 2 interpreter",
                stdout + stderr,
            )
        finally:
            shutil.rmtree(temp_dir)


if __name__ == "__main__":
    unittest.main()
