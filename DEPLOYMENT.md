# CRYPTO FUTURES BOT - DEPLOYMENT GUIDE

## ✅ PRODUCTION READY STATUS

Your bot has been tested and is **READY FOR PRODUCTION HOSTING** with:

- ✅ OKX API integration (data fetching)
- ✅ Technical analysis engine
- ✅ Confidence scoring system
- ✅ Signal generation
- ✅ SQLite database storage
- ✅ Telegram alert delivery
- ✅ Error handling & retry logic
- ✅ Logging system
- ✅ Docker support
- ✅ Heroku deployment ready

---

## 🚀 DEPLOYMENT OPTIONS

### Option 1: Local Development

```bash
# 1. Clone repository
git clone https://github.com/officialstretchfitnesscenter-code/Eeco-crypto-bot.git
cd Eeco-crypto-bot

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run end-to-end test
python test_e2e.py

# 5. Start bot
python main.py
```

### Option 2: Docker (Recommended for hosting)

```bash
# 1. Build image
docker build -t eeco-crypto-bot .

# 2. Run container
docker run -d \
  --name eeco-crypto-bot \
  -e OKX_API_KEY=your_key \
  -e OKX_API_SECRET=your_secret \
  -e OKX_API_PASSPHRASE=your_passphrase \
  -e TELEGRAM_BOT_TOKEN=8854251990:AAFOxZfQGP6dKYTExEL7YByAvf69Djnflqo \
  -e TELEGRAM_CHAT_ID=1490359174 \
  -v crypto-bot-data:/app/data \
  -v crypto-bot-logs:/app/logs \
  eeco-crypto-bot

# 3. View logs
docker logs -f eeco-crypto-bot
```

### Option 3: Docker Compose

```bash
# 1. Update .env with credentials
vi .env

# 2. Start services
docker-compose up -d

# 3. View logs
docker-compose logs -f

# 4. Stop services
docker-compose down
```

### Option 4: Heroku Deployment

```bash
# 1. Install Heroku CLI
# Download from: https://devcenter.heroku.com/articles/heroku-cli

# 2. Login to Heroku
heroku login

# 3. Create app
heroku create eeco-crypto-bot

# 4. Set environment variables
heroku config:set OKX_API_KEY=your_key
heroku config:set OKX_API_SECRET=your_secret
heroku config:set OKX_API_PASSPHRASE=your_passphrase
heroku config:set TELEGRAM_BOT_TOKEN=8854251990:AAFOxZfQGP6dKYTExEL7YByAvf69Djnflqo
heroku config:set TELEGRAM_CHAT_ID=1490359174
heroku config:set ENV=production

# 5. Deploy
git push heroku main

# 6. View logs
heroku logs --tail
```

### Option 5: VPS/Cloud Server (AWS, DigitalOcean, etc.)

```bash
# 1. SSH into server
ssh user@your_server_ip

# 2. Clone repository
git clone https://github.com/officialstretchfitnesscenter-code/Eeco-crypto-bot.git
cd Eeco-crypto-bot

# 3. Install Python
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv

# 4. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 5. Install dependencies
pip install -r requirements.txt

# 6. Create .env file
cp .env.example .env
vi .env  # Add credentials

# 7. Test deployment
python test_e2e.py

# 8. Run with systemd (auto-restart on reboot)
sudo nano /etc/systemd/system/crypto-bot.service
```

Create `/etc/systemd/system/crypto-bot.service`:

```ini
[Unit]
Description=Crypto Futures Bot
After=network.target

[Service]
Type=simple
User=crypto
WorkingDirectory=/home/crypto/Eeco-crypto-bot
Environment="PATH=/home/crypto/Eeco-crypto-bot/venv/bin"
ExecStart=/home/crypto/Eeco-crypto-bot/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then:

```bash
sudo systemctl daemon-reload
sudo systemctl enable crypto-bot
sudo systemctl start crypto-bot
sudo systemctl status crypto-bot
```

---

## 🧪 TESTING BEFORE DEPLOYMENT

### Run End-to-End Test

```bash
python test_e2e.py
```

This tests:
1. ✅ Configuration loading
2. ✅ Database initialization
3. ✅ OKX API connection
4. ✅ Trading pair fetching
5. ✅ Ticker data fetch
6. ✅ Candle data fetch
7. ✅ Technical analysis
8. ✅ Confidence scoring
9. ✅ Signal generation
10. ✅ Database storage
11. ✅ Telegram initialization
12. ✅ Telegram alert delivery

### Run Original Test Deploy

```bash
python test_deploy.py
```

This tests individual components separately.

---

## 📋 CONFIGURATION

### Required Environment Variables

```bash
OKX_API_KEY=your_okx_api_key
OKX_API_SECRET=your_okx_api_secret
OKX_API_PASSPHRASE=your_okx_api_passphrase
TELEGRAM_BOT_TOKEN=8854251990:AAFOxZfQGP6dKYTExEL7YByAvf69Djnflqo
TELEGRAM_CHAT_ID=1490359174
SCAN_INTERVAL=3600
CONFIDENCE_THRESHOLD=88
COOLDOWN_HOURS=6
ENV=production
```

### Optional Customization

Edit `config/settings.py`:

```python
# Change confidence weights
CONFIDENCE_WEIGHTS = {
    'price_expansion': 0.15,
    'relative_volume': 0.20,
    'open_interest': 0.15,
    'trend': 0.15,
    'market_structure': 0.15,
    'breakout_strength': 0.10,
    'multi_tf_alignment': 0.10,
}

# Change risk thresholds
RISK_THRESHOLDS = {
    'low': {'volatility_max': 0.02, 'oi_change_min': 0.10},
    'medium': {'volatility_max': 0.05, 'oi_change_min': 0.05},
    'high': {'volatility_max': float('inf'), 'oi_change_min': 0.0},
}
```

---

## 📊 MONITORING

### Check Bot Status

```bash
# View logs
tail -f logs/bot.log

# View database signals
sqlite3 data/signals.db "SELECT * FROM signals ORDER BY timestamp DESC LIMIT 10;"

# Count today's signals
sqlite3 data/signals.db "SELECT COUNT(*) FROM signals WHERE DATE(timestamp) = DATE('now');"
```

### Common Log Messages

```
✅ Signal generated for BTC-USDT-SWAP: BUY LONG
✅ Scan completed in 45.32s. Signals: 3
⚠️  No pairs found
❌ API Timeout
```

---

## 🔧 TROUBLESHOOTING

### No signals generated

```bash
# Check confidence threshold
grep CONFIDENCE_THRESHOLD .env

# Lower threshold temporarily
echo "CONFIDENCE_THRESHOLD=75" >> .env

# View analysis logs
tail -f logs/bot.log | grep "Confidence"
```

### Telegram not sending

```bash
# Verify credentials
echo $TELEGRAM_BOT_TOKEN
echo $TELEGRAM_CHAT_ID

# Test manually
python -c "from telegram.notifier import TelegramNotifier; TelegramNotifier().send_message('Test')"
```

### API connection errors

```bash
# Test OKX API
python -c "from core.okx_api import OKXAPIClient; print(OKXAPIClient().get_all_swap_instruments()[:5])"

# Check network
ping okx.com
```

### Database issues

```bash
# Check database integrity
sqlite3 data/signals.db "PRAGMA integrity_check;"

# Backup database
cp data/signals.db data/signals.db.backup

# Reset database
rm data/signals.db
python -c "from database.db_manager import DatabaseManager; DatabaseManager()"
```

---

## 📈 PERFORMANCE

### Expected Scan Times

- **Pair fetching**: 2-5 seconds
- **Per-pair analysis**: 0.1-0.5 seconds
- **Total scan time**: 1-3 minutes (for ~50 pairs)
- **Telegram delivery**: < 1 second

### Resource Usage

- **CPU**: < 5% during scans
- **Memory**: 50-100 MB
- **Network**: ~1-2 MB per scan
- **Storage**: ~100 KB per 100 signals

---

## 🔒 SECURITY

### Best Practices

1. **Never commit .env file**
   ```bash
   # Already in .gitignore
   cat .gitignore | grep .env
   ```

2. **Use strong API credentials**
   - Rotate keys regularly
   - Use read-only API keys
   - Restrict IP whitelist on OKX

3. **Secure your bot token**
   - Don't share Telegram token
   - Use environment variables
   - Never commit credentials

4. **Database security**
   - Backup data regularly
   - Store backups securely
   - Monitor database access

---

## 📞 SUPPORT

If you encounter issues:

1. Check `logs/bot.log` for error messages
2. Review this guide for troubleshooting
3. Run `python test_e2e.py` to diagnose
4. Check OKX API status
5. Verify Telegram token validity

---

## 📝 NEXT STEPS

1. ✅ Add OKX API credentials to `.env`
2. ✅ Run `python test_e2e.py` to verify
3. ✅ Choose hosting option (Docker recommended)
4. ✅ Deploy and monitor
5. ✅ Monitor logs and signals
6. ✅ Adjust settings as needed

**Bot is production-ready. Happy trading! 🚀**
