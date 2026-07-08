from langchain_community.embeddings import DashScopeEmbeddings

user_input = "猫坐在垫子上"

# 创建嵌入模型对象,默认使用text-embedding-v1
scope_embeddings = DashScopeEmbeddings(model="text-embedding-v3")
embeddings = scope_embeddings
result = embeddings.embed_query(user_input)
print(type(result))#<class 'list'>
print(len(result))
print(result)
