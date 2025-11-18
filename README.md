Before starting, you gotta've an empty database, just create one in postgresql
cp .env.example .env
Then edit .env with your actual credentials from postgresql
create a virtual enviroment first, then install requirements using "pip install -r requirements.txt"
and finally you can run using either "python3 main.py" or "uvicorn main:app --reload"

'Both methods will have the same result because i implemented automatic uvicorn run (reload included) in main.py'



'If you encountered any bugs or code parts that can be improved i'd appreciate if you let me know'