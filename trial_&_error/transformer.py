# # Use a pipeline as a high-level helper
# from transformers import pipeline

# # # ROBERTA BASE NOT WORKING WELL model - 1
# # pipe = pipeline("text-classification", model="papluca/xlm-roberta-base-language-detection" , device = "mps" )

# lrcs = "I'm sorry but Don't wanna talk I need a moment before I go It's nothing personal I draw the blinds They don't need to see me cry 'Cause even if they understand They don't understand So then when I'm finished I'm all 'bout my business And ready to save the world I'm takin' my misery Make it my bitch Can't be everyone's favourite girl So, take aim and fire away I've never been so wide awake No, nobody but me can keep me safe And I'm on my way The blood moon is on the rise The fire burning in my eyes No, nobody but me can keep me safe And I'm on my way ♪ Lo siento mucho (Farru) Pero me voy (eh) Porque a tu lado me di cuenta que nada soy (eh-eh) Y me cansé de luchar y de guerrear en vano De estar en la línea de fuego y de meter la mano Acepto mis errores, también soy humano Y tú no ve que lo hago porque te amo (pum-pum-pum-pum) Pero ya (ya) No tengo más na que hacer aquí (aquí) Me voy, llegó la hora de partir (partir) De mi propio camino, seguir lejos de ti So, take aim and fire away I've never been so wide awake No, nobody but me can keep me safe And I'm on my way The blood moon is on the rise (is on the rise, na-na) The fire burning in my eyes (the fire burning in my eyes, na) No, nobody but me can keep me safe And I'm on my way ♪ (I'm on my way) (Ever... everybody keep me safe) (Ever... everybody keep me safe) (Ever... everybody keep me safe) (Ever... everybody) (Everybody on my way) So, take aim and fire away I've never been so wide awake No, nobody but me can keep me safe And I'm on my way The blood moon is on the rise The fire burning in my eyes No, nobody but me can keep me safe And I'm on my way"
# # result = pipe(lrcs[:514] , top_k = 3)
# # print(result)

# # from transformers import AutoTokenizer, AutoModelForSequenceClassification
# # tokenizer = AutoTokenizer.from_pretrained('Mike0307/multilingual-e5-language-detection')
# # model = AutoModelForSequenceClassification.from_pretrained('Mike0307/multilingual-e5-language-detection', num_labels=45)

# # multi-lingual model - 2
# # pipe = pipeline("text-classification", model="Mike0307/multilingual-e5-language-detection" , device = "mps" )


# from transformers import AutoTokenizer, AutoModelForSequenceClassification
# tokenizer = AutoTokenizer.from_pretrained('Mike0307/multilingual-e5-language-detection')
# model = AutoModelForSequenceClassification.from_pretrained('Mike0307/multilingual-e5-language-detection', num_labels=45)
# import torch

# languages = [
#     "Arabic", "Basque", "Breton", "Catalan", "Chinese_China", "Chinese_Hongkong", 
#     "Chinese_Taiwan", "Chuvash", "Czech", "Dhivehi", "Dutch", "English", 
#     "Esperanto", "Estonian", "French", "Frisian", "Georgian", "German", "Greek", 
#     "Hakha_Chin", "Indonesian", "Interlingua", "Italian", "Japanese", "Kabyle", 
#     "Kinyarwanda", "Kyrgyz", "Latvian", "Maltese", "Mongolian", "Persian", "Polish", 
#     "Portuguese", "Romanian", "Romansh_Sursilvan", "Russian", "Sakha", "Slovenian", 
#     "Spanish", "Swedish", "Tamil", "Tatar", "Turkish", "Ukranian", "Welsh"
# ]

# def predict(text, model, tokenizer, device = torch.device('cpu')):
#     model.to(device)
#     model.eval()
#     tokenized = tokenizer(text, padding='max_length', truncation=True, max_length=128, return_tensors="pt")
#     input_ids = tokenized['input_ids']
#     attention_mask = tokenized['attention_mask']
#     with torch.no_grad():
#         input_ids = input_ids.to(device)
#         attention_mask = attention_mask.to(device)
#         outputs = model(input_ids=input_ids, attention_mask=attention_mask)
#     logits = outputs.logits
#     probabilities = torch.nn.functional.softmax(logits, dim=1)
#     return probabilities

# def get_topk(probabilities, languages, k=3):
#     topk_prob, topk_indices = torch.topk(probabilities, k)
#     topk_prob = topk_prob.cpu().numpy()[0].tolist()
#     topk_indices = topk_indices.cpu().numpy()[0].tolist()
#     topk_labels = [languages[index] for index in topk_indices]
#     return topk_prob, topk_labels

# text = "你的測試句子"
# probabilities = predict(lrcs, model, tokenizer)
# topk_prob, topk_labels = get_topk(probabilities, languages)
# print(topk_prob, topk_labels)

# # [0.999620258808, 0.00025940246996469, 2.7690215574693e-05]
# # ['Chinese_Taiwan', 'Chinese_Hongkong', 'Chinese_China']


# # result = pipe(lrcs)
# # print(result)


import requests
import json

lrcs = "I'm sorry but Don't wanna talk I need a moment before I go It's nothing personal I draw the blinds They don't need to see me cry 'Cause even if they understand They don't understand So then when I'm finished I'm all 'bout my business And ready to save the world I'm takin' my misery Make it my bitch Can't be everyone's favourite girl So, take aim and fire away I've never been so wide awake No, nobody but me can keep me safe And I'm on my way The blood moon is on the rise The fire burning in my eyes No, nobody but me can keep me safe And I'm on my way ♪ Lo siento mucho (Farru) Pero me voy (eh) Porque a tu lado me di cuenta que nada soy (eh-eh) Y me cansé de luchar y de guerrear en vano De estar en la línea de fuego y de meter la mano Acepto mis errores, también soy humano Y tú no ve que lo hago porque te amo (pum-pum-pum-pum) Pero ya (ya) No tengo más na que hacer aquí (aquí) Me voy, llegó la hora de partir (partir) De mi propio camino, seguir lejos de ti So, take aim and fire away I've never been so wide awake No, nobody but me can keep me safe And I'm on my way The blood moon is on the rise (is on the rise, na-na) The fire burning in my eyes (the fire burning in my eyes, na) No, nobody but me can keep me safe And I'm on my way ♪ (I'm on my way) (Ever... everybody keep me safe) (Ever... everybody keep me safe) (Ever... everybody keep me safe) (Ever... everybody) (Everybody on my way) So, take aim and fire away I've never been so wide awake No, nobody but me can keep me safe And I'm on my way The blood moon is on the rise The fire burning in my eyes No, nobody but me can keep me safe And I'm on my way"

url = "https://language-identify-detector.p.rapidapi.com/languageIdentify"

payload = { "text": lrcs }
headers = {
	"x-rapidapi-key": "c3a0ff933cmsh9c6ca83440520f7p1f106ajsn86d70f424094",
	"x-rapidapi-host": "language-identify-detector.p.rapidapi.com",
	"Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
langs = response.json()["languageCodes"]

# print(json.dumps(response.json() , indent=4))
# print((response.json()["languageCodes"]))
top_langs = [i["code"] for i in langs if i["confidence"]>0.1 ]
print(top_langs)

# # Use a pipeline as a high-level helper
# from transformers import pipeline

# pipe = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base" , device = "mps" , top_k = 7)
# scores = {i["label"] :  i["score"] for i in pipe(lrcs)[0] if i["score"]>0.3}
# print(scores)

# lst = ["anger" , "disgust" , "fear" , "joy" , "neutral" , "sadness" , "surprise"]

# # sentiments = [0,0,0,0,0,0,0]
# # place_dict = dict(zip(lst , list(range(len(lst)))))
# # for i in scores : 
# #     sentiments[place_dict[i]] = scores[i]

# sentiments = [scores.get(key, 0) for key in lst]

# print(sentiments)


