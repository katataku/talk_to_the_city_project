
from sentence_transformers import SentenceTransformer
from langchain.embeddings import OpenAIEmbeddings
import pandas as pd
from tqdm import tqdm
import os

embed_model_name = 'paraphrase-multilingual-mpnet-base-v2'
model = SentenceTransformer(embed_model_name)

def embedding(config):
    dataset = config['output_dir']
    path = f"outputs/{dataset}/embeddings.pkl"
    arguments = pd.read_csv(f"outputs/{dataset}/args.csv")
    embeddings = []
    for i in tqdm(range(0, len(arguments), 1000)):
        args = arguments["argument"].tolist()[i: i + 1000]
        # embeds = OpenAIEmbeddings().embed_documents(args)
        embeds = model.encode(args, show_progress_bar=False).tolist()
        embeddings.extend(embeds)
    df = pd.DataFrame(
        [
            {"arg-id": arguments.iloc[i]["arg-id"], "embedding": e}
            for i, e in enumerate(embeddings)
        ]
    )
    df.to_pickle(path)
