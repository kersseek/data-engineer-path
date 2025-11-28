class Persona():
    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido

    def mostrar_info(self):
        print(f''' 
              Nombre: {self.nombre}
              Apellido: {self.apellido}
              ''')


class Alumno(Persona):
    def __init__(self, nombre, apellido, matricula):
        super().__init__(nombre, apellido)
        self.nombre = nombre
        self.apellido = apellido
        self.__matricula = matricula
        self.cursos_inscritos = []

    @property
    def matricula(self):
        return self.__matricula

    @matricula.setter
    def matricula(self, matricula):
        self.__matricula = matricula

    def inscribirse(self, curso):
        self.cursos_inscritos.append(curso)
        curso.agregar_alumno(self)

    def mostrar_cursos(self):
        print(f"Cursos inscritos por {self.nombre} {self.apellido}:")
        for curso in self.cursos_inscritos:
            print(f"- {curso.nombre_curso}")

    def mostrar_info(self):
        print(
            f"Alumno: {self.nombre} {self.apellido} | Matrícula: {self.matricula}")


class Profesor(Persona):
    def __init__(self, nombre, apellido, especialidad):
        super().__init__(nombre, apellido)
        self.nombre = nombre
        self.apellido = apellido
        self.especialidad = especialidad
        self.curso_asignado = []

    def asignar_curso(self, curso):
        self.curso_asignado.append(curso)

    def mostrar_cursos(self):
        for curso in self.curso_asignado:
            print(f"- {curso.nombre_curso}")

    def mostrar_info(self):
        print(f''' 
Nombre: {self.nombre}
Apellido: {self.apellido}
Especialidad: {self.especialidad}
        ''')


class Curso():
    def __init__(self, nombre_curso, profesor):
        self.nombre_curso = nombre_curso
        self.profesor = profesor
        self.alumnos = []

    def agregar_alumno(self, alumno):
        self.alumnos.append(alumno)

    def mostrar_alumnos(self):
        print(f"Alumnos inscritos en {self.nombre_curso}:")
        for alumno in self.alumnos:
            print(f"- {alumno.nombre} {alumno.apellido}")

    def mostrar_info(self):
        print(f''' 
Nombre de curso: {self.nombre_curso}
        ''')


# Crear profesores
profesor1 = Profesor("Mario", "Sánchez", "Matemáticas")
profesor2 = Profesor("Laura", "Pérez", "Programación")

# Crear alumnos
alumno1 = Alumno("Alexis", "Salgado", "A001")
alumno2 = Alumno("Fernanda", "Lopez", "A002")
alumno3 = Alumno("Carlos", "Ramirez", "A003")

# Crear cursos
curso1 = Curso("Álgebra", profesor1)
curso2 = Curso("Python Básico", profesor2)

# Asignar cursos a profesores
profesor1.asignar_curso(curso1)
profesor2.asignar_curso(curso2)

# Inscribir alumnos en cursos
alumno1.inscribirse(curso1)
alumno1.inscribirse(curso2)

alumno2.inscribirse(curso2)

alumno3.inscribirse(curso1)

# Mostrar cursos de cada profesor
profesor1.mostrar_cursos()
profesor2.mostrar_cursos()

# Mostrar cursos de cada alumno
alumno1.mostrar_cursos()
alumno2.mostrar_cursos()
alumno3.mostrar_cursos()

# Mostrar alumnos en cada curso
curso1.mostrar_alumnos()
curso2.mostrar_alumnos()
