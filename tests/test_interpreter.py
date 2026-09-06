#!/usr/bin/env python3
import unittest
import json
import os
import sys
from pathlib import Path

# Agregar bridge al path
sys.path.insert(0, str(Path(__file__).parent.parent / "bridge"))

from interpreter import Interpreter

class TestInterpreter(unittest.TestCase):
    def setUp(self):
        self.mappings_file = "config/mappings.json"
        self.source_file = "src/idea.cpp"
        self.interpreter = Interpreter(self.mappings_file)
    
    def test_mappings_load(self):
        """Verificar que los mappings se cargan correctamente"""
        self.assertIsNotNone(self.interpreter.mappings)
        self.assertIn("abstracciones", self.interpreter.mappings)
        self.assertIn("Tanger", self.interpreter.mappings["abstracciones"])
    
    def test_source_reading(self):
        """Verificar que se puede leer el archivo fuente"""
        source = self.interpreter.read_source_file(self.source_file)
        self.assertIsNotNone(source)
        self.assertIn("Tanger", source)
    
    def test_token_extraction(self):
        """Verificar que se extraen tokens correctamente"""
        source = self.interpreter.read_source_file(self.source_file)
        tokens = self.interpreter.extract_tokens_from_cpp(source)
        self.assertGreater(len(tokens), 0)
        
        # Verificar que hay al menos una abstracción
        abstracciones = [t for t in tokens if t.get("tipo") == "abstraccion"]
        self.assertGreater(len(abstracciones), 0)
    
    def test_ast_generation(self):
        """Verificar que se genera el AST correctamente"""
        ast = self.interpreter.process_file(self.source_file)
        self.assertIsNotNone(ast)
        self.assertIn("abstracciones", ast)
        self.assertGreater(len(ast["abstracciones"]), 0)

    def test_unknown_classes_are_ignored(self):
        """Las clases fuera de mappings no deben entrar al AST."""
        source = "class Unknown { public: void run() {} };"
        tokens = self.interpreter.extract_tokens_from_cpp(source)
        self.assertEqual(
            [token for token in tokens if token.get("tipo") == "abstraccion"],
            []
        )

    def test_supported_includes_are_preserved(self):
        """Los includes configurados deben producir tokens de namespace."""
        source = "#include <chrono>\n#include <vector>\n"
        tokens = self.interpreter.extract_tokens_from_cpp(source)
        namespaces = {
            token["nombre"]
            for token in tokens
            if token.get("tipo") == "std_namespace"
        }
        self.assertEqual(namespaces, {"chrono", "vector"})

if __name__ == "__main__":
    unittest.main()
