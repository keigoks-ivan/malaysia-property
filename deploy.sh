#!/bin/bash
# ── Deploy to cPanel shared hosting ──
# Remote: investmq@85.187.128.56:/home/investmq/public_html/myproperty
# Syncs only web-facing files (HTML, CSS, JS, data JSON)

set -e

REMOTE_USER="investmq"
REMOTE_HOST="85.187.128.56"
REMOTE_PATH="/home/investmq/public_html/myproperty"
LOCAL_PATH="/Users/ivanchang/malaysia-property/"

echo "=== Deploying to ${REMOTE_HOST}:${REMOTE_PATH} ==="
echo ""

# 1. Test connectivity
echo "[1/2] Testing SSH connection..."
if ! ssh -o ConnectTimeout=10 -o BatchMode=yes "${REMOTE_USER}@${REMOTE_HOST}" echo "connected" >/dev/null 2>&1; then
    echo ""
    echo "ERROR: SSH connection failed."
    echo ""
    echo "Possible causes:"
    echo "  1. Host key not yet trusted → run: ssh ${REMOTE_USER}@${REMOTE_HOST}"
    echo "     and type 'yes' when prompted"
    echo "  2. SSH key not set up → copy your key: ssh-copy-id ${REMOTE_USER}@${REMOTE_HOST}"
    echo "  3. Password auth required → run this script without BatchMode:"
    echo "     rsync -avz --progress ... (see below)"
    echo "  4. Firewall blocking port 22 → check with: nc -zv ${REMOTE_HOST} 22"
    echo "  5. Wrong IP or username → verify in cPanel > General Information"
    echo ""
    exit 1
fi
echo "  SSH OK"

# 2. Rsync (exclude non-web files)
echo "[2/2] Syncing files..."
rsync -avz --progress --delete \
    --exclude='.git/' \
    --exclude='scripts/' \
    --exclude='deploy.sh' \
    --exclude='README.md' \
    --exclude='CLAUDE.md' \
    --exclude='.gitignore' \
    --exclude='*.zip' \
    --exclude='*.py' \
    --exclude='.DS_Store' \
    --exclude='node_modules/' \
    "${LOCAL_PATH}" "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}"

echo ""
echo "=== Deploy complete ==="
echo "Site: https://investmquest.com/myproperty/"
