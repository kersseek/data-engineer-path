class Vehiculo:
    def __init__(self, marca, modelo, precio):
        self.marca = marca
        self._modelo = modelo
        self.__precio = precio

    def mostrar_info(self):
        print('Marca: ', self.marca)
        print('Modelo: ', self._modelo)
        print('Precio: ', self.__precio)

    def calcular_impuesto(self, tasa):
        impuesto = self.precio * tasa
        return impuesto

    @property
    def precio(self):
        return self.__precio

    @precio.setter
    def precio(self, nuevo_precio):
        if nuevo_precio > 0:
            self.__precio = nuevo_precio
        else:
            print('El precio nuevo no es mayor a 0')


class Auto(Vehiculo):
    def __init__(self, marca, modelo, precio, puertas):
        super().__init__(marca, modelo, precio)
        self.puertas = puertas

        print('Impuesto: ', super().calcular_impuesto(0.05))

    def mostrar_info(self):
        super().mostrar_info()
        print('Puertas: ', self.puertas)


class Moto(Vehiculo):
    def __init__(self, marca, modelo, precio, cilindrada):
        super().__init__(marca, modelo, precio)
        self.cilindrada = cilindrada

        if self.cilindrada < 500:
            print('Impuesto: ', super().calcular_impuesto(0.05))
        elif self.cilindrada > 500:
            print('Impuesto: ', super().calcular_impuesto(0.08))
        else:
            print("La moto no cumple con las especificaciones")

    def mostrar_info(self):
        super().mostrar_info()
        print('Cilindrada: ', self.cilindrada)


auto = Auto("Toyota", "Corolla", 20000, 5)
auto.mostrar_info()
