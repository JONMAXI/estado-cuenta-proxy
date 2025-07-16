# Usa una imagen oficial de Python
FROM python:3.10-slim

# Crea y usa un directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expón el puerto por default
EXPOSE 8080

# Ejecuta la app
CMD ["python", "app.py"]
