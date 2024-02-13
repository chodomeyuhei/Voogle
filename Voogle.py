import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

class SearchEngine:
    def __init__(self, documents):
        self.documents = documents

    def search_local(self, query):
        results = []
        for doc in self.documents:
            if query.lower() in doc["text"].lower():
                results.append(doc)
        return results

    def search_wikipedia(self, query, lang='ja'):
        base_url = f"https://{lang}.wikipedia.org/w/api.php"
        params = {
            'action': 'query',
            'list': 'search',
            'srsearch': query,
            'format': 'json'
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            search_results = response.json().get('query', {}).get('search', [])
            return [{'id': result['pageid'], 'text': result['snippet']} for result in search_results]
        else:
            return []

# サンプルドキュメントデータ
documents = [
    {"id": 1, "text": "Pythonは汎用の高水準言語です。"},
    {"id": 2, "text": "検索エンジンは情報を検索するためのツールです。"},
    {"id": 3, "text": "人工知能はコンピュータによる知的な振る舞いを実現する技術です。"},
    {"id": 4, "text": "Web開発では、HTML、CSS、JavaScriptなどの技術が使われます。"},
    {"id": 5, "text": "データサイエンティストはデータから有益な情報を引き出す専門家です。"}
]

# SearchEngineインスタンスの作成
search_engine = SearchEngine(documents)

@app.route("/", methods=["GET", "POST"])
def search():
    # 以前の関数の内容は変更なし
    if request.method == "POST":
        query = request.form["query"]
        local_results = search_engine.search_local(query)
        wiki_results = search_engine.search_wikipedia(query)
        all_results = local_results + wiki_results
        if not all_results:
            return "検索結果はありません。"
        else:
            result_text = "<br>".join([f"<div><strong>ID:</strong> {result['id']}, <strong>Text:</strong> {result['text']}</div>" for result in all_results])
            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>検索エンジン</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        margin: 0 auto;
                        max-width: 800px;
                        padding: 20px;
                    }}
                    h1 {{
                        color: #333;
                    }}
                    form {{
                        margin-bottom: 20px;
                    }}
                    input[type="text"] {{
                        margin-right: 10px;
                        padding: 10px;
                        width: calc(100% - 122px);
                    }}
                    input[type="submit"] {{
                        padding: 10px 20px;
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        cursor: pointer;
                    }}
                    input[type="submit"]:hover {{
                        background-color: #45a049;
                    }}
                    div {{
                        margin-bottom: 10px;
                        padding: 10px;
                        background-color: #f2f2f2;
                        border-left: 4px solid #4CAF50;
                    }}
                </style>
            </head>
            <body>
                <h1>検索エンジン</h1>
                <form method="POST">
                    <label for="query">検索キーワード:</label>
                    <input type="text" name="query" id="query" required>
                    <input type="submit" value="検索">
                </form>
                {result_text}
            </body>
            </html>
            """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>検索エンジン</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0 auto;
                max-width: 800px;
                padding: 20px;
            }
            h1 {
                color: #333;
            }
            form {
                margin-bottom: 20px;
            }
            input[type="text"] {
                margin-right: 10px;
                padding: 10px;
                width: calc(100% - 122px);
            }
            input[type="submit"] {
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                border: none;
                cursor: pointer;
            }
            input[type="submit"]:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <h1>検索エンジン</h1>
        <form method="POST">
            <label for="query">検索キーワード:</label>
            <input type="text" name="query" id="query" required>
            <input type="submit" value="検索">
        </form>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)
