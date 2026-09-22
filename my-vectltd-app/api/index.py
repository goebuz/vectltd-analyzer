import os
import re
import requests
from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Updated API Endpoint & Token
APIFY_TOKEN = os.environ.get("APIFY_TOKEN", "apify_api_rFppbA1XFrs9mYNXT6zx6vfTKMNdK14ukmAA")
APIFY_URL = f"https://api.apify.com/v2/key-value-stores/kbv0vW9x6ZRwSZ8vL/records/INPUT?token={APIFY_TOKEN}"

HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VectLTD - Adobe Stock Asset & Portfolio Analyzer</title>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-main: #060911;
            --bg-card: #0d1322;
            --bg-input: #080d1a;
            --border-color: #1e293b;
            --border-focus: #38bdf8;
            --accent-blue: #2563eb;
            --accent-cyan: #38bdf8;
            --accent-green: #10b981;
            --accent-purple: #a855f7;
            --text-main: #f8fafc;
            --text-muted: #64748b;
            --text-dim: #94a3b8;
            --font-mono: 'Fira Code', monospace;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }
        body { background-color: var(--bg-main); color: var(--text-main); padding: 25px 20px; min-height: 100vh; }
        .dashboard-container { max-width: 1480px; margin: 0 auto; }
        
        .brand-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }
        .brand-logo {
            font-size: 22px;
            font-weight: 800;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 10px;
            letter-spacing: -0.5px;
        }
        .brand-logo span { color: var(--accent-cyan); }
        .sub-tag {
            font-family: var(--font-mono);
            font-size: 11px;
            color: var(--accent-green);
            background: rgba(16, 185, 129, 0.1);
            padding: 4px 10px;
            border-radius: 4px;
            border: 1px solid rgba(16, 185, 129, 0.3);
        }

        .control-panel { 
            background: var(--bg-card); 
            border: 1px solid var(--border-color); 
            border-radius: 12px; 
            padding: 24px; 
            margin-bottom: 25px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            position: relative;
        }
        
        .panel-title { 
            font-size: 13px; 
            font-weight: 700; 
            color: var(--accent-cyan); 
            margin-bottom: 18px; 
            display: flex; 
            align-items: center; 
            gap: 8px;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-family: var(--font-mono);
        }

        .search-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)) 170px; 
            gap: 14px; 
            margin-bottom: 20px; 
            align-items: end; 
        }
        
        .field-group { display: flex; flex-direction: column; gap: 6px; }
        .field-group label { 
            font-size: 11px; 
            color: var(--text-dim); 
            text-transform: uppercase; 
            font-weight: 700; 
            letter-spacing: 0.5px;
            font-family: var(--font-mono);
        }
        .field-group input, .field-group select { 
            width: 100%; 
            background: var(--bg-input); 
            border: 1px solid var(--border-color); 
            color: #fff; 
            padding: 12px 14px; 
            border-radius: 8px; 
            font-size: 13px; 
            outline: none; 
            transition: all 0.2s ease; 
        }
        .field-group input:focus, .field-group select:focus { 
            border-color: var(--border-focus); 
            box-shadow: 0 0 10px rgba(56, 189, 248, 0.25); 
        }

        .btn-analyze { 
            background: linear-gradient(135deg, var(--accent-blue), #1d4ed8); 
            color: #fff; 
            border: 1px solid rgba(255,255,255,0.1); 
            padding: 0 20px; 
            border-radius: 8px; 
            font-weight: 700; 
            cursor: pointer; 
            font-size: 13px; 
            transition: all 0.2s ease; 
            height: 43px; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            gap: 8px;
            box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);
            font-family: var(--font-mono);
            text-transform: uppercase;
        }
        .btn-analyze:hover { 
            transform: translateY(-2px); 
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.6); 
            background: linear-gradient(135deg, #3b82f6, var(--accent-blue));
        }

        .filters-bar { 
            display: grid; 
            grid-template-columns: repeat(3, 1fr); 
            gap: 14px; 
            padding-top: 18px; 
            border-top: 1px solid rgba(255, 255, 255, 0.05); 
        }

        .summary-bar { 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            margin-bottom: 22px; 
            background: rgba(13, 19, 34, 0.8);
            border: 1px solid var(--border-color);
            padding: 14px 20px;
            border-radius: 10px;
        }
        .summary-title { font-size: 16px; font-weight: 700; color: #fff; }
        .summary-pills { display: flex; gap: 10px; font-family: var(--font-mono); }
        .stat-pill { 
            padding: 6px 14px; 
            border-radius: 6px; 
            font-size: 12px; 
            font-weight: 700; 
            border: 1px solid transparent; 
        }
        .pill-total { background: #1e293b; color: #cbd5e1; border-color: #334155; }
        .pill-ai { background: rgba(168, 85, 247, 0.15); color: #d8b4fe; border-color: rgba(168, 85, 247, 0.3); }
        .pill-standard { background: rgba(16, 185, 129, 0.15); color: #6ee7b7; border-color: rgba(16, 185, 129, 0.3); }

        .asset-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(290px, 1fr)); gap: 20px; }
        
        .asset-card { 
            background: var(--bg-card); 
            border: 1px solid var(--border-color); 
            border-radius: 12px; 
            overflow: hidden; 
            display: flex; 
            flex-direction: column; 
            transition: all 0.25s ease; 
        }
        .asset-card:hover { 
            transform: translateY(-4px); 
            border-color: var(--border-focus); 
            box-shadow: 0 10px 25px -5px rgba(56, 189, 248, 0.2); 
        }

        .img-wrapper { 
            position: relative; 
            width: 100%; 
            height: 200px; 
            background: #04060a; 
            overflow: hidden; 
        }
        .img-wrapper img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s ease; }
        .asset-card:hover .img-wrapper img { transform: scale(1.04); }

        .overlay-badge { 
            position: absolute; 
            padding: 4px 9px; 
            border-radius: 5px; 
            font-size: 10px; 
            font-weight: 700; 
            font-family: var(--font-mono);
            backdrop-filter: blur(8px); 
            z-index: 2; 
            letter-spacing: 0.5px;
        }
        .badge-kind { top: 10px; left: 10px; background: rgba(6, 9, 17, 0.85); color: #f8fafc; border: 1px solid rgba(255,255,255,0.15); text-transform: uppercase; }
        
        .badge-ai { 
            top: 10px; 
            right: 10px; 
            background: linear-gradient(135deg, rgba(147, 51, 234, 0.9), rgba(192, 132, 252, 0.9)); 
            color: #ffffff; 
            border: 1px solid rgba(255,255,255,0.3); 
            box-shadow: 0 0 10px rgba(168, 85, 247, 0.5);
        }
        .badge-standard { 
            top: 10px; 
            right: 10px; 
            background: rgba(16, 185, 129, 0.85); 
            color: #ffffff; 
            border: 1px solid rgba(52, 211, 153, 0.4);
            box-shadow: 0 0 10px rgba(16, 185, 129, 0.3);
        }

        .card-body { padding: 15px; display: flex; flex-direction: column; flex: 1; gap: 8px; }
        .asset-title { 
            font-size: 13px; 
            font-weight: 600; 
            color: var(--text-main); 
            line-height: 1.4; 
            height: 36px; 
            overflow: hidden; 
            text-overflow: ellipsis; 
            display: -webkit-box; 
            -webkit-line-clamp: 2; 
            -webkit-box-orient: vertical; 
        }
        .author-row { display: flex; align-items: center; justify-content: space-between; font-size: 12px; color: var(--text-dim); }
        .author-row a { color: var(--accent-cyan); text-decoration: none; font-weight: 600; font-family: var(--font-mono); }
        .author-row a:hover { text-decoration: underline; }
        
        .cat-text { font-size: 11px; color: var(--text-muted); font-weight: 500; }
        
        .tags-container { display: flex; flex-wrap: wrap; gap: 4px; height: 42px; overflow: hidden; margin-top: 4px; }
        .tag-pill { background: #080d1a; color: #94a3b8; font-size: 10px; padding: 3px 6px; border-radius: 4px; border: 1px solid #1e293b; font-family: var(--font-mono); }

        .card-footer { 
            display: flex; 
            gap: 8px; 
            padding: 10px 15px; 
            background: #080d1a; 
            border-top: 1px solid var(--border-color); 
            margin-top: auto; 
            font-family: var(--font-mono);
        }
        .stat-box { 
            flex: 1; 
            padding: 6px 8px; 
            border-radius: 6px; 
            text-align: center; 
            font-size: 11px; 
            font-weight: 700; 
        }
        .stat-dl { background: rgba(168, 85, 247, 0.1); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.25); }
        .stat-date { background: rgba(16, 185, 129, 0.1); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.25); }
        
        #statusMessage { 
            text-align: center; 
            padding: 80px 20px; 
            font-size: 14px; 
            color: var(--text-dim); 
            font-family: var(--font-mono);
        }
    </style>
</head>
<body>

<div class="dashboard-container">
    <div class="brand-header">
        <div class="brand-logo">
            <span>VectLTD</span> Asset Hub
        </div>
        <div class="sub-tag">STATUS: ONLINE • API CONNECTED</div>
    </div>

    <div class="control-panel">
        <div class="panel-title">
            ⚙️ Search & Filtering Engine
        </div>

        <div class="search-grid">
            <div class="field-group">
                <label>Contributor ID / Profile URL</label>
                <input type="text" id="searchInput" placeholder="e.g. 213463451">
            </div>
            <div class="field-group">
                <label>Single Asset ID / URL</label>
                <input type="text" id="assetIdInput" placeholder="e.g. 841165203">
            </div>
            <div class="field-group">
                <label>Keyword Filter (Optional)</label>
                <input type="text" id="keywordInput" placeholder="e.g. vector, pattern">
            </div>
            <button class="btn-analyze" onclick="runAnalysis()">🔍 Analyze</button>
        </div>

        <div class="filters-bar">
            <div class="field-group">
                <label>Sort By</label>
                <select id="sortFilter">
                    <option value="downloads">Most Downloads</option>
                    <option value="relevance">Relevance</option>
                    <option value="newest">Newest Uploads</option>
                </select>
            </div>
            <div class="field-group">
                <label>Content Type</label>
                <select id="typeFilter">
                    <option value="all">All Content Types</option>
                    <option value="photo">Photos Only</option>
                    <option value="vector">Vectors Only</option>
                    <option value="illustration">Illustrations Only</option>
                    <option value="video">Videos Only</option>
                </select>
            </div>
            <div class="field-group">
                <label>Generative AI Filter</label>
                <select id="aiFilter">
                    <option value="">All Assets (Include AI)</option>
                    <option value="only">AI Generated Only</option>
                    <option value="exclude">Standard Only (Non-AI)</option>
                </select>
            </div>
        </div>
    </div>

    <div id="resultsHeader" class="summary-bar" style="display: none;">
        <div class="summary-title" id="resultsCountText">Results Overview</div>
        <div class="summary-pills">
            <span class="stat-pill pill-total" id="totalBadge">0 Assets</span>
            <span class="stat-pill pill-ai" id="aiBadge">0 AI</span>
            <span class="stat-pill pill-standard" id="nonAiBadge">0 Standard</span>
        </div>
    </div>

    <div id="statusMessage">Enter a Contributor ID, Single Asset ID, or Keyword above to begin analysis.</div>
    <div class="asset-grid" id="assetGrid"></div>
</div>

<script>
function checkIsAiAsset(item) {
    if (!item) return false;

    if (item.is_generative_ai === true || item.isGenerativeAi === true || 
        item.is_ai === true || item.isAi === true || 
        item.is_gentech === true || item.isGentech === true || item.gentech === true) {
        return true;
    }

    if (item.aiStatus && item.aiStatus !== 'not_ai' && item.aiStatus !== 'none') return true;
    if (item.ai === 'only' || item.ai === 'generative') return true;

    let title = (item.title || item.assetTitle || '').toLowerCase();
    if (title.includes('generative ai') || title.includes('ai generated') || title.includes('ai illustration') || title.includes('generative')) {
        return true;
    }

    if (item.keywords && Array.isArray(item.keywords)) {
        for (let k of item.keywords) {
            let kw = (typeof k === 'object' ? (k.name || k.text || '') : String(k)).toLowerCase();
            if (kw === 'generative ai' || kw === 'ai generated' || kw === 'generative' || kw === 'generative-ai' || kw === 'ai-generated') {
                return true;
            }
        }
    }

    return false;
}

async function runAnalysis() {
    let query = document.getElementById('searchInput').value.trim();
    let assetId = document.getElementById('assetIdInput').value.trim();
    let keyword = document.getElementById('keywordInput').value.trim();
    let sortVal = document.getElementById('sortFilter').value;
    let typeVal = document.getElementById('typeFilter').value;
    let aiVal = document.getElementById('aiFilter').value;

    let statusDiv = document.getElementById('statusMessage');
    let grid = document.getElementById('assetGrid');
    let header = document.getElementById('resultsHeader');

    if(!query && !assetId && !keyword) {
        alert("Please enter at least a Contributor ID, Single Asset ID, or Keyword!");
        return;
    }

    grid.innerHTML = "";
    header.style.display = "none";
    statusDiv.style.display = "block";
    statusDiv.innerHTML = "<span style='color: var(--accent-cyan);'>⚡ Fetching data from Apify... Please wait.</span>";

    try {
        let response = await fetch('/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                query: query,
                asset_id: assetId,
                keyword: keyword,
                sort: sortVal,
                content_type: typeVal,
                ai_type: aiVal
            })
        });

        let data = await response.json();

        if(data.error) {
            statusDiv.innerHTML = "<span style='color: #ef4444;'>❌ Error: " + data.error + "</span>";
            return;
        }

        let items = Array.isArray(data) ? data : (data.items || data.data || []);

        if(!items || items.length === 0) {
            statusDiv.innerHTML = "No assets found matching your query.";
            return;
        }

        statusDiv.style.display = "none";
        header.style.display = "flex";
        renderResults(items, assetId || query || keyword);

    } catch (err) {
        statusDiv.innerHTML = "<span style='color: #ef4444;'>❌ Connection Error: " + err + "</span>";
    }
}

function renderResults(items, searchLabel) {
    let grid = document.getElementById('assetGrid');
    grid.innerHTML = "";

    let aiCount = 0;
    let nonAiCount = 0;

    items.forEach(item => {
        let isAi = checkIsAiAsset(item);
        if(isAi) aiCount++; else nonAiCount++;

        let imgUrl = item.preview_url || item.comp_url || item.thumbnail_url || item.compUrl || item.thumbnailUrl || 'https://via.placeholder.com/300x200?text=No+Preview';
        let title = item.title || item.assetTitle || 'Untitled Asset';
        let creator = item.creator_name || item.creator || item.creatorName || item.creatorId || searchLabel;
        let downloads = item.nb_downloads !== undefined ? item.nb_downloads : (item.downloadCount !== undefined ? item.downloadCount : (item.downloads || 0));
        
        let categoryName = 'General';
        if (item.category) {
            categoryName = typeof item.category === 'object' ? (item.category.name || item.category.label || 'General') : item.category;
        } else if (item.categoryName) {
            categoryName = item.categoryName;
        }

        let assetKind = item.asset || item.contentType || 'Asset';
        let assetUrl = item.details_url || item.url || item.assetUrl || `https://stock.adobe.com/${item.id || item.stock_id || ''}`;
        let rawDate = item.creation_date || item.upload_date || item.creationDate || item.date || '';
        let formattedDate = rawDate ? String(rawDate).split('T')[0].split(' ')[0] : 'N/A';

        let keywordsHtml = '';
        if(item.keywords && Array.isArray(item.keywords)) {
            keywordsHtml = item.keywords.slice(0, 7).map(k => {
                let text = typeof k === 'object' ? (k.name || k.text) : k;
                return `<span class="tag-pill">${text}</span>`;
            }).join('');
        }

        let cardHtml = `
            <div class="asset-card">
                <div class="img-wrapper">
                    <img src="${imgUrl}" alt="Thumbnail" loading="lazy">
                    <span class="overlay-badge badge-kind">${assetKind}</span>
                    ${isAi 
                        ? '<span class="overlay-badge badge-ai">🤖 AI GENERATED</span>' 
                        : '<span class="overlay-badge badge-standard">📷 STANDARD</span>'
                    }
                </div>
                <div class="card-body">
                    <div class="asset-title" title="${title}">${title}</div>
                    <div class="author-row">
                        <span>👤 <b>${creator}</b></span>
                        ${assetUrl ? `<a href="${assetUrl}" target="_blank">LINK 🔗</a>` : ''}
                    </div>
                    <div class="cat-text">📁 ${categoryName}</div>
                    <div class="tags-container">${keywordsHtml}</div>
                </div>
                <div class="card-footer">
                    <div class="stat-box stat-dl">📥 ${downloads.toLocaleString()} DLs</div>
                    <div class="stat-box stat-date">📅 ${formattedDate}</div>
                </div>
            </div>
        `;
        grid.innerHTML += cardHtml;
    });

    document.getElementById('resultsCountText').innerText = `Results for "${searchLabel}"`;
    document.getElementById('totalBadge').innerText = `${items.length} Total Assets`;
    document.getElementById('aiBadge').innerText = `${aiCount} AI Generated`;
    document.getElementById('nonAiBadge').innerText = `${nonAiCount} Standard`;
}
</script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_LAYOUT)

@app.route("/analyze", methods=["POST"])
def analyze():
    req_data = request.json or {}
    query = str(req_data.get("query", "")).strip()
    asset_id_raw = str(req_data.get("asset_id", "")).strip()
    keyword = str(req_data.get("keyword", "")).strip()
    sort_val = req_data.get("sort", "downloads")
    content_type = req_data.get("content_type", "all")
    ai_type = req_data.get("ai_type", "")

    payload = {
        "maxItems": 100,
        "order": sort_val,
        "ai": ai_type if ai_type in ["only", "exclude"] else ""
    }

    if content_type and content_type != "all":
        payload["asset"] = content_type

    if asset_id_raw:
        asset_match = re.search(r'\d+', asset_id_raw)
        if asset_match:
            payload["query"] = asset_match.group(0)
    elif query:
        id_match = re.search(r'\d+', query)
        if id_match:
            payload["creatorId"] = int(id_match.group(0))

    if keyword and "query" not in payload:
        payload["query"] = keyword

    try:
        # PUT Request sending input parameters to Key-Value Store
        api_response = requests.put(
            APIFY_URL, 
            json=payload, 
            headers={"Content-Type": "application/json"},
            timeout=120
        )

        if api_response.status_code in [200, 201]:
            try:
                return jsonify(api_response.json())
            except Exception:
                return jsonify({"message": "Data posted successfully to Apify Key-Value Store", "status": "success"})
        else:
            return jsonify({
                "error": f"Apify API Error ({api_response.status_code}): {api_response.text}"
            }), api_response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)