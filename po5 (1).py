"""
Enhanced Pocket Option Trading Bot with Webpage Loading Detection
"""

import pyautogui
import time
import pyperclip
import keyboard
import webbrowser
import pygetwindow as gw
import random
import os
from datetime import datetime
import re
import sys
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')
import pytesseract
import cv2
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\theli\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

def scale_x(percent):
    screen_width, _ = pyautogui.size()
    return int(screen_width * percent)

def scale_y(percent):
    _, screen_height = pyautogui.size()
    return int(screen_height * percent)
import pytesseract
from PIL import ImageGrab

import pyautogui
from PIL import ImageGrab
import pytesseract

def get_current_balance():
    # Calibrated coordinates for balance
    x, y = 1371, 116
    screenshot = ImageGrab.grab(bbox=(x-100, y-30, x+100, y+30))

    gray = screenshot.convert('L')
    gray = gray.point(lambda p: p > 180 and 255)  # threshold to clean image

    text = pytesseract.image_to_string(gray, config='--psm 7 -c tessedit_char_whitelist=0123456789.')
    print("OCR Clean Text:", text)

    match = re.search(r'\d+(\.\d+)?', text)
    if match:
        return float(match.group())
    return None

def get_result_from_balance():
    before = get_current_balance()
    print("Balance Before:", before)

    # Wait for trade to close
    time.sleep(35)

    after = get_current_balance()
    print("Balance After:", after)

    if before is not None and after is not None:
            if after > before:
                return 'W'
            elif after < before:
             return 'L'
            else:
             return 'BE'
def wait_for_balance_change(before_balance, timeout=10):
    """
    Wait for balance to change with short timeout.
    before_balance = balance before trade
    timeout = max seconds to wait
    """
    start_time = time.time()

    while time.time() - start_time < timeout:
        current = get_current_balance()
        if current is None:  # ignore blank OCR
            time.sleep(0.5)
            continue

        if before_balance is not None:
            if current > before_balance:
                return 'W'
            elif current < before_balance:
                return 'L'
            else:
                return 'BE'

        time.sleep(0.5)  # check twice per second

    return None  # timeout reached
def read_current_payout(retries=5, delay=1.0):
    x, y = 1089, 300
    width, height = 60, 30
    for attempt in range(retries): 
        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
                # Convert to OpenCV BGR
        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        # Convert to HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Wider green range
        lower_green = np.array([30, 30, 30])
        upper_green = np.array([100, 255, 255])
        mask = cv2.inRange(hsv, lower_green, upper_green)

        # Masked image
        result = cv2.bitwise_and(img, img, mask=mask)
        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

        # Enhance contrast
        gray = cv2.equalizeHist(gray)

        # Threshold
        _, thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)

        # OCR
        text = pytesseract.image_to_string(thresh, config='--psm 7 -c tessedit_char_whitelist=0123456789+.%')
        print("Payout OCR Text (green enhanced):", text)

        # Regex: + optional, number only
        match = re.search(r'\+?(\d+)', text)
        if match:
            return float(match.group(1))
        time.sleep(delay)
    return None
def change_pair(retries=5, delay=1.0):
    for attempt in range(retries): 
        print(f"[CHANGE PAIR] Attempt {attempt+1}/{retries}")

        # Dropdown open
        pyautogui.click(212, 177)
        time.sleep(4)

        print("Dropdown open")
        time.sleep(1)

        # Search box focus
        pyautogui.moveTo(434, 254, duration=0.5)
        time.sleep(0.5)

        pyautogui.doubleClick(434, 254)
        time.sleep(0.3)

        # Type eur
        pyautogui.write("eur", interval=0.05)
        time.sleep(0.5)

        pyautogui.press('enter')
        print("[INFO] Typed 'eur' and pressed Enter")
        time.sleep(2)

        # 🔥 1️⃣ FIRST: new_pair.jpg check
        location = pyautogui.locateOnScreen("new_pair.jpg", confidence=0.8)

        if location:
            print("[SUCCESS] new_pair.jpg found → clicking")
            pyautogui.click(pyautogui.center(location))
            time.sleep(2)
            return True

        # 🔁 2️⃣ SECOND: pair_select.jpg check
        location = pyautogui.locateOnScreen("pair_select.jpg", confidence=0.8)

        if location:
            print("[SUCCESS] pair_select.jpg found → clicking")
            pyautogui.click(pyautogui.center(location))
            time.sleep(2)
            return True

        # ❌ Agar dono na milen
        print("[INFO] No image found, retrying...")
        time.sleep(delay)

    print("[FAILED] ⚠️ Could not select new pair after retries")
    return False 

       
# ===================== CONFIGURATION =====================
AI_TRADING_BUTTON = (1251, 524)  # Pocket Option coordinates
CONTINUE_DEMO_BUTTON = (1540, 540)   # example – calibrate with F5
TOP_UP_CLOSE_BUTTON = (1670, 230)
NEW_SESSION_BUTTON = (1529, 431)  # Excel/Sheets coordinates
TRADE_RESULT_POSITION = (1300, 600)  # Position to check W/L result
PAYOUT_POSITION = (1097, 310)  # Position to check pair payout percentage
CURRENT_PAIR_POSITION = (1200, 350)  # Position to check current trading pair
SWITCH_PAIR_BUTTON = (1350, 400)  # Position of switch pair button
PLACE_TRADE_BUTTON = (1300, 650)  # Position to place trade
MARGIN_BUTTON = (1250, 700)  # Position of margin button
CONFIRM_TRADE_BUTTON = (1350, 650)  # Position to confirm trade

# Loading indicator positions (adjust based on your screen)
LOADING_INDICATORS = {
    'pocket_option': [
        (1200, 200, (60, 140, 180)),
        (1250, 250, (70, 150, 190)),
    ],
    'google_sheets': [
        (scale_x(0.45), scale_y(0.20), (66, 133, 244)),
        (scale_x(0.50), scale_y(0.25), (66, 133, 244)),
    ]
}


POCKET_OPTION_URL = "https://pocketoption.com/en/cabinet"
GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/1GGljR_W_wakgZEMEhT5iLsItLn-2WOSNeTsURndJmGM/edit?gid=1952273284#gid=1952273284"

POCKET_KEYWORDS = ['Pocket Option',
    'Innovative Trading',
    'pocketoption'] 

 
# Trading configuration

PAYOUT_THRESHOLD = 92  # Minimum payout percentage

# Available pairs with their typical payouts


# ===================== ENHANCED WEBPAGE DETECTION =====================

class WebpageDetector:
    @staticmethod
    def wait_for_loading_complete(timeout=30, check_interval=0.5):
        """Wait for webpage to finish loading by monitoring activity"""
        print(f"\n[LOADING] Waiting for page to load (max {timeout} seconds)...")
        
        start_time = time.time()
        last_change_time = time.time()
        last_screenshot = None
        
        while time.time() - start_time < timeout:
            # Take a screenshot of a small region
            current_screenshot = pyautogui.screenshot(region=(100, 100, 200, 200))
            
            if last_screenshot:
                # Check if screenshots are different (page is still loading)
                if not WebpageDetector.are_images_similar(current_screenshot, last_screenshot):
                    last_change_time = time.time()
                    print(f"[LOADING] Page still loading... changes detected")
            
            # If no changes for 3 seconds, assume page is loaded
            if time.time() - last_change_time > 3:
                print(f"[LOADING] ✓ Page appears to be fully loaded")
                return True
            
            last_screenshot = current_screenshot
            time.sleep(check_interval)
        
        print(f"[LOADING] ⚠️  Page loading timeout reached")
        return False
    
    @staticmethod
    def are_images_similar(img1, img2, threshold=0.95):
        """Check if two images are similar"""
        if img1.size != img2.size:
            return False
        
        pixels1 = list(img1.getdata())
        pixels2 = list(img2.getdata())
        
        similar_pixels = 0
        total_pixels = len(pixels1)
        
        for i in range(total_pixels):
            if abs(pixels1[i][0] - pixels2[i][0]) < 10 and \
               abs(pixels1[i][1] - pixels2[i][1]) < 10 and \
               abs(pixels1[i][2] - pixels2[i][2]) < 10:
                similar_pixels += 1
        
        similarity = similar_pixels / total_pixels
        return similarity > threshold

    @staticmethod
    def check_element_visible(position, expected_color=None, description="element"):
        """Check if a specific element is visible on screen"""
        try:
            x, y = position
            
            # Check if position is within screen bounds
            screen_width, screen_height = pyautogui.size()
            if not (0 <= x < screen_width and 0 <= y < screen_height):
                print(f"[VISIBILITY] ✗ {description} position out of bounds")
                return False
            
            # Check pixel color if expected color is provided
            if expected_color:
                pixel_color = pyautogui.pixel(x, y)
                color_match = all(
                    abs(pixel_color[i] - expected_color[i]) < 30 
                    for i in range(3)
                )
                
                if color_match:
                    print(f"[VISIBILITY] ✓ {description} is visible at ({x}, {y})")
                    return True
                else:
                    print(f"[VISIBILITY] ✗ {description} color mismatch")
                    return False
            else:
                # Just check if we can read pixel (basic visibility check)
                pyautogui.pixel(x, y)
                print(f"[VISIBILITY] ✓ {description} position is visible")
                return True
                
        except Exception as e:
            print(f"[VISIBILITY] ✗ Cannot access {description}: {e}")
            return False
    
    @staticmethod
    def verify_button_state(position, button_name, max_attempts=7):
        """Verify button is clickable before clicking"""
        print(f"\n[VERIFYING] Checking {button_name} button state...")
        
        for attempt in range(max_attempts):
            # Check if button area is visible
            x, y = position
            
            # Take a screenshot of button area
            try:
                button_area = pyautogui.screenshot(region=(x-20, y-20, 40, 40))
                
                # Save for debugging if needed
                debug_dir = "button_debug"
                os.makedirs(debug_dir, exist_ok=True)
                debug_file = os.path.join(debug_dir, f"{button_name}_attempt{attempt+1}.png")
                button_area.save(debug_file)
                
                # Check if button area looks "clickable" (not grayed out)
                avg_color = WebpageDetector.get_average_color(button_area)
                
                # Check if button is not too dark (grayed out)
                if avg_color > 20:  # Adjust this threshold as needed
                    print(f"[VERIFYING] ✓ {button_name} appears clickable")
                    return True
                else:
                    print(f"[VERIFYING] {button_name} may be disabled (attempt {attempt+1}/{max_attempts})")
                    
            except Exception as e:
                print(f"[VERIFYING] Error checking {button_name}: {e}")
            
            time.sleep(2)
        
        print(f"[VERIFYING] ✗ {button_name} not ready after {max_attempts} attempts")
        return False
    
    @staticmethod
    def get_average_color(image):
        """Get average brightness of an image"""
        pixels = list(image.getdata())
        if not pixels:
            return 0
        
        total_brightness = sum(sum(pixel[:3]) // 3 for pixel in pixels)
        return total_brightness // len(pixels)
    
    @staticmethod
    def wait_for_specific_content(positions_with_colors, timeout=20):
        """Wait for specific content to appear on screen"""
        print(f"[WAITING] Looking for specific content...")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            all_found = True
            
            for pos_data in positions_with_colors:
                if len(pos_data) == 2:  # position only
                    x, y = pos_data
                    if not WebpageDetector.check_element_visible((x, y), description="content"):
                        all_found = False
                        break
                elif len(pos_data) == 3:  # position with color
                    x, y, expected_color = pos_data
                    if not WebpageDetector.check_element_visible((x, y), expected_color, "content"):
                        all_found = False
                        break
            
            if all_found:
                print("[WAITING] ✓ All expected content found")
                return True
            
            time.sleep(0.5)
        
        print("[WAITING] ✗ Timeout waiting for content")
        return False

# ===================== ENHANCED MOUSE FUNCTIONS =====================

def safe_move_and_click(x, y, description="button", verify_first=True, max_retries=3):
    """Enhanced click function with webpage loading verification"""
    
    for attempt in range(max_retries):
        try:
            print(f"\n[{description.upper()}] Attempt {attempt + 1}/{max_retries}")
            
            # Step 1: Verify webpage is loaded
            if verify_first:
                print(f"[CHECK] Verifying webpage is loaded...")
                if not WebpageDetector.wait_for_loading_complete():
                    print(f"[CHECK] ⚠️  Page may not be fully loaded")
            
            # Step 2: Verify button is visible and clickable
            if verify_first:
                if not WebpageDetector.verify_button_state((x, y), description):
                    print(f"[CHECK] Button verification failed, retrying...")
                    time.sleep(2)
                    continue
            
            # Step 3: Move to position with visual feedback
            current_x, current_y = pyautogui.position()
            print(f"[MOUSE] Moving from ({current_x}, {current_y}) to ({x}, {y})")
            
            # Move in steps for visual verification
            pyautogui.moveTo(x, y, duration=0.7, tween=pyautogui.easeInOutQuad)
            time.sleep(0.3)
            
            # Verify we reached the target
            final_x, final_y = pyautogui.position()
            if abs(final_x - x) > 10 or abs(final_y - y) > 10:
                print(f"[MOUSE] Missed target: ({final_x}, {final_y}) vs ({x}, {y})")
                continue
            
            # Step 4: Highlight position briefly
            for _ in range(2):
                pyautogui.mouseDown()
                time.sleep(0.05)
                pyautogui.mouseUp()
                time.sleep(0.05)
            
            # Step 5: Perform the actual click
            pyautogui.click()
            print(f"[SUCCESS] ✓ Successfully clicked {description} at ({x}, {y})")
            
            # Step 6: Wait for action to complete
            action_wait_time = 1.5 if "AI Trading" in description or "New Session" in description else 0.5
            print(f"[WAIT] Waiting {action_wait_time}s for action to complete...")
            time.sleep(action_wait_time)
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print(f"[RETRY] Waiting 2 seconds before retry...")
                time.sleep(2)
    
    print(f"[FAILED] ✗ Could not click {description} after {max_retries} attempts")
    return False
import pyautogui
import time

def click_button_by_image(image_path, description="button", max_attempts=5):
    for attempt in range(max_attempts):
        print(f"[{description.upper()}] Attempt {attempt+1}/{max_attempts}")
        try:
            # Use confidence for fuzzy matching
            location = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
            if location:
                pyautogui.moveTo(location.x, location.y, duration=0.5)
                pyautogui.click()
                print(f"[SUCCESS] ✓ Clicked {description} at {location}")
                return True
            else:
                print(f"[INFO] {description} image not found on screen")
        except Exception as e:
            print(f"[ERROR] Image click failed: {e}")
        time.sleep(1)
    print(f"[FAILED] ✗ Could not click {description}")
    return False
def click_top_tab(image_path="top_tab.jpg", max_attempts=5):
    """
    Click on the top browser tab using image recognition
    """
    for attempt in range(max_attempts):
        print(f"[TOP TAB] Attempt {attempt+1}/{max_attempts}")
        try:
            # Only check top 150px of the screen for speed
            region = (0, 0, pyautogui.size().width, 150)
            location = pyautogui.locateCenterOnScreen(image_path, confidence=0.7, region=region)
            if location:
                pyautogui.moveTo(location.x, location.y, duration=0.5)
                pyautogui.click()
                print(f"[SUCCESS] ✓ Clicked top tab at {location}")
                return True
            else:
                print("[INFO] Top tab image not found on screen")
        except Exception as e:
            print(f"[ERROR] Image click failed: {e}")
        time.sleep(1)
    print("[FAILED] ✗ Could not click top tab")
    return False

def wait_and_verify_page_load(page_type, timeout=30):
    """Wait for specific page to load and verify key elements"""
    print(f"\n[PAGE LOAD] Waiting for {page_type} to load...")
    
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        # Check for loading indicators
        if page_type in LOADING_INDICATORS:
            loading_detected = False
            for indicator in LOADING_INDICATORS[page_type]:
                if len(indicator) == 3:
                    x, y, loading_color = indicator
                    try:
                        screen_width, screen_height = pyautogui.size()

                        # Check if coordinate is inside screen
                        if 0 <= x < screen_width and 0 <= y < screen_height:
                            pixel_color = pyautogui.pixel(x, y)
                        else:
                            print(f"[WARNING] Coordinate out of screen: {x},{y}")
                            return False

                    except Exception as e:
                        print(f"[WARNING] Pixel read failed: {e}")
                        return False

                    color_diff = sum(abs(pixel_color[i] - loading_color[i]) for i in range(3))
                    if color_diff < 50:  # Still showing loading colors
                        loading_detected = True
                        break
            
            if not loading_detected:
                print(f"[PAGE LOAD] ✓ {page_type} loading indicators cleared")
                
                # Additional verification for specific pages
                if page_type == 'google_sheets':
                    # Check for spreadsheet grid
                    if WebpageDetector.check_element_visible((scale_x(0.60), scale_y(0.40)), description="Spreadsheet grid"):
                        print(f"[PAGE LOAD] ✓ Google Sheets fully loaded")
                        return True
                
                elif page_type == 'pocket_option':
                    # Check for trading interface
                    if WebpageDetector.check_element_visible((1250, 500), description="Trading interface"):
                        print(f"[PAGE LOAD] ✓ Pocket Option fully loaded")
                        return True
        
        time.sleep(1)
    
    print(f"[PAGE LOAD] ⚠️  {page_type} load timeout, proceeding anyway")
    return False

# ===================== ENHANCED BROWSER MANAGEMENT =====================

class BrowserManager:

     @staticmethod
     def open_and_wait(url, page_type, window_title_keywords, timeout=30):
        """Open URL and wait for page to fully load"""
        print(f"\n[BROWSER] Opening {page_type}...")
        print(f"[URL] {url}")
        
        webbrowser.open(url)
        time.sleep(3)

        window_activated = False
        for attempt in range(5):
            windows = gw.getAllWindows()
            for window in windows:
                window_title = window.title.lower()
                if any(keyword.lower() in window_title for keyword in window_title_keywords):
                    if window.isMinimized: 
                        window.restore()
                        window.activate()
                    
                    print(f"[WINDOW] ✓ Activated: {window.title[:50]}")
                    window_activated = True
                    break

            if window_activated:
                break

            print(f"[WINDOW] Attempt {attempt + 1}: Window not found, waiting...")
            time.sleep(2)

        if not window_activated:
            print(f"[WARNING] Could not find {page_type} window")

        wait_and_verify_page_load(page_type, timeout)

        print(f"[BROWSER] Waiting for dynamic content...")
        time.sleep(3)

        return window_activated

     @staticmethod
     def switch_to_window(title_keywords, bring_to_front=True):
        """Switch to window containing specific keywords"""

        windows = gw.getAllWindows()

        for window in windows:
            window_title = window.title.lower()

            for keyword in title_keywords:
                if keyword.lower() in window_title:
                    try:
                        if bring_to_front:
                            if window.isMinimized:
                                window.restore()
                            window.activate()
                            time.sleep(1)

                        print(f"[SWITCH] ✓ Activated: {window.title}")
                        return True

                    except Exception as e:
                        print(f"[SWITCH ERROR] {e}")

        print(f"[SWITCH] ✗ Window not found: {title_keywords}")
        return False

# ===================== ENHANCED TRADE TRACKER =====================

class EnhancedTradeTracker:
    def __init__(self):
        # Trade counting
        self.current_trade_count = 0
        self.current_wins = 0
        self.current_losses = 0
        self.consecutive_losses = 0

        # Trading limits (define karo)
        self.total_trades = 12      # total trades per session
        self.win_trades = 2         # target wins
        self.loss_trades = self.total_trades - self.win_trades  # allowed losses

        # Margin / Pair
        self.base_margin = 1.0
        self.margin_multiplier = 1.0
        self.current_pair = None

        # Daily stop-loss
        self.highest_balance = 0
        self.daily_stop_loss = None
        self.start_of_day = datetime.now().date()
        self.trade_history = []
        print("[TRADE TRACKER] Initialized with total_trades =", self.total_trades)
    def read_total_trades_from_sheet(self):
            """Read total trades directly from Google Sheets using specific coordinates"""

            if not BrowserManager.switch_to_window(['Google Sheets', 'Sheets']):
                print("[ERROR] Could not switch to Google Sheets")
                return self.total_trades

            # Click the cell at specific coordinates
            pyautogui.click(881, 428)  # Mouse coordinate for total trades cell
            time.sleep(0.2)

            # Copy the value
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.1)
            value = pyperclip.paste().strip()

            try:
                total = int(value)
                print(f"[SHEET] Total trades read from coordinate: {total}")

                # Update tracker values
                self.total_trades = total
                self.loss_trades = self.total_trades - self.win_trades

                return total

            except ValueError:
                print("[ERROR] Could not read total trades from sheet, keeping previous value")
                return self.total_trades
    def read_trade_amount(tracker):
        """Google Sheets se current trade amount read karo"""
        if not BrowserManager.switch_to_window(['Google Sheets', 'Sheets']):
            print("[ERROR] Google Sheets switch failed")
            return tracker.base_margin  # fallback

        start_row = 5  # first trade row
        column_index = 4  # Column D (trade amount column)
        target_row = start_row + tracker.current_trade_count

        # Go to top-left (A1)
        pyautogui.hotkey('ctrl', 'home')
        time.sleep(0.2)

        # Move down to target row
        pyautogui.press('down', presses=target_row-1, interval=0.05)

        # Move right to trade amount column
        pyautogui.press('right', presses=column_index-1, interval=0.05)

        # Copy value
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.1)
        trade_amount_text = pyperclip.paste().strip()

        # Replace comma with dot
        trade_amount_text = trade_amount_text.replace("$", "").replace(",", ".").strip()

        try:
            amount = float(trade_amount_text)
            print(f"[TRADE AMOUNT] Successfully read: {amount}")
            return amount
        except:
            print(f"[ERROR] Could not convert '{trade_amount_text}' to float. Using base margin.")
            return tracker.base_margin
    def sync_trade_count_from_sheet(self):
        """
        Google Sheet se detect karo ke kitni trades already complete ho chuki hain
        """
        print("[SYNC] Checking existing trade results in Google Sheet...")

        if not BrowserManager.switch_to_window(['Google Sheets', 'Sheets']):
            print("[ERROR] Cannot switch to Google Sheets for sync")
            return

        pyautogui.hotkey('ctrl', 'home')
        time.sleep(0.5)

        start_row = 5
        completed_trades = 0

        for i in range(self.total_trades):
            target_row = start_row + i

            pyautogui.hotkey('ctrl', 'home')
            time.sleep(0.2)

            pyautogui.press('down', presses=target_row-1, interval=0.03)
            pyautogui.press('right', presses=2, interval=0.03)  # Result column

            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.1)

            cell_value = pyperclip.paste().strip().upper()

            if cell_value in ['W', 'L']:
                completed_trades += 1
            else:
                break  # stop when empty row found

        self.current_trade_count = completed_trades
        print(f"[SYNC] Found {completed_trades} completed trades. Starting from next row.")

    def update_trade_result(self, result, trade_amount=None, pair=None, payout=None):
        """Google Sheets mein W/L update karo"""
        max_attempts = 5
        attempt = 0
        success = False

        while not success and attempt < max_attempts:
            attempt += 1
            if not BrowserManager.switch_to_window(['Google Sheets', 'Sheets']):
                print(f"[SPREADSHEET] Attempt {attempt}: Could not switch")
                time.sleep(1)
                continue

            pyautogui.hotkey('ctrl', 'home')
            time.sleep(0.2)
            start_row = 5
            target_row = start_row + self.current_trade_count
            pyautogui.press('down', presses=target_row-1, interval=0.05)
            pyautogui.press('right', presses=2, interval=0.05)  # Column C ya result column

            pyautogui.typewrite(result.upper(), interval=0.05)
            pyautogui.press('enter')
            print(f"[SPREADSHEET] Trade result '{result}' updated in row {target_row}")
            success = True

        if result and result.upper() == 'W':
            self.current_wins += 1
            self.consecutive_losses = 0  
            print("[TRACKER] Win detected → Consecutive losses reset to 0")
            
        else :
            self.current_losses += 1
            self.consecutive_losses += 1
            print(f"[TRACKER] Loss detected → Consecutive losses: {self.consecutive_losses}")

        self.current_trade_count += 1
        self.trade_history.append({
            'trade_number': self.current_trade_count +1 ,
            'result': result.upper(),
            'margin': trade_amount or self.base_margin,
            'pair': pair or self.current_pair,
            
        })



    def check_new_day(self):
        """Check if new day started"""
        today = datetime.now().date()
        if today != self.start_of_day:
            print("[NEW DAY] ✨ New day detected, resetting tracker")
            self.start_of_day = today
            self.current_trade_count = 0
            self.current_wins = 0
            self.current_losses = 0
            self.highest_balance = 0
            self.daily_stop_loss = None
            return True
        return False


# ===================== ENHANCED TRADING BOT =====================

class EnhancedTradingBot:
    def __init__(self):
        print("\n" + "="*60)
        print("ENHANCED TRADING BOT WITH LOADING DETECTION")
        print("="*60)
        
        self.tracker = EnhancedTradeTracker()
        self.eur_pairs = [
    "EUR/USD",
    "EUR/JPY",
    "EUR/GBP",
    "EUR/CHF",
    "EUR/AUD",
    "EUR/NZD",
    "EUR/CAD"
                  ]

# Rotation control
        self.current_pair_index = 0
        self.pair_switched_this_cycle = False
        self.is_running = False
        
        screen_width, screen_height = pyautogui.size()
        print(f"Screen: {screen_width} x {screen_height}")
        print("="*60)
    
    def initialize_google_sheets(self):
        """Open and initialize Google Sheets with proper loading waits"""
        print("\n" + "="*60)
        print("INITIALIZING GOOGLE SHEETS")
        print("="*60)
        
        # Open Google Sheets
        BrowserManager.open_and_wait(
            url=GOOGLE_SHEETS_URL,
            page_type='google_sheets',
            window_title_keywords=['Google Sheets', 'Sheets'],
            timeout=40
        )
        
        # Wait for complete load
        time.sleep(3)
        
    
            
            
            # Wait for spreadsheet to be ready for input
        WebpageDetector.wait_for_loading_complete(timeout=10)
        time.sleep(2)
        self.tracker.read_total_trades_from_sheet()    
            # Set initial values (simulated)
        print("\n[SETUP] Setting initial values in spreadsheet:")
        print(f"  • Total Trades: {self.tracker.total_trades}")
        print(f"  • Win Trades: {self.tracker.win_trades}")
        print(f"  • Loss Trades: {self.tracker.loss_trades}")
            
            # Additional wait for spreadsheet processing
        time.sleep(2)
        self.tracker.sync_trade_count_from_sheet()    
        return True
        
    
    # initialize_pocket_option me AI button click hata do
    def initialize_pocket_option(self):
        print("\n" + "="*60)
        print("INITIALIZING POCKET OPTION")
        print("="*60)

        # Open Pocket Option
        BrowserManager.open_and_wait(
            url=POCKET_OPTION_URL,
            page_type='pocket_option',
            window_title_keywords=POCKET_KEYWORDS,
            timeout=40
        )

        # Additional wait for trading interface
        print("[WAIT] Waiting for trading interface to load...")
        time.sleep(5)

        # Remove AI Trading button click from here
        # self.tracker.current_pair = random.choice(list(AVAILABLE_PAIRS.keys()))
        # print(f"[SETUP] Starting with pair: {self.tracker.current_pair}")

        return True

    
    def execute_trade_cycle(self):

    # Step 1: Read amount from sheet
        trade_amount = self.tracker.read_trade_amount()

        # Step 2: Switch to Pocket Option
        if not click_top_tab("top_tab.jpg"):
              return "ERROR"
        time.sleep(4)
        payout = read_current_payout()
        print(f"[DEBUG] Payout OCR Text: {payout}")
        if payout is None:
            print("Payout not read, trade continue")
        elif payout >= 92:
            print(f"Payout {payout}%  → trade continue")
        else:
            print(f"Payout {payout}%  → pair change ")
            change_pair()
        amount_x, amount_y = 1112, 256

        print(f"[INFO] Clicking Amount field at ({amount_x}, {amount_y})")

        try:
            # Click on amount field
            pyautogui.click(amount_x, amount_y)
            time.sleep(0.5)
            
            # Double click to select old value
            pyautogui.doubleClick(amount_x, amount_y)
            time.sleep(0.5)
            
            # Select all and paste new trade amount
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.2)
            
            pyperclip.copy(f"{trade_amount:.2f}")
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.2)
            
            pyautogui.press('enter')
            print(f"[SUCCESS] Trade amount set to {trade_amount:.2f}")

        except Exception as e:
            print(f"[ERROR] Could not set trade amount: {e}")
            print("[WARNING] Using Sheet value instead")
            trade_amount = self.tracker.read_trade_amount()


        before_balance = get_current_balance()
        print("Balance Before:", before_balance)   

        # Step 5: Click AI Trade
        click_button_by_image("ai_trading_button.jpg", "AI Trading Button")
      
        time.sleep(40.0)
        # Step 6: Wait for balance change
        result = wait_for_balance_change(before_balance, timeout=60)
        # 🔁 Break-even handling
        while result == 'BE':
            print("[ACTION] Break-even detected → Clicking AI Trading again")
            time.sleep(4)
            payout = read_current_payout()
            print(f"[DEBUG] Payout OCR Text: {payout}")
            if payout is None:
                print("Payout not read, trade continue")
            elif payout >= 92:
                print(f"Payout {payout}%  → trade continue")
            else:
                print(f"Payout {payout}%  → pair change ")
                safe_move_and_click(212, 177, description="Switch pair dropdown") 
                time.sleep(2) 
            click_button_by_image("pair_select.jpg", "Select new pair")
            time.sleep(2)
            click_button_by_image("ai_trading_button.jpg", "AI Trading Button")

            # Wait again for trade to close
            time.sleep(40)

            # Check result again
            result = wait_for_balance_change(before_balance, timeout=60)

            print(f"[INFO] Result after BE re-trade: {result}")
            if result in ['W', 'L']:
                print(f"[FINAL RESULT] {result} → Updating Google Sheet")
                break
              
        # Step 7: Switch to Google Sheet
        if not click_top_tab("top_tab2.jpg"):
            return "ERROR"

        # Step 8: Update sheet
        self.tracker.update_trade_result(result, trade_amount=trade_amount)
        pair_switch_threshold = self.tracker.total_trades - 3

        if (
            self.tracker.current_losses >= pair_switch_threshold
            and not self.pair_switched_this_cycle
        ):

            print("[PAIR SWITCH] Loss threshold reached → switching pair and placing trade")

            # 1️⃣ Read next trade amount
            trade_amount = self.tracker.read_trade_amount()
            print(f"[PAIR SWITCH] Next trade amount from sheet: {trade_amount}")

            # 2️⃣ Switch to trading tab
            click_top_tab("top_tab.jpg")
            time.sleep(3)

            # 3️⃣ Get next pair
            self.current_pair_index += 1

            if self.current_pair_index >= len(self.eur_pairs):
                self.current_pair_index = 0

            next_pair = self.eur_pairs[self.current_pair_index]

            print(f"[PAIR SWITCH] Changing pair to {next_pair}")
            

            pyautogui.click(212, 177)
            time.sleep(4)

            print("Dropdown open")
            time.sleep(1)
            
            expected_coords = [(620, 354), (623, 384), (617, 416), (627, 446)]

            # Choose the pair you want (for example, index 0)
            target_coords = expected_coords[0]

            # Click the exact pair
            pyautogui.click(target_coords)
            print(f"[PAIR SELECT] Clicked pair at {target_coords}")
            time.sleep(2)
            self.tracker.current_pair = next_pair
            self.pair_switched_this_cycle = True

            # 4️⃣ Enter trade amount
            amount_x, amount_y = 1112, 256

            print(f"[PAIR SWITCH] Setting new trade amount {trade_amount}")

            pyautogui.click(amount_x, amount_y)
            time.sleep(0.5)

            pyautogui.doubleClick(amount_x, amount_y)
            time.sleep(0.5)

            pyautogui.hotkey('ctrl', 'a')

            pyperclip.copy(f"{trade_amount:.2f}")
            pyautogui.hotkey('ctrl', 'v')

            pyautogui.press('enter')

            time.sleep(1)

            # 5️⃣ Place trade
            print("[PAIR SWITCH] Placing trade after pair switch")

            click_button_by_image("ai_trading_button.jpg", "AI Trading Button")
            time.sleep(40)

            # Check result again
            result = wait_for_balance_change(before_balance, timeout=60)
            if not click_top_tab("top_tab2.jpg"):
             return "ERROR"
            self.tracker.update_trade_result(result, trade_amount=trade_amount)
            
        # ===================== GREAT LOSS CHECK =====================
        great_loss_threshold = self.tracker.total_trades - 1
        if self.tracker.consecutive_losses >= great_loss_threshold:
            print(f"[SAFETY RESET] Great Loss triggered ({self.tracker.consecutive_losses} consecutive losses) → Resetting session.")

            # Reset tracker counters
            self.tracker.current_trade_count = 0
            self.tracker.current_wins = 0
            self.tracker.current_losses = 0
            self.tracker.consecutive_losses = 0

            # Click margin field and set default value
            print("[RESET] Moving to margin field (849, 404)")
            pyautogui.moveTo(849, 404, duration=3)
            time.sleep(1)
            pyautogui.click()
            time.sleep(1)
            pyperclip.copy("700")
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.5)
            pyautogui.press('enter')

            # Click New Session button
            click_button_by_image("new_session_button.jpg", "New Session Button", max_attempts=5)
            time.sleep(7)
            pyautogui.click(304,404)  # Mouse coordinate for total trades cell
            time.sleep(0.2)
            # Copy the value
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.1)
            
           # Reset tracker counters
            self.tracker.current_trade_count = 0
            self.tracker.current_wins = 0
            self.tracker.current_losses = 0
            self.tracker.consecutive_losses = 0

            # Re-read trade amount after UI fully loads
            trade_amount = self.tracker.read_trade_amount()
            print(f"[RESET] After Great Loss reset, new trade amount: {trade_amount}")
            time.sleep(4)

            # Ensure pair switch flag reset
            self.pair_switched_this_cycle = False    

            
        
        
        if result == 'W':
            print("[ACTION] Trade won → Resetting session and tracker counters...")

            # Reset counters first
            self.tracker.current_trade_count = 0
            self.tracker.current_wins = 0
            self.tracker.current_losses = 0
            self.consecutive_losses = 0


            # Click New Session button
            click_button_by_image("new_session_button.jpg", "New Session Button", max_attempts=5)
            time.sleep(7)

            # After reset, read **trade amount from row 5, column D**
            trade_amount = self.tracker.read_trade_amount()
            print(f"[RESET] After session reset, new trade amount: {trade_amount}")

        return result
        

    def run_safe_trading_bot(self):
        """Main trading loop with all safety checks"""
        print("\n" + "="*60)
        print("STARTING SAFE TRADING BOT")
        print("="*60)
        
        self.is_running = True
        
        try:
            # Step 1: Initialize Pocket Option FIRST
            if not self.initialize_pocket_option():
                print("[ERROR] Failed to initialize Pocket Option")
                return
            
            time.sleep(3)
            
            # Step 2: Initialize Google Sheets AFTER AI button click
            if not self.initialize_google_sheets():
                print("[ERROR] Failed to initialize Google Sheets")
                return
            
            # Main trading loop
            print("\n" + "="*60)
            print("ENTERING MAIN TRADING LOOP")
            print("="*60)
            
            while (self.is_running and 
                   self.tracker.current_trade_count < self.tracker.total_trades):
                
                print(f"\n[PROGRESS] Trade {self.tracker.current_trade_count + 1}/{self.tracker.total_trades}")
                print(f"[STATUS] Wins: {self.tracker.current_wins}/{self.tracker.win_trades}")
                print(f"[STATUS] Losses: {self.tracker.current_losses}/{self.tracker.loss_trades}")
                
                # Execute trading cycle
                result = self.execute_trade_cycle()

                
                if result == "TARGET_ACHIEVED":
                    print("\n🎉 TARGET ACHIEVED! Required wins reached!")
                    break
                elif result == "STOP_LOSS":
                    print("\n⚠️  STOP LOSS TRIGGERED! Maximum losses reached!")
                    break
                elif result == "MAX_TRADES":
                    print("\n📊 MAXIMUM TRADES REACHED!")
                    break
                elif result == "CONTINUE":
                    continue
                elif result == "ERROR":
                    print("\n❌ ERROR in trading cycle!")
                    break
                
                # Check for manual stop
                if keyboard.is_pressed('esc'):
                    print("\n[USER] Manual stop requested")
                    break
                
                # Brief pause between cycles
                time.sleep(1)
            
            # Final report
            self.generate_final_report()
            
        except KeyboardInterrupt:
            print("\n[USER] Trading interrupted by user")
        except Exception as e:
            print(f"\n[ERROR] Trading bot error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.is_running = False
    
    def generate_final_report(self):
        """Generate detailed final report"""
        print("\n" + "="*60)
        print("FINAL TRADING REPORT")
        print("="*60)
        
        if self.tracker.current_trade_count > 0:
            win_rate = (self.tracker.current_wins / self.tracker.current_trade_count) * 100
        else:
            win_rate = 0
        
        print(f"\n📈 PERFORMANCE SUMMARY:")
        print(f"   Total Trades Executed: {self.tracker.current_trade_count}")
        print(f"   Wins: {self.tracker.current_wins}")
        print(f"   Losses: {self.tracker.current_losses}")
        print(f"   Win Rate: {win_rate:.1f}%")
        print(f"   Final Pair: {self.tracker.current_pair}")
        
        if self.tracker.trade_history:
            print(f"\n📋 TRADE HISTORY:")
            for trade in self.tracker.trade_history[-10:]:  # Show last 10 trades
                result_symbol = "✅" if trade['result'] == 'W' else "❌"
                print(f"   #{trade['trade_number']}: {result_symbol} ${trade['margin']:.2f} | {trade['payout']}% | {trade['pair']}")
        
        print("\n" + "="*60)
    
    def test_loading_detection(self):
        """Test the webpage loading detection system"""
        print("\n" + "="*60)
        print("TESTING LOADING DETECTION SYSTEM")
        print("="*60)
        
        test_url = "https://google.com"
        print(f"\n[TEST] Opening test page: {test_url}")
        webbrowser.open(test_url)
        time.sleep(3)
        
        print("[TEST] Testing loading detection...")
        if WebpageDetector.wait_for_loading_complete(timeout=15):
            print("[TEST] ✓ Loading detection working")
        else:
            print("[TEST] ✗ Loading detection failed")
        
        print("[TEST] Testing element visibility check...")
        test_position = (500, 300)
        if WebpageDetector.check_element_visible(test_position, description="Test position"):
            print("[TEST] ✓ Element visibility check working")
        else:
            print("[TEST] ✗ Element visibility check failed")
        
        print("\n[TEST] Loading detection test complete")
        print("="*60)
    
    def calibrate_coordinates(self):
        """Help user calibrate button coordinates"""
        print("\n" + "="*60)
        print("COORDINATE CALIBRATION MODE")
        print("="*60)
        
        print("\n📋 INSTRUCTIONS:")
        print("1. Move your mouse to each button position")
        print("2. Press F9 to save the current position")
        print("3. Press ESC to exit calibration")
        
        print("\n🔧 CALIBRATE BUTTONS:")
        print("  [1] AI Trading Button")
        print("  [2] New Session Button")
        print("  [3] Trade Result Position")
        print("  [4] Payout Position")
        
        current_button = None
        
        try:
            while True:
                x, y = pyautogui.position()
                print(f"\rMouse: ({x}, {y}) - Calibrating: {current_button}", end="")
                
                if keyboard.is_pressed('1'):
                    current_button = "AI Trading Button"
                    print(f"\n[SAVED] {current_button}: ({x}, {y})")
                    time.sleep(0.5)
                
                if keyboard.is_pressed('2'):
                    current_button = "New Session Button"
                    print(f"\n[SAVED] {current_button}: ({x}, {y})")
                    time.sleep(0.5)
                
                if keyboard.is_pressed('esc'):
                    print("\n\n[EXIT] Calibration complete")
                    break
                
                time.sleep(0.1)
        
        except KeyboardInterrupt:
            print("\n\n[EXIT] Calibration interrupted")
    
    def run(self):
        """Main bot interface with enhanced controls"""
        print("\n" + "="*60)
        print("ENHANCED TRADING BOT CONTROLS")
        print("="*60)
        print("\n🛠️  COMMANDS:")
        print("  F1  = Start safe trading bot")
        print("  F2  = Initialize Google Sheets")
        print("  F3  = Initialize Pocket Option")
        print("  F4  = Test loading detection")
        print("  F5  = Calibrate coordinates")
        print("  F6  = Show current status")
        print("  F7  = Generate report")
        print("  ESC = Exit")
        print("="*60)
        
        try:
            while True:
                if keyboard.is_pressed('f1'):
                    print("\n[START] Starting safe trading bot...")
                    self.run_safe_trading_bot()
                    time.sleep(0.5)
                    while keyboard.is_pressed('f1'):
                        time.sleep(0.1)
                
                if keyboard.is_pressed('f2'):
                    print("\n[INIT] Initializing Google Sheets...")
                    self.initialize_google_sheets()
                    time.sleep(0.5)
                    while keyboard.is_pressed('f2'):
                        time.sleep(0.1)
                
                if keyboard.is_pressed('f3'):
                    print("\n[INIT] Initializing Pocket Option...")
                    self.initialize_pocket_option()
                    time.sleep(0.5)
                    while keyboard.is_pressed('f3'):
                        time.sleep(0.1)
                
                if keyboard.is_pressed('f4'):
                    print("\n[TEST] Testing loading detection...")
                    self.test_loading_detection()
                    time.sleep(0.5)
                    while keyboard.is_pressed('f4'):
                        time.sleep(0.1)
                
                if keyboard.is_pressed('f5'):
                    print("\n[CALIBRATE] Entering calibration mode...")
                    self.calibrate_coordinates()
                    time.sleep(0.5)
                    while keyboard.is_pressed('f5'):
                        time.sleep(0.1)
                
                if keyboard.is_pressed('f6'):
                    print("\n[STATUS] Current bot status:")
                    print(f"  Trades: {self.tracker.current_trade_count}/{self.tracker.total_trades}")
                    print(f"  Wins: {self.tracker.current_wins}/{self.tracker.win_trades}")
                    print(f"  Losses: {self.tracker.current_losses}/{self.tracker.loss_trades}")
                    print(f"  Current Pair: {self.tracker.current_pair}")
                    print(f"  Margin Multiplier: {self.tracker.margin_multiplier}")
                    time.sleep(0.5)
                    while keyboard.is_pressed('f6'):
                        time.sleep(0.1)
                
                if keyboard.is_pressed('f7'):
                    print("\n[REPORT] Generating current report...")
                    self.generate_final_report()
                    time.sleep(0.5)
                    while keyboard.is_pressed('f7'):
                        time.sleep(0.1)
                
                if keyboard.is_pressed('esc'):
                    print("\n[EXIT] Stopping bot...")
                    self.is_running = False
                    break
                
                time.sleep(0.1)
        
        except KeyboardInterrupt:
            print("\n[INFO] Bot stopped by user")
        
        finally:
            print("\n" + "="*60)
            print("BOT SESSION COMPLETE")
            print("="*60)

# ===================== MAIN =====================

if __name__ == "__main__":
    try:
        # Safety configuration
        pyautogui.FAILSAFE = True  # Enable fail-safe for safety
        pyautogui.PAUSE = 0.1  # Small pause between actions
        
        print("\n" + "="*60)
        print("SAFE TRADING BOT WITH WEBPAGE VERIFICATION")
        print("="*60)
        print(f"\n⚙️  CONFIGURATION:")
        
        
        print(f"  Payout Threshold: {PAYOUT_THRESHOLD}%")
        print(f"  Timeouts: 30-40 seconds for page loads")
        print("="*60)
        
        # Create debug directory
        os.makedirs("button_debug", exist_ok=True)
        os.makedirs("screenshots", exist_ok=True)
        
        print("\n⚠️  IMPORTANT: Before starting:")
        print("1. Make sure browsers are installed")
        print("2. You're logged into both platforms")
        print("3. Use F5 to calibrate coordinates first")
        
        print("\nStarting in 5 seconds...")
        for i in range(5, 0, -1):
            print(f"  {i}...")
            time.sleep(1)
        
        bot = EnhancedTradingBot()
        bot.run()
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
        