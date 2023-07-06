import sqlite3


# Configurar la conexión a la base de datos SQLite
DATABASE = 'inventario.db'

def get_db_connection():
    print("Obteniendo conexión...") # Para probar que se ejecuta la función
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Crear la tabla 'productos' si no existe
def create_table():
    print("Creando tabla productos...") # Para probar que se ejecuta la función
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            codigo INTEGER PRIMARY KEY,
            descripcion TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
        ) ''')
    conn.commit()
    cursor.close()
    conn.close()

# Verificar si la base de datos existe, si no, crearla y crear la tabla
def create_database():
    print("Creando la BD...") # Para probar que se ejecuta la función
    conn = sqlite3.connect(DATABASE)
    conn.close()
    create_table()

# Programa principal
# Crear la base de datos y la tabla si no existen
create_database()

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
    def __init__(self):
        self.conexion = get_db_connection()
        self.cursor = self.conexion.cursor()

    # Este método permite crear objetos de la clase "Producto" y agregarlos al inventario.
    def agregar_producto(self, codigo, descripcion, cantidad, precio):
        producto_existente = self.consultar_producto(codigo)
        if producto_existente:
            print("Ya existe un producto con ese código.")
            return False
        nuevo_producto = Producto(codigo, descripcion, cantidad, precio)
        sql = f'INSERT INTO productos VALUES ({codigo}, "{descripcion}", {cantidad}, {precio});'
        self.cursor.execute(sql)
        self.conexion.commit()
        return True
 
    # Este método permite consultar datos de productos que están en el inventario
    # Devuelve el producto correspondiente al código proporcionado o False si no existe.
    def consultar_producto(self, codigo):
        sql = f'SELECT * FROM productos WHERE codigo = {codigo};'
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        if row:
            codigo, descripcion, cantidad, precio = row
            return Producto(codigo, descripcion, cantidad, precio)
        return False


    # Este método permite modificar datos de productos que están en el inventario
    # Utiliza el método consultar_producto del inventario y modificar del producto.
    def modificar_producto(self, codigo, nueva_descripcion, nueva_cantidad, nuevo_precio):
        producto = self.consultar_producto(codigo)
        if producto:
            producto.modificar(nueva_descripcion, nueva_cantidad, nuevo_precio)
            sql = f'UPDATE productos SET descripcion = "{nueva_descripcion}", cantidad = {nueva_cantidad}, precio = {nuevo_precio} WHERE codigo = {codigo};' 
            self.cursor.execute(sql)
            self.conexion.commit()

    # Este método elimina el producto indicado por codigo de la lista mantenida en el inventario.
    def eliminar_producto(self, codigo):
        sql = f'DELETE FROM productos WHERE codigo = {codigo};' 
        self.cursor.execute(sql)
        if self.cursor.rowcount > 0:
            print(f'Producto {codigo} eliminado.')
            self.conexion.commit()
        else:
            print(f'Producto {codigo} no encontrado.')


    # Este método imprime en la terminal una lista con los datos de los productos que figuran en el inventario.
    def listar_productos(self):
        print("-"*50)
        print("Lista de productos en el inventario:")
        print("Código\tDescripción\tCant\tPrecio")
        self.cursor.execute("SELECT * FROM productos")
        rows = self.cursor.fetchall()
        for row in rows:
            codigo, descripcion, cantidad, precio = row
            print(f'{codigo}\t{descripcion}\t{cantidad}\t{precio}')
        print("-"*50)


class Carrito:
    # Definimos el constructor e inicializamos los atributos de instancia
    def __init__(self):
        self.conexion = sqlite3.connect('inventario.db')  # Conexión a la BD
        self.cursor = self.conexion.cursor()
        self.items = []


    # Este método permite agregar productos del inventario al carrito.
    def agregar(self, codigo, cantidad, inventario):
        producto = inventario.consultar_producto(codigo)
        if producto is False:
            print("El producto no existe.")
            return False
        if producto.cantidad < cantidad:
            print("Cantidad en stock insuficiente.")
            return False

        for item in self.items:
            if item.codigo == codigo:
                item.cantidad += cantidad
                sql = f'UPDATE productos SET cantidad = cantidad - {cantidad}  WHERE codigo = {codigo};'
                self.cursor.execute(sql)
                self.conexion.commit()
                return True

        nuevo_item = Producto(codigo, producto.descripcion, cantidad, producto.precio)
        self.items.append(nuevo_item)
        sql = f'UPDATE productos SET cantidad = cantidad - {cantidad}  WHERE codigo = {codigo};'
        self.cursor.execute(sql)
        self.conexion.commit()
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
                sql = f'UPDATE productos SET cantidad = cantidad + {cantidad} WHERE codigo = {codigo};'
                self.cursor.execute(sql)
                self.conexion.commit()
                return True


    def mostrar(self):
        print("-"*50)
        print("Lista de productos en el carrito:")
        print("Código\tDescripción\tCant\tPrecio")
        for item in self.items:
            print(f'{item.codigo}\t{item.descripcion}\t{item.cantidad}\t{item.precio}')
        print("-"*50)

# Programa principal
# Crear la base de datos y la tabla si no existen
create_database()

# Crear una instancia de la clase Inventario
mi_inventario = Inventario()

# Agregar productos al inventario
mi_inventario.agregar_producto(1, 'CATARATAS y otros 7 noches Pensión Completa', 35, 90000)
mi_inventario.agregar_producto(2, 'CATARATAS 7 noches Media Pensión', 35, 75000)
mi_inventario.agregar_producto(3, 'NOA y otros 7 noches Pensión Completa', 30, 80000)
mi_inventario.agregar_producto(4, 'NOA y otros 7 noches Media Pensión', 30, 65000)
mi_inventario.agregar_producto(5, 'CUYO 7 noches Pensión Completa', 28, 85000)
mi_inventario.agregar_producto(6, 'USHUAIA 7 noches Pensión Completa', 25, 150000)

# Consultar algún producto del inventario
print(mi_inventario.consultar_producto(3)) #Existe, se muestra la dirección de memoria
print(mi_inventario.consultar_producto(8)) #No existe, se muestra False

# Listar los productos del inventario
mi_inventario.listar_productos()

# Modificar un producto del inventario
mi_inventario.modificar_producto(2, 'CATARATAS y otros 7 noches Media Pensión', 35, 75000)

# Listar nuevamente los productos del inventario para ver la modificación
mi_inventario.listar_productos()

# Eliminar un producto
mi_inventario.eliminar_producto(3)

# Listar nuevamente los productos del inventario para ver la eliminación
mi_inventario.listar_productos()

# Crear una instancia de la clase Carrito
mi_carrito = Carrito()
# Agregar 2 unidades del producto con código 1 al carrito
mi_carrito.agregar(1, 2, mi_inventario)  
# Agregar 1 unidad del producto con código 2 al carrito
mi_carrito.agregar(2, 1, mi_inventario)  

# Mostrar el contenido del carrito y del inventario
mi_carrito.mostrar()
mi_inventario.listar_productos()

'''''''''
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
'''

# ---------------------------------------------------------------------
# Ejemplo de uso de las clases y objetos definidos antes:
# ---------------------------------------------------------------------

""" DESDE ACÁ COMENTO

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
 """