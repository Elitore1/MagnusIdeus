import json
import re
from pathlib import Path

class Tokenizer:
    def __init__(self, mappings_file):
        with open(mappings_file) as f:
            self.mappings = json.load(f)
        self.tokens = []
    
    def extract_from_cpp(self, cpp_code):
        """Extrae abstracciones y std namespaces de C++"""
        self.tokens = []
        
        # 1. Extraer clases (abstracciones)
        class_pattern = r"class\s+(\w+)\s*\{([^}]*)\}"
        for match in re.finditer(class_pattern, cpp_code, re.DOTALL):
            class_name = match.group(1)
            class_body = match.group(2)
            
            if class_name in self.mappings["abstracciones"]:
                self.tokens.append({
                    "tipo": "abstraccion",
                    "nombre": class_name,
                    "atributos": self._extract_attributes(class_body),
                    "metodos": self._extract_methods(class_body)
                })
        
        # 2. Extraer std namespaces
        std_pattern = r"std::(\w+)"
        for match in re.finditer(std_pattern, cpp_code):
            ns = match.group(1)
            if ns in self.mappings["std_namespaces"]:
                self.tokens.append({
                    "tipo": "std_namespace",
                    "nombre": ns,
                    "mapeos": self.mappings["std_namespaces"][ns]
                })
        
        # 3. Extraer tipos de datos
        self._extract_types(cpp_code)
        
        return self.tokens
    
    def _extract_attributes(self, class_body):
        """Extrae atributos de la clase"""
        attr_pattern = r"(\w+)\s+(\w+)\s*[=;]"
        attributes = []
        for match in re.finditer(attr_pattern, class_body):
            tipo = match.group(1)
            nombre = match.group(2)
            attributes.append({"nombre": nombre, "tipo": tipo})
        return attributes
    
    def _extract_methods(self, class_body):
        """Extrae métodos de la clase"""
        method_pattern = r"void\s+(\w+)\s*\([^)]*\)"
        methods = []
        for match in re.finditer(method_pattern, class_body):
            methods.append(match.group(1))
        return methods
    
    def _extract_types(self, cpp_code):
        """Extrae tipos de datos usados"""
        for cpp_type, mappings in self.mappings["tipos_datos"].items():
            if cpp_type in cpp_code:
                self.tokens.append({
                    "tipo": "tipo_dato",
                    "cpp": cpp_type,
                    "mapeos": mappings
                })
    
    def save_tokens(self, output_file):
        """Guarda tokens en JSON"""
        with open(output_file, "w") as f:
            json.dump(self.tokens, f, indent=2)
        print(f"✓ Tokens guardados en {output_file}")
    
    def load_tokens(self, input_file):
        """Carga tokens desde JSON"""
        with open(input_file) as f:
            self.tokens = json.load(f)
        return self.tokens


# Uso independiente
if __name__ == "__main__":
    tokenizer = Tokenizer("config/mappings.json")
    
    with open("src/idea.cpp") as f:
        cpp_code = f.read()
    
    tokens = tokenizer.extract_from_cpp(cpp_code)
    tokenizer.save_tokens("intermediate/tokens.json")
    
    print(f"✓ Tokens extraídos: {len(tokens)}")
