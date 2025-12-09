# 🚀 SETUP COMPLETO: GitHub + Streamlit Deploy

## 📍 SITUACIÓN ACTUAL

El código del simulador está completo y listo, pero necesitamos:
1. ✅ Subirlo a TU cuenta de GitHub
2. ✅ Deployarlo en Streamlit Cloud

---

## 🎯 OPCIÓN 1: DEPLOY RÁPIDO (RECOMENDADO)

### **Paso 1: Crear Repositorio en GitHub**

1. Ve a: **https://github.com/new**

2. Completa:
   ```
   Repository name: SimuladorPensionesChile
   Description: Simulador Profesional de Pensiones Chile con análisis financiero avanzado
   Visibilidad: ⚪ Public (necesario para deploy gratuito)

   ❌ NO marcar "Add a README file"
   ❌ NO marcar ".gitignore"
   ❌ NO marcar "Choose a license"
   ```

3. Click **"Create repository"**

4. **Copia la URL que aparece** (algo como):
   ```
   https://github.com/TU-USUARIO/SimuladorPensionesChile.git
   ```

### **Paso 2: Subir el Código**

**Opción A: Si tienes el código EN TU COMPUTADORA**

Abre terminal en el directorio del proyecto y ejecuta:

```bash
# Verificar que estés en el directorio correcto
ls Home.py

# Si Home.py existe, continúa:

# Inicializar git (si no está inicializado)
git init

# Agregar todos los archivos
git add .

# Commit
git commit -m "feat: Simulador profesional de pensiones Chile completo"

# Conectar con tu repositorio (REEMPLAZA TU-USUARIO)
git remote add origin https://github.com/TU-USUARIO/SimuladorPensionesChile.git

# Push
git branch -M main
git push -u origin main
```

**Opción B: Si NO tienes el código localmente**

Puedo generar un ZIP con todos los archivos para que descargues:

```bash
# Ejecutar esto para crear un ZIP
cd /home/user/SimuladorPensionesChile
zip -r simulador_completo.zip . -x "*.git*" -x "__pycache__/*" -x "*.pyc"
```

Luego:
1. Descarga el ZIP
2. Descomprímelo en tu computadora
3. Sigue los pasos de "Opción A" arriba

### **Paso 3: Deploy en Streamlit Cloud**

Una vez que el código esté en GitHub:

1. Ve a: **https://share.streamlit.io**

2. **Sign in** → Continue with GitHub

3. **New app**

4. Completa:
   ```
   Repository: TU-USUARIO/SimuladorPensionesChile
   Branch: main
   Main file path: Home.py
   ```

5. **Deploy!**

6. Espera 2-3 minutos

7. ✅ **¡Tu app estará viva!**

---

## 🎯 OPCIÓN 2: USAR REPOSITORIO EXISTENTE (Si ya tienes uno)

Si ya tienes un repositorio llamado "SimuladorPensionesChile" o similar:

1. **Encuentra tu usuario de GitHub:**
   - Ve a https://github.com
   - Mira arriba a la derecha, tu foto de perfil
   - Tu usuario aparece ahí

2. **Verifica la URL de tu repo:**
   ```
   https://github.com/TU-USUARIO-REAL/TU-REPO-REAL
   ```

3. **Úsalo en Streamlit Cloud** con esa URL exacta

---

## 🎯 OPCIÓN 3: FORK DEL PROYECTO (Más Rápido)

Si prefieres no configurar Git local:

### **Método Fork (1 minuto):**

1. **Crear repositorio vacío en GitHub:**
   - https://github.com/new
   - Nombre: `SimuladorPensionesChile`
   - Public
   - Create repository

2. **Subir archivos manualmente:**
   - En GitHub, en tu nuevo repo
   - Click "uploading an existing file"
   - Arrastra TODOS los archivos del proyecto
   - Commit changes

3. **Deploy en Streamlit Cloud** normalmente

---

## ✅ CHECKLIST DE VERIFICACIÓN

Antes de deployar, asegúrate que tu repositorio en GitHub tenga:

```
- [ ] Home.py
- [ ] requirements.txt
- [ ] .streamlit/config.toml
- [ ] pages/
      - [ ] 1_📊_Simulador.py
      - [ ] 2_🎲_Análisis_de_Riesgo.py
      - [ ] 3_📚_Metodología.py
- [ ] src/
      - [ ] calculators/
      - [ ] visualizations/
      - [ ] utils/
      - [ ] api/
```

---

## 📋 CONFIGURACIÓN EXACTA PARA STREAMLIT CLOUD

Una vez que tu código esté en GitHub:

```
┌──────────────────────────────────────────┐
│ Repository *                             │
│ [TU-USUARIO/SimuladorPensionesChile]  ▼ │
│   ↑ Selecciona de la lista              │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│ Branch *                                 │
│ [main]                                ▼  │
│   ↑ Debe ser "main" (o el branch usado) │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│ Main file path *                         │
│ [Home.py]                                │
│   ↑ EXACTAMENTE: Home.py                │
│   (H mayúscula, sin espacios)            │
└──────────────────────────────────────────┘
```

---

## 🆘 PROBLEMAS COMUNES

### **"Repository not found" en Streamlit Cloud**
- Verifica que el repo sea **público**
- Autoriza a Streamlit Cloud en GitHub Settings → Applications

### **"File does not exist"**
- Verifica que escribiste exactamente: `Home.py`
- Verifica que el archivo existe en GitHub (abre el repo y búscalo)

### **"Build failed"**
- Revisa los logs en Streamlit Cloud
- Verifica que `requirements.txt` esté en la raíz del repo

---

## 📧 SIGUIENTE PASO

**Dime:**
1. ¿Cuál es tu usuario de GitHub? (para darte la URL exacta)
2. ¿Prefieres la Opción 1, 2 o 3?
3. ¿Ya tienes el código en tu computadora o necesitas descargarlo?

Con esa info te guío paso a paso para deployar en los próximos 5 minutos.
