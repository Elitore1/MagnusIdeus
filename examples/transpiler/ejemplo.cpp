#include <iostream>
#include <memory>
#include <vector>

class Ser {
public:
    // Método puro virtual: Ser es un molde abstracto (no ocupa memoria por sí mismo)
    virtual void actuar() const = 0;
    virtual ~Ser() = default; // destructor virtual para polimorfismo seguro
};

class Humano : public Ser {
    std::string nombre;
public:
    Humano(std::string n) : nombre(std::move(n)) {}
    void actuar() const override { // sobrescritura: redefine comportamiento heredado
        std::cout << nombre << " piensa y siente.\n";
    }
};

class Robot : public Ser {
    std::string id;
public:
    Robot(std::string i) : id(std::move(i)) {}
    void actuar() const override {
        std::cout << "Robot " << id << " ejecuta instrucciones.\n";
    }
};

int main() {
    // Instancias concretas: ocupan memoria
    std::vector<std::unique_ptr<Ser>> seres;
    seres.emplace_back(std::make_unique<Humano>("Ari"));
    seres.emplace_back(std::make_unique<Robot>("R2"));

    // Polimorfismo: tratamos todos como Ser*, pero se ejecuta la implementación concreta
    for (const auto& s : seres) s->actuar();

    return 0;
}
