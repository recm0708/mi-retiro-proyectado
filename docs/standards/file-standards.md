# Estándares de archivos

## Propósito

Define los criterios mínimos que deben cumplir los archivos nuevos del proyecto.

Las reglas específicas de estructura interna por extensión pueden mantenerse en
políticas técnicas especializadas siempre que no contradigan los estándares
NOR.1.

## Código fuente

Debe contener:

- propósito claro;
- responsabilidad delimitada;
- estructura mantenible;
- comentarios únicamente cuando aporten información útil;
- documentación cuando exista lógica compleja;
- nombre y ubicación conformes con `naming-conventions.md`.

## Documentación

Debe indicar claramente:

- objetivo;
- alcance;
- estado cuando corresponda;
- relación con otros documentos;
- condición de documento vigente, auditoría o histórico cuando pueda ser ambigua.

## Archivos JSON

Deben mantener formato válido y una estructura clara.

Los datos normativos conservan los nombres oficiales definidos por la fuente.
La nomenclatura del archivo no autoriza cambiar claves o valores cuyo significado
forme parte de un contrato regulatorio o de datos.

## Pruebas

Las pruebas deben ubicarse bajo `tests/`, seguir la convención `test_*.py` cuando
sean pruebas Python y expresar el contrato permanente que protegen.

Los identificadores históricos pueden conservarse cuando sean necesarios para
demostrar una regresión concreta.

## Evidencias de auditoría

Una evidencia se versiona solamente cuando:

- aporta trazabilidad durable;
- es compatible con los invariantes del repositorio;
- tiene una ubicación canónica bajo `docs/audits/`;
- puede mantenerse sin convertir el repositorio en almacenamiento de volcados.

Cuando un resultado sea reproducible y su volcado bruto sea temporal, local,
muy voluminoso o contenga patrones que no deben reintroducirse, se documentan el
comando, el conteo y los hallazgos relevantes sin versionar el volcado.

## Archivos temporales y locales

Los archivos generados durante revisiones, pruebas o auditorías no deben
permanecer en ubicaciones permanentes sin una razón documentada.

Los paquetes `.zip`, copias de trabajo, parches locales, logs e inventarios
temporales siguen `root-and-local-artifacts.md` y `.gitignore`.
