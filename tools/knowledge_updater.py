"""
knowledge_updater.py — research-paper-writer SECOND-KNOWLEDGE-BRAIN updater

Crawls ArXiv, Semantic Scholar, and PubMed for recent academic papers,
scores them by recency + relevance + citation count, and appends new
entries to SECOND-KNOWLEDGE-BRAIN.md. Deduplicates by DOI hash.

Usage:
    python knowledge_updater.py --topic "transformer attention NLP"
    python knowledge_updater.py --topic "climate change ecology" --days 90
    python knowledge_updater.py  # uses DEFAULT_TOPICS list

Requirements:
    pip install requests crawl4ai python-dateutil hashlib
"""

import argparse
import hashlib
import json
import os
import re
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import requests
from dateutil.parser import parse as parse_date

# ── Configuration ──────────────────────────────────────────────────────────────

BRAIN_FILE = Path(__file__).parent.parent / "SECOND-KNOWLEDGE-BRAIN.md"
CACHE_FILE = Path(__file__).parent / ".doi_cache.json"

DEFAULT_TOPICS = [
    "academic paper writing automation",
    "large language model scientific writing",
    "automated literature review",
    "citation generation neural network",
    "knowledge gap analysis research",
]

DEFAULT_DAYS = 90
MAX_RESULTS_PER_SOURCE = 15
MIN_SCORE_THRESHOLD = 0.35

SEMANTIC_SCHOLAR_BASE = "https://api.semanticscholar.org/graph/v1"
ARXIV_BASE = "https://export.arxiv.org/api/query"
PUBMED_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
CROSSREF_BASE = "https://api.crossref.org/works"

ARXIV_CATEGORIES = ["cs.AI", "cs.CL", "cs.LG", "cs.IR", "stat.ML"]

RELEVANCE_KEYWORDS = [
    "research paper", "academic writing", "scientific writing",
    "literature review", "citation", "bibliography", "knowledge gap",
    "systematic review", "meta-analysis", "paper generation",
    "automated writing", "llm writing", "language model research",
    "scholarly", "peer review", "academic",
]

# ── DOI Cache (deduplication) ───────────────────────────────────────────────────

def load_doi_cache() -> set:
    """Load the set of already-indexed DOI hashes from cache file."""
    if CACHE_FILE.exists():
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return set(data.get("doi_hashes", []))
    return set()


def save_doi_cache(doi_hashes: set) -> None:
    """Persist the DOI hash set to cache file."""
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump({"doi_hashes": list(doi_hashes), "updated": datetime.utcnow().isoformat()}, f, indent=2)


def doi_hash(doi: str) -> str:
    """Return SHA-256 hex of a normalized DOI string."""
    normalized = doi.strip().lower().lstrip("https://doi.org/").lstrip("doi:")
    return hashlib.sha256(normalized.encode()).hexdigest()


# ── Scoring ─────────────────────────────────────────────────────────────────────

def recency_score(year: int) -> float:
    current_year = datetime.utcnow().year
    age = current_year - year
    if age <= 0:
        return 1.0
    elif age == 1:
        return 0.85
    elif age == 2:
        return 0.65
    elif age == 3:
        return 0.45
    else:
        return 0.2


def relevance_score(title: str, abstract: str, topic: str) -> float:
    text = (title + " " + abstract).lower()
    topic_words = set(re.sub(r"[^a-z0-9 ]", "", topic.lower()).split())
    keyword_words = set(" ".join(RELEVANCE_KEYWORDS).split())
    all_target = topic_words | keyword_words
    matches = sum(1 for w in all_target if w in text)
    return min(matches / max(len(all_target), 1), 1.0)


def citation_score(citation_count: int) -> float:
    return min(citation_count / 200.0, 1.0)


def compute_score(year: int, title: str, abstract: str, citations: int, topic: str) -> float:
    r = recency_score(year)
    rel = relevance_score(title, abstract, topic)
    c = citation_score(citations)
    return round(r * 0.3 + rel * 0.5 + c * 0.2, 3)


# ── Source: Semantic Scholar ────────────────────────────────────────────────────

def search_semantic_scholar(query: str, days: int) -> list[dict]:
    """Search Semantic Scholar for papers matching the query."""
    papers = []
    cutoff_year = datetime.utcnow().year - (days // 365 + 1)
    params = {
        "query": query,
        "limit": MAX_RESULTS_PER_SOURCE,
        "fields": "title,authors,year,venue,citationCount,externalIds,abstract",
        "sort": "relevance",
    }
    try:
        resp = requests.get(f"{SEMANTIC_SCHOLAR_BASE}/paper/search", params=params, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        for item in data.get("data", []):
            year = item.get("year") or 0
            if year < cutoff_year:
                continue
            doi = (item.get("externalIds") or {}).get("DOI", "")
            arxiv_id = (item.get("externalIds") or {}).get("ArXiv", "")
            url = f"https://doi.org/{doi}" if doi else (f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else "")
            authors_list = [a.get("name", "") for a in (item.get("authors") or [])]
            papers.append({
                "title": item.get("title", ""),
                "authors": authors_list[:3],
                "year": year,
                "venue": item.get("venue", "arXiv preprint"),
                "doi": doi,
                "url": url,
                "abstract": (item.get("abstract") or "")[:300],
                "citations": item.get("citationCount") or 0,
                "source": "Semantic Scholar",
            })
        time.sleep(1.2)  # respect rate limit
    except Exception as e:
        print(f"  [WARN] Semantic Scholar search failed: {e}")
    return papers


# ── Source: ArXiv ───────────────────────────────────────────────────────────────

def search_arxiv(query: str, days: int) -> list[dict]:
    """Search ArXiv using the Atom API."""
    papers = []
    cat_filter = " OR ".join(f"cat:{c}" for c in ARXIV_CATEGORIES)
    full_query = f"({query}) AND ({cat_filter})"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": MAX_RESULTS_PER_SOURCE,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    try:
        resp = requests.get(ARXIV_BASE, params=params, timeout=15)
        resp.raise_for_status()
        # parse Atom XML minimally
        text = resp.text
        entries = re.findall(r"<entry>(.*?)</entry>", text, re.DOTALL)
        cutoff = datetime.utcnow() - timedelta(days=days)
        for entry in entries:
            title_m = re.search(r"<title>(.*?)</title>", entry, re.DOTALL)
            published_m = re.search(r"<published>(.*?)</published>", entry)
            abstract_m = re.search(r"<summary>(.*?)</summary>", entry, re.DOTALL)
            authors_m = re.findall(r"<name>(.*?)</name>", entry)
            arxiv_id_m = re.search(r"<id>http.*?/abs/([^<]+)</id>", entry)

            title = title_m.group(1).strip().replace("\n", " ") if title_m else ""
            published = published_m.group(1) if published_m else ""
            abstract = abstract_m.group(1).strip()[:300] if abstract_m else ""
            authors = authors_m[:3]
            arxiv_id = arxiv_id_m.group(1) if arxiv_id_m else ""

            try:
                pub_date = parse_date(published)
                if pub_date.replace(tzinfo=None) < cutoff:
                    continue
                year = pub_date.year
            except Exception:
                year = datetime.utcnow().year

            papers.append({
                "title": title,
                "authors": authors,
                "year": year,
                "venue": "arXiv preprint",
                "doi": "",
                "url": f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else "",
                "abstract": abstract,
                "citations": 0,
                "source": "ArXiv",
            })
        time.sleep(0.5)
    except Exception as e:
        print(f"  [WARN] ArXiv search failed: {e}")
    return papers


# ── Source: PubMed ──────────────────────────────────────────────────────────────

def search_pubmed(query: str, days: int) -> list[dict]:
    """Search PubMed for recent papers (biomedical topics)."""
    papers = []
    try:
        # Step 1: esearch
        search_params = {
            "db": "pubmed",
            "term": query,
            "retmax": MAX_RESULTS_PER_SOURCE,
            "sort": "date",
            "retmode": "json",
            "datetype": "pdat",
            "reldate": days,
        }
        resp = requests.get(f"{PUBMED_BASE}/esearch.fcgi", params=search_params, timeout=15)
        resp.raise_for_status()
        ids = resp.json().get("esearchresult", {}).get("idlist", [])
        if not ids:
            return papers

        # Step 2: efetch summary
        fetch_params = {
            "db": "pubmed",
            "id": ",".join(ids[:10]),
            "retmode": "json",
        }
        fetch_resp = requests.get(f"{PUBMED_BASE}/esummary.fcgi", params=fetch_params, timeout=15)
        fetch_resp.raise_for_status()
        result = fetch_resp.json().get("result", {})

        for pmid in ids[:10]:
            item = result.get(str(pmid), {})
            title = item.get("title", "")
            year_str = item.get("pubdate", "")[:4]
            year = int(year_str) if year_str.isdigit() else datetime.utcnow().year
            authors = [a.get("name", "") for a in (item.get("authors") or [])[:3]]
            venue = item.get("source", "PubMed")
            doi = ""
            for id_obj in item.get("articleids", []):
                if id_obj.get("idtype") == "doi":
                    doi = id_obj.get("value", "")
                    break
            url = f"https://doi.org/{doi}" if doi else f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"

            papers.append({
                "title": title,
                "authors": authors,
                "year": year,
                "venue": venue,
                "doi": doi,
                "url": url,
                "abstract": "",
                "citations": 0,
                "source": "PubMed",
            })
        time.sleep(0.5)
    except Exception as e:
        print(f"  [WARN] PubMed search failed: {e}")
    return papers


# ── Deduplication & Filtering ───────────────────────────────────────────────────

def deduplicate(papers: list[dict], existing_hashes: set) -> tuple[list[dict], set]:
    """Remove papers already in the knowledge brain or duplicate within this batch."""
    seen_hashes = set()
    seen_titles = set()
    new_papers = []

    for p in papers:
        identifier = p.get("doi") or p.get("url") or p.get("title")
        h = doi_hash(identifier) if identifier else None

        if h and (h in existing_hashes or h in seen_hashes):
            continue

        title_normalized = re.sub(r"[^a-z0-9]", "", p["title"].lower())
        if title_normalized in seen_titles:
            continue

        if h:
            seen_hashes.add(h)
        seen_titles.add(title_normalized)
        new_papers.append(p)

    return new_papers, seen_hashes


# ── Brain File Append ───────────────────────────────────────────────────────────

def format_authors(authors: list[str]) -> str:
    if not authors:
        return "Unknown"
    if len(authors) == 1:
        return authors[0]
    if len(authors) == 2:
        return " & ".join(authors)
    return authors[0] + " et al."


def append_to_brain(papers: list[dict], topic: str, today: str) -> int:
    """Append new paper entries to SECOND-KNOWLEDGE-BRAIN.md. Returns count added."""
    if not papers:
        return 0

    if not BRAIN_FILE.exists():
        print(f"  [WARN] Brain file not found at {BRAIN_FILE}")
        return 0

    rows = []
    for p in papers:
        authors_str = format_authors(p["authors"])
        doi_display = p.get("doi") or p.get("url") or "N/A"
        rows.append(
            f"| {p['title'][:70]} | {authors_str} | {p['year']} | "
            f"{p['venue'][:30]} | {doi_display} | {p.get('score', 0.0):.2f} | {today} |"
        )

    log_entry = f"| {today} | {', '.join([p['source'] for p in papers[:1]])} | {len(papers)} | {topic[:40]} | Auto-crawl |\n"

    with open(BRAIN_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n\n<!-- Auto-appended by knowledge_updater.py on {today} | topic: {topic} -->\n")
        for row in rows:
            f.write(row + "\n")
        # Append to update log
        f.write(f"\n<!-- Log: {log_entry} -->\n")

    return len(papers)


# ── Main Pipeline ───────────────────────────────────────────────────────────────

def run_pipeline(topic: str, days: int = DEFAULT_DAYS, verbose: bool = True) -> dict:
    today = datetime.utcnow().strftime("%Y-%m-%d")
    existing_hashes = load_doi_cache()

    if verbose:
        print(f"\n[knowledge_updater] Topic: '{topic}' | Days: {days} | Date: {today}")
        print(f"  Existing indexed papers (hash count): {len(existing_hashes)}")

    # Collect from all sources
    all_papers: list[dict] = []
    if verbose:
        print("  Searching Semantic Scholar...")
    all_papers.extend(search_semantic_scholar(topic, days))
    if verbose:
        print(f"    Found {len(all_papers)} papers so far")
        print("  Searching ArXiv...")
    arxiv_papers = search_arxiv(topic, days)
    all_papers.extend(arxiv_papers)
    if verbose:
        print(f"    Found {len(all_papers)} papers so far")
        print("  Searching PubMed...")
    all_papers.extend(search_pubmed(topic, days))
    if verbose:
        print(f"    Total raw collected: {len(all_papers)}")

    # Score each paper
    for p in all_papers:
        p["score"] = compute_score(
            p.get("year", 2020),
            p.get("title", ""),
            p.get("abstract", ""),
            p.get("citations", 0),
            topic,
        )

    # Sort by score
    all_papers.sort(key=lambda x: x["score"], reverse=True)

    # Filter by minimum score
    all_papers = [p for p in all_papers if p["score"] >= MIN_SCORE_THRESHOLD]

    # Deduplicate against existing cache + within this batch
    new_papers, new_hashes = deduplicate(all_papers, existing_hashes)
    if verbose:
        print(f"  After dedup: {len(new_papers)} new papers to add")

    # Append to brain
    added = append_to_brain(new_papers, topic, today)

    # Update cache
    existing_hashes.update(new_hashes)
    save_doi_cache(existing_hashes)

    result = {
        "topic": topic,
        "date": today,
        "raw_collected": len(all_papers) + (len(all_papers) - len(all_papers)),  # raw before dedup
        "new_added": added,
        "total_indexed": len(existing_hashes),
    }
    if verbose:
        print(f"  Added {added} new papers to SECOND-KNOWLEDGE-BRAIN.md")
        print(f"  Total indexed (all time): {len(existing_hashes)}")
    return result


def main():
    parser = argparse.ArgumentParser(description="Update research-paper-writer knowledge brain")
    parser.add_argument("--topic", type=str, help="Topic to search for")
    parser.add_argument("--days", type=int, default=DEFAULT_DAYS, help="Days back to search (default: 90)")
    parser.add_argument("--all-defaults", action="store_true", help="Run all default topics")
    parser.add_argument("--quiet", action="store_true", help="Suppress verbose output")
    args = parser.parse_args()

    verbose = not args.quiet
    results = []

    if args.all_defaults or not args.topic:
        print(f"Running default topics ({len(DEFAULT_TOPICS)} topics)...")
        for t in DEFAULT_TOPICS:
            r = run_pipeline(t, args.days, verbose)
            results.append(r)
    else:
        r = run_pipeline(args.topic, args.days, verbose)
        results.append(r)

    print("\n=== Summary ===")
    total_added = sum(r["new_added"] for r in results)
    print(f"Topics processed: {len(results)}")
    print(f"Total new papers added: {total_added}")
    for r in results:
        print(f"  [{r['topic'][:40]}]: +{r['new_added']} papers")


if __name__ == "__main__":
    main()
