Introducción

La presente aplicación está diseñada para la gestión integral de gimnasios, proporcionando herramientas para el manejo eficiente de clientes, membresías, registros de ingreso, y análisis de datos. Además, incluye un generador de reportes en formato PDF para facilitar la toma de decisiones basadas en datos.

Características Principales

1. Gestión de Clientes

Agregar Clientes: Permite registrar información básica de nuevos clientes, incluyendo nombre, edad, DNI, contacto y preferencias.

Editar Clientes: Ofrece la opción de actualizar datos existentes, como dirección o número de teléfono.

Eliminar Clientes: Proporciona la capacidad de eliminar registros de clientes de forma segura.

2. Membresías

Asignar Membresías: Permite vincular membresías personalizadas a cada cliente, estableciendo la duración y el número de clases disponibles.

Editar Membresías: Posibilidad de modificar las condiciones de una membresía activa.

Eliminar Membresías: Elimina membresías cuando ya no son requeridas o están vencidas.

Personalización de Membresías: Ofrece la opción de configurar membresías utilizando días o meses como base temporal, así como ajustar los precios según las necesidades del gimnasio.

3. Registro de Ingresos

Ventana exclusiva para los clientes donde pueden registrar su ingreso mediante su DNI.

Control de Clases: El sistema descontará automáticamente una clase del saldo de la membresía al momento del ingreso.

Notificaciones: Si un cliente se queda sin clases disponibles, se mostrará un mensaje visual (cartel rojo) indicando la necesidad de renovar su membresía.

4. Análisis y Gráficas

Distribución por Edades: Gráficas que muestran qué rangos de edad tienen mayor frecuencia de asistencia.

Horarios de Mayor Afluencia: Gráficas que reflejan los horarios con mayor cantidad de visitas, permitiendo ajustar recursos y horarios del gimnasio.

5. Generación de Reportes

Reportes en PDF: Permite generar reportes detallados sobre clientes, membresías activas, ingresos diarios, y análisis de uso del gimnasio.

Reporte Mensual: Suma todos los ingresos mensuales y presenta gráficas que detallan:

Clientes que ingresaron durante el mes, especificando su tipo de plan.

Frecuencia de ingresos de cada cliente.

Ventanas y Diseño de la Interfaz

1. Ventana de Administración

Exclusiva para el personal del gimnasio. Contiene:

Panel para gestión de clientes.

Herramientas para asignar, editar y eliminar membresías.

Gráficas analíticas sobre edades y horarios.

Botón para generar reportes en PDF.

2. Ventana de Registro de Ingresos

Disponible en un monitor separado para el acceso de los clientes. Contiene:

Campo para ingreso de DNI.

Indicador visual que confirma el registro exitoso y descuenta una clase.

Notificación en caso de clases agotadas.

Tecnologías y Requerimientos

Lenguajes y Herramientas:

Backend: Python (con SQLite).

Frontend: Tkinter (con animaciones y botones interactivos).

Base de Datos:

SQLite para almacenar datos de clientes, membresías e ingresos.

Requerimientos del Sistema:

Computadora con capacidad de ejecución para Python.

Monitor adicional para la ventana de registro de ingresos.
