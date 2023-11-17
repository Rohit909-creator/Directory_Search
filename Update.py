import os
from sklearn.metrics.pairwise import cosine_similarity
import json
from openai import OpenAI
import numpy as np
client = OpenAI()

# path = 'C:\\Users\\ROHIT FRANCIS\\OneDrive\\Desktop\\ALL Here\\AI_Ideas\\Directory Search'
path = "<path goes here>"

class Search():

    def __init__(self) -> None:

        self.embeddings = []
        
        with open(path+"\\Dir_Embed_data.json","r") as f:
            s = f.read()
            d = json.loads(s)

        keys = list(d.keys())
        keys = keys[3:]
        self.keys = keys
        for key in self.keys:
            self.embeddings.append(d[key])
        # print(self.keys)
    def query(self, q):

        embs = self.get_embedding(q)
        probs = cosine_similarity([embs], self.embeddings)
        idx = probs.argmax(axis=-1)
        args = np.argsort(probs)[0].tolist()
        results = [self.keys[index] for index in args]
        # print(results)
        return probs, idx, self.keys[idx.item()], results[-1::-1]

    def get_embedding(self,text:str, model="text-embedding-ada-002"):
        text = text.replace("\n", " ")
        return client.embeddings.create(input = [text], model=model).data[0].embedding
     
    def update(self, embs,key):

        with open(path+"\\Dir_Embed_data.json","r") as f:
            s = f.read()
            d = json.loads(s)

        d[key] = embs

        with open(path+"\\Dir_Embed_data.json","w") as f:
            s = json.dumps(d)
            f.write(s)

        self.embeddings.append(embs)
        self.keys.append(key)
if __name__ == '__main__':
    s = Search()
    # embs = s.get_embedding('hello how are you?')
    # print(len(embs))
    # s.update([1,2],"1")
    # s.update([1,2],"3")
    probs, idx, path_, results = s.query("A file about Moon Mission")
    print(probs, idx, path_, results)
    with open(path+"\\Dir_Embed_data.json","r") as f:
        s = f.read()
        d = json.loads(s)
    
    print(f'\n\n\n{d.keys()}')
    # print(len(d[list(d.keys())[-1]]))
    
            
