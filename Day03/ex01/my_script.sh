#!/bin/sh

LOG_FILE="install.log"
PATH_PY_URL="https://github.com/jaraco/path.git"
VENE_DIR="local_lib"
PROGRAM="my_program.py"

# Vérifiez si virtualenv est installé, sinon installe
if ! command -v virtualenv &> /dev/null
then
    echo "virtualenv n'est pas installé. Installation..."
    pip install --user virtualenv
    # Ajoute le chemin de virtualenv à PATH
    export PATH=$PATH:~/.local/bin
fi

# Crée un environnement virtuel
virtualenv --python=python3 $VENE_DIR

# Active l'environnement virtuel
. $VENE_DIR/bin/activate

pip --version

# Installe le module path.py
pip install --log $LOG_FILE --force-reinstall git+$PATH_PY_URL

# Exécuter le programme Python
python $PROGRAM