# Export Invoices Guide - For Your Friend

## 📋 Quick Export Instructions (Spanish)

### Paso 1: Exportar Facturas de Cliente 2024-2025

1. **Ir a:** Contabilidad → Clientes → Facturas
   - O: Facturación → Clientes → Facturas

2. **Filtrar por fecha:**
   - Click en "Filtros"
   - Agregar filtro: "Fecha de factura"
   - Desde: 01/01/2024
   - Hasta: 31/12/2025
   - Aplicar

3. **Seleccionar todas:**
   - Click en checkbox arriba de la lista
   - Si hay más de 80, click "Seleccionar todas las X facturas"

4. **Exportar:**
   - Click: Acción → Exportar
   - Formato: CSV
   - Seleccionar campos:
     - ✅ Número (name)
     - ✅ Cliente (partner_id/name)
     - ✅ NIF Cliente (partner_id/vat)
     - ✅ Fecha de factura (invoice_date)
     - ✅ Fecha de vencimiento (invoice_date_due)
     - ✅ Estado (state)
     - ✅ Total (amount_total)
     - ✅ Impuestos (amount_tax)
     - ✅ Base imponible (amount_untaxed)
     - ✅ Condiciones de pago (invoice_payment_term_id/name)
     - ✅ Referencia (ref)
     - ✅ Origen (invoice_origin)
     - ✅ Moneda (currency_id/name)

5. **Guardar archivo:**
   - Nombre: `facturas_2024_2025.csv`
   - Enviar a tu amigo

---

### Paso 2: Exportar Líneas de Factura (Opcional pero Recomendado)

1. **Ir a:** Contabilidad → Configuración → Líneas de asiento contable
   - O buscar: "Líneas de factura"

2. **Filtrar:**
   - Tipo de movimiento: Factura de cliente
   - Fecha: 01/01/2024 - 31/12/2025

3. **Seleccionar todas y exportar:**
   - Campos:
     - ✅ Factura (move_id/name)
     - ✅ Producto (product_id/name)
     - ✅ Referencia interna (product_id/default_code)
     - ✅ Descripción (name)
     - ✅ Cantidad (quantity)
     - ✅ Precio unitario (price_unit)
     - ✅ Impuesto (tax_ids/name)
     - ✅ Subtotal (price_subtotal)
     - ✅ Total (price_total)

4. **Guardar:**
   - Nombre: `lineas_facturas_2024_2025.csv`

---

### Paso 3: Exportar Pagos (Opcional)

1. **Ir a:** Contabilidad → Clientes → Pagos

2. **Filtrar:**
   - Tipo: Pago entrante
   - Fecha: 2024-2025

3. **Exportar:**
   - Campos:
     - ✅ Número (name)
     - ✅ Cliente (partner_id/name)
     - ✅ Fecha (date)
     - ✅ Importe (amount)
     - ✅ Método de pago (payment_method_id/name)
     - ✅ Referencia (ref)
     - ✅ Estado (state)

4. **Guardar:**
   - Nombre: `pagos_2024_2025.csv`

---

## 🔍 Verificación

Después de exportar, verificar:

- ✅ Archivo no está vacío
- ✅ Tiene encabezados (primera línea)
- ✅ Número de líneas coincide con número de facturas
- ✅ Todos los campos tienen datos
- ✅ Fechas en formato correcto

---

## 📧 Enviar Archivos

**Opciones:**
1. Email (si < 25MB)
2. Google Drive / Dropbox
3. WeTransfer (gratis hasta 2GB)
4. OneDrive

**Archivos a enviar:**
- `facturas_2024_2025.csv` (requerido)
- `lineas_facturas_2024_2025.csv` (recomendado)
- `pagos_2024_2025.csv` (opcional)

---

## ❓ Preguntas Frecuentes

**P: ¿Cuántas facturas debería haber?**
R: Depende del negocio. Típicamente 200-2000 facturas por año.

**P: ¿Qué pasa si hay muchas facturas?**
R: Odoo puede exportar hasta 2000 a la vez. Si hay más, exportar por año.

**P: ¿Necesito exportar facturas borrador?**
R: No, solo facturas validadas (estado: Publicado/Pagado).

**P: ¿Y las facturas de 2026?**
R: Exportar separadamente después de validar 2024-2025.

**P: ¿Necesito acceso de administrador?**
R: Sí, o permisos de Contabilidad/Facturación.

---

## 🚨 Problemas Comunes

### Error: "No se puede exportar"
- Verificar permisos de usuario
- Intentar con menos registros
- Exportar por año separado

### Error: "Archivo muy grande"
- Exportar por año
- Exportar solo campos esenciales
- Usar formato CSV (no Excel)

### Error: "Caracteres extraños en CSV"
- Abrir con LibreOffice Calc
- Encoding: UTF-8
- Separador: coma

---

## 📞 Soporte

Si tiene problemas:
1. Tomar captura de pantalla del error
2. Contar cuántas facturas hay (aproximado)
3. Verificar versión de Odoo (Ayuda → Acerca de)
4. Contactar a tu amigo
