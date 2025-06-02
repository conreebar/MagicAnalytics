Proposal:

do analytics on major Magic: the Gathering tournaments

How:
via a reusable tool that can:
1. take in jsons of decks in a metagame, or a specific tournament via webscraping
2. assign an embedding to the cards and decks and archetypes in a given batch
3. using the RAG assignment as a model, give ai analytics on what decks are the best to use in a subset, other cool data like what are the more unique decks that placed high, what was the cheapest deck that did well, etc
4. show all this data that I have scrounged on a vercel app, where I can keep tabs on different analytics I have done to reference from in the future
5. have a (probably) redis database storing things for the project

6. ![image](https://github.com/user-attachments/assets/bd56cda2-f825-41e6-b132-a13612a6c207)
7. ![image](https://github.com/user-attachments/assets/e307eba7-a34e-41df-9ca7-7bb56b064a82)


goals:
-by 6/4: upload all scraped data to DB
-by 6/5: get embeddings going for deck, card, and archetype for my first batch
-by 6/6: have some back-endy analytics ready using RAG/embeddings
-by 6/7: begin work on a vercel frontend, re-eval here to see what pace I am at
