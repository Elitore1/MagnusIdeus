from abc import ABC, abstractmethod

class Ser(ABC):
    @abstractmethod
    def actuar(self):
        pass

class Humano(Ser):
    def __init__(self, nombre):
        self.nombre = nombre
    def actuar(self):
        print(f"{self.nombre} piensa y siente.")

class Robot(Ser):
    def __init__(self, id):
        self.id = id
    def actuar(self):
        print(f"Robot {self.id} ejecuta instrucciones.")

def main():
    seres = [Humano("Ari"), Robot("R2")]
    for s in seres:  # Duck typing / polimorfismo: basta con que implementen actuar()
        s.actuar()

if __name__ == "__main__":
    main()
