### Setup Steps:
1. Download Python Version 3 
2. pull intouch-ui-python in git
3. in the terminal run the following: 
```
python3 -m venv VENV
. VENV/bin/activate
pip install -r requirements.txt 
deactivate
```
4. Set Python Interpreter preferences in your IDE to your `VENV/bin/python` path.
3. Run a test using IDE

### Run Steps by folder
1. using cmd in window, navigate to the test folder and type in pytest folder_name/
ex. pytest crowdstreet_registration/ --reruns 3 --html=.\reports\report.html

### different option on running the scripts
1. install pip install pytest-rerunfailures
2. install pip install pytest-html
2. run using this command pytest --reruns 3 --html=.\reports\report.html
3. run with delay pytest --reruns 5 --reruns-delay 1
4. individual failure: @pytest.mark.flaky(reruns=5)
5. individual with delay @pytest.mark.flaky(reruns=5, reruns_delay=2)
6. parallel pip install pytest-xdist then syntax to run ----> pytest -n 3
