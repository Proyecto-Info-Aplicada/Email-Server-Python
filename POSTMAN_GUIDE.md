# Guía de Uso - Postman Collection

## 📥 Importar la Colección

1. **Abrir Postman**
2. Click en **"Import"** (esquina superior izquierda)
3. Seleccionar **"Upload Files"**
4. Buscar y seleccionar: `Email-Server-Postman-Collection.json`
5. Click en **"Import"**

## 📋 Contenido de la Colección

La colección incluye **5 requests organizados**:

### 1. Health Check (GET /)
- **Propósito:** Verificar que el servidor está corriendo
- **URL:** `http://localhost:5001/`
- **Respuesta esperada:**
```json
{
  "message": "Email Server corriendo correctamente ✅"
}
```

### 2. Health Check Endpoint (GET /health)
- **Propósito:** Health check específico del servicio
- **URL:** `http://localhost:5001/health`
- **Respuesta esperada:**
```json
{
  "status": "healthy",
  "service": "email-server"
}
```

### 3. Enviar Email con PDF (POST /send-email-task)
- **Propósito:** Request completo con todos los campos
- **Incluye:** Script pre-request que genera UUID automático
- **Body:**
```json
{
    "CorrelationId": "{{correlation_id}}",
    "EmailAddress": "destinatario@example.com",
    "Subject": "Reporte generado automáticamente",
    "MessageBody": "Estimado usuario,\n\nAdjunto encontrará su documento PDF solicitado.",
    "PdfFileName": "reporte.pdf"
}
```

### 4. Enviar Email - Ejemplo Mínimo
- **Propósito:** Solo campos obligatorios
- **Usa valores por defecto** para campos opcionales
- **Body:**
```json
{
    "CorrelationId": "abc123-def456-ghi789",
    "EmailAddress": "test@example.com"
}
```

### 5. Enviar Email - Ejemplo Completo
- **Propósito:** Caso de uso real (facturación)
- **Todos los campos personalizados**
- **Body:**
```json
{
    "CorrelationId": "550e8400-e29b-41d4-a716-446655440000",
    "EmailAddress": "cliente@empresa.com",
    "Subject": "Factura Electrónica - Mes de Octubre 2025",
    "MessageBody": "Estimado cliente...",
    "PdfFileName": "factura_octubre_2025.pdf"
}
```

## 🔧 Variables de Colección

La colección incluye variables pre-configuradas:

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `base_url` | `http://localhost:5001` | URL base del servidor |
| `correlation_id` | (auto-generado) | UUID generado automáticamente |

### Modificar Variables

1. Click en la colección **"Email Server Python API"**
2. Ir a la pestaña **"Variables"**
3. Editar el valor según necesites
4. Click en **"Save"**

## 📝 Ejemplos de Respuestas

### ✅ Respuesta Exitosa (200 OK)
```json
{
    "status": "success",
    "message": "Correo enviado correctamente a usuario@ejemplo.com"
}
```

### ❌ Error - Falta campo obligatorio (400 Bad Request)
```json
{
    "error": "Falta el campo 'EmailAddress'"
}
```

### ❌ Error - JSON inválido (400 Bad Request)
```json
{
    "error": "No se envió JSON"
}
```

### ❌ Error del servidor (500 Internal Server Error)
```json
{
    "error": "Descripción del error interno"
}
```

## 🧪 Cómo Probar

### Paso 1: Verificar que el servidor está corriendo
1. Ejecutar el request: **"Health Check"**
2. Debe retornar status `200 OK`

### Paso 2: Preparar el Storage Server
**Importante:** El Email Server obtiene los PDFs desde un Storage Server.

Asegúrate de que:
- El Storage Server está corriendo en `http://localhost:5000`
- Existe un PDF con el `CorrelationId` que vas a usar
- El endpoint del Storage es: `GET /pdf-storage/{correlationId}`

### Paso 3: Enviar un email de prueba

#### Opción A - Con campos mínimos:
1. Ejecutar: **"Enviar Email - Ejemplo Mínimo"**
2. Modificar el `CorrelationId` con un ID válido de tu Storage
3. Modificar el `EmailAddress` con tu email de prueba
4. Click en **"Send"**

#### Opción B - Personalizado completo:
1. Ejecutar: **"Enviar Email - Ejemplo Completo"**
2. Personalizar todos los campos según tu necesidad
3. Click en **"Send"**

### Paso 4: Verificar el resultado
- ✅ Status `200`: Email enviado exitosamente
- ❌ Status `400`: Error de validación (revisar campos)
- ❌ Status `500`: Error del servidor (revisar logs)

## 🔍 Debugging

### Ver logs del servidor
Los logs se guardan en: `logs/email-server.log`

### Errores comunes

**1. Connection refused**
- ✅ Verificar que el servidor está corriendo en puerto 5001

**2. "Error al obtener PDF"**
- ✅ Verificar que el Storage Server está corriendo
- ✅ Verificar que el `CorrelationId` existe en el Storage

**3. "Error al enviar correo"**
- ✅ Verificar que `credentials.json` está configurado
- ✅ Verificar autenticación OAuth (primera vez abre navegador)

## 🎯 Tips

### Generar UUIDs automáticos
El request "Enviar Email con PDF" incluye un script que genera UUIDs automáticos.

Para usar en otros requests:
```javascript
pm.variables.set('correlation_id', pm.variables.replaceIn('{{$randomUUID}}'));
```

### Cambiar el servidor destino
Si el servidor corre en otra URL:
1. Editar variable `base_url`
2. O cambiar directamente en cada request

### Guardar respuestas
1. Después de un request exitoso
2. Click en **"Save Response"**
3. Click en **"Save as Example"**

## 📞 Soporte

Si tienes problemas:
1. Verificar logs en `logs/email-server.log`
2. Revisar que todas las dependencias estén instaladas
3. Verificar configuración de Gmail API
4. Consultar `README.md` y `ARCHITECTURE.md`

---

**Última actualización:** 2025-10-22
