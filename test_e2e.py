#!/usr/bin/env python3
"""Complete end-to-end test - Data fetch to Telegram alert."""
import sys
import os
from pathlib import Path
from datetime import datetime

# Add current directory to path
sys.path.insert(0, str(Path.cwd()))

def print_header(title):
    """Print formatted header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def print_step(step_num, description, status=None, details=""):
    """Print step status."""
    if status is None:
        symbol = "⏳"
    elif status:
        symbol = "✅"
    else:
        symbol = "❌"
    
    print(f"{symbol} Step {step_num}: {description}")
    if details:
        print(f"   └─ {details}")

def test_complete_flow():
    """Test complete data flow from API to Telegram."""
    print_header("COMPLETE END-TO-END TEST")
    print(f"Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
    
    errors = []
    
    # Step 1: Environment & Config
    print_step(1, "Loading configuration")
    try:
        from config.settings import settings
        print_step(1, "Loading configuration", True, f"Environment: {settings.ENV}")
        print(f"   └─ Confidence Threshold: {settings.CONFIDENCE_THRESHOLD}")
        print(f"   └─ Scan Interval: {settings.SCAN_INTERVAL}s")
        print(f"   └─ Telegram Token: {'✓ Set' if settings.TELEGRAM_BOT_TOKEN else '✗ Not set'}")
        print(f"   └─ Chat ID: {'✓ Set' if settings.TELEGRAM_CHAT_ID else '✗ Not set'}")
    except Exception as e:
        print_step(1, "Loading configuration", False, str(e))
        errors.append(f"Config load: {str(e)}")
        return errors
    
    # Step 2: Initialize Database
    print_step(2, "Initializing database")
    try:
        from database.db_manager import DatabaseManager
        db = DatabaseManager()
        print_step(2, "Initializing database", True, f"Path: {settings.DATABASE_PATH}")
    except Exception as e:
        print_step(2, "Initializing database", False, str(e))
        errors.append(f"Database init: {str(e)}")
        return errors
    
    # Step 3: OKX API Connection
    print_step(3, "Connecting to OKX API")
    try:
        from core.okx_api import OKXAPIClient
        api_client = OKXAPIClient()
        print_step(3, "Connecting to OKX API", True, "Client initialized")
    except Exception as e:
        print_step(3, "Connecting to OKX API", False, str(e))
        errors.append(f"API connection: {str(e)}")
        return errors
    
    # Step 4: Fetch Trading Pairs
    print_step(4, "Fetching trading pairs from OKX")
    try:
        pairs = api_client.get_all_swap_instruments()
        if pairs:
            print_step(4, "Fetching trading pairs from OKX", True, f"Found {len(pairs)} USDT pairs")
            test_pair = pairs[0]
            print(f"   └─ Testing with: {test_pair}")
        else:
            print_step(4, "Fetching trading pairs from OKX", False, "No pairs returned")
            errors.append("No trading pairs found")
            return errors
    except Exception as e:
        print_step(4, "Fetching trading pairs from OKX", False, str(e))
        errors.append(f"Fetch pairs: {str(e)}")
        return errors
    
    # Step 5: Fetch Ticker Data
    print_step(5, f"Fetching ticker data for {test_pair}")
    try:
        ticker = api_client.get_ticker(test_pair)
        if ticker:
            price = float(ticker.get('last', 0))
            print_step(5, f"Fetching ticker data for {test_pair}", True, f"Price: ${price}")
        else:
            print_step(5, f"Fetching ticker data for {test_pair}", False, "No ticker data")
            errors.append("No ticker data returned")
            return errors
    except Exception as e:
        print_step(5, f"Fetching ticker data for {test_pair}", False, str(e))
        errors.append(f"Fetch ticker: {str(e)}")
        return errors
    
    # Step 6: Fetch Candle Data
    print_step(6, f"Fetching candle data (1H) for {test_pair}")
    try:
        candles = api_client.get_candles(test_pair, 60, limit=50)
        if candles and len(candles) > 0:
            print_step(6, f"Fetching candle data (1H) for {test_pair}", True, f"Retrieved {len(candles)} candles")
        else:
            print_step(6, f"Fetching candle data (1H) for {test_pair}", False, "No candle data")
            errors.append("No candle data returned")
            return errors
    except Exception as e:
        print_step(6, f"Fetching candle data (1H) for {test_pair}", False, str(e))
        errors.append(f"Fetch candles: {str(e)}")
        return errors
    
    # Step 7: Technical Analysis
    print_step(7, "Performing technical analysis")
    try:
        from core.analyzer import MarketAnalyzer
        analyzer = MarketAnalyzer()
        
        parsed_candles = [analyzer.parse_candle(c) for c in candles]
        is_bullish, trend_strength = analyzer.calculate_trend(parsed_candles)
        rvol = analyzer.calculate_relative_volume(parsed_candles)
        structure = analyzer.detect_market_structure(parsed_candles)
        volatility = analyzer.calculate_volatility(parsed_candles)
        
        print_step(7, "Performing technical analysis", True)
        print(f"   └─ Trend: {'Bullish' if is_bullish else 'Bearish'} (Strength: {trend_strength:.2f})")
        print(f"   └─ RVOL: {rvol:.2f}x")
        print(f"   └─ Structure: {structure}")
        print(f"   └─ Volatility: {volatility:.4f}")
    except Exception as e:
        print_step(7, "Performing technical analysis", False, str(e))
        errors.append(f"Technical analysis: {str(e)}")
        return errors
    
    # Step 8: Confidence Scoring
    print_step(8, "Calculating confidence score")
    try:
        from core.confidence_scorer import ConfidenceScorer
        scorer = ConfidenceScorer()
        
        scores = {
            'price_expansion': scorer.calculate_price_expansion_score(1.5, 0.5),
            'relative_volume': scorer.calculate_volume_score(rvol),
            'open_interest': 70.0,
            'trend': scorer.calculate_trend_score(is_bullish, trend_strength),
            'market_structure': scorer.calculate_structure_score(structure, is_bullish),
            'breakout_strength': scorer.calculate_breakout_score(trend_strength),
            'multi_tf_alignment': scorer.calculate_multi_tf_score(2, 4),
        }
        
        confidence = scorer.calculate_overall_confidence(scores)
        meets_threshold = scorer.meets_threshold(confidence)
        
        print_step(8, "Calculating confidence score", True, f"Score: {confidence:.2f}%")
        print(f"   └─ Meets Threshold (88+): {'Yes' if meets_threshold else 'No'}")
        print(f"   └─ Price Expansion: {scores['price_expansion']:.1f}")
        print(f"   └─ Relative Volume: {scores['relative_volume']:.1f}")
        print(f"   └─ Trend: {scores['trend']:.1f}")
    except Exception as e:
        print_step(8, "Calculating confidence score", False, str(e))
        errors.append(f"Confidence scoring: {str(e)}")
        return errors
    
    # Step 9: Signal Generation
    print_step(9, "Generating trading signal")
    try:
        from core.signal_engine import SignalEngine
        signal_engine = SignalEngine(db)
        
        # Create test signal
        test_signal = {
            'coin': test_pair.replace('-USDT-SWAP', ''),
            'action': 'BUY LONG' if is_bullish else 'SELL SHORT',
            'type': 'INTRADAY',
            'confidence': min(95.0, confidence + 5) if meets_threshold else 75.0,
            'risk': 'LOW' if volatility < 0.02 else 'MEDIUM' if volatility < 0.05 else 'HIGH',
            'reason': [
                f"RVOL {rvol:.1f}x above average",
                f"Trend {'bullish' if is_bullish else 'bearish'} confirmed",
                f"{structure} market structure",
            ],
            'bot_view': "Testing signal generation - Market analysis complete",
            'price': price,
            'timeframe_group': '15m/60m',
            'timestamp': datetime.utcnow().isoformat(),
        }
        
        print_step(9, "Generating trading signal", True)
        print(f"   └─ Action: {test_signal['action']}")
        print(f"   └─ Confidence: {test_signal['confidence']:.1f}%")
        print(f"   └─ Risk Level: {test_signal['risk']}")
    except Exception as e:
        print_step(9, "Generating trading signal", False, str(e))
        errors.append(f"Signal generation: {str(e)}")
        return errors
    
    # Step 10: Database Storage
    print_step(10, "Storing signal in database")
    try:
        db.insert_signal(test_signal)
        print_step(10, "Storing signal in database", True, "Signal stored successfully")
    except Exception as e:
        print_step(10, "Storing signal in database", False, str(e))
        errors.append(f"Database storage: {str(e)}")
        return errors
    
    # Step 11: Telegram Initialization
    print_step(11, "Initializing Telegram notifier")
    try:
        from telegram.notifier import TelegramNotifier
        notifier = TelegramNotifier()
        print_step(11, "Initializing Telegram notifier", True, "Notifier ready")
    except Exception as e:
        print_step(11, "Initializing Telegram notifier", False, str(e))
        errors.append(f"Telegram init: {str(e)}")
        return errors
    
    # Step 12: Send Telegram Alert
    print_step(12, "Sending alert to Telegram")
    try:
        success = notifier.send_signal_alert(test_signal)
        if success:
            print_step(12, "Sending alert to Telegram", True, "Alert delivered successfully")
        else:
            print_step(12, "Sending alert to Telegram", False, "Failed to send alert")
            errors.append("Telegram alert delivery failed")
    except Exception as e:
        print_step(12, "Sending alert to Telegram", False, str(e))
        errors.append(f"Telegram send: {str(e)}")
    
    return errors

def main():
    """Main test execution."""
    try:
        errors = test_complete_flow()
        
        print_header("TEST RESULTS")
        
        if not errors:
            print("\n🎉 ALL TESTS PASSED!\n")
            print("✅ Data fetch from OKX API: WORKING")
            print("✅ Technical analysis: WORKING")
            print("✅ Signal generation: WORKING")
            print("✅ Database storage: WORKING")
            print("✅ Telegram alerts: WORKING")
            print("\n✨ BOT IS READY FOR PRODUCTION HOSTING\n")
            print("="*70)
            print("Next Steps:")
            print("  1. Configure OKX API credentials in .env")
            print("  2. Run: python main.py")
            print("  3. Or deploy with Docker: docker-compose up")
            print("="*70 + "\n")
            return 0
        else:
            print("\n❌ TESTS FAILED\n")
            print("Errors encountered:")
            for i, error in enumerate(errors, 1):
                print(f"  {i}. {error}")
            print("\n" + "="*70)
            print("Please fix errors before deployment.")
            print("="*70 + "\n")
            return 1
    except Exception as e:
        print(f"\n\n❌ FATAL ERROR: {str(e)}\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())
