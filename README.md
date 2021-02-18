# libinhood

## Install
git clone https://github.com/SichengLi/libinhood.git
cd libinhood
sudo python3 setup.py install

## Usage
### placeStopLossOrderForAllYourStocks.py
- go into placeStopLossOrderForAllYourStocks.py, paste your Robinhood username and password
- run it. You will receive a SMS code on your phone for login verification
- this program will: read all your stocks -> place a Stop Loss Sell order for each of your stock, the stop_loss_price is based on current price (e.g. stop_loss_price = current_price * 0.984)
- by default the order is to sell all your quantity