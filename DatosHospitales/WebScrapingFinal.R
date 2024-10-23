# Cargar el paquete necesario
library(rvest)
library(stringr)
library(dplyr)


# Lista de identificadores de hospitales
identificadores <- c("110051","110327","140230","140044","180016","180150","230011","230011","290017","290022","290069","410021","410042","040059","210123","390015","090155","240016","370037","470029","080667","080958","030165","030015","460018","280989","281315","200261","480078","480176","260027")

# Crear una lista para almacenar los datos de cada hospital
datos_hospitales <- list()

# Recorrer la lista de identificadores y obtener los datos de cada hospital
for (identificador in identificadores) {
  # Definir la URL para el hospital actual
  url <- paste0("https://www.sanidad.gob.es/ciudadanos/centros.do?metodo=realizarDetalle&tipo=hospital&numero=", identificador)
  
  # Realizar la solicitud HTTP y parsear la página
  page <- read_html(url)
  
  # Encontrar la tabla "datos generales del hospital seleccionado"
  tabla_datos_generales <- page %>% html_node(xpath = '//*[@summary="datos generales del hospital seleccionado"]')
  
  if (!is.null(tabla_datos_generales)) {
    # Extraer los datos de la tabla
    datos <- tabla_datos_generales %>%
      html_table() %>%
      as.data.frame()
    
    # Limpiar los datos en la variable "datos" eliminando \r, \n y \t
    datos <- datos %>%
      mutate_all(~str_replace_all(., "[\r\n\t]", ""))
    
    # Transponer la tabla para invertir filas y columnas
    datos_invertidos <- as.data.frame(t(datos))
    
    # Establecer la primera fila como nombres de columna
    colnames(datos_invertidos) <- datos_invertidos[1, ]
    datos_invertidos <- datos_invertidos[-1, ]  # Eliminar la primera fila
    
    # Almacenar los datos del hospital en la lista
    datos_hospitales[[identificador]] <- datos_invertidos
  } else {
    cat("No se encontró la tabla 'datos generales del hospital seleccionado' para el identificador ", identificador, "\n")
  }
}

# Crear un DataFrame con los datos de todos los hospitales
datos_completos <- do.call(rbind, datos_hospitales)

# Ruta al archivo CSV donde se guardará la información de todos los hospitales
archivo_csv_completo <- "datos_hospitales_completo.csv"

# Guardar los datos de todos los hospitales en un archivo CSV
write.csv(datos_completos, file = archivo_csv_completo, row.names = FALSE)

# Imprimir un mensaje de confirmación
cat("Los datos de todos los hospitales se han guardado en", archivo_csv_completo, "\n")
