# Task 2: Automated Testing with AI
# Selenium-based Login Test Automation

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import json
from datetime import datetime

class AIEnhancedLoginTester:
    def __init__(self, headless=False):
        """Initialize the AI-enhanced login tester"""
        self.results = {
            'test_run_timestamp': datetime.now().isoformat(),
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'test_details': []
        }
        
        # Setup Chrome options
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
    
    def create_test_login_page(self):
        """Create a simple HTML login page for testing"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Login Page</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 50px; }
                .login-form { max-width: 300px; margin: 0 auto; }
                input { width: 100%; padding: 10px; margin: 5px 0; }
                button { width: 100%; padding: 10px; background: #007bff; color: white; border: none; }
                .error { color: red; margin-top: 10px; }
                .success { color: green; margin-top: 10px; }
            </style>
        </head>
        <body>
            <div class="login-form">
                <h2>Login Test Page</h2>
                <form id="loginForm">
                    <input type="text" id="username" placeholder="Username" required>
                    <input type="password" id="password" placeholder="Password" required>
                    <button type="submit" id="loginBtn">Login</button>
                </form>
                <div id="message"></div>
            </div>
            
            <script>
                document.getElementById('loginForm').addEventListener('submit', function(e) {
                    e.preventDefault();
                    const username = document.getElementById('username').value;
                    const password = document.getElementById('password').value;
                    const messageDiv = document.getElementById('message');
                    
                    // Simple validation logic
                    if (username === 'admin' && password === 'password123') {
                        messageDiv.innerHTML = '<div class="success">Login successful!</div>';
                        messageDiv.className = 'success';
                    } else {
                        messageDiv.innerHTML = '<div class="error">Invalid credentials!</div>';
                        messageDiv.className = 'error';
                    }
                });
            </script>
        </body>
        </html>
        """
        
        with open('test_login_page.html', 'w') as f:
            f.write(html_content)
        
        return 'file://' + os.path.abspath('test_login_page.html')
    
    def test_valid_login(self, username, password):
        """Test valid login credentials"""
        test_name = f"Valid Login Test - {username}"
        start_time = time.time()
        
        try:
            # Navigate to login page
            self.driver.get(self.create_test_login_page())
            
            # AI-enhanced element detection with multiple strategies
            username_field = self.find_element_ai_enhanced("username", ["#username", "input[name='username']", "input[type='text']"])
            password_field = self.find_element_ai_enhanced("password", ["#password", "input[name='password']", "input[type='password']"])
            login_button = self.find_element_ai_enhanced("login", ["#loginBtn", "button[type='submit']", "input[type='submit']"])
            
            # Enter credentials
            username_field.clear()
            username_field.send_keys(username)
            password_field.clear()
            password_field.send_keys(password)
            
            # Click login
            login_button.click()
            
            # Wait for result and verify success
            success_message = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "success"))
            )
            
            execution_time = time.time() - start_time
            self.record_test_result(test_name, True, f"Login successful for {username}", execution_time)
            return True
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.record_test_result(test_name, False, str(e), execution_time)
            return False
    
    def test_invalid_login(self, username, password):
        """Test invalid login credentials"""
        test_name = f"Invalid Login Test - {username}"
        start_time = time.time()
        
        try:
            # Navigate to login page
            self.driver.get(self.create_test_login_page())
            
            # AI-enhanced element detection
            username_field = self.find_element_ai_enhanced("username", ["#username", "input[name='username']", "input[type='text']"])
            password_field = self.find_element_ai_enhanced("password", ["#password", "input[name='password']", "input[type='password']"])
            login_button = self.find_element_ai_enhanced("login", ["#loginBtn", "button[type='submit']", "input[type='submit']"])
            
            # Enter credentials
            username_field.clear()
            username_field.send_keys(username)
            password_field.clear()
            password_field.send_keys(password)
            
            # Click login
            login_button.click()
            
            # Wait for error message
            error_message = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "error"))
            )
            
            execution_time = time.time() - start_time
            self.record_test_result(test_name, True, f"Correctly rejected invalid credentials for {username}", execution_time)
            return True
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.record_test_result(test_name, False, str(e), execution_time)
            return False
    
    def find_element_ai_enhanced(self, element_type, selectors):
        """AI-enhanced element finding with fallback strategies"""
        for selector in selectors:
            try:
                if selector.startswith('#'):
                    return self.driver.find_element(By.ID, selector[1:])
                elif selector.startswith('.'):
                    return self.driver.find_element(By.CLASS_NAME, selector[1:])
                else:
                    return self.driver.find_element(By.CSS_SELECTOR, selector)
            except NoSuchElementException:
                continue
        
        raise NoSuchElementException(f"Could not find {element_type} element with any of the provided selectors")
    
    def record_test_result(self, test_name, passed, message, execution_time):
        """Record test results for analysis"""
        self.results['total_tests'] += 1
        if passed:
            self.results['passed_tests'] += 1
        else:
            self.results['failed_tests'] += 1
        
        self.results['test_details'].append({
            'test_name': test_name,
            'status': 'PASSED' if passed else 'FAILED',
            'message': message,
            'execution_time': round(execution_time, 3),
            'timestamp': datetime.now().isoformat()
        })
    
    def run_comprehensive_test_suite(self):
        """Run comprehensive login test suite"""
        print("Starting AI-Enhanced Login Test Suite...")
        print("="*50)
        
        # Test valid credentials
        valid_tests = [
            ('admin', 'password123'),
        ]
        
        # Test invalid credentials
        invalid_tests = [
            ('admin', 'wrongpassword'),
            ('wronguser', 'password123'),
            ('', ''),
            ('admin', ''),
            ('', 'password123'),
            ('user123', 'pass456'),
        ]
        
        # Run valid login tests
        for username, password in valid_tests:
            self.test_valid_login(username, password)
            time.sleep(1)  # Small delay between tests
        
        # Run invalid login tests
        for username, password in invalid_tests:
            self.test_invalid_login(username, password)
            time.sleep(1)  # Small delay between tests
        
        # Generate summary
        self.generate_test_report()
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        success_rate = (self.results['passed_tests'] / self.results['total_tests']) * 100
        
        print(f"\nTest Execution Summary:")
        print(f"Total Tests: {self.results['total_tests']}")
        print(f"Passed: {self.results['passed_tests']}")
        print(f"Failed: {self.results['failed_tests']}")
        print(f"Success Rate: {success_rate:.1f}%")
        print("\nDetailed Results:")
        
        for test in self.results['test_details']:
            status_icon = "✓" if test['status'] == 'PASSED' else "✗"
            print(f"{status_icon} {test['test_name']}: {test['status']} ({test['execution_time']}s)")
            if test['status'] == 'FAILED':
                print(f"   Error: {test['message']}")
        
        # Save results to JSON file
        with open('test_results.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\nDetailed results saved to 'test_results.json'")
    
    def cleanup(self):
        """Cleanup resources"""
        self.driver.quit()
        
        # Clean up test file
        import os
        if os.path.exists('test_login_page.html'):
            os.remove('test_login_page.html')

# Main execution
if __name__ == "__main__":
    import os
    
    tester = AIEnhancedLoginTester(headless=True)  # Run in headless mode
    
    try:
        tester.run_comprehensive_test_suite()
    finally:
        tester.cleanup() 