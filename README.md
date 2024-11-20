# H2_SGE_1-T_AdrianLopezGil
H2_SGE_1ºT_AdrianLopezGil

# Gestión de Encuestas

Este proyecto es una aplicación de escritorio en Python para gestionar encuestas relacionadas con el consumo de alcohol y sus efectos en la salud. Utiliza **Tkinter** para la interfaz gráfica, **MySQL** como base de datos y **Pandas** junto con **Matplotlib** para el análisis de datos y visualización.

## Características

- **CRUD**: Crear, leer, actualizar y eliminar encuestas.
- **Filtros dinámicos**: Filtrar encuestas por criterios como edad, sexo o consumo semanal.
- **Exportación**: Guardar los datos filtrados en un archivo Excel.
- **Gráficos**:
  - Distribución de edades de los encuestados.
  - Consumo de alcohol por edad.
- **Interfaz gráfica**: Intuitiva y fácil de usar.

## Requisitos

Antes de ejecutar la aplicación, asegúrate de tener instalados los siguientes componentes:

- **Python 3.x**
- Módulos de Python:
  - `mysql.connector`
  - `pandas`
  - `matplotlib`
  - `tkinter` (incluido por defecto con Python)
- **MySQL** como servidor de base de datos.

## La interfaz te permitirá:

- **Agregar nuevas encuestas** llenando los campos correspondientes y presionando el botón **Agregar Encuesta**.
- **Visualizar las encuestas existentes** en un formato tabular.
- **Aplicar filtros dinámicos** para analizar subconjuntos de los datos.
- **Generar gráficos** para análisis visual.
- **Exportar datos filtrados** a Excel.

## Funcionalidades principales

### Gestión de datos
- **Agregar Encuesta**: Inserta un nuevo registro en la base de datos.
- **Ver Encuestas**: Muestra todos los registros en una vista tabular.
- **Modificar Datos**: Permite editar una encuesta seleccionada.
- **Eliminar Encuesta**: Elimina un registro específico de la base de datos.

### Visualización
- **Gráfico Edad**: Histograma que muestra la distribución de edades.
- **Gráfico Consumo**: Diagrama de barras que relaciona la edad con el consumo semanal de alcohol.

### Exportación
- **Exportar a Excel**: Guarda los datos filtrados en un archivo Excel para análisis adicional.

## Licencia

Este proyecto está bajo la licencia MIT.

## Configuración Base de Datos(MySQL)

1. Crea la base de datos en MySQL utilizando el siguiente esquema:

```sql
CREATE DATABASE ENCUESTAS;

USE ENCUESTAS;

CREATE TABLE ENCUESTA (
    idEncuesta INT AUTO_INCREMENT PRIMARY KEY,
    edad INT,
    Sexo VARCHAR(7),
    BebidasSemana INT,
    CervezasSemana INT,
    BebidasFinSemana INT,
    BebidasDestiladasSemana INT,
    VinosSemana INT,
    PerdidasControl INT,
    DiversionDependenciaAlcohol CHAR(2),
    ProblemasDigestivos CHAR(2),
    TensionAlta CHAR(12),
    DolorCabeza CHAR(12)
);
