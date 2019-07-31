## Soundrebound ServerBIT + p5 sketch

0. Ensure ServerBIT configuration is alright:
  -  config.json
  -  ServerBIT.py => comment out thread.start_new_thread(BITalino_handler...)
  -  ServerBIT.py => launch thread.start_new_thread(BITalino_simulate...) instead  
  -  check that the .txt acquisition file is available
  -  check that the assets folder exists  
1. Launch a pyhton3 http server on the current folder  (python -m http.server)  
2. Launch ServerBIT executable  
3. Open index.html on the browser (http://localhost:8000/index.html)  
