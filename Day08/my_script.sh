
LOG_FILE="pip_install.log"
PYTHON_PATH="/usr/bin/python3"
VENE_DIR="django_venv"

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

# pip version
pip --version

# pip install
pip install --force-reinstall -r requirement.txt