#!/bin/sh

cd .. 

# Solicitar los inputs al usuario
read -p "  ~~~~>_  Por favor, indique los archivos a agregar al commit (. para todos): " commit_file
read -p "  ~~~~>_  Por favor, indique un mensaje para el commit: " commit_message
read -p "  ~~~~>_  Por favor, indique la rama donde se enviara su commit: " commit_branch

# Construir los comandos
add_files="git add $commit_file"
add_message="git commit -m '$commit_message'" 
send_push="git push -u origin $commit_branch"

# Ejecutar los comandos
echo "  ~~~~>_  Agregando archivos...  "
echo "$add_files"
eval $add_files

echo "  ~~~~>_  Agregando mensaje...  "
echo "$add_message"
eval $add_message

echo "  ~~~~>_  Enviando commit...  "
echo "$send_push"
eval $send_push
