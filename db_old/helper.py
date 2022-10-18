import nltk
from nltk.translate import bleu
from nltk.translate.bleu_score import SmoothingFunction
smoothie = SmoothingFunction().method4

class NlpHelper():
    def __init__(self):
        super(NlpHelper, self)



    def similarity(self,sentence1,sentence2):   

        return bleu([sentence1], sentence2, smoothing_function=smoothie)
       
      
        #return nltk.edit_distance(sentence1, sentence2)





helper = NlpHelper()
print(helper.similarity("cити молл","циты малл"))


