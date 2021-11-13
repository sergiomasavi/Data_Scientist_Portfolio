echo "Installing environment on Mac M1"
sleep 5s
echo "Installing pandas (version=1.3.4)"
pip install pandas
echo "Installing numpy (verison=1.21.4)"
pip install numpy
echo "Installing sklearn (version=1.0.1)"
pip install sklearn
echo "Installing yfinance (version=0.1.44)"
pip install yfinance
echo "Installing Graphviz (version=0.18)"
conda install -c conda-forge python-graphviz
echo "Installing quandl (version=3.7.0)"
conda install -c anaconda quandl
echo "Instaling talib"
brew install ta-lib
conda install -c conda-forge ta-lib