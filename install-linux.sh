#!/bin/bash
# ADHI-HUB Linux app installer
# Creates a clickable app entry in the Linux applications menu.
# Usage:  bash install-linux.sh
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"
APP_NAME="ADHI-HUB"
DESKTOP_DIR="$HOME/.local/share/applications"
DESKTOP_FILE="$DESKTOP_DIR/adhi-hub.desktop"

chmod +x "$DIR/run.sh"

mkdir -p "$DESKTOP_DIR"

cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Type=Application
Version=1.0
Name=ADHI-HUB
Comment=The ultimate video & music downloader
Exec=bash -c "cd '$DIR' && ./run.sh; echo; read -p 'Press Enter to close...'"
Path=$DIR
Icon=applications-multimedia
Terminal=true
Categories=Utility;AudioVideo;Network;
Keywords=download;video;music;youtube;mp3;mp4;
EOF

echo "✔ Installed! ADHI-HUB is now in your applications menu."
echo "  (some desktops need logout/login or:  update-desktop-database $DESKTOP_DIR)"
echo "  location: $DESKTOP_FILE"