# I. CRAW DATA 


  Craw data from Goodread by Selenium and Python. 

# Installation and Run

  1. Python3 .
  
  2. Clone this repository .

    $ git clone https://github.com/congdaoduy298/Crawl-Data.git 

  3. Install dependencies .

    $ cd Crawl-Data/
   
    $ pip3 install -r requirements.txt 
   
  4. Run file by terminal .

    $ python crawl_books.py

# Result 
     
  Total running time: 6181s


# II. NAMED ENTITY RECOGNITION


  Get Vietnamese NER by using VnCoreNLP and English NER by using nltk + spacy.

# Installation
  
  1. Python 3.4+.

  2. Clone VnCoreNLP repository and install vncorenlp.

    $ git clone https://github.com/vncorenlp/VnCoreNLP

    $ pip3 install vncorenlp
  
  3. Java 1.8+

  4. File VnCoreNLP-1.1.1.jar (27MB) and folder models (115MB) are placed in the same working folder.

  5. Change current directory 

    $ cp data.json get_ner.py ./VnCoreNLP/
    
    $ cd VnCoreNLP/

  4. NLTK Library 

    $ pip3 install nltk
  
  5. Spacy Library 

    $ pip3 install spacy

    $ python3 -m spacy download en_core_web_sm

# Run

  1. Run VnCoreNLP server.

    $ vncorenlp -Xmx2g <FULL-PATH-to-VnCoreNLP-jar-file> -p 9000 -a "wseg,pos,ner"
  
  2. Open new terminal.

    $ python3 get_ner.py

# REFERENCES

  [VnCoreNLP: A Vietnamese Natural Language Processing Toolkit](https://github.com/vncorenlp/VnCoreNLP)

  [Named Entity Recognition with NLTK and SpaCy](https://towardsdatascience.com/named-entity-recognition-with-nltk-and-spacy-8c4a7d88e7da)