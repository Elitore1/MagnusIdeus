import json
import re
from pathlib import Path
import sys

class Interpreter:
    def __init__(self, mappings_file):
        with open(mappings_file, 'r', encoding='utf-8') as f:
            self.mappings = json.load(f)
        self.ast = {
            "abstracciones": [],
            "namespaces": [],
            "tipos": [],
            "flujo": []
        }
        self.source_code = None
    
    def read_source_file(self, source_path):
        try:
            with open(source_path, 'r', encoding='utf-8') as f:
                self.source_code = f.read()
            print(f"✅ Archivo fuente leído: {source_path}")
            return self.source_code
        except FileNotFoundError:
            print(f"❌ Error: No se encontró el archivo '{source_path}'")
            return None
        except Exception as e:
            print(f"❌ Error al leer '{source_path}': {e}")
            return None
    
    def extract_tokens_from_cpp(self, source_code):
        tokens = []
        
        class_pattern = r'class\s+(\w+)\s*\{([^}]*)\}'
        for match in re.finditer(class_pattern, source_code, re.DOTALL):
            class_name = match.group(1)
            class_body = match.group(2)
            
            if class_name in self.mappings.get("abstracciones", {}):
                token = {
                    "tipo": "abstraccion",
                    "nombre": class_name,
                    "linea": source_code[:match.start()].count('\n') + 1
                }
                
                attributes = []
                attr_pattern = r'(\w+)\s+(\w+)\s*[;=]'
                for attr_match in re.finditer(attr_pattern, class_body):
                    attr_type = attr_match.group(1)
                    attr_name = attr_match.group(2)
                    if attr_type not in ['public', 'private', 'protected']:
                        attributes.append({
                            "nombre": attr_name,
                            "tipo": attr_type
                        })
                
                if attributes:
                    token["atributos"] = attributes
                
                methods = []
                method_pattern = r'(\w+)\s+(\w+)\s*\(([^)]*)\)'
                for method_match in re.finditer(method_pattern, class_body):
                    return_type = method_match.group(1)
                    method_name = method_match.group(2)
                    if return_type not in ['public', 'private', 'protected']:
                        methods.append(method_name)
                
                if methods:
                    token["metodos"] = methods
                
                tokens.append(token)
        
        std_pattern = r'#include\s*<(\w+)>'
        for match in re.finditer(std_pattern, source_code):
            namespace = match.group(1)
            if namespace in self.mappings.get("std_namespaces", {}):
                tokens.append({
                    "tipo": "std_namespace",
                    "nombre": namespace,
                    "linea": source_code[:match.start()].count('\n') + 1
                })
        
        Path("intermediate").mkdir(parents=True, exist_ok=True)
        with open("intermediate/tokens.json", "w", encoding='utf-8') as f:
            json.dump(tokens, f, indent=2, ensure_ascii=False)
        print(f"✅ Tokens guardados en intermediate/tokens.json")
        
        return tokens
    
    def interpret_tokens(self, tokens):
        self.ast = {
            "abstracciones": [],
            "namespaces": [],
            "tipos": [],
            "flujo": []
        }
        
        for token in tokens:
            if token.get("tipo") == "abstraccion":
                self._process_abstraccion(token)
            elif token.get("tipo") == "std_namespace":
                self._process_namespace(token)
            elif token.get("tipo") == "tipo_dato":
                self._process_tipo(token)
        
        return self.ast
    
    def _process_abstraccion(self, token):
        abstraccion_def = self.mappings["abstracciones"].get(token["nombre"])
        if not abstraccion_def:
            print(f"⚠️ Advertencia: Abstracción '{token['nombre']}' no encontrada")
            return
        
        ast_node = {
            "nombre": token["nombre"],
            "descripcion": abstraccion_def.get("descripcion", ""),
            "atributos": self._map_attributes(token.get("atributos", [])),
            "metodos": self._map_methods(token.get("metodos", [])),
            "mapeos_lenguajes": {
                "python": abstraccion_def.get("python", ""),
                "js": abstraccion_def.get("js", ""),
                "rust": abstraccion_def.get("rust", "")
            },
            "linea": token.get("linea", 0)
        }
        
        self.ast["abstracciones"].append(ast_node)
        self.ast["flujo"].append({
            "paso": len(self.ast["flujo"]) + 1,
            "tipo": "abstraccion",
            "nombre": token["nombre"],
            "linea": token.get("linea", 0)
        })
    
    def _process_namespace(self, token):
        ns_def = self.mappings["std_namespaces"].get(token["nombre"])
        if not ns_def:
            print(f"⚠️ Advertencia: Namespace '{token['nombre']}' no encontrado")
            return
        
        ast_node = {
            "nombre": token["nombre"],
            "descripcion": ns_def.get("descripcion", ""),
            "mapeos": {
                "python": ns_def.get("python", ""),
                "js": ns_def.get("js", ""),
                "rust": ns_def.get("rust", "")
            },
            "linea": token.get("linea", 0)
        }
        
        self.ast["namespaces"].append(ast_node)
    
    def _process_tipo(self, token):
        ast_node = {
            "tipo_cpp": token.get("tipo_cpp", ""),
            "mapeos": token.get("mapeos", {}),
            "linea": token.get("linea", 0)
        }
        
        self.ast["tipos"].append(ast_node)
    
    def _map_attributes(self, attributes):
        mapped = []
        for attr in attributes:
            tipo_cpp = attr.get("tipo", "")
            tipo_mapeo = self.mappings.get("tipos_datos", {}).get(tipo_cpp, {})
            
            mapped.append({
                "nombre": attr["nombre"],
                "tipo_cpp": tipo_cpp,
                "mapeos": tipo_mapeo
            })
        return mapped
    
    def _map_methods(self, methods):
        return [{"nombre": m} for m in methods]
    
    def process_file(self, source_path, output_file=None):
        source_code = self.read_source_file(source_path)
        if not source_code:
            return None
        
        tokens = self.extract_tokens_from_cpp(source_code)
        print(f"✅ Extraídos {len(tokens)} tokens")
        
        ast = self.interpret_tokens(tokens)
        
        if output_file:
            self.save_ast(output_file)
        
        return ast
    
    def save_ast(self, output_file):
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.ast, f, indent=2, ensure_ascii=False)
        print(f"✅ AST guardado en {output_file}")
    
    def load_ast(self, input_file):
        with open(input_file, 'r', encoding='utf-8') as f:
            self.ast = json.load(f)
        return self.ast
    
    def print_summary(self):
        """Imprime un resumen del AST - AHORA COMO MÉTODO DE CLASE"""
        print("\n" + "="*50)
        print("📊 RESUMEN DEL AST")
        print("="*50)
        print(f"📌 Abstracciones: {len(self.ast['abstracciones'])}")
        for abs in self.ast['abstracciones']:
            print(f"  - {abs['nombre']}: {abs.get('descripcion', 'Sin descripción')}")
            if abs.get('atributos'):
                print(f"    Atributos: {', '.join([a['nombre'] for a in abs['atributos']])}")
            if abs.get('metodos'):
                print(f"    Métodos: {', '.join([m['nombre'] for m in abs['metodos']])}")
        
        print(f"\n📌 Namespaces std: {len(self.ast['namespaces'])}")
        for ns in self.ast['namespaces']:
            print(f"  - {ns['nombre']} → Python: {ns['mapeos'].get('python', 'N/A')}")
        
        print(f"\n📌 Tipos de datos: {len(self.ast['tipos'])}")
        for tipo in self.ast['tipos']:
            print(f"  - {tipo.get('tipo_cpp', '')} → {tipo.get('mapeos', {}).get('python', 'N/A')}")
        
        print(f"\n📌 Flujo de ejecución: {len(self.ast['flujo'])} pasos")
        print("="*50)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Intérprete de código C++ a AST')
    parser.add_argument('--abs_path', help='Ruta al archivo fuente C++', default='src/idea.cpp')
    parser.add_argument('--mappings', help='Ruta al archivo de mapeos JSON', default='config/mappings.json')
    parser.add_argument('--output', help='Ruta de salida para el AST', default='intermediate/ast.json')
    parser.add_argument('--verbose', action='store_true', help='Mostrar información detallada')
    
    args = parser.parse_args()
    
    if not Path(args.abs_path).exists():
        print(f"❌ Error: No se encontró el archivo '{args.abs_path}'")
        sys.exit(1)
    
    if not Path(args.mappings).exists():
        print(f"❌ Error: No se encontró el archivo de mappings '{args.mappings}'")
        sys.exit(1)
    
    print("🚀 Iniciando interpretación...")
    print(f"📁 Archivo fuente: {args.abs_path}")
    print(f"📁 Archivo mappings: {args.mappings}")
    
    interpreter = Interpreter(args.mappings)
    ast = interpreter.process_file(args.abs_path, args.output)
    
    if ast:
        if args.verbose:
            interpreter.print_summary()
        else:
            print(f"\n✅ Interpretación completada exitosamente")
            print(f"📊 AST generado con {len(ast['abstracciones'])} abstracciones")
    else:
        print("❌ Error durante la interpretación")
        sys.exit(1)
