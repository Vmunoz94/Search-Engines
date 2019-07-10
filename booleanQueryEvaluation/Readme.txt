Programming Language used: Python 3
External Libraries/Programs: NLTK

1.	NLTK must be installed in order for the program to work.
     To install NLTK, type the following sentence in the terminal window
          “python3 -m pip install nltk”.

2.	NLTK uses other external packages.
     To install NLTK’s external libraries type and enter the following commands in the terminal window.
          a.	“python3”
          b.	“import nltk”
          c.	“nltk.download()”

3.	The NLTK downloader will open up, I proceeded to download all packages even though all of them are not necessary.
     I encountered an error during this process, and to resolve my error I had to go to
          Finder -> Applications -> Python 3.6 -> click on Install Certificates.command.

4.	Once all the packages are installed, make sure that the document.txt file is in the same directory as the
     inverted_index_construction.py and boolean_query_evaluator.py file.
     If the document.txt file is not in the same directory, then the program will not be able to find the file resulting in an error.

5.	Once all the previous steps are complete, to run the program type “python3 boolean_query_evaluation.py”.
     This will automatically create the invertedIndex.txt file.
     Proceed in entering the search query in the following format (ex. Puppy and Kittens),
     the results will be placed in the queryResults.txt file.
