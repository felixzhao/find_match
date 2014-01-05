def update_docs(unk, cand, doc, train_vecotrs):
    updated_vectors = doc.copy()
    updated_vectors[cand] = train_vecotrs[cand]
    del updated_vectors[unk]
    return updated_vectors
