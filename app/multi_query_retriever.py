from app.query_rewriter import QueryRewriter
from app.hybrid_retriever import HybridRetriever



class MultiQueryRetriever:


    def __init__(self):

        self.rewriter = QueryRewriter()

        self.retriever = HybridRetriever()



    def search(
        self,
        query,
        top_k=20
    ):

        # 1. Query Rewrite

        queries = self.rewriter.rewrite(
            query
        )


        all_results = []


        # 2. 多 Query 检索

        for q in queries:

            results = self.retriever.search(
                q,
                top_k=top_k,
                candidate_k=50
            )

            all_results.extend(
                results
            )


        # 3. 去重

        unique = {}


        for item in all_results:

            chunk_id = item["id"]

            if chunk_id not in unique:

                unique[chunk_id] = item



        return list(
            unique.values()
        )
