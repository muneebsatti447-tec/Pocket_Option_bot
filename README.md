Pocket Option Trade Manager Automation Bot

This project automates the trading workflow between Pocket Option and a Trade Manager.

Features
Opens Pocket Option and Trade Manager automatically.
Reads the current trade amount from the Trade Manager.
Updates the trade amount in Pocket Option.
Clicks the AI Trade button to execute a trade.
Monitors the trade result (Win/Loss).
On Win:
Marks W in the Trade Manager.
Starts a new session.
Reads the new trade amount.
Updates Pocket Option with the new amount.
Continues trading.
On Loss:
Marks L next to the traded amount.
Waits for the Trade Manager to generate the next amount.
Updates Pocket Option with the new amount.
Continues trading until a winning trade occurs.
Implements a daily stop-loss equal to 20% below the highest account balance reached during the day.
Automatically resets and starts a new trading session when a new day begins.
Technologies
Python
Selenium or Playwright
PyAutoGUI (optional)
OpenCV (optional for screen recognition)

Disclaimer: This project is for educational and automation purposes only. Users are responsible for complying with the terms and conditions of their broker or trading platform. Automated trading may involve financial risk.
