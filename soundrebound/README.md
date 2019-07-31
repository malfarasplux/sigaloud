## Soundrebound ServerBIT + p5 sketch

### Setup  
0. Ensure ServerBIT configuration is alright:
  -  config.json
  -  ServerBIT.py => comment out thread.start_new_thread(BITalino_handler...)
  -  ServerBIT.py => launch thread.start_new_thread(BITalino_simulate...) instead  
  -  check that the .txt acquisition file is available
  -  check that the assets folder exists  
1. Launch a pyhton3 http server on the current folder  (python -m http.server)  
2. Launch ServerBIT executable  
3. Open index.html on the browser (http://localhost:8000/index.html)  

![example](/soundrebound/example_2PZT_rs.jpg)

### Idea  
1. ServerBIT opens a prerecorded BITalino file (example with 2 PZT) and streams via websockets  
2. A Javascript processes it and represents the data through p5 and flot  
3. p5 allows the exploration of bouncing ball features linked to the sensing data  

