import faiss

#Approximate Nearest Neighbor
def ann(x, q, nlist=100, m=8, dims=64):
    quantizer = faiss.IndexFlatL2(dims) 
    index = faiss.IndexIVFPQ(quantizer, dims, nlist, m, 8)
                                    # 8 specifies that each sub-vector is encoded as 8 bits
    index.train(x)
    index.add(x)  
    k = 1                          # we want to see 1st nearest neighbor
    _, I = index.search(q, k)     # actual search
    return I