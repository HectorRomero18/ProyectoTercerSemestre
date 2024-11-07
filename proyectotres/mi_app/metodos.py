# metodos.py
class Nodo:
    def __init__(self, persona, siguiente=None):
        """
        Inicializa un nodo con una persona y un puntero al siguiente nodo.
        
        :param persona: Instancia de la clase Persona que se almacenará en el nodo.
        :param siguiente: Nodo siguiente al nodo actual, por defecto es None.
        """
        self.persona = persona  # Almacena la instancia de Persona
        self.siguiente = siguiente  # Puntero al siguiente nodo

class ListaEnlazada:
    def __init__(self):
        """Inicializa la lista enlazada vacía, donde 'primero' es None."""
        self.primero = None  # Inicializa la cabeza de la lista enlazada

    def insertar(self, persona):
        """
        Inserta un nuevo nodo con la persona en el final de la lista enlazada.
        
        :param persona: Instancia de la clase Persona que se insertará en la lista.
        """
        try:
            nuevo_nodo = Nodo(persona)  # Crear el nuevo nodo con la persona
            if not self.primero:
                # Si la lista está vacía, el nuevo nodo es el primero
                self.primero = nuevo_nodo
            else:
                # Si la lista no está vacía, recorrer la lista hasta el final
                actual = self.primero
                while actual.siguiente is not None:
                    actual = actual.siguiente
                # Enlazar el nuevo nodo al final de la lista
                actual.siguiente = nuevo_nodo
        except Exception as e:
            print(f"Error al insertar nodo: {e}")

    def ordenar(self, atributo):
        """
        Ordena la lista enlazada usando el método de burbuja según un atributo específico.
        
        :param atributo: Atributo por el cual se ordenarán los nodos ('nombre', 'apellido', 'edad', 'atendido').
        """
        try:
            if self.primero is None:
                # Si la lista está vacía, no hay nada que ordenar
                return
            
            while True:
                intercambiado = False
                actual = self.primero
                while actual.siguiente is not None:
                    siguiente = actual.siguiente
                    # Comparar según el atributo especificado
                    if (atributo == 'nombre' and actual.persona.nombre > siguiente.persona.nombre) or \
                       (atributo == 'apellido' and actual.persona.apellido > siguiente.persona.apellido) or \
                       (atributo == 'atendido' and actual.persona.atendido < siguiente.persona.atendido) or \
                       (atributo == 'edad' and actual.persona.edad > siguiente.persona.edad):
                        # Intercambiar las personas entre los nodos
                        actual.persona, siguiente.persona = siguiente.persona, actual.persona
                        intercambiado = True
                    actual = siguiente
                if not intercambiado:
                    # Si no hubo intercambios, la lista ya está ordenada
                    break
        except Exception as e:
            print(f"Error al ordenar la lista: {e}")
    
    def buscar_todas(self, valor, atributo='nombre'):
        """
        Busca todas las personas en la lista enlazada por un atributo específico.
        
        :param valor: El valor a buscar (nombre, apellido, edad).
        :param atributo: El atributo por el cual se buscará (por defecto 'nombre').
        :return: Lista de personas que coinciden con el valor y atributo especificados.
        """
        try:
            actual = self.primero
            personas_encontradas = []  # Lista para almacenar las personas encontradas
            while actual:
                # Comparar según el atributo y el valor proporcionado
                if (atributo == 'nombre' and actual.persona.nombre.lower() == valor.lower()) or \
                   (atributo == 'apellido' and actual.persona.apellido.lower() == valor.lower()) or \
                   (atributo == 'edad' and str(actual.persona.edad) == str(valor)):  # Comparar como cadena
                    personas_encontradas.append(actual.persona)  # Añadir a la lista de resultados
                actual = actual.siguiente
            return personas_encontradas  # Retorna la lista de personas encontradas
        except Exception as e:
            print(f"Error al buscar personas: {e}")
            return []  # Retornar lista vacía si hay un error

    def mostrar(self):
        """
        Muestra todas las personas de la lista enlazada en una lista.

        :return: Lista con todas las personas de la lista enlazada.
        """
        try:
            personas = []
            actual = self.primero
            while actual:
                personas.append(actual.persona)  # Agregar la persona al resultado
                actual = actual.siguiente
            return personas  # Retorna la lista con todas las personas
        except Exception as e:
            print(f"Error al mostrar la lista: {e}")
            return []  # Retornar lista vacía en caso de error
