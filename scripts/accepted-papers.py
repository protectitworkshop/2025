#!/usr/bin/env python3

# Usage (from the top-level directory in the git repository):
# python3 scripts/accepted-papers.py

import csv
import json

def format_paper(paper_dict, talks, poster_mapping):
    title = """
                        <a data-toggle="collapse" href="#abs{id}" class="paper-title">
                            ({poster}) {title}
""".format(id=paper_dict['id'], poster=poster_mapping[paper_dict['id']], title=paper_dict['title'])
    if paper_dict['id'] in talks:
        title += """
                            <font color="#d07200"><b>(contributed talk)</b></font>
"""
    title += """
                        </a>
"""
    if 'url' in paper_dict:
        title += """
                        &nbsp;&nbsp;<a href="{url}" class="link-paper">[URL]</a>
""".format(url = paper_dict['url'])
    if 'pdf' in paper_dict:
        title += """
                        &nbsp;&nbsp;<a href="pdfs/{pdf}" class="link-paper">[PDF]</a>
""".format(pdf = paper_dict['pdf'])
    return """
                <div class="panel panel-default panel-paper">
                    <div class="panel-body panel-paper-body">
                        <span class="paper-author">
                            {authors}
                        </span><br />
                        {title}
                    </div>
                    <div id="abs{id}" class="panel-footer panel-paper-footer collapse">
                        {abstract}
                    </div>
                </div>
""".format(authors=paper_dict['authors'], title=title, id=paper_dict['id'], abstract=paper_dict['abstract'])

def read_papers(filename):
    result = []
    with open(filename, encoding="utf8") as f:
        data = json.load(f)
        for p in data:
            if p['status'] != 'accepted':
                continue
            paper = {}
            paper['id'] = int(p['pid'])
            paper['title'] = p['title']
            paper['abstract'] = p['abstract']
            authors = []
            for a in p['authors']:
                author = " ".join([a['first'], a['last']])
                if 'affiliation' in a:
                    author += " ({})".format(a['affiliation'])
                authors += [author]
            paper['authors'] = ", ".join(authors)
            if 'final' in p:
                paper['pdf'] = p['final']['content_file']
            if 'link_full_paper' in p:
                paper['url'] = p['link_full_paper']
            result += [paper]
    return result

def read_poster_mapping(filename):
    result = {}
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            result[int(row['ID'])] = row['Poster Area']
    return result

if __name__ == '__main__':
    # Define inputs.
    talks = [6,22,26,33,41,49,69]
    csv_file = "data/ppml21-data.csv"
    json_file = "data/ppml21-data.json"

    # Parse inputs.
    papers = read_papers(json_file)
    poster_mapping = read_poster_mapping(csv_file)

    # Sort papers by poster area.
    def by_poster_area(p):
        area = poster_mapping[p['id']]
        return (area[0], int(area[1:]))
    papers.sort(key = by_poster_area)

    # Print formatted papers.
    print("\n".join([format_paper(p, talks, poster_mapping) for p in papers]))