class Estudiante(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    cedula = models.CharField(max_length=30, unique=True)
    correo = models.EmailField()

    def _str_(self):
        return "%s %s %s %s" % (self.nombre,
                self.apellido,
                self.cedula,
                self.correo)

    def get_provincia(self):
        """
        """
        dato = self.cedula[0:2]
        valor = "Sin Provincia"
        if dato == "11":
            valor = "Loja"
        else:
            if dato == "17":
                valor = "Pichincha"
        return valor

    def obtener_valorTelefonos(self):
        valor = 0 
        for num in self.numeros_telefonicos.all():
            valor = valor + num.valor_mensual
        return valor


class NumeroTelefonico(models.Model):
    telefono = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    valor_mensual = models.FloatField(default=0.0) 
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE,
            related_name="numeros_telefonicos")

    def _str_(self):
        return "%s %s" % (self.telefono, self.tipo)