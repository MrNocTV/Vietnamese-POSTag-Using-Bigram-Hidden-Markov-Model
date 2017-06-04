# Vietnamese-POSTag-Using-Bigram-Hidden-Markov-Model

Requirement:
  - Python3
  - vnTagger tool (Google to download and read README.txt to know how to use it)
  
 
 Directory/File Info:
   - Training data is stored inside train directory, divided into two files:
       + tag.txt: Each line in this file is tag sequence for its corresponding line in word.txt
         Example: Np V V
                  C N V V 
                  ...
       + word.txt: Each line in this file is a sequence of observations (or words if you want), and each line is corresponding to 
        1 line in tag.txt
        Example:
                  Nam đi học
                  có con_chuột đang ăn
       + viterbi_algo.py: This is the file contains HMM, run this file to get hmm_output.txt (the structure of this file is the 
        same as tag.txt). We compare hmm_output.txt and tag.txt inside test directory to measure the accuracy. 
       + word_tagged.xml: This file generated by vnTagger tool, which uses Maximum Entropy Model. The test sentences are the same
        with those used to test HMM (tag.txt and word.txt inside test directory).
 

To run Hidden Markov Model:
  - go to code directory, run viterbi_algo.py
  - to know the accuracy of vnTagger's output, run check_maxent_output.py
  - to train with different training set or retrain the model (if you want), run train.py
