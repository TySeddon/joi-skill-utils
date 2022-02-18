
# pip install azure-ai-textanalytics==5.1.0
# pip install azure-ai-textanalytics==5.2.0b1
# pip install azure-ai-language-questionanswering

from joi_skill_utils.nlp import NLP
from joi_skill_utils.dialog import Dialog

kb_project = 'joi-ruth'
nlp = NLP(kb_project)

#object_text = "garden, flower, daffodil, pretty"
object_text = "ice cream, Susanna, beach, walk, Clearwater"
object_text = "playing pinochle with Fred and Margaret"
#object_text = "crochet blanket for grandchildren"
#object_text = "'Jello with fruit', party"
#object_text = "'Jello with fruit', birthday party"
#object_text = " \"Say this exactly\", beach, walk "

q = "crocheted blankets"
responses = nlp.answer_question_kb(q)
NLP.print_kb_responses(responses)

dialog = Dialog(nlp, 'Ruth')
prompts = dialog.compose_prompts(object_text)
for p in prompts:
    print(f"{p.prompt}, ({p.confidence}), {p.source}")
quit()


