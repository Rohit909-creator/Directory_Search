import openai
import os
from sklearn.metrics.pairwise import cosine_similarity
import json
openai.api_key = os.environ['API_KEY']

path = 'C:\\Users\\ROHIT FRANCIS\\OneDrive\\Desktop\\ALL Here\\AI_Ideas\\Directory Search'


class Search():

    def __init__(self) -> None:

        self.embeddings = []
        
        with open(path+"\\Dir_Embed_data.json","r") as f:
            s = f.read()
            d = json.loads(s)

        keys = list(d.keys())
        keys = keys[3:]

        for key in keys:
            self.embeddings.append(d[key])
        
    def query(self, query):

        embs = self.get_embedding(query)
        probs = cosine_similarity([embs], self.embeddings)
        idx = probs.argmax(axis=-1)
        return probs, idx

    def get_embedding(self,text, model="text-embedding-ada-002"):
        text = text.replace("\n", " ")
        return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']
    def update(self, embs,key):

        with open(path+"\\Dir_Embed_data.json","r") as f:
            s = f.read()
            d = json.loads(s)

        d[key] = embs

        with open(path+"\\Dir_Embed_data.json","w") as f:
            s = json.dumps(d)
            f.write(s)

if __name__ == '__main__':
    s = Search()
    # embs = s.get_embedding('hello how are you?')
    # print(len(embs))
    s.update([1,2],"1")
    s.update([1,2],"3")
    probs, idx = s.query("a folder named hi")
    print(probs, idx)
    with open(path+"\\Dir_Embed_data.json","r") as f:
        s = f.read()
        d = json.loads(s)
    print(d.keys())
    # print(len(d[list(d.keys())[-1]]))
    
            