# 🚀 Guía de Deploy en Streamlit Cloud

## Pasos para Deploy GRATIS en Streamlit Cloud

### 1️⃣ Preparar el Repositorio en GitHub

```bash
# Asegurarse de estar en el directorio del proyecto
cd SimuladorPensionesChile

# Inicializar git (si no está inicializado)
git init

# Agregar archivos
git add .

# Commit
git commit -m "feat: Simulador profesional de pensiones Chile completo"

# Conectar con GitHub
git remote add origin https://github.com/TU-USUARIO/SimuladorPensionesChile.git

# Push
git push -u origin main
```

### 2️⃣ Deploy en Streamlit Cloud

1. **Ir a:** [share.streamlit.io](https://share.streamlit.io)

2. **Sign in** con GitHub

3. **New app** → Seleccionar:
   - Repository: `TU-USUARIO/SimuladorPensionesChile`
   - Branch: `main`
   - Main file path: `Home.py`

4. **Deploy!**

5. Tu app estará en: `https://TU-USUARIO-simuladorpensioneschile.streamlit.app`

### 3️⃣ Configuración Avanzada (Opcional)

Si quieres personalizar la URL o configurar secrets:

**Secrets** (si usaras APIs con keys):
```toml
# En Streamlit Cloud > Settings > Secrets
[api]
key = "tu-api-key"
```

**Configuración Custom Domain:**
1. Streamlit Cloud > Settings
2. Custom subdomain: `pension-simulator`
3. URL final: `pension-simulator.streamlit.app`

## ✅ Verificación Post-Deploy

- [ ] App carga correctamente
- [ ] Página Home se ve bien
- [ ] Simulador funciona
- [ ] APIs obtienen datos (UF, inflación)
- [ ] Gráficos se renderizan
- [ ] PDFs se generan
- [ ] No hay errores en logs

## 🐛 Troubleshooting

### Error: ModuleNotFoundError

**Solución:** Verificar que `requirements.txt` tenga todas las dependencias.

```bash
pip freeze > requirements.txt
```

### Error: API timeout

**Solución:** Las APIs externas pueden fallar ocasionalmente. El código tiene valores por defecto (fallback).

### Error: Memory limit

**Solución:** Streamlit Cloud gratis tiene límites de RAM. Reducir:
- Tamaño de simulaciones Monte Carlo
- Cache de datos
- Número de gráficos simultáneos

## 📊 Monitoreo

Una vez deployed:

1. **Analytics:** Streamlit Cloud muestra:
   - Visitantes diarios
   - Tiempo de uso
   - Errores

2. **Logs:** Acceder en tiempo real desde el dashboard

3. **Updates:** Cada push a `main` redeploya automáticamente

## 🔄 Actualizar la App

```bash
# Hacer cambios
git add .
git commit -m "fix: mejora en cálculo de pensiones"
git push

# Streamlit Cloud detecta el push y redeploya automáticamente ⚡
```

## 💡 Tips Pro

### Agregar un Badge al README

```markdown
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://tu-app.streamlit.app)
```

### Optimizar Performance

```python
# Usar cache en funciones pesadas
import streamlit as st

@st.cache_data(ttl=3600)  # Cache por 1 hora
def cargar_datos_pesados():
    return data_fetcher.obtener_datos_completos()
```

### Analytics con Google

Agregar en `.streamlit/config.toml`:

```toml
[browser]
gatherUsageStats = false  # Desactivar analytics de Streamlit

# Usar Google Analytics en el HTML/JS custom
```

## 🎉 ¡Listo!

Tu simulador estará 100% funcional y **GRATIS** en Streamlit Cloud.

**Límites gratuitos:**
- Apps ilimitadas
- Recursos compartidos
- Sin límite de visitantes (dentro de lo razonable)
- Deploy automático
- SSL incluido
- Uptime 24/7

**Para upgrade a Teams/Enterprise:**
- Más recursos
- Autenticación custom
- Prioridad en soporte
- Analytics avanzados

Pero para uso personal/educativo/pequeños clientes: **el plan gratuito es perfecto** ✅
