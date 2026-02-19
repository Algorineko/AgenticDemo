#!/usr/bin/env bash
set -euo pipefail

# ====== 定位仓库根目录 ======
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
BACKEND_DIR="${ROOT_DIR}/AgenticArxiv"
FRONTEND_DIR="${ROOT_DIR}/AgenticArxivWeb"

# ====== 参数（可通过环境变量覆盖） ======
B_HOST="${BACKEND_HOST:-0.0.0.0}"
B_PORT="${BACKEND_PORT:-8000}"
B_RELOAD="${BACKEND_RELOAD:-1}"

F_HOST="${FRONTEND_HOST:-0.0.0.0}"
F_PORT="${FRONTEND_PORT:-5173}"

RUN_DIR="${ROOT_DIR}/.run"
mkdir -p "${RUN_DIR}"

# 可选：传 --logs 则把输出写到文件
USE_LOGS=0
if [[ "${1:-}" == "--logs" ]]; then
  USE_LOGS=1
fi

require_cmd() {
  local c="$1"
  if ! command -v "${c}" >/dev/null 2>&1; then
    echo "[all] ERROR: command not found: ${c}" >&2
    exit 1
  fi
}

[[ -d "${BACKEND_DIR}" ]] || { echo "[all] ERROR: backend dir not found: ${BACKEND_DIR}" >&2; exit 1; }
[[ -d "${FRONTEND_DIR}" ]] || { echo "[all] ERROR: frontend dir not found: ${FRONTEND_DIR}" >&2; exit 1; }

require_cmd uvicorn
require_cmd npm

BACKEND_PID=""
FRONTEND_PID=""

cleanup() {
  echo
  echo "[all] stopping..."
  if [[ -n "${BACKEND_PID}" ]] && kill -0 "${BACKEND_PID}" >/dev/null 2>&1; then
    kill "${BACKEND_PID}" >/dev/null 2>&1 || true
  fi
  if [[ -n "${FRONTEND_PID}" ]] && kill -0 "${FRONTEND_PID}" >/dev/null 2>&1; then
    kill "${FRONTEND_PID}" >/dev/null 2>&1 || true
  fi
  echo "[all] stopped."
}
trap cleanup INT TERM EXIT

echo "[all] repo: ${ROOT_DIR}"
echo "[all] backend:  http://${B_HOST}:${B_PORT}   (reload=${B_RELOAD})"
echo "[all] frontend: http://${F_HOST}:${F_PORT}"
echo

# ====== 启动后端 ======
if [[ "${USE_LOGS}" == "1" ]]; then
  BACKEND_LOG="${RUN_DIR}/backend.log"
  : > "${BACKEND_LOG}"
  (
    cd "${BACKEND_DIR}"
    if [[ "${B_RELOAD}" == "1" ]]; then
      uvicorn api.app:app --host "${B_HOST}" --port "${B_PORT}" --reload
    else
      uvicorn api.app:app --host "${B_HOST}" --port "${B_PORT}"
    fi
  ) >> "${BACKEND_LOG}" 2>&1 &
  BACKEND_PID=$!
  echo "[all] backend started (pid=${BACKEND_PID}), log: ${BACKEND_LOG}"
else
  (
    cd "${BACKEND_DIR}"
    if [[ "${B_RELOAD}" == "1" ]]; then
      uvicorn api.app:app --host "${B_HOST}" --port "${B_PORT}" --reload
    else
      uvicorn api.app:app --host "${B_HOST}" --port "${B_PORT}"
    fi
  ) &
  BACKEND_PID=$!
  echo "[all] backend started (pid=${BACKEND_PID})"
fi

# ====== 启动前端 ======
if [[ "${USE_LOGS}" == "1" ]]; then
  FRONTEND_LOG="${RUN_DIR}/frontend.log"
  : > "${FRONTEND_LOG}"
  (
    cd "${FRONTEND_DIR}"
    npm run dev -- --host "${F_HOST}" --port "${F_PORT}"
  ) >> "${FRONTEND_LOG}" 2>&1 &
  FRONTEND_PID=$!
  echo "[all] frontend started (pid=${FRONTEND_PID}), log: ${FRONTEND_LOG}"
else
  (
    cd "${FRONTEND_DIR}"
    npm run dev -- --host "${F_HOST}" --port "${F_PORT}"
  ) &
  FRONTEND_PID=$!
  echo "[all] frontend started (pid=${FRONTEND_PID})"
fi

# 记录 PID，方便你手动 kill
echo "${BACKEND_PID}" > "${RUN_DIR}/backend.pid"
echo "${FRONTEND_PID}" > "${RUN_DIR}/frontend.pid"

echo
echo "[all] running... (Ctrl+C to stop both)"
echo "[all] pid files: ${RUN_DIR}/backend.pid , ${RUN_DIR}/frontend.pid"
echo

# 任何一个退出就触发 cleanup
wait -n "${BACKEND_PID}" "${FRONTEND_PID}"
exit 0
