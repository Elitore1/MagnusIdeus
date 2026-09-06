#include <iostream>
#include <chrono>
#include <vector>

// Abstracción: Tanger (Problema)
class Tanger {
public:
    std::string problema = "renderizado_3d";
    void diagnosticar() { std::cout << "Problema identificado\n"; }
};

// Abstracción: Espejo (Análisis)
class Espejo {
public:
    void analizar(Tanger& t) { std::cout << "Analizando: " << t.problema << "\n"; }
};

// Abstracción: Modulus (Puente)
class Modulus {
public:
    std::string traducir(const std::string& idea) {
        return "TRADUCIDO:" + idea;
    }
};

// Abstracción: Cayo (Planificación)
class Cayo {
public:
    std::vector<std::string> pasos;
    void planificar() { pasos.push_back("paso_1"); }
};

// Abstracción: Barca (Ejecución)
class Barca {
public:
    void ejecutar() { std::cout << "Ejecutando...\n"; }
};
