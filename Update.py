import openai
import os
from sklearn.metrics.pairwise import cosine_similarity
import json
openai.api_key = os.environ['API_KEY']

# path = 'C:\\Users\\ROHIT FRANCIS\\OneDrive\\Desktop\\ALL Here\\AI_Ideas\\Directory Search'
path = "C:\\Users\\ROHIT FRANCIS\\OneDrive\\Desktop\\ALL Here\\AI_Ideas\\DirectorySearch_2_0"

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
    def query(self, query):

        embs = self.get_embedding(query)
        probs = cosine_similarity([embs], self.embeddings)
        idx = probs.argmax(axis=-1)
        return probs, idx, self.keys[idx.item()]

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

        self.embeddings.append(embs)
        self.keys.append(key)
if __name__ == '__main__':
    s = Search()
    # embs = s.get_embedding('hello how are you?')
    # print(len(embs))
    # s.update([1,2],"1")
    # s.update([1,2],"3")
    probs, idx, path_ = s.query("AI projects by Rohit Francis")
    print(probs, idx, path_)
    with open(path+"\\Dir_Embed_data.json","r") as f:
        s = f.read()
        d = json.loads(s)
    
    # print(f'\n\n\n{d.keys()}')
    # print(len(d[list(d.keys())[-1]]))
    
            
