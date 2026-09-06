import json
from pathlib import Path
import argparse
import sys

class Generator:
    def __init__(self, mappings_file):
        with open(mappings_file, 'r', encoding='utf-8') as f:
            self.mappings = json.load(f)
        self.generated_code = ""
    
    def generate_from_ast(self, ast, target_lang, output_file):
        # Agregar la extensión correcta según el lenguaje
        extensions = {
            "python": ".py",
            "js": ".js",
            "rust": ".rs"
        }
        
        # Si output_file no tiene la extensión correcta, agregarla
        if not output_file.endswith(extensions[target_lang]):
            output_file = output_file + extensions[target_lang]
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if target_lang == "python":
            self._generate_python(ast)
        elif target_lang == "js":
            self._generate_javascript(ast)
        elif target_lang == "rust":
            self._generate_rust(ast)
        else:
            print(f"⚠️ Lenguaje '{target_lang}' no soportado")
            self._generate_python(ast)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(self.generated_code)
        
        print(f"✅ Código generado en {output_file}")
        return self.generated_code

    def _generate_python(self, ast):
        """Genera código Python REAL a partir del AST"""
        code_lines = []
        code_lines.append("# Código generado automáticamente a partir de C++")
        code_lines.append("# Generado por Esclarificador")
        code_lines.append("")
        
        # Imports necesarios
        imports = set()
        for ns in ast.get("namespaces", []):
            ns_name = ns["nombre"]
            if ns_name in self.mappings.get("std_namespaces", {}):
                python_module = self.mappings["std_namespaces"][ns_name].get("python", "")
                if python_module and python_module not in ["list", "dict"]:
                    imports.add(f"import {python_module}")
        
        if imports:
            for imp in sorted(imports):
                code_lines.append(imp)
            code_lines.append("")
        
        # Generar clases
        for abstraccion in ast.get("abstracciones", []):
            class_name = abstraccion["nombre"]
            desc = abstraccion.get("descripcion", "")
            python_name = self.mappings["abstracciones"][class_name].get("python", class_name)
            
            code_lines.append(f"class {python_name}:")
            code_lines.append(f'    """{desc}"""')
            code_lines.append("    ")
            
            # Constructor
            attributes = abstraccion.get("atributos", [])
            if attributes:
                code_lines.append("    def __init__(self):")
                for attr in attributes:
                    attr_name = attr["nombre"]
                    attr_type = attr.get("tipo_cpp", "")
                    python_type = self.mappings["tipos_datos"].get(attr_type, {}).get("python", "str")
                    
                    if python_type == "str":
                        default_val = '""'
                    elif python_type == "int":
                        default_val = "0"
                    elif python_type == "list":
                        default_val = "[]"
                    elif python_type == "dict":
                        default_val = "{}"
                    elif python_type == "bool":
                        default_val = "False"
                    else:
                        default_val = "None"
                    
                    code_lines.append(f"        self.{attr_name} = {default_val}  # {attr_type}")
                code_lines.append("")
            else:
                code_lines.append("    def __init__(self):")
                code_lines.append("        pass")
                code_lines.append("")
            
            # Métodos
            methods = abstraccion.get("metodos", [])
            for metodo in methods:
                method_name = metodo["nombre"]
                code_lines.append(f"    def {method_name}(self):")
                
                if method_name == "diagnosticar":
                    code_lines.append(f'        print("🔍 Diagnosticando {class_name}...")')
                    code_lines.append("        return True")
                elif method_name == "analizar":
                    code_lines.append('        print("📊 Analizando...")')
                    code_lines.append("        return self")
                elif method_name == "traducir":
                    code_lines.append('        print("🔄 Traduciendo...")')
                    code_lines.append('        return "TRADUCIDO"')
                elif method_name == "planificar":
                    code_lines.append('        print("📋 Planificando...")')
                    code_lines.append('        self.pasos = ["paso_1"]')
                    code_lines.append("        return self.pasos")
                elif method_name in ["ejecutar", "run"]:
                    code_lines.append('        print("⚡ Ejecutando...")')
                    code_lines.append("        return True")
                else:
                    code_lines.append(f'        print("▶️ Ejecutando {method_name}...")')
                
                code_lines.append("")
            
            code_lines.append("")
        
        # Función main
        if ast.get("abstracciones"):
            code_lines.append("def main():")
            code_lines.append('    print("🚀 Iniciando ejecución...")')
            code_lines.append('    print("="*40)')
            code_lines.append("")
            
            for abstraccion in ast.get("abstracciones", []):
                class_name = abstraccion["nombre"]
                python_name = self.mappings["abstracciones"][class_name].get("python", class_name)
                code_lines.append(f"    # Crear instancia de {python_name}")
                code_lines.append(f"    {class_name.lower()}_instance = {python_name}()")
                methods = abstraccion.get("metodos", [])
                if methods:
                    first_method = methods[0]["nombre"]
                    code_lines.append(f"    {class_name.lower()}_instance.{first_method}()")
                code_lines.append("")
            
            code_lines.append('    print("="*40)')
            code_lines.append('    print("✅ Ejecución completada")')
            code_lines.append("")
            code_lines.append("if __name__ == '__main__':")
            code_lines.append("    main()")
        
        self.generated_code = "\n".join(code_lines)

    def _generate_javascript(self, ast):
        """Genera código JavaScript REAL a partir del AST"""
        code_lines = []
        code_lines.append("// Código generado automáticamente a partir de C++")
        code_lines.append("// Generado por Esclarificador")
        code_lines.append("")
        
        for abstraccion in ast.get("abstracciones", []):
            class_name = abstraccion["nombre"]
            js_name = self.mappings["abstracciones"][class_name].get("js", class_name)
            desc = abstraccion.get("descripcion", "")
            
            code_lines.append(f"class {js_name} {{")
            code_lines.append(f"    /** {desc} */")
            
            attributes = abstraccion.get("atributos", [])
            if attributes:
                code_lines.append("    constructor() {")
                for attr in attributes:
                    attr_name = attr["nombre"]
                    js_type = attr.get("mapeos", {}).get("js", "string")
                    if js_type in ["Array", "Object"]:
                        default_val = "[]" if js_type == "Array" else "{}"
                    else:
                        default_val = '""' if js_type == "string" else "null"
                    code_lines.append(f"        this.{attr_name} = {default_val};")
                code_lines.append("    }")
            else:
                code_lines.append("    constructor() {")
                code_lines.append("        // Constructor vacío")
                code_lines.append("    }")
            
            methods = abstraccion.get("metodos", [])
            for metodo in methods:
                method_name = metodo["nombre"]
                code_lines.append("")
                code_lines.append(f"    {method_name}() {{")
                
                if method_name == "diagnosticar":
                    code_lines.append(f'        console.log("🔍 Diagnosticando {class_name}...");')
                    code_lines.append("        return true;")
                elif method_name == "analizar":
                    code_lines.append('        console.log("📊 Analizando...");')
                    code_lines.append("        return this;")
                elif method_name == "traducir":
                    code_lines.append('        console.log("🔄 Traduciendo...");')
                    code_lines.append('        return "TRADUCIDO";')
                elif method_name == "planificar":
                    code_lines.append('        console.log("📋 Planificando...");')
                    code_lines.append('        this.pasos = ["paso_1"];')
                    code_lines.append("        return this.pasos;")
                elif method_name in ["ejecutar", "run"]:
                    code_lines.append('        console.log("⚡ Ejecutando...");')
                    code_lines.append("        return true;")
                else:
                    code_lines.append(f'        console.log("▶️ Ejecutando {method_name}...");')
                
                code_lines.append("    }")
            
            code_lines.append("}")
            code_lines.append("")
        
        if ast.get("abstracciones"):
            code_lines.append("function main() {")
            code_lines.append('    console.log("🚀 Iniciando ejecución...");')
            code_lines.append('    console.log("=".repeat(40));')
            code_lines.append("")
            
            for abstraccion in ast.get("abstracciones", []):
                class_name = abstraccion["nombre"]
                js_name = self.mappings["abstracciones"][class_name].get("js", class_name)
                code_lines.append(f"    // Crear instancia de {js_name}")
                code_lines.append(f"    const {class_name.lower()}Instance = new {js_name}();")
                methods = abstraccion.get("metodos", [])
                if methods:
                    first_method = methods[0]["nombre"]
                    code_lines.append(f"    {class_name.lower()}Instance.{first_method}();")
                code_lines.append("")
            
            code_lines.append('    console.log("=".repeat(40));')
            code_lines.append('    console.log("✅ Ejecución completada");')
            code_lines.append("}")
            code_lines.append("")
            code_lines.append("main();")
        
        self.generated_code = "\n".join(code_lines)

    def _generate_rust(self, ast):
        """Genera código Rust REAL a partir del AST"""
        code_lines = []
        code_lines.append("// Código generado automáticamente a partir de C++")
        code_lines.append("// Generado por Esclarificador")
        code_lines.append("")
        
        # Imports
        imports = set()
        imports.add("use std::vec::Vec;")
        
        for ns in ast.get("namespaces", []):
            ns_name = ns["nombre"]
            if ns_name in self.mappings.get("std_namespaces", {}):
                rust_module = self.mappings["std_namespaces"][ns_name].get("rust", "")
                if rust_module and rust_module != "Vec":
                    if rust_module.startswith("std::"):
                        imports.add(f"use {rust_module};")
                    else:
                        imports.add(f"use std::{rust_module};")
        
        for imp in sorted(imports):
            code_lines.append(imp)
        code_lines.append("")
        
        # Structs
        for abstraccion in ast.get("abstracciones", []):
            class_name = abstraccion["nombre"]
            rust_name = self.mappings["abstracciones"][class_name].get("rust", class_name)
            desc = abstraccion.get("descripcion", "")
            
            code_lines.append(f"// {desc}")
            code_lines.append(f"struct {rust_name} {{")
            
            attributes = abstraccion.get("atributos", [])
            if attributes:
                for attr in attributes:
                    attr_name = attr["nombre"]
                    rust_type = self._map_rust_type(attr.get("tipo_cpp", ""))
                    code_lines.append(f"    {attr_name}: {rust_type},")
            else:
                code_lines.append("    // Sin atributos")
            
            code_lines.append("}")
            code_lines.append("")
            
            methods = abstraccion.get("metodos", [])
            if methods:
                code_lines.append(f"impl {rust_name} {{")
                
                if attributes:
                    code_lines.append(f"    fn new() -> Self {{")
                    code_lines.append(f"        Self {{")
                    for attr in attributes:
                        attr_name = attr["nombre"]
                        rust_type = self._map_rust_type(attr.get("tipo_cpp", ""))
                        default_val = self._get_rust_default(rust_type)
                        code_lines.append(f"            {attr_name}: {default_val},")
                    code_lines.append("        }")
                    code_lines.append("    }")
                else:
                    code_lines.append(f"    fn new() -> Self {{")
                    code_lines.append(f"        Self {{ }}")
                    code_lines.append("    }")
                code_lines.append("")
                
                for metodo in methods:
                    method_name = metodo["nombre"]
                    code_lines.append(f"    fn {method_name}(&self) {{")
                    
                    if method_name == "diagnosticar":
                        code_lines.append(f'        println!("🔍 Diagnosticando {{}}...", stringify!({rust_name}));')
                    elif method_name == "analizar":
                        code_lines.append('        println!("📊 Analizando...");')
                    elif method_name == "traducir":
                        code_lines.append('        println!("🔄 Traduciendo...");')
                    elif method_name == "planificar":
                        code_lines.append('        println!("📋 Planificando...");')
                    elif method_name in ["ejecutar", "run"]:
                        code_lines.append('        println!("⚡ Ejecutando...");')
                    else:
                        code_lines.append(f'        println!("▶️ Ejecutando {{}}...", "{method_name}");')
                    
                    code_lines.append("    }")
                    code_lines.append("")
                
                code_lines.append("}")
                code_lines.append("")
        
        # Main
        if ast.get("abstracciones"):
            code_lines.append("fn main() {")
            code_lines.append('    println!("🚀 Iniciando ejecución...");')
            code_lines.append('    println!("{}", "=".repeat(40));')
            code_lines.append("")
            
            for abstraccion in ast.get("abstracciones", []):
                class_name = abstraccion["nombre"]
                rust_name = self.mappings["abstracciones"][class_name].get("rust", class_name)
                code_lines.append(f"    // Crear instancia de {rust_name}")
                code_lines.append(f"    let {class_name.lower()}_instance = {rust_name}::new();")
                methods = abstraccion.get("metodos", [])
                if methods:
                    first_method = methods[0]["nombre"]
                    code_lines.append(f"    {class_name.lower()}_instance.{first_method}();")
                code_lines.append("")
            
            code_lines.append('    println!("{}", "=".repeat(40));')
            code_lines.append('    println!("✅ Ejecución completada");')
            code_lines.append("}")
        
        self.generated_code = "\n".join(code_lines)

    def _map_rust_type(self, cpp_type):
        """Mapea tipos de C++ a Rust"""
        type_map = {
            "string": "String",
            "std::string": "String",
            "int": "i32",
            "float": "f64",
            "bool": "bool",
            "vector": "Vec<String>",
            "std::vector": "Vec<String>",
        }
        return type_map.get(cpp_type, "String")

    def _get_rust_default(self, rust_type):
        """Obtiene valor por defecto para tipos Rust"""
        defaults = {
            "String": 'String::from("")',
            "i32": "0",
            "f64": "0.0",
            "bool": "false",
            "Vec<String>": "Vec::new()",
        }
        return defaults.get(rust_type, "Default::default()")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generador de código desde AST de C++')
    parser.add_argument("--abs_path", help="Ruta al archivo fuente C++", default="src/idea.cpp")
    parser.add_argument("--mappings", help="Ruta al archivo de mapeos JSON", default="config/mappings.json")
    parser.add_argument("--output", help="Ruta base de salida para el código generado (sin extensión)", default="output/generated/idea")
    parser.add_argument("--verbose", action="store_true", help="Mostrar información detallada")
    parser.add_argument("--lang", choices=["python", "js", "rust"], default="python", help="Lenguaje destino")
    
    args = parser.parse_args()

    # Verificar que el AST existe
    ast_file = "intermediate/ast.json"
    if not Path(ast_file).exists():
        print(f"❌ Error: No se encontró el archivo AST '{ast_file}'")
        print("💡 Ejecuta primero: python3 bridge/interpreter.py")
        sys.exit(1)

    # Cargar AST
    with open(ast_file, 'r', encoding='utf-8') as f:
        ast = json.load(f)

    if args.verbose:
        print(f"📁 Archivo AST: {ast_file}")
        print(f"📁 Archivo mappings: {args.mappings}")
        print(f"🎯 Lenguaje destino: {args.lang}")
        print(f"📁 Archivo salida base: {args.output}")

    # Generar código (la extensión se agrega automáticamente)
    generator = Generator(args.mappings)
    generator.generate_from_ast(ast, args.lang, args.output)
