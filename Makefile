run:
	python.exe -m src.main
clean:
	pyclean .
depends:
	pip install -r requirements.txt

ldepends:
	pip install -r --break-system-packages
lrun:
	python3 -m src.main

