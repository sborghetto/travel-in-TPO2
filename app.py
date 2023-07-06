import sqlite3

class Producto:
    # Definimos el constructor e inicializamos los atributos de instancia
    def __init__(self, codigo, descripcion, cantidad, precio):
        self.codigo = codigo           # Código 
        self.descripcion = descripcion # Descripción
        self.cantidad = cantidad       # Cantidad disponible (stock)
        self.precio = precio           # Precio 

    # Este método permite modificar un producto.
    def modificar(self, nueva_descripcion, nueva_cantidad, nuevo_precio):
        self.descripcion = nueva_descripcion  # Modifica la descripción
        self.cantidad = nueva_cantidad        # Modifica la cantidad
        self.precio = nuevo_precio            # Modifica el precio

class Inventario:
    # Definimos el constructor e inicializamos los atributos de instancia
    def __init__(self):
        self.productos = []  # Lista de productos en el inventario (variable de clase)

    # Este método permite crear objetos de la clase "Producto" y agregarlos al inventario.
    def agregar_producto(self, codigo, descripcion, cantidad, precio):
        nuevo_producto = Producto(codigo, descripcion, cantidad, precio)
        self.productos.append(nuevo_producto)  # Agrega un nuevo producto a la lista

    # Este método permite consultar datos de productos que están en el inventario
    # Devuelve el producto correspondiente al código proporcionado o False si no existe.
    def consultar_producto(self, codigo):
        for producto in self.productos:
            if producto.codigo == codigo:
                return producto # Retorna un objeto
        return False

    # Este método permite modificar datos de productos que están en el inventario
    # Utiliza el método consultar_producto del inventario y modificar del producto.
    def modificar_producto(self, codigo, nueva_descripcion, nueva_cantidad, nuevo_precio):
        producto = self.consultar_producto(codigo)
        if producto:
            producto.modificar(nueva_descripcion, nueva_cantidad, nuevo_precio)

    # Este método elimina el producto indicado por codigo de la lista mantenida en el inventario.
    def eliminar_producto(self, codigo):
        eliminar = False
        for producto in self.productos:
            if producto.codigo == codigo:
                eliminar = True
                producto_eliminar = producto       
        if eliminar == True:
            self.productos.remove(producto_eliminar)
            print(f'Producto {codigo} eliminado.')
        else:
            print(f'Producto {codigo} no encontrado.')

    # Este método imprime en la terminal una lista con los datos de los productos que figuran en el inventario.
    def listar_productos(self):
        print("-"*50)
        print("Lista de productos en el inventario:")
        print("Código\tDescripción\t\tCant\tPrecio")
        for producto in self.productos:
            print(f'{producto.codigo}\t{producto.descripcion}\t{producto.cantidad}\t{producto.precio}')
        print("-"*50)

class Carrito:
    # Definimos el constructor e inicializamos los atributos de instancia
    def __init__(self):
        self.items = []  # Lista de items en el carrito (variable de clase)

    # Este método permite agregar productos del inventario al carrito.
    def agregar(self, codigo, cantidad, inventario):
        # Nos aseguramos que el producto esté en el inventario
        producto = inventario.consultar_producto(codigo)
        if producto is False: 
            print("El producto no existe.")
            return False

        # Verificamos que la cantidad en stock sea suficiente
        if producto.cantidad < cantidad:
            print("Cantidad en stock insuficiente.")
            return False

        # Si existe y hay stock, vemos si ya existe en el carrito.
        for item in self.items:
            if item.codigo == codigo:
                item.cantidad += cantidad
                # Actualizamos la cantidad en el inventario
                producto = inventario.consultar_producto(codigo)
                producto.modificar(producto.descripcion, producto.cantidad - cantidad, producto.precio)
                return True

        # Si no existe en el carrito, lo agregamos como un nuevo item.
        nuevo_item = Producto(codigo, producto.descripcion, cantidad, producto.precio)
        self.items.append(nuevo_item)
        # Actualizamos la cantidad en el inventario
        producto = inventario.consultar_producto(codigo)
        producto.modificar(producto.descripcion, producto.cantidad - cantidad, producto.precio)
        return True

    # Este método quita unidades de un elemento del carrito, o lo elimina.
    def quitar(self, codigo, cantidad, inventario):
        for item in self.items:
            if item.codigo == codigo:
                if cantidad > item.cantidad:
                    print("Cantidad a quitar mayor a la cantidad en el carrito.")
                    return False
                item.cantidad -= cantidad
                if item.cantidad == 0:
                    self.items.remove(item)
                # Actualizamos la cantidad en el inventario
                producto = inventario.consultar_producto(codigo)
                producto.modificar(producto.descripcion, producto.cantidad + cantidad, producto.precio)
                return True

        # Si el bucle finaliza sin novedad, es que ese producto NO ESTA en el carrito.
        print("El producto no se encuentra en el carrito.")
        return False

    def mostrar(self):
        print("-"*50)
        print("Lista de productos en el carrito:")
        print("Código\tDescripción\t\tCant\tPrecio")
        for item in self.items:
            print(f'{item.codigo}\t{item.descripcion}\t{item.cantidad}\t{item.precio}')
        print("-"*50)



# Programa principal
producto = Producto(1, 'Cataratas 7 noches Pensión Completa', 30, 90000)
# Accedemos a los atributos del objeto
print(f'{producto.codigo} | {producto.descripcion} | {producto.cantidad} | {producto.precio}')
# Modificar los datos del producto
producto.modificar('Cataratas y otros 7 noches Pensión Completa', 35, 90000) 
print(f'{producto.codigo} | {producto.descripcion} | {producto.cantidad} | {producto.precio}')

# Crear una instancia de la clase Inventario
mi_inventario = Inventario() 

# Agregar productos 
mi_inventario.agregar_producto(1, 'CATARATAS y otros 7 noches Pensión Completa', 35, 90000)
mi_inventario.agregar_producto(2, 'CATARATAS y otros 7 noches Media Pensión ', 35, 75000)
mi_inventario.agregar_producto(3, 'NOA y otros 7 noches Pensión Completa', 30, 80000)
mi_inventario.agregar_producto(4, 'NOA y otros 7 noches Media Pensión', 30, 65000)
mi_inventario.agregar_producto(5, 'CUYO 7 noches Pensión Completa', 28, 85000)
mi_inventario.agregar_producto(6, 'USUAHIA 7 noches Pensión Completa', 25, 150000)

# Consultar un producto 
producto = mi_inventario.consultar_producto(3)
if producto != False:
    print(f'Producto encontrado:\nCódigo: {producto.codigo}\nDescripción: {producto.descripcion}\nCantidad: {producto.cantidad}\nPrecio: {producto.precio}')  
else:
    print("Producto no encontrado.")

# Modificar un producto 
mi_inventario.modificar_producto(6, 'USUAHIA - CALAFATE 7 noches Pensión Completa', 25, 150000)

# Listar todos los productos
mi_inventario.listar_productos()

# Eliminar un producto 
mi_inventario.eliminar_producto(2)

# Confirmamos que haya sido eliminado
mi_inventario.listar_productos()


# ---------------------------------------------------------------------
# Ejemplo de uso de las clases y objetos definidos antes:
# ---------------------------------------------------------------------

# Crear una instancia de la clase Inventario
mi_inventario = Inventario()

# Crear una instancia de la clase Carrito
mi_carrito = Carrito()

# Crear 6 productos y agregarlos al inventario
mi_inventario.agregar_producto(1, 'CATARATAS y otros 7 noches Pensión Completa', 35, 90000)
mi_inventario.agregar_producto(2, 'CATARATAS y otros 7 noches Media Pensión ', 35, 75000)
mi_inventario.agregar_producto(3, 'NOA y otros 7 noches Pensión Completa', 30, 80000)
mi_inventario.agregar_producto(4, 'NOA y otros 7 noches Media Pensión', 30, 65000)
mi_inventario.agregar_producto(5, 'CUYO 7 noches Pensión Completa', 28, 85000)
mi_inventario.agregar_producto(6, 'USUAHIA 7 noches Pensión Completa', 25, 150000)

# Listar todos los productos del inventario
mi_inventario.listar_productos()

# Agregar 2 productos al carrito
mi_carrito.agregar(1, 2, mi_inventario) # Agregar 2 unidades del producto con código 1 al carrito
mi_carrito.agregar(3, 4, mi_inventario) # Agregar 1 unidad del producto con código 3 al carrito
mi_carrito.quitar (1, 1, mi_inventario) # Quitar 1 unidad del producto con código 1 al carrito
# Listar todos los productos del carrito
mi_carrito.mostrar()
# Quitar 1 producto al carrito
mi_carrito.quitar (1, 1, mi_inventario) # Quitar 1 unidad del producto con código 1 al carrito
# Listar todos los productos del carrito
mi_carrito.mostrar()
# Mostramos el inventario
mi_inventario.listar_productos()
