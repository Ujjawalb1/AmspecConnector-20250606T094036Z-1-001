
cd "$(dirname "$0")" || exit
source venv/Scripts/activate
python src/invoice_package/main.py
