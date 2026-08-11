# Casos de validación

Este directorio se reserva para casos reproducibles y anonimizados.

## Reglas

- No almacenar PDFs personales originales.
- No incluir nombres, cédulas, números de Seguro Social ni otros identificadores.
- Preferir pruebas automatizadas con datos mínimos.
- Registrar en `docs/VALIDACION.md` el propósito del caso y el resultado esperado.
- Los documentos originales, si se conservan localmente para contraste, deben ubicarse en `tests/casos_validacion/originales/`, ruta ignorada por Git.

Las pruebas automatizadas del proyecto se ejecutan con:

```powershell
python -m unittest discover -s tests -v
```
