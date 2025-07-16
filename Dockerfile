# Usa una imagen oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos
COPY . .

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 8080 (el que usa Cloud Run)
EXPOSE 8080

# Comando para ejecutar la app
CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app"]
