#!/usr/bin/env python3
"""
Esclarificador - Transpilador de C++ a Python, JavaScript y Rust
Punto de entrada unificado con LOGGING COMPLETO
"""

import sys
import argparse
from pathlib import Path
import subprocess
import json
import datetime

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

from interpreter import Interpreter
from generator import Generator

class Esclarificador:
    def __init__(self):
        self.source_file = "src/idea.cpp"
        self.mappings_file = "config/mappings.json"
        self.ast_file = "intermediate/ast.json"
        self.output_base = "output/generated/idea"
        self.log_file = "output/logs.txt"
        
        # Asegurar que el directorio de logs existe
        Path(self.log_file).parent.mkdir(parents=True, exist_ok=True)
        
        # TRUNCAR LOG AL INICIAR (nuevo)
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [INFO] === NUEVA EJECUCIÓN ===\n")
            f.write(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [INFO] Logs limpiados al inicio\n")
    
    def log(self, message, level="INFO"):
        """Registra un mensaje con timestamp en el archivo de logs"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        
        # Escribir en archivo (append)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + "\n")
        
        # También mostrar en consola (con formato)
        if level == "STEP":
            print(f"\n📌 {message}")
        elif level == "OK":
            print(f"  ✅ {message}")
        elif level == "ERROR":
            print(f"  ❌ {message}")
        elif level == "WARNING":
            print(f"  ⚠️ {message}")
        else:
            print(f"  📝 {message}")
    
    def interpret(self, verbose=False):
        """Paso 1: Interpretar C++ a AST"""
        self.log("📖 Iniciando interpretación...", "STEP")
        self.log(f"   Archivo fuente: {self.source_file}", "INFO")
        self.log(f"   Archivo mappings: {self.mappings_file}", "INFO")
        
        interpreter = Interpreter(self.mappings_file)
        ast = interpreter.process_file(self.source_file, self.ast_file)
        
        if ast:
            self.log(f"✅ AST generado con {len(ast['abstracciones'])} abstracciones", "OK")
            if verbose:
                # Capturar la salida de print_summary
                print("\n📊 Resumen detallado del AST:")
                interpreter.print_summary()
        else:
            self.log("❌ Error al generar AST", "ERROR")
        
        return ast
    
    def generate(self, lang, verbose=False):
        """Paso 2: Generar código en el lenguaje especificado"""
        self.log(f"🔧 Generando código {lang}...", "STEP")
        
        # Cargar AST
        with open(self.ast_file, 'r', encoding='utf-8') as f:
            ast = json.load(f)
        
        # Generar
        generator = Generator(self.mappings_file)
        output_file = f"{self.output_base}.{self._get_extension(lang)}"
        generator.generate_from_ast(ast, lang, output_file)
        
        self.log(f"✅ Código {lang} generado en {output_file}", "OK")
        if verbose:
            # Mostrar primeras líneas del código generado
            with open(output_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()[:5]
                self.log(f"   Primeras líneas de {lang}:", "INFO")
                for line in lines:
                    self.log(f"     {line.rstrip()}", "INFO")
        
        return output_file
    
    def _get_extension(self, lang):
        extensions = {
            "python": "py",
            "js": "js",
            "rust": "rs"
        }
        return extensions.get(lang, "txt")
    
    def compile_rust(self, verbose=False):
        """Paso 3: Compilar Rust"""
        self.log("🦀 Compilando Rust...", "STEP")
        
        rs_file = f"{self.output_base}.rs"
        bin_file = self.output_base
        
        result = subprocess.run(
            ["rustc", rs_file, "-o", bin_file],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            self.log(f"✅ Binario generado: {bin_file}", "OK")
            if verbose:
                self.log(f"   Tamaño: {Path(bin_file).stat().st_size} bytes", "INFO")
            return True
        else:
            self.log(f"⚠️ Advertencias en compilación", "WARNING")
            if result.stderr:
                for line in result.stderr.split('\n'):
                    if 'warning:' in line:
                        self.log(f"   {line.strip()}", "WARNING")
            return False
    
    def run_pipeline(self, langs=None, verbose=False):
        """Ejecuta el pipeline completo con logging"""
        self.log("", "INFO")
        self.log("="*50, "INFO")
        self.log("🚀 ESCLARIFICADOR - PIPELINE COMPLETO", "STEP")
        self.log("="*50, "INFO")
        self.log(f"📅 Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", "INFO")
        self.log(f"🔧 Lenguajes a generar: {', '.join(langs) if langs else 'python, js, rust'}", "INFO")
        
        # Paso 1: Interpretar
        self.log("", "INFO")
        self.log("📖 PASO 1: Interpretando C++...", "STEP")
        self.interpret(verbose)
        
        # Paso 2: Generar
        if langs is None:
            langs = ["python", "js", "rust"]
        
        self.log("", "INFO")
        self.log("🔧 PASO 2: Generando código...", "STEP")
        for lang in langs:
            self.generate(lang, verbose)
        
        # Paso 3: Compilar Rust
        if "rust" in langs:
            self.log("", "INFO")
            self.log("🦀 PASO 3: Compilando Rust...", "STEP")
            self.compile_rust(verbose)
        
        # Paso 4: Ejecutar ejemplos
        self.log("", "INFO")
        self.log("▶️ PASO 4: Ejecutando ejemplos:", "STEP")
        self.log("-"*40, "INFO")
        
        # Python
        if "python" in langs and Path(f"{self.output_base}.py").exists():
            self.log("🐍 Ejecutando Python...", "STEP")
            result = subprocess.run(["python3", f"{self.output_base}.py"], capture_output=False)
            self.log(f"   Python exit code: {result.returncode}", "INFO")
        
        # Rust
        if "rust" in langs and Path(self.output_base).exists():
            self.log("🦀 Ejecutando Rust...", "STEP")
            result = subprocess.run([self.output_base], capture_output=False)
            self.log(f"   Rust exit code: {result.returncode}", "INFO")
        
        # JavaScript
        if "js" in langs and Path(f"{self.output_base}.js").exists():
            self.log("📜 Ejecutando JavaScript...", "STEP")
            result = subprocess.run(["node", f"{self.output_base}.js"], capture_output=True, text=True)
            if result.returncode == 0:
                self.log(f"   JavaScript exit code: {result.returncode}", "INFO")
            else:
                self.log("⚠️ Node.js no disponible o error al ejecutar", "WARNING")
        
        self.log("", "INFO")
        self.log("="*50, "INFO")
        self.log("✅ ¡Pipeline completado exitosamente!", "OK")
        self.log("="*50, "INFO")


def main():
    parser = argparse.ArgumentParser(
        description="Esclarificador - Transpilador de C++ a múltiples lenguajes"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Comando a ejecutar")
    
    interpret_parser = subparsers.add_parser("interpret", help="Interpretar C++ a AST")
    interpret_parser.add_argument("--verbose", "-v", action="store_true", help="Mostrar detalles")
    
    generate_parser = subparsers.add_parser("generate", help="Generar código")
    generate_parser.add_argument("--lang", choices=["python", "js", "rust"], default="python", help="Lenguaje destino")
    generate_parser.add_argument("--verbose", "-v", action="store_true", help="Mostrar detalles")
    
    compile_parser = subparsers.add_parser("compile", help="Compilar Rust")
    compile_parser.add_argument("--verbose", "-v", action="store_true", help="Mostrar detalles")
    
    run_parser = subparsers.add_parser("run", help="Ejecutar pipeline completo")
    run_parser.add_argument("--langs", nargs="+", choices=["python", "js", "rust"], default=["python", "js", "rust"], help="Lenguajes a generar")
    run_parser.add_argument("--verbose", "-v", action="store_true", help="Mostrar detalles")
    
    clean_parser = subparsers.add_parser("clean", help="Limpiar archivos generados")
    
    args = parser.parse_args()
    
    esclarificador = Esclarificador()
    
    if args.command == "interpret":
        esclarificador.interpret(args.verbose)
    
    elif args.command == "generate":
        esclarificador.generate(args.lang, args.verbose)
    
    elif args.command == "compile":
        esclarificador.compile_rust(args.verbose)
    
    elif args.command == "run":
        esclarificador.run_pipeline(args.langs, args.verbose)
    
    elif args.command == "clean":
        print("🧹 Limpiando archivos generados...")
        import shutil
        for path in ["intermediate", "output/generated"]:
            if Path(path).exists():
                shutil.rmtree(path)
                print(f"  ✅ Eliminado: {path}")
        Path("intermediate").mkdir(exist_ok=True)
        Path("output/generated").mkdir(parents=True, exist_ok=True)
        
        # Limpiar logs
        if Path(esclarificador.log_file).exists():
            with open(esclarificador.log_file, 'w', encoding='utf-8') as f:
                f.write(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [INFO] Logs limpiados por comando clean\n")
            print(f"  ✅ Logs limpiados")
        print("✅ Limpieza completada")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
