#!/usr/bin/env python3
"""
Test script for Domain Classification Game
"""

from domain_data import get_random_domains, verify_answers, LEGITIMATE_DOMAINS, SUSPICIOUS_DOMAINS

def test_domain_generation():
    """Test domain generation"""
    print("=== Testing Domain Generation ===")
    domains = get_random_domains(30)
    
    print(f"Generated {len(domains)} domains")
    print(f"Total legitimate domains available: {len(LEGITIMATE_DOMAINS)}")
    print(f"Total suspicious domains available: {len(SUSPICIOUS_DOMAINS)}")
    
    legitimate_count = sum(1 for d in domains if d["is_legitimate"])
    suspicious_count = len(domains) - legitimate_count
    
    print(f"Legitimate in sample: {legitimate_count}")
    print(f"Suspicious in sample: {suspicious_count}")
    print(f"Legitimate percentage: {legitimate_count/len(domains)*100:.1f}%")
    
    print("\nSample domains:")
    for i, domain in enumerate(domains[:10]):
        status = "✅ Legitimate" if domain["is_legitimate"] else "❌ Suspicious"
        print(f"{i+1:2}. {domain['domain']:30} - {status}")
    
    return domains

def test_answer_verification():
    """Test answer verification"""
    print("\n=== Testing Answer Verification ===")
    
    # Generate test domains
    domains = get_random_domains(10)
    
    # Simulate perfect answers
    print("Test 1: Perfect answers (100% correct)")
    perfect_answers = [
        {"domain": d["domain"], "is_legitimate": d["is_legitimate"]} 
        for d in domains
    ]
    result = verify_answers(perfect_answers, domains)
    print(f"Result: {result['correct_count']}/{result['total_count']} correct, Passed: {result['passed']}")
    
    # Simulate all wrong answers
    print("\nTest 2: All wrong answers (0% correct)")
    wrong_answers = [
        {"domain": d["domain"], "is_legitimate": not d["is_legitimate"]} 
        for d in domains
    ]
    result = verify_answers(wrong_answers, domains)
    print(f"Result: {result['correct_count']}/{result['total_count']} correct, Passed: {result['passed']}")
    
    # Simulate 70% correct answers
    print("\nTest 3: 70% correct answers")
    mixed_answers = []
    for i, d in enumerate(domains):
        if i < 7:  # First 7 correct
            mixed_answers.append({"domain": d["domain"], "is_legitimate": d["is_legitimate"]})
        else:  # Last 3 wrong
            mixed_answers.append({"domain": d["domain"], "is_legitimate": not d["is_legitimate"]})
    
    result = verify_answers(mixed_answers, domains)
    print(f"Result: {result['correct_count']}/{result['total_count']} correct, Passed: {result['passed']}")

def test_passing_threshold():
    """Test the passing threshold (need >20/30 correct)"""
    print("\n=== Testing Passing Threshold ===")
    
    domains = get_random_domains(30)
    
    # Test exactly 20 correct (should fail)
    print("Test: Exactly 20/30 correct (should FAIL)")
    test_answers = []
    for i, d in enumerate(domains):
        if i < 20:  # First 20 correct
            test_answers.append({"domain": d["domain"], "is_legitimate": d["is_legitimate"]})
        else:  # Last 10 wrong
            test_answers.append({"domain": d["domain"], "is_legitimate": not d["is_legitimate"]})
    
    result = verify_answers(test_answers, domains)
    print(f"Result: {result['correct_count']}/{result['total_count']} correct, Passed: {result['passed']} {'✅' if not result['passed'] else '❌'}")
    
    # Test exactly 21 correct (should pass)
    print("\nTest: Exactly 21/30 correct (should PASS)")
    test_answers = []
    for i, d in enumerate(domains):
        if i < 21:  # First 21 correct
            test_answers.append({"domain": d["domain"], "is_legitimate": d["is_legitimate"]})
        else:  # Last 9 wrong
            test_answers.append({"domain": d["domain"], "is_legitimate": not d["is_legitimate"]})
    
    result = verify_answers(test_answers, domains)
    print(f"Result: {result['correct_count']}/{result['total_count']} correct, Passed: {result['passed']} {'✅' if result['passed'] else '❌'}")

def show_sample_domains():
    """Show some sample domains from each category"""
    print("\n=== Sample Domains ===")
    
    print("LEGITIMATE DOMAINS (first 20):")
    for i, domain in enumerate(LEGITIMATE_DOMAINS[:20]):
        print(f"  {i+1:2}. {domain}")
    
    print(f"\n... and {len(LEGITIMATE_DOMAINS)-20} more legitimate domains")
    
    print("\nSUSPICIOUS DOMAINS (first 20):")
    for i, domain in enumerate(SUSPICIOUS_DOMAINS[:20]):
        print(f"  {i+1:2}. {domain}")
    
    print(f"\n... and {len(SUSPICIOUS_DOMAINS)-20} more suspicious domains")

if __name__ == "__main__":
    print("🌐 Domain Classification Game - Test Suite")
    print("=" * 50)
    
    # Run all tests
    domains = test_domain_generation()
    test_answer_verification()
    test_passing_threshold()
    show_sample_domains()
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")
    print("\nGame Logic Summary:")
    print("- 30 domains total (mix of ~70% legitimate, ~30% suspicious)")
    print("- Player must classify each as 'Legitimate' or 'Suspicious'")
    print("- Need MORE than 20 correct (21+) to pass the challenge")
    print("- Passing unlocks the puzzle!")
