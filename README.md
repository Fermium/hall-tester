# hall-tester

1. install conda
2. `sudo apt-get install libbz2-dev`
3. `conda install r-essentials`
4. `export LD_LIBRARY_PATH="/home/d/anaconda3/lib/R/lib:$LD_LIBRARY_PATH"`
3. `pip install -r requirements.txt`

# How it works

Il file principale è `run.py`. Per eseguirlo: `python3 run.py`

Ogni test è posto nella propria sottocartella all'interno di `tests` ed è chiamato `test.py`. Il nome del test è automaticamente preso dal nome della cartella.

Si suggerisce di nominare i test con un numero progressivo per assicurarsi che vengano eseguiti in ordine.
I test vengono eseguiti in ordine alfabetico.


Il file `test.py` eredita l'ambiente di `run.py` inclusi

* Una variabile d'ambiente chiamata "TESTNAME"
* Un dizionario, accessibile in R/W chiamato tests. Ci ci accede con tests[TESTNAME] ed esso contiene
  - `path` full path a test.py
  - `status` Può avere i valori "not yet run" (default), "success" o "failure". Va modificato al termine dell'esecuzione di test.py per indicare i risultati del test
  - `asset_path` directory dove salvare quello che volete, creata automaticamente prima dell'avvio di test.py
