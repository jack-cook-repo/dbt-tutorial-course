#
# cd into a new virtualenv directory and source this file
# *DO NOT RUN IT*
#

if [ -d "./env" ]; then
    echo "Virtual Environment already exists.Only activation is required."  
    source env/bin/activate
else
    python3 -m venv env
    source env/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
fi
