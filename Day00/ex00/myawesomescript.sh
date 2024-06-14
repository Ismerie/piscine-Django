#!/bin/sh

# Vérifie qu´il y a exactement un argument et suit la redirection
if [ "$#" -eq 1 ]; then
    curl -s -I "$1" | grep -i ^location: | cut -d ' ' -f2
fi