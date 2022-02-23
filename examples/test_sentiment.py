from joi_skill_utils.nlp import NLP
from joi_skill_utils.dialog import Dialog

kb_project = 'joi-ruth'
nlp = NLP(kb_project)

document = "I hate that flower"
document = "I love that flower"
document = "We used to live in Sommerville"
document = "died"

response = nlp.get_sentiment(document)
print(response)
