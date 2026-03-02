# Guía de Configuración del Formato de Facturas en Odoo

## 📋 Configuración del Logo y Formato de Facturas

Esta guía te ayudará a personalizar el formato de tus facturas en Odoo Online, incluyendo el logo de la empresa.

---

## 1️⃣ Añadir el Logo de la Empresa

### Paso 1: Acceder a la Configuración de la Empresa
1. Ve a **Ajustes** (Settings) en el menú principal
2. En la sección **Empresas** (Companies), haz clic en **Actualizar información** (Update Info)
3. O ve directamente a: **Ajustes → Usuarios y Empresas → Empresas**

### Paso 2: Subir el Logo
1. Haz clic en el nombre de tu empresa (Exartia)
2. En la parte superior izquierda, verás un espacio para la imagen
3. Haz clic en el icono de la cámara o en el espacio de la imagen
4. Selecciona tu archivo de logo (PNG o JPG recomendado)
5. **Tamaño recomendado:** 300x100 píxeles o similar (proporción horizontal)
6. Haz clic en **Guardar**

**El logo aparecerá automáticamente en:**
- Facturas
- Presupuestos
- Albaranes
- Todos los documentos PDF

---

## 2️⃣ Configurar el Formato de las Facturas

### Opción A: Configuración Básica (Recomendado)

#### Paso 1: Diseño del Documento
1. Ve a **Ajustes → General Settings**
2. Busca la sección **Diseño de Documentos** (Document Layout)
3. Selecciona uno de los diseños predefinidos:
   - **Limpio** (Clean): Diseño minimalista
   - **Estándar** (Standard): Diseño clásico
   - **Moderno** (Modern): Diseño contemporáneo
   - **Boxed**: Con bordes y cajas

#### Paso 2: Colores de la Empresa
1. En la misma sección, configura:
   - **Color primario**: Color principal de tu marca
   - **Color secundario**: Color de acento
2. Estos colores se aplicarán a:
   - Encabezados de facturas
   - Líneas divisorias
   - Elementos destacados

#### Paso 3: Información de la Empresa
1. Ve a **Ajustes → Usuarios y Empresas → Empresas**
2. Edita tu empresa y completa:
   - **Nombre de la empresa**
   - **Dirección completa**
   - **Teléfono**
   - **Email**
   - **Sitio web**
   - **NIF/CIF**
3. Esta información aparecerá en todas las facturas

### Opción B: Personalización Avanzada (Requiere conocimientos técnicos)

Para personalización avanzada del diseño de facturas:

1. Ve a **Ajustes → Técnico → Vistas** (debes activar el modo desarrollador)
2. Busca la vista: `account.report_invoice_document`
3. Puedes crear una vista heredada para personalizar el diseño

**⚠️ Advertencia:** Esto requiere conocimientos de XML/QWeb. No recomendado sin experiencia técnica.

---

## 3️⃣ Configurar Pie de Página de Facturas

### Paso 1: Añadir Información Bancaria
1. Ve a **Contactos → Configuración → Cuentas Bancarias**
2. Añade las cuentas bancarias de tu empresa
3. Esta información aparecerá automáticamente en las facturas

### Paso 2: Añadir Texto Personalizado
1. Ve a **Ajustes → Usuarios y Empresas → Empresas**
2. Edita tu empresa
3. En la pestaña **Configuración**, busca **Pie de página de informes** (Report Footer)
4. Añade texto personalizado, por ejemplo:
   ```
   Gracias por su confianza
   Datos bancarios: IBAN ES12 3456 7890 1234 5678 9012
   ```

---

## 4️⃣ Configurar Términos y Condiciones

### Añadir Términos en Facturas
1. Ve a **Facturación → Configuración → Términos y Condiciones**
2. O edita una factura y añade términos en el campo **Términos y Condiciones**
3. Puedes crear plantillas predefinidas:
   - Ve a **Facturación → Configuración → Términos y Condiciones**
   - Crea nuevos términos
   - Selecciónalos al crear facturas

---

## 5️⃣ Vista Previa y Prueba

### Verificar el Formato
1. Abre cualquier factura (por ejemplo, INV/2025/00100)
2. Haz clic en **Imprimir → Factura**
3. Verifica que aparezca:
   - ✅ Logo de la empresa
   - ✅ Información de la empresa
   - ✅ Diseño seleccionado
   - ✅ Colores corporativos
   - ✅ Pie de página

### Ajustar si es Necesario
- Si el logo es muy grande/pequeño: Redimensiona la imagen y vuelve a subirla
- Si falta información: Completa los datos de la empresa
- Si no te gusta el diseño: Cambia el layout en Ajustes

---

## 6️⃣ Configuraciones Adicionales Útiles

### Numeración de Facturas
**Ya configurado:** Tus facturas continúan desde INV/2025/01140

Para cambiar el formato:
1. Ve a **Ajustes → Técnico → Secuencias**
2. Busca "Factura de Cliente" (Customer Invoice)
3. Edita el formato (por ejemplo: `FAC/%(year)s/%(seq)s`)

### Idioma de las Facturas
1. Ve a **Contactos** y abre un cliente
2. En la pestaña **Ventas y Compras**, selecciona el **Idioma**
3. Las facturas se generarán en ese idioma automáticamente

### Moneda
**Ya configurado:** EUR (Euro)

Para facturas en otras monedas:
1. Ve a **Facturación → Configuración → Monedas**
2. Activa las monedas necesarias
3. Selecciona la moneda al crear la factura

---

## 7️⃣ Plantillas de Email para Facturas

### Personalizar Email de Envío
1. Ve a **Ajustes → Técnico → Emails → Plantillas**
2. Busca "Factura: Enviar por email" (Invoice: Send by email)
3. Personaliza:
   - Asunto del email
   - Cuerpo del mensaje
   - Firma

**Ejemplo de mensaje personalizado:**
```
Estimado/a ${object.partner_id.name},

Adjuntamos la factura ${object.name} por un importe de ${object.amount_total} ${object.currency_id.symbol}.

Gracias por su confianza.

Saludos cordiales,
${user.name}
${user.company_id.name}
```

---

## 8️⃣ Checklist Final

Antes de enviar facturas a clientes, verifica:

- [ ] Logo de la empresa subido y visible
- [ ] Información de la empresa completa (dirección, teléfono, email, NIF)
- [ ] Diseño de documento seleccionado
- [ ] Colores corporativos configurados
- [ ] Cuentas bancarias añadidas
- [ ] Pie de página personalizado (si aplica)
- [ ] Términos y condiciones añadidos (si aplica)
- [ ] Vista previa de factura correcta
- [ ] Plantilla de email personalizada (opcional)

---

## 🎨 Consejos de Diseño

### Logo
- **Formato:** PNG con fondo transparente (recomendado)
- **Tamaño:** 300x100 px o 600x200 px (para alta resolución)
- **Peso:** Menos de 500 KB
- **Proporción:** Horizontal (3:1 o 2:1)

### Colores
- Usa los colores de tu marca corporativa
- El color primario debe tener buen contraste con blanco
- Evita colores muy brillantes o neón

### Información
- Mantén la información concisa
- Incluye solo datos relevantes
- Verifica que el NIF/CIF sea correcto

---

## ❓ Problemas Comunes

### El logo no aparece en el PDF
- **Solución:** Limpia la caché del navegador (Ctrl+F5)
- Verifica que el logo esté guardado en la empresa
- Regenera el PDF de la factura

### El diseño no cambia
- **Solución:** Guarda los cambios en Ajustes
- Espera unos segundos y recarga la página
- Regenera el PDF de la factura

### La información no se actualiza
- **Solución:** Verifica que hayas guardado los cambios
- Comprueba que estás editando la empresa correcta
- Cierra sesión y vuelve a entrar

---

## 📞 Soporte

Si necesitas ayuda adicional:
1. Consulta la documentación oficial de Odoo: https://www.odoo.com/documentation
2. Contacta con soporte de Odoo Online
3. Busca en el foro de la comunidad: https://www.odoo.com/forum

---

**¡Listo! Tus facturas ahora tendrán un aspecto profesional con tu logo y formato personalizado.**
