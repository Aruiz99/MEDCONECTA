![bANNER](https://github.com/Aruiz99/MEDCONECTA_test/assets/116668101/0dec8dba-4a37-44b3-b0cb-1f96e757e0ec)


## Índice
- [Introducción](#introduccion)
- [Metodología](#metodología)
   - [Datos iniciales](#datos-iniciales)
   - [Desarrollo](#desarrollo)
   - [Resultados](#resultados)
- [Uso](#uso)
- [Estado del Proyecto](#estado-del-proyecto)
- [Licencia](#licencia)

## Introducción 
El proyecto MEDCONECTA tiene como objetivo principal la delineación de una red de corredores que maximicen la coherencia espacial de la Infraestructura Verde (IV) identificando los niveles de conservación o restauración que se requieren para asegurar la funcionalidad del sistema.

Teniendo en cuenta que las transferencias funcionales entre ecosistemas suelen darse más fácilmente si el espacio intermedio tiene propiedades similares, se ensayará un algoritmo en el sureste
peninsular, utilizando la información de Andalucía, Región de Murcia y Comunidad Valenciana. Además, se integrará la identificación de acciones de restauración o gestión según los estándares de Soluciones basadas en la Naturaleza de la UICN (Unión Internacional para la Conservación de la Naturaleza).

Un aspecto fundamental de esta metodología es la inclusión de un componente participativo que involucra a técnicos y gestores del medio. Esta participación activa permitirá recopilar conocimientos prácticos y perspectivas locales que enriquecerán la planificación y ejecución del proyecto. Se espera que los resultados de esta investigación proporcionen una base técnica sólida que oriente a las autoridades reguladoras en el desarrollo integral de la Infraestructura Verde. 

## Metodología
En esta sección se llevará a cabo un análisis de los datos iniciales recopilados para el proyecto MEDCONECTA. Este análisis permitirá establecer un contexto completo y sólido sobre el cual se fundamentará el desarrollo del proyecto.

Posteriormente, se presentará una explicación detallada del funcionamiento del algoritmo principal. Se describirá paso a paso la metodología utilizada para la optimización y creación del mapa de afinidad que, tras la posterior revisión de los técnicos, se convertirá en la red de corredores verdes.

Finalmente, se exhibirán ejemplos representativos de los resultados obtenidos a través del proceso de implementación del algoritmo. Estos ejemplos proporcionarán una vista general de como se comporta el algoritmo. Se mostrarán visualizaciones y datos concretos que ilustren su impacto potencial en la región. Estos resultados servirán como referencia para evaluar la eficacia y relevancia de las estrategias desarrolladas en el marco del proyecto MEDCONECTA.

### Datos iniciales
El algoritmo se basa en dos conjuntos de datos principales como entrada. Por un lado, utilizamos el mapa base de trabajo conocido como '2dRUE', que representa la condición de la tierra y actúa como nuestra referencia principal. Por otro lado, empleamos un conjunto inicial de datos llamado 'semillas' o 'zonas núcleo', que consiste en un subconjunto de Lugares de Importancia Comunitaria (LIC) pertenecientes a la RedNatura2000, específicamente ubicados en el sureste peninsular. Estas 'semillas' proporcionan puntos iniciales clave para la aplicación del algoritmo en el proceso de delineación de corredores verdes.

#### 2dRUE
El "2dRUE" es una metodología que emplea dos componentes, valoración y seguimiento, para evaluar la condición de la tierra en función de la eficiencia en el uso de la lluvia, comparando la capacidad ecológica actual de los sitios con sus condiciones potenciales de referencia y detectando tendencias de cambio a lo largo del tiempo. En una primera instancia se ha empleado el componente de valoración, que se refiere al estado de degradación y trata de cuantificar el rendimiento ecológico de cada sitio respecto a sus condiciones potenciales de referencia. Su paradigma es que la Eficiencia en el Uso de la Lluvia (RUE por sus siglas en inglés) es máxima en sitios con una condición ecológica favorable, para lo que usa dos
implementaciones temporales de este concepto que indican respectivamente biomasa media y productividad máxima. En ella, cada sitio es comparado sincrónicamente con todos los demás durante el período de análisis. La comparación entre la situación actual y el potencial teórico proporciona información valiosa sobre la degradación, el desarrollo o la estabilidad de los ecosistemas a lo largo del tiempo, concretamente este mapa hace referencia al periodo 2010 - 2019.

Su leyenda refleja niveles crecientes de madurez y complejidad en una escala ecológica (Anomalía de Bajo Rendimiento, Basal, Muy Degradado, Degradado, Productivo con Baja Biomasa, Productivo
con Alta Biomasa, Submaduro, Maduro, Referencia y Anomalía de Alto Rendimiento).

<!-- Salto adicional -->
<!-- Salto adicional -->

![Imagen2](https://github.com/Aruiz99/MEDCONECTA_test/assets/116668101/1cb52c11-571b-4ba0-88b4-ef9d30c517af)

<!-- Salto adicional -->

Para más información acerca del 2dRUE se puede acceder al siguiente documento: [Mapa de la Condición de la Tierra en España: 2000-2010](https://digital.csic.es/bitstream/10261/200778/1/2dRUE_ES_EnFinal_v7.pdf)

#### RedNatura2000
La Red Natura 2000 es un conjunto de áreas protegidas establecido en la Unión Europea con el propósito de salvaguardar y conservar la biodiversidad. Está compuesta por Lugares de Importancia Comunitaria (LIC) y Zonas de Especial Protección para las Aves (ZEPA), esta red abarca espacios cruciales para la preservación de hábitats naturales, especies animales y vegetales en peligro, contribuyendo significativamente a la conservación de la naturaleza y el equilibrio ecológico en Europa. 

En este algorimo se ha empleado un subconjunto de los LIC como semillas iniciales, concretamente se han empleado los LIC que se encuentran en zonas de aridez o colindantes a ellas. Para determinar las zonas de aridez se ha empleado el índice de aridez FAO-UNEP y se han seleccionado aquellas que poseen un índice FAO-UNEP de (0.05 - 0.20).

<!-- Salto adicional -->

![Layout 2](https://github.com/Aruiz99/MEDCONECTA_test/assets/116668101/70b92b72-b86d-44a0-a17d-0b190a6b5b43)

<!-- Salto adicional -->
<!-- Salto adicional -->

Para más información acerca de la RedNatura2000 se puede acceder al siguiente enlace:
[Red Natura 2000 - Ministerio de España](https://www.miteco.gob.es/es/biodiversidad/temas/espacios-protegidos/red-natura-2000.html)

### Desarrollo

El algoritmo central del proyecto MEDCONECTA se basa en un algoritmo de crecimiento. A partir de un conjunto inicial de semillas, se lleva a cabo un análisis de su entorno utilizando la información proporcionada por el 2dRUE. El objetivo es identificar y buscar áreas afines o similares alrededor de estas semillas iniciales. Este proceso permite determinar las áreas que presentan similitudes ecológicas con las semillas, contribuyendo así a la delimitación de zonas con características ambientales favorables para la conformación de corredores o conexiones naturales.

Para identificar áreas afines alrededor de las semillas se va a comparar la composición original de la semilla en base al 2dRUE con la composición de diferentes muestras de terreno alrededor de la semilla. Estas muestras se extraerán de los bordes de la semilla y consistirán en por cada punto del borde de la semilla se trazará un kernel de NxN alrededor del punto y se comparará todo lo que esté fuera de la semilla con la composicion original de la misma.

Para identificar áreas afines con las semillas iniciales, se llevará a cabo un proceso de comparación entre la composición original de las semillas y la composición de diversas muestras de terreno extraídas de los alrededores de estas semillas. 
En este contexto, la "composición" se refiere al histograma que muestra la distribución o la cantidad de píxeles asociados con cada categoría del 2dRUE dentro de un área o conjunto específico.

Las muestras se obtendrán de los bordes de las semillas mediante un enfoque de kernel. Específicamente, para cada punto en el borde de la semilla, se trazará un kernel de tamaño NxN alrededor de dicho punto. Se comparará la composición de cada muestra asociada a cada punto del borde con la composición original de la semilla.

A continuación, se mostrará un ejemplo de semilla con su compsición asociada, concretamente la semilla corresponde con el LIC de Sierra Nevada:

<!-- Salto adicional -->
![Captura de pantalla 2023-12-01 203402](https://github.com/Aruiz99/MEDCONECTA_test/assets/116668101/9e0a327d-852c-435e-b9b0-313b632562b1)
<!-- Salto adicional -->

De la misma manera, se mostrará un ejemplo de muestra alrededor de la semilla original.

<!-- Salto adicional -->
![Captura de pantalla 2023-12-01 203441](https://github.com/Aruiz99/MEDCONECTA_test/assets/116668101/7b8ecf9a-6ab6-4b8f-9c4c-74bcd9844f76)
<!-- Salto adicional -->


![desarrollo](https://github.com/Aruiz99/MEDCONECTA_test/assets/116668101/dd6c212e-a077-4d0c-b456-a198790b5c40)

![Captura de pantalla 2023-12-02 113659](https://github.com/Aruiz99/MEDCONECTA_test/assets/116668101/20fa7497-dc71-4295-9870-2a4ddc67ba9e)
![orloci](https://github.com/Aruiz99/MEDCONECTA_test/assets/116668101/b5d322e5-58b5-498a-8fba-716e340cce57)

### Resultados

Muestra los resultados o hallazgos obtenidos del proyecto.


![id_growing](https://github.com/Aruiz99/MEDCONECTA_test/assets/116668101/046c529c-c50b-4a11-826e-9f50982dfa1a)

## Uso


Explica cómo utilizar tu proyecto, proporciona ejemplos, capturas de pantalla y demostraciones si es posible.

## Estado del proyecto
Este proyecto se encuentra actualmente en una fase de desarrollo activa. Se pueden encontrar errores y funcionalidades incompletas. Se recomienda utilizarlo con precaución en cualquier entorno de producción.

## Licencia

```python
// Ejemplo de código
h = 1
python ´´´


![Captura de pantalla 2023-09-19 125746](https://github.com/Aruiz99/MEDCONECTA_test/assets/116668101/f701a90d-7db0-4183-84c2-3b7d4680496d)






