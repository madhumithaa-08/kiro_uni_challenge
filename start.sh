#!/usr/bin/env bash
set -e

echo "🚀 Starting DSA Vault Full Web Software..."

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"

# Check Python environment in backend
if [ ! -d "$BACKEND_DIR/.venv" ]; then
    echo "📦 Creating Python virtual environment in backend..."
    python3 -m venv "$BACKEND_DIR/.venv"
    source "$BACKEND_DIR/.venv/bin/activate"
    pip install -q -r "$BACKEND_DIR/requirements.txt"
else
    source "$BACKEND_DIR/.venv/bin/activate"
fi

# Function to clean up background processes on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down DSA Vault services..."
    kill $(jobs -p) 2>/dev/null || true
}
trap cleanup EXIT

echo "⚡ Starting FastAPI backend on http://localhost:8000..."
cd "$BACKEND_DIR"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

echo "⚡ Starting Vite frontend on http://localhost:5173..."
cd "$FRONTEND_DIR"
npm run dev &
FRONTEND_PID=$!

sleep 2

# Open browser if on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    open http://localhost:5173 || true
fi

echo ""
echo "✅ DSA Vault is live at http://localhost:5173"
echo "Press Ctrl+C to stop all services."
echo ""

wait
