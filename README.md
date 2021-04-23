# Crypto dashboard
A simple way to monitor your favorite cryptocurrencies and your wallet on the crypto.org chain (CRO).
![screenshot of the dashboard](https://user-images.githubusercontent.com/37737972/115888660-73626080-a453-11eb-8291-2796212947e1.png)


# How to preview
1. Python must be installed. You will find all the files and instructions [here](https://www.python.org/downloads/)
2. Run the `crypto_dashboard.py` script with python
3. In your favorite browser, access [localhost:5000](localhost:5000)

# How to setup for run
## Prerequisites
1. Python must be installed. You will find all the files and instructions [here](https://www.python.org/downloads/)
2. You must have an API Key for CoinMarketCap. You can get one for free by opening a Basic account [on their website](https://pro.coinmarketcap.com/)
3. If you don't have a address on the CRO chain yet, you may use one of [these wallets](https://crypto.org/wallets) to create one. Please keep your public address in mind, since we will need it soon. **Be careful !!** _Never disclose your mnemonic phrase or private key to anyone! They may be able to access your funds._

## Setting up the app
1. Open the `config.json` file in your favorite text editor
2. Paste your API key and CRO address in the indicated places
3. Where prompted, type the tickers for the cryptocurrencies you want to track. If you have several, use a coma `,`as separator.
4. Switch the value of `testMode` to `false`
5. Save the file

## Dark mode
You can chose whether to use light or dark theme for the user interface. To do so :
1. Open the `config.json` file in your favorite text editor
2. Switch the value of `darkMode` to `false` if you want light mode. Set it to `true`if you want to enable dark mode.
3. Save the file

## Launching the app
Run the `crypto_dashboard.py` script with python.

## Using the app
In your favorite browser, access [localhost:5000](localhost:5000)
