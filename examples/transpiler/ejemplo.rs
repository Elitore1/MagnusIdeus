trait Ser {
    fn actuar(&self);
}

struct Humano {
    nombre: String,
}

impl Ser for Humano {
    fn actuar(&self) {
        println!("{} piensa y siente.", self.nombre);
    }
}

struct Robot {
    id: String,
}

impl Ser for Robot {
    fn actuar(&self) {
        println!("Robot {} ejecuta instrucciones.", self.id);
    }
}

fn main() {
    let seres: Vec<Box<dyn Ser>> = vec![
        Box::new(Humano { nombre: "Ari".into() }),
        Box::new(Robot { id: "R2".into() }),
    ];

    for s in seres.iter() {
        s.actuar(); // dispatch dinámico vía trait object
    }
}
