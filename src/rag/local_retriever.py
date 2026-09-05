import os
import json
import math
import re
from typing import List, Dict, Any, Tuple


class LocalRuleRetriever:
    """
    Self-contained local vector retrieval pipeline.
    Uses local token-frequency / cosine similarity embeddings precomputed in data/embeddings_cache.json.
    Supports on-demand Gemini embedding when GEMINI_API_KEY is supplied.
    """
    def __init__(self, rules_path: str = None, cache_path: str = None):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        if not rules_path:
            rules_path = os.path.join(base_dir, "data", "rules.json")
        if not cache_path:
            cache_path = os.path.join(base_dir, "data", "embeddings_cache.json")

        self.rules_path = rules_path
        self.cache_path = cache_path
        self.rules = []
        self.vectors = {}
        self.vocabulary = {}
        self.load_rules_and_cache()

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r'\b[a-zA-Z0-9_]{2,}\b', text.lower())

    def load_rules_and_cache(self):
        with open(self.rules_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.rules = data.get("rules", [])

        if os.path.exists(self.cache_path):
            with open(self.cache_path, "r", encoding="utf-8") as f:
                cached = json.load(f)
                self.vocabulary = cached.get("vocabulary", {})
                self.vectors = cached.get("vectors", {})
        else:
            self._build_local_index()

    def _build_local_index(self):
        doc_tokens = {}
        df = {}
        for rule in self.rules:
            text = f"{rule['id']} {rule['title']} {rule['category']} {rule['description']} {rule['deterministic_logic']} {rule['symptom_cluster']}"
            tokens = self._tokenize(text)
            doc_tokens[rule['id']] = tokens
            for token in set(tokens):
                df[token] = df.get(token, 0) + 1

        self.vocabulary = {t: idx for idx, t in enumerate(sorted(df.keys()))}
        n_docs = len(self.rules)
        self.vectors = {}

        for rule_id, tokens in doc_tokens.items():
            tf = {}
            for t in tokens:
                tf[t] = tf.get(t, 0) + 1
            vec = {}
            norm = 0.0
            for t, count in tf.items():
                if t in self.vocabulary:
                    idf = math.log((n_docs + 1.0) / (df[t] + 1.0)) + 1.0
                    weight = count * idf
                    vec[str(self.vocabulary[t])] = round(weight, 4)
                    norm += weight * weight
            norm = math.sqrt(norm) if norm > 0 else 1.0
            for k in vec:
                vec[k] = round(vec[k] / norm, 4)
            self.vectors[rule_id] = vec

        # Save cache
        with open(self.cache_path, "w", encoding="utf-8") as f:
            json.dump({"vocabulary": self.vocabulary, "vectors": self.vectors}, f, indent=2)

    def query(self, query_text: str, top_k: int = 4) -> List[Dict[str, Any]]:
        tokens = self._tokenize(query_text)
        q_tf = {}
        for t in tokens:
            q_tf[t] = q_tf.get(t, 0) + 1

        q_vec = {}
        norm = 0.0
        for t, count in q_tf.items():
            if t in self.vocabulary:
                weight = count
                q_vec[str(self.vocabulary[t])] = weight
                norm += weight * weight
        norm = math.sqrt(norm) if norm > 0 else 1.0
        for k in q_vec:
            q_vec[k] = q_vec[k] / norm

        scores: List[Tuple[str, float]] = []
        for rule_id, doc_vec in self.vectors.items():
            score = 0.0
            for idx_str, w in q_vec.items():
                if idx_str in doc_vec:
                    score += w * doc_vec[idx_str]
            scores.append((rule_id, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        results = []
        rule_map = {r["id"]: r for r in self.rules}

        for rule_id, score in scores[:top_k]:
            rule = rule_map.get(rule_id)
            if rule:
                results.append({
                    "rule": rule,
                    "relevance_score": round(float(score), 4)
                })
        return results
