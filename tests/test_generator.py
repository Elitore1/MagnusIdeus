#!/usr/bin/env python3
import unittest
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "bridge"))

from generator import Generator

class TestGenerator(unittest.TestCase):
    def setUp(self):
        self.mappings_file = "config/mappings.json"
        self.generator = Generator(self.mappings_file)
        
        ast_file = "intermediate/ast.json"
        if not Path(ast_file).exists():
            interpreter_module = __import__("interpreter")
            interpreter_module.Interpreter(self.mappings_file).process_file(
                "src/idea.cpp", ast_file
            )
        with open(ast_file, 'r', encoding='utf-8') as f:
            self.ast = json.load(f)
    
    def test_generator_load(self):
        """Verificar que el generador se carga correctamente"""
        self.assertIsNotNone(self.generator.mappings)
    
    def test_python_generation(self):
        """Verificar que genera código Python"""
        if not self.ast["abstracciones"]:
            self.skipTest("No hay abstracciones para probar")
        
        code = self.generator.generate_from_ast(self.ast, "python", "/tmp/test.py")
        self.assertIsNotNone(code)
        self.assertIn("class", code)
    
    def test_js_generation(self):
        """Verificar que genera código JavaScript"""
        if not self.ast["abstracciones"]:
            self.skipTest("No hay abstracciones para probar")
        
        code = self.generator.generate_from_ast(self.ast, "js", "/tmp/test.js")
        self.assertIsNotNone(code)
        self.assertIn("class", code)
    
    def test_rust_generation(self):
        """Verificar que genera código Rust"""
        if not self.ast["abstracciones"]:
            self.skipTest("No hay abstracciones para probar")
        
        code = self.generator.generate_from_ast(self.ast, "rust", "/tmp/test.rs")
        self.assertIsNotNone(code)
        self.assertIn("struct", code)

if __name__ == "__main__":
    unittest.main()
