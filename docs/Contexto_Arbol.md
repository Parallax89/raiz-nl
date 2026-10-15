# Contexto — Portal de donación de árboles

Hackathon Grok Monterrey. Documento para el equipo.

Fecha: 14 de octubre de 2026.

Este archivo fija la idea, las correcciones de fondo y el plan de desarrollo. Sirve para alinear discurso, mapa y producto antes de construir.

## De dónde sale

La minuta del evento planteaba tres retos. Este proyecto combina el 1 y el 3. El reto 2 (uso del agua del Río Bravo y evidencia ante la CILA) queda fuera.

El hackathon es de comunidad tecnológica en Monterrey, con problemas locales. Equipos de hasta 4 personas y de 2 a 2.5 horas. Entregables: código en repositorio, video demo y presentación en vivo opcional.

- **Reto 1.** Infiltración y restauración en la sierra después de incendios. Las cuencas que importan son las que alimentan las presas de abastecimiento: San Juan, Ramos, Pilón y Santa Catarina hacia El Cuchillo, más La Boca.
- **Reto 3.** Calidad del aire en la zona metropolitana. Las zonas que se nombraron son Pesquería, Cadereyta, Juárez y Santa Catarina, además de García, Apodaca y la industria del poniente. La refinería de Cadereyta es la fuente de SO₂ que más se cita.

## La idea

Un portal donde una persona dona un árbol y elige el propósito:

1. Restaurar cuenca quemada que aporta agua a las presas, o
2. Sumar arbolado donde la zona metropolitana tiene peor aire y menos sombra.

Después ve un mapa corto, con las zonas prioritarias de ese propósito, y elige una. Si quiere, se publica en una cuenta de X y se le etiqueta. El texto de esa publicación lo confirma antes.

La idea es pertinente. El ciudadano elige un propósito y el mapa le enseña lugares distintos. Hay que corregir qué promete cada árbol.

## Correcciones de fondo

### 1. El árbol de sierra no sube el nivel de la presa

Reforestar entra solo donde se cruzan tres cosas:

- hay cicatriz de incendio,
- esa ladera escurre hacia una presa de abastecimiento,
- el terreno se puede plantar y mantener.

Para Monterrey esas presas son El Cuchillo (ríos San Juan, Ramos, Pilón y Santa Catarina), La Boca y, si se incluye el acueducto, Cerro Prieto.

El efecto defendible de plantar ahí es sujetar suelo, bajar el azolve y frenar el pico de escurrimiento en laderas que perdieron cobertura. Eso protege la cuenca y la infraestructura. No es un litro nuevo en la cortina.

La baja de El Cuchillo, de 80–85% a cerca de 50%, la empujan la extracción y la sequía. De la presa salen unos 5 m³/s para el segundo acueducto, y la ciudad requiere del orden de 16 m³/s. Esa historia no se le atribuye al árbol.

Lampazos, parte de Galeana y Doctor Arroyo pueden tener cicatriz y aun así quedarse fuera: no alimentan esas presas. La máscara de cuenca es la que decide, no el hecho de que haya habido fuego en el estado.

La cifra de 17,000 hectáreas no se usa como dato del mapa hasta tener fuente, años y polígono. Los incendios recientes que sí están documentados son más chicos y sirven como candidatos a revisar, no como lista cerrada:

| Sitio | Cuándo | Magnitud reportada | Nota |
|---|---|---|---|
| Los Cuartones y Ciénega de González, Santiago | Mayo 2024 | Hasta 400 ha con el fuego aún activo | Cumbres. Hay que confirmar que la cuenca cae a La Boca o a El Cuchillo. |
| Las Adjuntas / Los Mauricios, Santiago | Febrero 2024 | 14–15 ha | Parque Nacional Cumbres de Monterrey. |
| La Purísima, Iturbide | Enero 2024 | Unas 85 ha | Cabeza de cuenca del sur. Confirmar presa de destino. |
| Puerto de Dolores, Doctor Arroyo | Mayo 2024 | 250–260 ha | Candidato débil: probable fuera de la cuenca de abastecimiento. |
| Cañón de Vacas, Aramberri | Abril 2025 | Cerca de 279 ha | Igual: filtrar por cuenca antes de mostrarlo. |
| La Esperanza, Galeana | Mayo 2025 | 300 ha | Igual. |
| Sierra de Lampazos | Agosto 2026 | 45 ha | No aporta a El Cuchillo. |

Santa Catarina municipio no es un solo punto. La sierra (Huasteca, Cumbres) puede ir al mapa de agua si la cuenca cuadra. La zona urbana e industrial va al mapa de aire.

El nombre "Las Indias", que apareció en la minuta como río, no está confirmado. No se usa en materiales hasta ubicar el cauce.

### 2. El árbol urbano no apaga la refinería

Pesquería, Cadereyta, Juárez, Santa Catarina, García y Apodaca sí son el territorio del segundo propósito. Lo que se prioriza es colonia con gente, poca copa y peor aire, en parque, camellón, escuela o borde de río donde haya quien plante.

Plantar en la cerca de la refinería no baja el SO₂. El árbol cambia sombra, calor y, muy localmente, partículas. El texto del portal dice eso.

Para la primera versión bastan las estaciones del SIMA y una capa de déficit de arbolado. Sentinel-2 no mide SO₂, NO₂ ni CO. Esos gases están en Sentinel-5P (TROPOMI) y no hacen falta para elegir las primeras colonias. Las muertes atribuidas a la contaminación son una estimación de carga de enfermedad, ligada sobre todo a PM2.5. No se presentan como un conteo de actas de defunción ni como algo que este árbol vaya a revertir.

### 3. Un árbol sin quien lo plante es un mapa de intenciones

Cada zona de la lista tiene un operador: ejido, municipio, parque, Pronatura Noreste u otra organización que reciba la planta. Dentro del Parque Nacional Cumbres de Monterrey no se planta sin la regla del área protegida.

El precio, cuando exista, incluye planta, plantación y mantenimiento. En Nuevo León, sin riego de establecimiento, la mayoría de los árboles no pasa el primer verano. El contador público dice "donados" mientras no haya plantación. "Plantados" y "vivos a 12 meses" entran cuando haya verificación.

## Cómo queda el producto

Una pregunta, dos mapas, pocos sitios.

1. La persona elige: restauración de cuenca o arbolado urbano.
2. Ve de 5 a 8 zonas, no una capa infinita.
3. Cada zona es una ficha con municipio, la razón en una frase, la presa a la que aporta o la estación del SIMA más cercana, cuántos árboles caben, cuántos van y quién planta.
4. Elige zona y número de árboles.
5. Ve el texto de la publicación y decide si se etiqueta. Sin ese visto bueno no hay etiqueta ni post.

### Textos que sí se pueden publicar

- Agua: "Donaron un árbol para restaurar [Los Cuartones], cuenca que aporta a El Cuchillo."
- Aire: "Donaron un árbol para arbolado en [colonia], una zona de [Juárez] con poca sombra y mala calidad del aire."

### Texto que no se publica

"Acaban de donar un árbol para mejorar el suministro de agua en el área metropolitana."

Promete litros que ese árbol no va a meter a la presa.

## Cómo se prioriza

**Agua.** Cicatriz reciente, dentro de la cuenca de una presa de abastecimiento, pendiente plantable (tope operativo de 30–35°), suelo desnudo o degradado, y alguien que deje entrar a la brigada.

Queda fuera lo que tenga pendiente mayor a 35°, bosque ya cerrado, mancha urbana, cuerpo de agua o predio sin acuerdo.

**Aire.** Peor aire medido, más gente, menos árboles, y un predio público o acordado donde quepa la planta.

La ficha explica esa razón en lenguaje llano. La fórmula se documenta en el método, a la vista de quien quiera revisarla.

## Plan de desarrollo

### Fase 1. Reglas y lista corta

Definir cuencas (El Cuchillo, La Boca y, si aplica, Cerro Prieto), máscara de exclusión y fichas de 5 a 8 sitios de agua y 5 a 8 de aire.

Datos: cicatrices de CONAFOR o severidad con Sentinel-2, subcuencas, modelo de elevación, pendiente, cobertura, estaciones del SIMA y mancha urbana.

Entregable: un GeoJSON y una ficha por sitio, más la lista de sitios descartados y el motivo. Aquí se cierra el discurso.

### Fase 2. Mapa estático

Una página con la pregunta inicial, los dos mapas y las fichas. Sin pago y sin X. La prueba es si una persona distingue cuenca y colonia en un minuto.

Stack: MapLibre y los GeoJSON de la fase 1.

### Fase 3. Donación simbólica y publicación

Apartar árboles contra la meta del sitio, vista previa del texto y publicación solo con permiso. Tras el visto bueno, un bot con las llaves de la cuenta publica el texto confirmado. Sin ese visto bueno no hay etiqueta ni post.

### Fase 4. Operación real

Precio con mantenimiento, receptor por sitio, especie según altitud (pino y encino en sierra; especies urbanas ya probadas en la ciudad), meta de sobrevivencia a 12 meses y permiso en área natural protegida.

## Qué no se construye todavía

- Pasarela de pago.
- Inventario de emisiones.
- Modelo satelital de gases.
- Mapa con todos los incendios del estado, sin filtro de cuenca.

Esas piezas no cambian la lista corta ni la credibilidad del texto.

## Siguiente corte

La fase 1: dos listas, máscara de exclusión y texto de cada ficha. Con eso se ve si el portal dice la verdad antes de diseñar la donación.

## Fuentes de este contexto

- Minuta "Pospuesto - Grok Monterrey Hackathon" (14 de octubre de 2026).
- Revisión de publicaciones en X sobre incendios forestales en Nuevo León, de octubre de 2023 a octubre de 2026. Es una detección de eventos que circularon en medios y en Protección Civil Nuevo León, no un censo oficial de CONAFOR.
- Correcciones de método: la cicatriz y la cuenca mandan sobre la hectárea redonda; Sentinel-2 no mide los gases del reto 3; el agua de tratado, el riego de Tamaulipas y el vaciado de El Cuchillo son cuentas distintas y no entran en este producto.
