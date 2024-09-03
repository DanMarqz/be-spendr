#!/bin/sh

cd ..

# Solicitar los inputs al usuario
read -p "~~~~>_  Por favor, indique el nombre de la imagen: " image_name
read -p "~~~~>_  Por favor, indique el tag de la imagen: " image_tag
read -p "~~~~>_  Por favor, indique las variables de la imagen (Ejemplo: -e VAR1='VAR1' -e VAR2='VAR2' ): " image_variables

docker_image=$image_name:$image_tag

# Construir los comandos
build_command="docker build -t \"$docker_image\" ."
run_command="docker run -it --rm -p 5000:5000 $image_variables --name $image_name $docker_image"

# Ejecutar los comandos
echo "~~~~>_  Ejecutando comando de build: "
echo "$build_command"
eval $build_command

echo "~~~~>_  Ejecutando comando de run: "
echo "$run_command"
eval $run_command