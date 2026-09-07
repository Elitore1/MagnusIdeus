class Ser {
  actuar() {
    throw new Error("Método 'actuar' debe implementarse");
  }
}

class Humano extends Ser {
  constructor(nombre) {
    super();
    this.nombre = nombre;
  }
  actuar() { // sobrescritura
    console.log(`${this.nombre} piensa y siente.`);
  }
}

class Robot extends Ser {
  constructor(id) {
    super();
    this.id = id;
  }
  actuar() {
    console.log(`Robot ${this.id} ejecuta instrucciones.`);
  }
}

const seres = [new Humano("Ari"), new Robot("R2")];
seres.forEach(s => s.actuar()); // polimorfismo en acción
