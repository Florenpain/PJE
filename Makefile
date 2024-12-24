install-dep-back:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

uninstall-dep-back:
	@echo "Uninstalling dependencies..."
	pip uninstall -r requirements.txt

install-dep-front:
	@echo "Installing dependencies..."
	cd frontend && npm install

uninstall-dep-front:
	@echo "Uninstalling dependencies..."
	cd frontend && npm uninstall

start-back:
	@echo "Starting backend..."
	cd backend && python -m uvicorn Main:app --reload

start-front:
	@echo "Starting frontend..."
	cd frontend && npm start