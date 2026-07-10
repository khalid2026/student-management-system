#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║   🚀 تشغيل تطبيق السائقين                                  ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# الألوان
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}📋 الخطوة 1: تشغيل Backend${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# فتح Terminal جديد لـ Backend
osascript <<EOF
tell application "Terminal"
    do script "cd /Users/khalidawadh/wasl-delivery-system/backend && echo '🔥 Starting Backend...' && npm run dev"
    activate
end tell
EOF

echo -e "${GREEN}✅ تم فتح Terminal للـ Backend${NC}"
echo ""
echo "⏳ انتظر 5 ثواني حتى يبدأ Backend..."
sleep 5

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}📋 الخطوة 2: تشغيل Driver App${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# فتح Terminal جديد لـ Driver App
osascript <<EOF
tell application "Terminal"
    do script "cd /Users/khalidawadh/wasl-delivery-system/driver-app && echo '📱 Starting Driver App...' && npm start"
    activate
end tell
EOF

echo -e "${GREEN}✅ تم فتح Terminal للـ Driver App${NC}"
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🎉 تم!${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "📱 الآن:"
echo "   1. انتظر ظهور QR Code في Terminal الثاني"
echo "   2. افتح Expo Go على جوالك"
echo "   3. امسح الـ QR Code"
echo ""
echo -e "${YELLOW}⚠️  تأكد أن الجوال والماك على نفس WiFi!${NC}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

