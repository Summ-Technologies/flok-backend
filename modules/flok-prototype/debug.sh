# Run this from the root of the repo and ensure your .env file exists
FLASK_APP=$PWD/modules/flok-prototype/server/ APP_CONFIG=$PWD/modules/flok-prototype/config.py env $(cat .env) flask run --host 0.0.0.0
