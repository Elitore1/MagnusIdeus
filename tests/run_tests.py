#!/usr/bin/env python3
import unittest
import sys
from pathlib import Path

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

# Importar tests
from test_interpreter import TestInterpreter
from test_generator import TestGenerator
from test_pipeline import TestPipeline

if __name__ == "__main__":
    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestInterpreter))
    suite.addTests(loader.loadTestsFromTestCase(TestGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestPipeline))
    
    # Ejecutar
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Salir con código apropiado
    sys.exit(0 if result.wasSuccessful() else 1)
