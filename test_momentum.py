#!/usr/bin/env python3
"""
Unit tests for MarketPulse momentum calculation and core functions
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'backend'))

import unittest
from main import MomentumCalculator

class TestMomentumCalculator(unittest.TestCase):
    """Test momentum calculation logic"""
    
    def setUp(self):
        self.calculator = MomentumCalculator()
    
    def test_positive_momentum(self):
        """Test bullish momentum calculation"""
        returns = [1.0, 2.0, 0.5, 1.5]  # All positive
        score = self.calculator.calculate_momentum_score(returns)
        self.assertEqual(score, 1.25)  # Average: (1+2+0.5+1.5)/4 = 1.25
        self.assertGreater(score, 0)  # Should be positive
    
    def test_negative_momentum(self):
        """Test bearish momentum calculation"""
        returns = [-1.0, -2.0, -0.5, -1.5]  # All negative
        score = self.calculator.calculate_momentum_score(returns)
        self.assertEqual(score, -1.25)  # Average: (-1-2-0.5-1.5)/4 = -1.25
        self.assertLess(score, 0)  # Should be negative
    
    def test_mixed_momentum(self):
        """Test mixed momentum (some positive, some negative)"""
        returns = [1.0, -1.0, 2.0, -2.0]  # Balanced
        score = self.calculator.calculate_momentum_score(returns)
        self.assertEqual(score, 0.0)  # Average: (1-1+2-2)/4 = 0
    
    def test_neutral_momentum(self):
        """Test neutral momentum"""
        returns = [0.1, -0.1, 0.05, -0.05]  # Very small values
        score = self.calculator.calculate_momentum_score(returns)
        self.assertEqual(score, 0.0)  # Should round to 0
        
    def test_empty_returns(self):
        """Test edge case: empty returns array"""
        returns = []
        score = self.calculator.calculate_momentum_score(returns)
        self.assertEqual(score, 0.0)  # Should handle gracefully
    
    def test_single_return(self):
        """Test edge case: single return value"""
        returns = [2.5]
        score = self.calculator.calculate_momentum_score(returns)
        self.assertEqual(score, 2.5)  # Should return the single value
    
    def test_rounding_precision(self):
        """Test that momentum score is properly rounded"""
        returns = [1.234567, 2.345678]  # High precision inputs
        score = self.calculator.calculate_momentum_score(returns)
        # Should be rounded to 2 decimal places
        self.assertEqual(score, 1.79)  # (1.234567+2.345678)/2 = 1.7901225 ≈ 1.79

class TestDataValidation(unittest.TestCase):
    """Test data validation and edge cases"""
    
    def test_ticker_validation(self):
        """Test ticker symbol validation"""
        valid_tickers = ["AAPL", "MSFT", "GOOGL", "NVDA", "TSLA"]
        invalid_tickers = ["", "TOOLONG123", None]
        
        # This would be implemented in a validation function
        # For now, just verify our test data
        for ticker in valid_tickers:
            self.assertTrue(len(ticker) <= 10)
            self.assertTrue(ticker.isalpha() or ticker.isalnum())
        
        for ticker in invalid_tickers:
            if ticker is not None:
                self.assertTrue(len(ticker) == 0 or len(ticker) > 10)

def run_tests():
    """Run all tests and provide summary"""
    print("🧪 Running MarketPulse Unit Tests...")
    print("=" * 50)
    
    # Run tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTest(loader.loadTestsFromTestCase(TestMomentumCalculator))
    suite.addTest(loader.loadTestsFromTestCase(TestDataValidation))
    
    # Run with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📊 Test Summary:")
    print(f"   Tests run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        if result.failures:
            print("\n💥 Failures:")
            for test, traceback in result.failures:
                print(f"   - {test}: {traceback.split('AssertionError: ')[-1].split('\\n')[0]}")
        if result.errors:
            print("\n🚨 Errors:")
            for test, traceback in result.errors:
                print(f"   - {test}: {traceback.split('\\n')[-2]}")
        return 1

if __name__ == "__main__":
    sys.exit(run_tests())