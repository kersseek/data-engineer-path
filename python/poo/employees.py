class Empleado():
    def __init__(self, nombre, apellido, salario):
        self.__nombre = nombre
        self.__apellido = apellido
        self.__salario = salario

    @property
    def salario(self):
        return self.__salario

    @salario.setter
    def salario(self, salario):
        self.__salario = salario

    def mostrar_info(self):
        print(f'''
              Nombre: {self.__nombre}
              Apellido: {self.__apellido}
              Salario: {self.__salario}
              ''')


class Desarrollador(Empleado):
    def __init__(self, nombre, apellido, salario, lenguaje):
        super().__init__(nombre, apellido, salario)
        self.lenguaje = lenguaje

    def mostrar_info(self):
        print(f'''
              Nombre: {self._Empleado__nombre}
              Apellido: {self._Empleado__apellido}
              Salario: {self._Empleado__salario}
              Lenguaje: {self.lenguaje}
              ''')


class Gerente(Empleado):
    def __init__(self, nombre, apellido, salario):
        super().__init__(nombre, apellido, salario)
        self.empleados_a_cargo = []

    def agregar_empleado(self, empleado):
        self.empleados_a_cargo.append(empleado)

    def remover_empleado(self, empleado):
        self.empleados_a_cargo.remove(empleado)

    def mostrar_empleados(self):
        print(
            f"Empleados a cargo de {self._Empleado__nombre} {self._Empleado__apellido}")
        for emp in self.empleados_a_cargo:
            emp.mostrar_info()

    def mostrar_info(self):
        print(f'''
              Nombre: {self._Empleado__nombre}
              Apellido: {self._Empleado__apellido}
              Salario: {self._Empleado__salario}
              ''')


emp1 = Empleado("Laura", "Gómez", 25000)
emp1.salario = 27000
emp1.mostrar_info()

dev1 = Desarrollador("Carlos", "Méndez", 30000, "Python")
dev1.mostrar_info()

ger1 = Gerente("Ana", "Ramírez", 40000)
ger1.mostrar_info()

# Agregar empleados bajo el gerente
ger1.agregar_empleado(emp1)
ger1.agregar_empleado(dev1)

# Mostrar empleados a cargo del gerente
ger1.mostrar_empleados()

# Quitar un empleado
ger1.remover_empleado(emp1)

# Mostrar empleados restantes
ger1.mostrar_empleados()
