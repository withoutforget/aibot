run:
	python.exe main.py
clean:
	pyclean .
depends:
	pip install -r requirements.txt

ldepends:
	pip install -r --break-system-packages
lrun:
	python3 main.py



