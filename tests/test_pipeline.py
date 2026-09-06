#!/usr/bin/env python3
import unittest
import subprocess
import json
import sys
from pathlib import Path

class TestPipeline(unittest.TestCase):
    def test_interpreter_runs(self):
        """Verificar que el intérprete se ejecuta sin errores"""
        result = subprocess.run(
            ["python3", "bridge/interpreter.py"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        self.assertEqual(result.returncode, 0, f"Error: {result.stderr}")
    
    def test_generator_python_runs(self):
        """Verificar que el generador Python se ejecuta sin errores"""
        result = subprocess.run(
            ["python3", "bridge/generator.py", "--lang", "python"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        self.assertEqual(result.returncode, 0, f"Error: {result.stderr}")
    
    def test_generated_python_executes(self):
        """Verificar que el código Python generado se ejecuta"""
        result = subprocess.run(
            ["python3", "output/generated/idea.py"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        self.assertEqual(result.returncode, 0, f"Error: {result.stderr}")
    
    def test_ast_json_generated(self):
        """Verificar que se genera ast.json"""
        ast_file = Path(__file__).parent.parent / "intermediate" / "ast.json"
        self.assertTrue(ast_file.exists(), "ast.json no fue generado")
        
        with open(ast_file, 'r') as f:
            data = json.load(f)
            self.assertIn("abstracciones", data)
            self.assertGreater(len(data["abstracciones"]), 0)

if __name__ == "__main__":
    unittest.main()
