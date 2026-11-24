#!/usr/bin/env python3
"""Generate the static LIGHT prototype. Run from this folder."""
import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent

PAGES = []


def media(name, depth):
    files = {
        PHOTO: "img/hero.jpg",
        ILLU: "img/idea.png",
        TALK: "img/talk.png",
        PATHWAY: "img/light-grafika.png",
    }
    return asset(files[name], depth)


def asset(path, depth):
    return "../" * depth + path


def link(url, depth):
    return "../" * depth + url


PHOTO = "grafiki dla DUT _V1.jpg"
ILLU = "DUT_www_graphic.v1.png"
TALK = "DUT_www_graphic.v3_followtheLIGHT.png"
PATHWAY = "LIGHT_grafika.png"


def chrome(p):
    d = p["depth"]
    lang = p["lang"]
    pl = lang == "pl"
    home = link("index.html" if pl else "en/index.html", d)
    other = link(p["alt"], d)
    labels = {
        "pl": {
            "skip": "Przejdź do treści",
            "menu": "Menu",
            "search": "Szukaj",
            "ph": "Czego szukasz?",
            "about": "O projekcie",
            "labs": "Laboratoria",
            "news": "Aktualności",
            "results": "Rezultaty",
            "files": "Do pobrania",
            "partners": "Partnerzy",
            "team": "Zespół",
            "contact": "Kontakt",
            "k": "Kartuzy",
            "l": "Lund",
            "i": "Innsbruck",
            "font": "Rozmiar czcionki",
            "contrast": "Zmień kontrast",
            "main": "Menu główne",
        },
        "en": {
            "skip": "Skip to content",
            "menu": "Menu",
            "search": "Search",
            "ph": "What are you looking for?",
            "about": "About",
            "labs": "Living labs",
            "news": "News",
            "results": "Results",
            "files": "Downloads",
            "partners": "Partners",
            "team": "Team",
            "contact": "Contact",
            "k": "Kartuzy",
            "l": "Lund",
            "i": "Innsbruck",
            "font": "Font size",
            "contrast": "Change contrast",
            "main": "Main menu",
        },
    }[lang]
    nav_url = {
        "about": "o-projekcie.html" if pl else "en/about.html",
        "labs": "laboratoria.html" if pl else "en/living-labs.html",
        "k": "laboratorium-kartuzy.html" if pl else "en/lab-kartuzy.html",
        "l": "laboratorium-lund.html" if pl else "en/lab-lund.html",
        "i": "laboratorium-innsbruck.html" if pl else "en/lab-innsbruck.html",
        "news": "aktualnosci.html" if pl else "en/news.html",
        "results": "rezultaty.html" if pl else "en/results.html",
        "files": "do-pobrania.html" if pl else "en/downloads.html",
        "partners": "partnerzy.html" if pl else "en/partners.html",
        "team": "zespol.html" if pl else "en/team.html",
        "contact": "kontakt.html" if pl else "en/contact.html",
        "search": "szukaj.html" if pl else "en/search.html",
    }

    def a(key):
        cur = ' aria-current="page"' if p.get("nav") == key else ""
        return f'<a href="{link(nav_url[key], d)}"{cur}>{labels[key]}</a>'

    crumbs = ""
    if p.get("crumbs"):
        items = [f'<li><a href="{home}">LIGHT</a></li>']
        for label, url in p["crumbs"][:-1]:
            items.append(f'<li><a href="{link(url, d)}">{label}</a></li>')
        items.append(f'<li>{p["crumbs"][-1][0]}</li>')
        crumbs = f'<nav class="crumbs" aria-label="{"Ścieżka" if pl else "Breadcrumb"}"><div class="wrap"><ol>{"".join(items)}</ol></div></nav>'

    side = ""
    if p.get("side"):
        lis = []
        for label, url, key in p["side"]:
            cur = ' aria-current="page"' if p.get("side_current") == key else ""
            lis.append(f'<li><a href="{link(url, d)}"{cur}>{label}</a></li>')
        title = p.get("side_title", "")
        side = f'<aside class="side"><p>{title}</p><ul>{"".join(lis)}</ul></aside>'

    if p.get("home"):
        main = p["body"]
    elif side:
        main = f'<div class="wrap layout">{side}<article class="prose" id="tresc">{p["body"]}</article></div>'
    else:
        main = f'<div class="wrap"><article class="prose" id="tresc">{p["body"]}</article></div>'

    title_block = ""
    if not p.get("home"):
        title_block = f'<div class="wrap page-title"><h1>{p["h1"]}</h1></div>'
        if not side:
            main = f'<div class="wrap"><article class="prose" id="tresc">{p["body"]}</article></div>'

    foot = footer(p)
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{p["title"]}</title>
  <meta name="description" content="{p["desc"]}">
  <link rel="stylesheet" href="{asset("css/style.css", d)}">
  <script>
    try {{
      var f = localStorage.getItem("light-font");
      if (f && f !== "0") document.documentElement.dataset.font = f;
      if (localStorage.getItem("light-contrast") === "1") document.documentElement.classList.add("contrast");
    }} catch (e) {{}}
  </script>
</head>
<body data-root="{"../" * d}">
  <a class="skip" href="#tresc">{labels["skip"]}</a>
  <div class="topbar">
    <div class="wrap">
      <div class="tools">
        <nav class="lang" aria-label="{"Język" if pl else "Language"}">
          <a href="{link(p["pl"], d)}" {"aria-current=\"true\"" if pl else ""}>PL</a>
          <a href="{other}" {"aria-current=\"true\"" if not pl else ""}>EN</a>
        </nav>
        <span>
          <button class="tool-btn" type="button" data-font="0" aria-pressed="false">A <span class="sr">{"normalny" if pl else "normal"}</span></button>
          <button class="tool-btn" type="button" data-font="1" aria-pressed="false">A+</button>
          <button class="tool-btn" type="button" data-font="2" aria-pressed="false">A++</button>
        </span>
        <button class="tool-btn" type="button" data-contrast aria-pressed="false">{labels["contrast"]}</button>
      </div>
    </div>
  </div>
  <header class="site-header">
    <div class="wrap header-row">
      <a class="brand" href="{home}">
        <img src="{asset("img/light-logo.png", d)}?v=3" alt="LIGHT">
      </a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="menu">{labels["menu"]}</button>
      <nav class="main-nav" id="menu" aria-label="{labels["main"]}">
        <ul>
          <li>{a("about")}</li>
          <li class="has-sub">{a("labs")}
            <ul class="submenu">
              <li><a href="{link(nav_url["k"], d)}">{labels["k"]}</a></li>
              <li><a href="{link(nav_url["l"], d)}">{labels["l"]}</a></li>
              <li><a href="{link(nav_url["i"], d)}">{labels["i"]}</a></li>
            </ul>
          </li>
          <li>{a("news")}</li>
          <li>{a("results")}</li>
          <li>{a("files")}</li>
          <li>{a("partners")}</li>
          <li>{a("team")}</li>
          <li>{a("contact")}</li>
        </ul>
      </nav>
      <form class="search" action="{link(nav_url["search"], d)}" method="get" role="search">
        <label class="sr" for="q-{p["id"]}">{labels["search"]}</label>
        <input id="q-{p["id"]}" type="search" name="q" placeholder="{labels["ph"]}">
        <button type="submit">{labels["search"]}</button>
      </form>
    </div>
  </header>
  {crumbs}
  {title_block}
  {main}
  {foot}
  <script src="{asset("js/search-index.js", d)}"></script>
  <script src="{asset("js/site.js", d)}"></script>
</body>
</html>
'''


def footer(p):
    d = p["depth"]
    pl = p["lang"] == "pl"
    if pl:
        text = """
        <div><h2>LIGHT</h2><p>Looking for Integrated Solutions for Healthy PEDs</p><p>Projekt koordynowany przez Politechnikę Gdańską.</p></div>
        <div><h2>Kontakt</h2><p>prof. dr hab. inż. arch. Justyna Martyniuk-Pęczek</p><p><a href="mailto:juspecze@pg.edu.pl">juspecze@pg.edu.pl</a></p><p>ul. Gabriela Narutowicza 11/12<br>80-233 Gdańsk</p></div>
        <div><h2>Na skróty</h2><p><a href="{labs}">Laboratoria miejskie</a></p><p><a href="{news}">Aktualności</a></p><p><a href="{files}">Do pobrania</a></p><p><a href="https://pg.edu.pl/">pg.edu.pl</a></p></div>
        """.format(
            labs=link("laboratoria.html", d),
            news=link("aktualnosci.html", d),
            files=link("do-pobrania.html", d),
        )
        legal = (
            "<p>Prototyp układu i treści. Docelowa strona powstanie w CMS Politechniki Gdańskiej, w szablonie uczelni. Wpisy aktualności i pliki oznaczone jako przykładowe nie są jeszcze opublikowanymi materiałami projektu.</p>"
            "<p>Projekt „LIGHT – Looking for Integrated Solutions for Healthy PEDs” (F-DUT-2024-0011) uzyskał dofinansowanie następujących agencji: Narodowego Centrum Badań i Rozwoju (NCBiR) w Polsce, Szwedzkiej Agencji Energetycznej (SEA) w Szwecji, Austriackiej Agencji Promocji Badań (FFG) w Austrii oraz Szwajcarskiej Narodowej Fundacji Nauki (SNSF) w Szwajcarii, w ramach partnerstwa Driving Urban Transitions, współfinansowanego przez Komisję Europejską. Wyłączna odpowiedzialność za treść tej strony spoczywa na projekcie i w żaden sposób nie odzwierciedla stanowiska Unii Europejskiej.</p>"
        )
    else:
        text = """
        <div><h2>LIGHT</h2><p>Looking for Integrated Solutions for Healthy PEDs</p><p>Coordinated by Gdańsk University of Technology.</p></div>
        <div><h2>Contact</h2><p>Prof. Justyna Martyniuk-Pęczek, PhD, DSc, Eng., Arch.</p><p><a href="mailto:juspecze@pg.edu.pl">juspecze@pg.edu.pl</a></p><p>ul. Gabriela Narutowicza 11/12<br>80-233 Gdańsk, Poland</p></div>
        <div><h2>Shortcuts</h2><p><a href="{labs}">Living labs</a></p><p><a href="{news}">News</a></p><p><a href="{files}">Downloads</a></p><p><a href="https://pg.edu.pl/en">pg.edu.pl</a></p></div>
        """.format(
            labs=link("en/living-labs.html", d),
            news=link("en/news.html", d),
            files=link("en/downloads.html", d),
        )
        legal = (
            "<p>Layout and content prototype. The live site will be published in the Gdańsk Tech CMS, using the university template. Sample news and files are not published project materials yet.</p>"
            "<p>Project “LIGHT – Looking for Integrated Solutions for Healthy PEDs” (F-DUT-2024-0011) has been funded by the following funding agencies: the National Centre for Research and Development (NCBiR) in Poland, the Swedish Energy Agency (SEA) in Sweden, the Austrian Research Promotion Agency (FFG) in Austria, and the Swiss National Science Foundation (SNSF) in Switzerland under the Driving Urban Transitions Partnership, which has been co-funded by the European Commission. The sole responsibility for the content of this website lies with the project and in no way reflects the views of the European Union.</p>"
        )
    return f'<footer class="site-footer"><div class="wrap footer-grid">{text}</div><div class="wrap legal">{legal}</div></footer>'


def add(page):
    PAGES.append(page)


def sr_style():
    return ""


# ---------- Polish ----------

def home_pl():
    d = 0
    graphic = media(PATHWAY, d)
    return f'''
<section class="hero">
  <div class="hero-media"><img src="{graphic}" alt="Main Transition Pathway: dzielnice dodatnie energetycznie, słońce, zabudowa, turbiny i zieleń"></div>
  <div class="wrap hero-copy" id="tresc">
    <p class="eyebrow">Driving Urban Transitions · Positive Energy Districts</p>
    <h1>LIGHT</h1>
    <p class="subtitle">Looking for Integrated Solutions for Healthy PEDs</p>
    <p class="lead">Zdrowe, energooszczędne i przyjazne mieszkańcom dzielnice. Projekt łączy transformację energetyczną z dostępem do światła dziennego, komfortem i zdrowiem.</p>
    <p><a class="more" href="o-projekcie.html">Poznaj projekt</a></p>
  </div>
</section>
<section class="section">
  <div class="wrap prose">
    <h2>Dlaczego zdrowe dzielnice energetyczne?</h2>
    <p>Zagęszczanie miast często kłóci się z dostępem do światła dziennego i jakością życia. LIGHT traktuje zdrowie mieszkańców jako część planowania dzielnic dodatnich energetycznie: obok energii, błękitno-zielonej infrastruktury i mobilności.</p>
    <p><a href="o-projekcie.html">Wyzwania i rozwiązanie</a></p>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="section-head"><h2>Trzy laboratoria miejskie</h2><a href="laboratoria.html">Więcej</a></div>
    {europe_map([
        ("laboratorium-lund.html", "Lund", 365.9, 265.5, 380, 252),
        ("laboratorium-kartuzy.html", "Kartuzy", 432.7, 285.8, 446, 278),
        ("laboratorium-innsbruck.html", "Innsbruck", 341.8, 390.4, 356, 378),
    ], "Mapa Europy z trzema laboratoriami LIGHT", "Kliknij kropkę: Lund, Kartuzy albo Innsbruck.")}
    {lab_cards(True, d)}
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="section-head"><h2>Aktualności</h2><a href="aktualnosci.html">Więcej</a></div>
    {home_news(True, d)}
  </div>
</section>
<section class="section soft">
  <div class="wrap">
    <div class="section-head"><h2>Co powstanie</h2><a href="rezultaty.html">Rezultaty</a></div>
    <div class="cards">
      <a class="card" href="rezultaty.html"><h3>Wytyczne LIGHT</h3><p>Praktyczne zalecenia dla zintegrowanego planowania miast.</p></a>
      <a class="card" href="rezultaty.html"><h3>Narzędzia CitySim i DALEC</h3><p>Otwarte rozszerzenia do oceny energii, światła i komfortu.</p></a>
      <a class="card" href="do-pobrania.html"><h3>Materiały do pobrania</h3><p>Raporty, prezentacje i dokumentacja — w miarę publikacji.</p></a>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Partnerzy</h2><a href="partnerzy.html">Całe konsorcjum</a></div>
    <p>11 instytucji z Polski, Austrii, Szwecji i Szwajcarii. Koordynacja: Politechnika Gdańska.</p>
    {partner_logos(True)}
  </div>
</section>
'''


def about_body(pl, d):
    if pl:
        return '''
<p>LIGHT proponuje, aby zdrowie i dobrostan mieszkańców były częścią planowania przestrzennego i przejścia do dzielnic dodatnich energetycznie.</p>
<h2 id="wyzwania">Wyzwania</h2>
<ul>
  <li>Zagęszczanie miast bywa sprzeczne z dostępem do światła dziennego i promieniowania słonecznego.</li>
  <li>Gęstsza zabudowa nasila miejską wyspę ciepła, hałas i pogarsza jakość powietrza.</li>
  <li>Trudno spiąć systemy energetyczne z błękitno-zieloną infrastrukturą i mobilnością.</li>
  <li>Renowacja dzielnic musi uwzględniać możliwości finansowe mieszkańców i sprawiedliwość zmiany.</li>
  <li>Brakuje narzędzi, które łączą wskaźniki energii ze zdrowiem fizycznym i psychicznym.</li>
</ul>
<h2 id="rozwiazanie">Rozwiązanie</h2>
<ul>
  <li>Trzy laboratoria miejskie: Kartuzy, Lund i wirtualne laboratorium w Innsbrucku.</li>
  <li>Rozwój narzędzi CitySim i DALEC oraz modelowanie scenariuszy z udziałem mieszkańców.</li>
  <li>Ramy finansowania regeneracyjnego: korzyści społeczne, środowiskowe i finansowe razem.</li>
</ul>
<h2 id="dane">Dane projektu</h2>
<dl class="facts">
  <div><dt>Akronim</dt><dd>LIGHT</dd></div>
  <div><dt>Pełna nazwa</dt><dd>Looking for Integrated Solutions for Healthy PEDs</dd></div>
  <div><dt>Ścieżka</dt><dd>Positive Energy Districts</dd></div>
  <div><dt>Podejście</dt><dd>Research-oriented approach</dd></div>
  <div><dt>Czas</dt><dd>36 miesięcy, 01.2026–12.2028</dd></div>
  <div><dt>Budżet</dt><dd>1&nbsp;263&nbsp;016,37 EUR</dd></div>
  <div><dt>Nakład pracy</dt><dd>162 osobomiesiące</dd></div>
  <div><dt>Koordynacja</dt><dd>Politechnika Gdańska</dd></div>
</dl>
<h2 id="zasady">Równość i zasada DNSH</h2>
<p>Ponad połowę zespołu badawczego i koordynację projektu stanowią kobiety. Konsorcjum ogranicza ślad węglowy: podróże lądowe, spotkania online, zielone zamówienia i mniej materiałów drukowanych.</p>
<p class="note">Dat etapów badawczych nie wpisujemy z góry. Oś czasu na stronie rezultatów ma na razie początek i koniec projektu. Kamienie milowe dojdą po uzgodnieniu z zespołem.</p>
'''
    return '''
<p>LIGHT makes residents’ health and well-being part of spatial planning and the transition towards Positive Energy Districts.</p>
<h2 id="challenges">Challenges</h2>
<ul>
  <li>Compact urban development often conflicts with access to daylight and solar radiation.</li>
  <li>Higher density intensifies the urban heat island, noise and poorer air quality.</li>
  <li>Energy systems, blue-green infrastructure and mobility are rarely planned together.</li>
  <li>Renovation has to remain affordable and socially just.</li>
  <li>Planning tools seldom link energy performance with physical and mental health.</li>
</ul>
<h2 id="solution">Proposed solution</h2>
<ul>
  <li>Three living labs: Kartuzy, Lund and a virtual lab in Innsbruck.</li>
  <li>Further development of CitySim and DALEC, with participatory scenario modelling.</li>
  <li>A regenerative finance frame for social, environmental and financial benefits together.</li>
</ul>
<h2 id="facts">Project data</h2>
<dl class="facts">
  <div><dt>Acronym</dt><dd>LIGHT</dd></div>
  <div><dt>Full title</dt><dd>Looking for Integrated Solutions for Healthy PEDs</dd></div>
  <div><dt>Pathway</dt><dd>Positive Energy Districts</dd></div>
  <div><dt>Approach</dt><dd>Research-oriented approach</dd></div>
  <div><dt>Duration</dt><dd>36 months, 01.2026–12.2028</dd></div>
  <div><dt>Budget</dt><dd>EUR 1,263,016.37</dd></div>
  <div><dt>Effort</dt><dd>162 person-months</dd></div>
  <div><dt>Coordinator</dt><dd>Gdańsk University of Technology</dd></div>
</dl>
<h2 id="principles">Equality and DNSH</h2>
<p>Women make up more than half of the research team and lead the project coordination. The consortium limits its carbon footprint through land travel, online meetings, green procurement and less printed material.</p>
<p class="note">Research-stage dates are not invented here. The timeline on the results page shows only the project start and end until milestones are agreed with the team.</p>
'''



def europe_map(places, label, caption):
    paths = (ROOT / "img" / "europe-land.txt").read_text(encoding="utf-8").splitlines()
    land = "".join(f'<path d="{d}"/>' for d in paths if d.strip())
    links = []
    for href, name, x, y, tx, ty in places:
        links.append(
            f'<a href="{href}" aria-label="{name}">'
            f'<rect class="map-label-hit" x="{x - 16}" y="{ty - 20}" width="{tx - x + 96}" height="{y - ty + 36}" rx="6"/>'
            f'<circle class="map-dot" cx="{x}" cy="{y}" r="8"/>'
            f'<text x="{tx}" y="{ty}">{name}</text></a>'
        )
    return (
        f'<figure class="europe"><svg class="europe-map" viewBox="0 0 760 620" role="img" aria-label="{label}">'
        f'<rect width="760" height="620" class="sea"/>'
        f'<g class="land">{land}</g>'
        f'{"".join(links)}</svg><figcaption>{caption}</figcaption></figure>'
    )


def lab_cards(pl, depth):
    if pl:
        rows = [
            ("laboratorium-kartuzy.html", "img/labs/kartuzy-bg.jpg", "center 45%", "cover", "Polska", "Kartuzy",
             "Renowacja istniejącej zabudowy, błękitno-zielona infrastruktura oraz opłacalność i skutki środowiskowe.",
             "Kartuzy z lotu ptaka"),
            ("laboratorium-lund.html", "img/labs/lund.jpg", "center bottom", "cover", "Szwecja", "Lund",
             "Zagęszczanie miasta łączone z wytwarzaniem energii i rozwiązaniami bezemisyjnymi.",
             "Widok na Lund"),
            ("laboratorium-innsbruck.html", "img/labs/innsbruck.jpg", "center 34%", "cover", "Austria · wirtualne laboratorium", "Innsbruck",
             "Scenariusze zagęszczania i ich wpływ na hałas, powietrze i światło dzienne.",
             "Ulica w Innsbrucku"),
        ]
        credit = "Zdjęcie Kartuz: Michał Czachorowski."
    else:
        rows = [
            ("en/lab-kartuzy.html", "img/labs/kartuzy-bg.jpg", "center 45%", "cover", "Poland", "Kartuzy",
             "Renovation of the existing fabric, blue-green infrastructure, cost and environmental effects.",
             "An aerial view of Kartuzy"),
            ("en/lab-lund.html", "img/labs/lund.jpg", "center bottom", "cover", "Sweden", "Lund",
             "Densification combined with energy generation and zero-emission solutions.",
             "A view of Lund"),
            ("en/lab-innsbruck.html", "img/labs/innsbruck.jpg", "center 34%", "cover", "Austria · virtual lab", "Innsbruck",
             "Densification scenarios and their effect on noise, air and daylight.",
             "A street in Innsbruck"),
        ]
        credit = "Kartuzy photo: Michał Czachorowski."
    bits = []
    for href, img, pos, fit, place, title, text, alt in rows:
        bits.append(
            f'<a class="card card-city" href="{link(href, depth)}" style="--city:url(\'../{img}?v=6\');--pos:{pos};--fit:{fit}">'
            f'<span class="shade"><p class="place">{place}</p><h3>{title}</h3><p>{text}</p></span>'
            f'<span class="sr">{alt}</span></a>'
        )
    note = f'<p class="photo-credit">{credit}</p>' if credit else ""
    return f'<div class="cards cards-labs">{"".join(bits)}</div>{note}'


def labs_body(pl, d):
    if pl:
        intro = "<p>Trzy laboratoria sprawdzają rozwiązania w różnych miastach europejskich. Kropka na mapie otwiera opis miejsca.</p>"
        places = [
            ("laboratorium-lund.html", "Lund", 365.9, 265.5, 380, 252),
            ("laboratorium-kartuzy.html", "Kartuzy", 432.7, 285.8, 446, 278),
            ("laboratorium-innsbruck.html", "Innsbruck", 341.8, 390.4, 356, 378),
        ]
        caption = "Lund w Szwecji, Kartuzy w Polsce, Innsbruck w Austrii. Innsbruck jest wirtualnym laboratorium."
        label = "Mapa Europy z trzema laboratoriami LIGHT"
        cards = lab_cards(True, d)
    else:
        intro = "<p>Three labs test the approach in different European cities. A dot on the map opens that place.</p>"
        places = [
            ("lab-lund.html", "Lund", 365.9, 265.5, 380, 252),
            ("lab-kartuzy.html", "Kartuzy", 432.7, 285.8, 446, 278),
            ("lab-innsbruck.html", "Innsbruck", 341.8, 390.4, 356, 378),
        ]
        caption = "Lund in Sweden, Kartuzy in Poland, Innsbruck in Austria. Innsbruck is a virtual living lab."
        label = "Map of Europe with the three LIGHT living labs"
        cards = lab_cards(False, d)
    return intro + europe_map(places, label, caption) + cards


def place_photo(src, alt, caption, depth):
    return (
        f'<figure class="figure place"><img src="{asset(src, depth)}" alt="{alt}">'
        f'<figcaption>{caption}</figcaption></figure>'
    )


def lab_kartuzy(pl, depth):
    photo = place_photo(
        "img/labs/kartuzy.jpg",
        "Kolegiata i jezioro w Kartuzach" if pl else "The collegiate church and lake in Kartuzy",
        "Kolegiata i jezioro w Kartuzach. Zdjęcie: Tomasz Drążkowski." if pl else "The collegiate church and lake in Kartuzy. Photo: Tomasz Drążkowski.",
        depth,
    )
    if pl:
        return f'''
<p>Kartuzy są laboratorium renowacji istniejącej zabudowy. Prace obejmują integrację błękitno-zielonej infrastruktury oraz ocenę opłacalności i skutków środowiskowych.</p>
{photo}
<p>Partnerem miejskim jest Gmina Kartuzy. Po stronie polskiej w konsorcjum są też Politechnika Gdańska, Gdański Uniwersytet Medyczny, Uniwersytet Gdański, Gdańska Fundacja Innowacji Społecznych i — jako partner stowarzyszony — Foton-OZE.</p>
<h2>Zakres</h2>
<ul>
  <li>renowacja energetyczna istniejącej tkanki miejskiej,</li>
  <li>błękitno-zielona infrastruktura,</li>
  <li>wykonalność ekonomiczna i zrównoważenie środowiskowe.</li>
</ul>
<h2>Powiązane aktualności</h2>
<p>Gdy pojawią się relacje z terenu, będą oznaczane tym laboratorium. Na razie jest tu wpis przykładowy:</p>
<p><a href="aktualnosci/badania.html">Badania w terenie i wizyty studyjne</a></p>
'''
    return f'''
<p>Kartuzy is the lab for renovating the existing urban fabric, integrating blue-green infrastructure, and judging economic feasibility and environmental effects.</p>
{photo}
<p>The municipal partner is the Municipality of Kartuzy. Polish consortium members also include Gdańsk University of Technology, the Medical University of Gdańsk, the University of Gdańsk, the Gdańsk Foundation for Social Innovation and, as an associated partner, Foton-OZE.</p>
<h2>Scope</h2>
<ul>
  <li>energy renovation of the existing urban fabric,</li>
  <li>blue-green infrastructure,</li>
  <li>economic feasibility and environmental sustainability.</li>
</ul>
<h2>Related news</h2>
<p>Field stories will be tagged with this lab. For now there is a sample item:</p>
<p><a href="news/fieldwork.html">Fieldwork and study visits</a></p>
'''


def lab_lund(pl, depth):
    photo = place_photo(
        "img/labs/lund.jpg",
        "Widok na Lund" if pl else "A view of Lund",
        "Widok na Lund." if pl else "A view of Lund.",
        depth,
    )
    if pl:
        return f'''
<p>Lund sprawdza zagęszczanie miasta połączone z wytwarzaniem energii i rozwiązaniami bezemisyjnymi.</p>
{photo}
<p>Prowadzi je Uniwersytet w Lund. Gmina Lund jest partnerem stowarzyszonym.</p>
<h2>Zakres</h2>
<ul>
  <li>procesy zagęszczania zabudowy,</li>
  <li>innowacyjne wytwarzanie energii,</li>
  <li>rozwiązania bezemisyjne.</li>
</ul>
<h2>Powiązane aktualności</h2>
<p><a href="aktualnosci/badania.html">Badania w terenie i wizyty studyjne</a></p>
'''
    return f'''
<p>Lund tests urban densification together with energy generation and zero-emission solutions.</p>
{photo}
<p>Lund University leads this work. Lund Municipality is an associated partner.</p>
<h2>Scope</h2>
<ul>
  <li>densification of the urban fabric,</li>
  <li>innovative energy generation,</li>
  <li>zero-emission solutions.</li>
</ul>
<h2>Related news</h2>
<p><a href="news/fieldwork.html">Fieldwork and study visits</a></p>
'''


def lab_inns(pl, depth):
    photo = place_photo(
        "img/labs/innsbruck.jpg",
        "Ulica w Innsbrucku" if pl else "A street in Innsbruck",
        "Ulica w Innsbrucku." if pl else "A street in Innsbruck.",
        depth,
    )
    if pl:
        return f'''
<p>Innsbruck jest wirtualnym laboratorium miejskim. Zespół przygotowuje wielokryterialne scenariusze zagęszczania w projektowaniu parametrycznym i ocenia ich wpływ na zdrowie: hałas, jakość powietrza i dostęp do światła dziennego.</p>
{photo}
<p>To Virtual Urban Living Lab, zgodnie z opisem projektu. Uniwersytet w Innsbrucku jest partnerem, a Innsbrucker Immobiliengesellschaft partnerem stowarzyszonym.</p>
<h2>Zakres</h2>
<ul>
  <li>scenariusze zagęszczania,</li>
  <li>światło dzienne, hałas i powietrze,</li>
  <li>powiązanie z rozwojem CitySim i DALEC.</li>
</ul>
<h2>Powiązane aktualności</h2>
<p><a href="aktualnosci/narzedzia.html">Postępy prac nad narzędziami cyfrowymi</a></p>
'''
    return f'''
<p>Innsbruck is a virtual urban living lab. The team builds multi-criteria densification scenarios with parametric design and reads their health effects: noise, air quality and access to daylight.</p>
{photo}
<p>The name used in the project is Virtual Urban Living Lab. Universität Innsbruck is a partner and Innsbrucker Immobiliengesellschaft is an associated partner.</p>
<h2>Scope</h2>
<ul>
  <li>densification scenarios,</li>
  <li>daylight, noise and air,</li>
  <li>links to the CitySim and DALEC extensions.</li>
</ul>
<h2>Related news</h2>
<p><a href="news/tools.html">Progress on the digital tools</a></p>
'''


REAL_NEWS = [
    {
        "id": "lund",
        "cat": "spotkania",
        "date": "27–30.09.2026",
        "img": "img/news/lund-01.jpg",
        "pl": {
            "file": "aktualnosci/lund.html",
            "kicker": "Spotkania",
            "title": "Spotkanie konsorcjum w Lund",
            "lead": "27–30 września 2026 r. partnerzy LIGHT spotkali się w Lund. Były sesje robocze, prezentacja narzędzi DALEC i wyjście w teren.",
            "alt": "Prezentacja podczas spotkania LIGHT w Lund",
        },
        "en": {
            "file": "en/news/lund.html",
            "kicker": "Meetings",
            "title": "Consortium meeting in Lund",
            "lead": "On 27–30 September 2026 the LIGHT partners met in Lund. The programme included working sessions, a presentation of the DALEC tools and a walk through the city.",
            "alt": "A presentation at the LIGHT meeting in Lund",
        },
    },
    {
        "id": "martigny",
        "cat": "badania",
        "date": "17.08.2026",
        "img": "img/news/martigny.jpg",
        "pl": {
            "file": "aktualnosci/martigny.html",
            "kicker": "Badania",
            "title": "Drony i model 3D Martigny",
            "lead": "Politechnika Gdańska i IDIAP zeskanowały Martigny dronami i fotogrametrią. Materiał posłuży do modelu 3D miasta, analiz światła dziennego oraz symulacji partnerów.",
            "alt": "Widok z nalotu nad Martigny",
        },
        "en": {
            "file": "en/news/martigny.html",
            "kicker": "Fieldwork",
            "title": "Drones and a 3D model of Martigny",
            "lead": "Gdańsk Tech and Idiap scanned Martigny with drones and photogrammetry. The material will become a 3D model of the city, for daylight studies and the partners’ simulations.",
            "alt": "A view from the drone survey over Martigny",
        },
    },
    {
        "id": "inauguracja",
        "cat": "spotkania",
        "date": "10.02.2026",
        "img": "img/news/inauguracja.jpg",
        "pl": {
            "file": "aktualnosci/inauguracja.html",
            "kicker": "Spotkania",
            "title": "PG inauguruje projekt LIGHT",
            "lead": "10 lutego 2026 r. na Wydziale Architektury Politechniki Gdańskiej zainaugurowano międzynarodowy projekt LIGHT. Dotyczy zdrowych dzielnic dodatnich energetycznie. Liderem jest Politechnika Gdańska.",
            "alt": "Inauguracja projektu LIGHT na Wydziale Architektury",
        },
        "en": {
            "file": "en/news/inauguration.html",
            "kicker": "Meetings",
            "title": "Gdańsk Tech launches LIGHT",
            "lead": "On 10 February 2026 the Faculty of Architecture launched the international LIGHT project. It works on healthy Positive Energy Districts. Gdańsk Tech is the lead partner.",
            "alt": "The LIGHT project launch at the Faculty of Architecture",
        },
    },
]

LUND_PHOTOS = [
    ("img/news/lund-01.jpg", "Prezentacja narzędzi DALEC podczas spotkania w Lund.", "DALEC tools presented at the Lund meeting."),
    ("img/news/lund-02.jpg", "Lot dronem podczas spotkania.", "A drone flight during the meeting."),
    ("img/news/lund-03.jpg", "Wyjście w teren: rozmowa na dziedzińcu.", "A site visit: a talk in a courtyard."),
    ("img/news/lund-04.jpg", "Budynek oglądany podczas pobytu w Lund.", "A building seen during the stay in Lund."),
    ("img/news/lund-05.jpg", "Spacer po Lund, przystanek Lund C.", "A walk through Lund, at the Lund C stop."),
    ("img/news/lund-06.jpg", "Zdjęcie grupowe uczestników spotkania w Lund.", "Group photo of the meeting participants in Lund."),
    ("img/news/lund-07.jpg", "Wspólny posiłek podczas spotkania.", "A shared meal during the meeting."),
    ("img/news/lund-08.jpg", "Sesja robocza: uczestnicy przy laptopach.", "A working session, with participants at their laptops."),
    ("img/news/lund-09.jpg", "Omówienie protokołu oceny sąsiedztwa i katalogu kryteriów.", "Discussion of the neighbourhood assessment protocol and the catalogue of criteria."),
    ("img/news/lund-10.jpg", "Wyjście w teren: omówienie mapy przy przystanku.", "A site visit: a map explained at a stop."),
    ("img/news/lund-11.jpg", "Prezentacja zespołu Uniwersytetu Gdańskiego o transformacji energetycznej miast.", "A presentation by the University of Gdańsk team on the urban energy transition."),
    ("img/news/lund-12.jpg", "Pokaz modelu zabudowy i zieleni.", "A demonstration of a model of buildings and greenery."),
    ("img/news/lund-13.jpg", "Zdjęcie grupowe na dziedzińcu.", "A group photo in a courtyard."),
    ("img/news/lund-14.jpg", "Prezentacja widoku miasta z lotu ptaka.", "A presentation of an aerial view of the city."),
    ("img/news/lund-15.jpg", "Prezentacja schematu projektu LIGHT.", "A presentation of the LIGHT project diagram."),
    ("img/news/lund-16.jpg", "Jérôme Kämpf omawia kolejne kroki pracy z modelem CitySim.", "Jérôme Kämpf presents the next steps for the CitySim model."),
    ("img/news/lund-17.jpg", "Prezentacja Idiap o modelowaniu zanieczyszczeń na zewnątrz.", "An Idiap presentation on outdoor pollutant modelling."),
]

SRC_LIGHT = "https://arch.pg.edu.pl/2026-02/pg-inauguruje-miedzynarodowy-projekt-light-w-ramach-dut-horyzont-europa"
SRC_MARTIGNY = "https://arch.pg.edu.pl/2026-08/drony-i-fotogrametria-cyfrowy-model-3d-miasta-martigny"


def home_news(pl, depth):
    lang = "pl" if pl else "en"
    feature = REAL_NEWS[0]
    copy = feature[lang]
    sides = []
    for item in REAL_NEWS[1:]:
        s = item[lang]
        sides.append(
            f'<li><a href="{link(s["file"], depth)}"><p class="kicker">{item["date"]} · {s["kicker"]}</p>'
            f'<h3>{s["title"]}</h3></a><img src="{asset(item["img"], depth)}" alt=""></li>'
        )
    return f'''<div class="news-home">
      <a class="feature" href="{link(copy["file"], depth)}">
        <img src="{asset(feature["img"], depth)}" alt="{copy["alt"]}">
        <p class="kicker">{feature["date"]} · {copy["kicker"]}</p>
        <h3>{copy["title"]}</h3>
        <p>{copy["lead"]}</p>
      </a>
      <ul class="news-side">{"".join(sides)}</ul>
    </div>'''


def news_list(pl, d):
    illu = media(ILLU, d)
    talk = media(TALK, d)
    if pl:
        items = [
            ("spotkania", "aktualnosci/spotkania.html", talk, "Spotkania", "Relacje ze spotkań konsorcjum", "Krótki opis tematu, kilka zdjęć i informacja, co dalej."),
            ("badania", "aktualnosci/badania.html", illu, "Badania", "Badania w terenie i wizyty studyjne", "Co zespół ogląda, jakie dane zbiera i dlaczego mają znaczenie."),
            ("warsztaty", "aktualnosci/warsztaty.html", illu, "Warsztaty", "Warsztaty i udział mieszkańców", "Rozmowy z samorządem, ekspertami i społecznościami lokalnymi."),
            ("rezultaty", "aktualnosci/narzedzia.html", illu, "Rezultaty", "Postępy prac nad narzędziami cyfrowymi", "Modelowanie, światło dzienne, komfort, CitySim i DALEC prostym językiem."),
        ]
        note = "Wpisy z oznaczeniem „przykład” pokazują tylko układ przyszłego tekstu. Nie opisują odbytych wydarzeń."
        filters = [("all", "Wszystkie"), ("spotkania", "Spotkania"), ("badania", "Badania"), ("warsztaty", "Warsztaty"), ("rezultaty", "Rezultaty")]
        cat_name = {}
    else:
        items = [
            ("meetings", "en/news/meetings.html", talk, "Meetings", "Consortium meetings", "A short account, a few photos and the next step."),
            ("fieldwork", "en/news/fieldwork.html", illu, "Fieldwork", "Fieldwork and study visits", "What the team looks at, which data it collects and why that matters."),
            ("workshops", "en/news/workshops.html", illu, "Workshops", "Workshops and residents", "Conversations with municipalities, experts and local communities."),
            ("results", "en/news/tools.html", illu, "Results", "Progress on the digital tools", "Modelling, daylight, comfort, CitySim and DALEC in plain language."),
        ]
        note = "Items marked “sample” only show the layout of a future story. They do not report events that have already happened."
        filters = [("all", "All"), ("meetings", "Meetings"), ("fieldwork", "Fieldwork"), ("workshops", "Workshops"), ("results", "Results")]
        cat_name = {"spotkania": "meetings", "badania": "fieldwork"}
    buttons = "".join(
        f'<button type="button" data-cat="{c}" aria-pressed="{"true" if c == "all" else "false"}">{name}</button>'
        for c, name in filters
    )
    lang = "pl" if pl else "en"
    lis = []
    for item in REAL_NEWS:
        s = item[lang]
        cat = cat_name.get(item["cat"], item["cat"])
        lis.append(
            f'<li data-cat="{cat}"><img src="{asset(item["img"], d)}" alt=""><div>'
            f'<p class="kicker">{item["date"]} · {s["kicker"]}</p>'
            f'<h2><a href="{link(s["file"], d)}">{s["title"]}</a></h2><p>{s["lead"]}</p></div></li>'
        )
    for cat, url, img, kicker, title, lead in items:
        lis.append(
            f'<li data-cat="{cat}"><img src="{img}" alt=""><div><p class="badge">{"Przykład" if pl else "Sample"} · {kicker}</p>'
            f'<h2><a href="{link(url, d)}">{title}</a></h2><p>{lead}</p></div></li>'
        )
    return f'<p class="note">{note}</p><div class="filters" data-filter="#lista">{buttons}</div><ul class="news-list" id="lista">{"".join(lis)}</ul>'


def article(pl, kind):
    texts = {
        "spotkania": (
            "To wzór wpisu o współpracy, nie relacja z konkretnego spotkania.",
            "Na stronie znajdą się relacje ze spotkań konsorcjum, warsztatów roboczych i uzgodnień między partnerami. Wpis będzie miał kilka zdjęć, krótki opis najważniejszych tematów i informację o kolejnych krokach.",
            "Kategoria, data i laboratorium będą polami wymaganymi lub opcjonalnymi w CMS. Ten adres jest przykładem stałego odnośnika, który później można wkleić w mediach społecznościowych.",
        ),
        "badania": (
            "To wzór wpisu o pracy w terenie.",
            "Takie relacje opiszą, co zespół bada, jakie miejsca odwiedza, jakie dane zbiera i dlaczego są ważne dla przyszłych rozwiązań. Tu będą fotografie z Kartuz i pozostałych laboratoriów, gdy powstaną i będą miały zgodę na publikację.",
            "Wpis można powiązać z laboratorium. W tym wzorze jest to Kartuzy i Lund.",
        ),
        "warsztaty": (
            "To wzór wpisu o udziale mieszkańców.",
            "Wpisy z tej kategorii zbiorą informacje o spotkaniach z samorządami, ekspertami i społecznościami. Co było przedmiotem rozmów i jakie potrzeby udało się nazwać.",
            "Tłumaczenie na drugi język publikujemy dopiero po weryfikacji, nie automatycznie.",
        ),
        "narzedzia": (
            "To wzór wpisu o narzędziach.",
            "Tu opisujemy postęp modelowania miejskiego, analiz światła dziennego i komfortu termicznego oraz rozwoju CitySim i DALEC. Język ma być zrozumiały poza zespołem badawczym.",
            "Gdy pojawią się program, dokumentacja albo instrukcja, wpis będzie linkował do biblioteki materiałów.",
        ),
    }
    texts_en = {
        "spotkania": (
            "This is a sample story about cooperation, not a report of a specific meeting.",
            "The site will carry notes from consortium meetings, working sessions and agreements between partners: a few photos, the main topics and the next step.",
            "Category, date and an optional lab will be fields in the CMS. This address shows the stable link a real story will have.",
        ),
        "badania": (
            "This is a sample story about fieldwork.",
            "These notes will say what the team studies, which places it visits, which data it collects and why that matters. Photos from Kartuzy and the other labs will be added when they exist and can be published.",
            "A story can be linked to a lab. This sample points to Kartuzy and Lund.",
        ),
        "warsztaty": (
            "This is a sample story about participation.",
            "Posts in this category will record meetings with municipalities, experts and communities: what was discussed and which needs were named.",
            "The other language is published only after someone checks it. It is not translated and posted automatically.",
        ),
        "narzedzia": (
            "This is a sample story about the tools.",
            "This is where progress on urban modelling, daylight, thermal comfort, CitySim and DALEC will be explained in plain language.",
            "When software, documentation or a guide is public, the story will link to the download library.",
        ),
    }
    lead, body, extra = (texts if pl else texts_en)[kind]
    img = {
        "spotkania": TALK,
        "badania": ILLU,
        "warsztaty": ILLU,
        "narzedzia": ILLU,
    }[kind]
    cap = "Materiał ilustracyjny projektu LIGHT." if pl else "Illustrative LIGHT project image."
    alt = "Grafika projektu LIGHT" if pl else "LIGHT project graphic"
    return f'''
<p class="badge">{"Przykładowy wpis" if pl else "Sample story"}</p>
<p class="lead">{lead}</p>
<figure class="figure"><img src="IMG" alt="{alt}"><figcaption>{cap}</figcaption></figure>
<p>{body}</p>
<p>{extra}</p>
'''.replace("IMG", "IMGPLACE")


def results_body(pl):
    if pl:
        return '''
<p>LIGHT ma zostawić wzorzec zdrowych, sprawnych i dostępnych dzielnic dodatnich energetycznie. Poniżej są planowane rezultaty. Nie są jeszcze opublikowane.</p>
<h2 id="ramy">Ramy transformacji</h2>
<p>Model, który inne europejskie miasta będą mogły powtórzyć.</p>
<h2 id="wytyczne">Wytyczne LIGHT</h2>
<p>Publiczne, praktyczne zalecenia do zintegrowanego planowania.</p>
<h2 id="narzedzia">Narzędzie wspierające decyzje</h2>
<p>Otwarte oprogramowanie oparte na rozszerzeniach CitySim i DALEC. CitySim ma objąć światło dzienne we wnętrzach oraz komfort termiczny wewnątrz i na zewnątrz. DALEC ma objąć zacienienie i światło dzienne w gęstej zabudowie. Z narzędzia skorzystają inwestorzy, planiści i samorządy.</p>
<h2 id="os">Oś czasu</h2>
<ul class="timeline">
  <li><strong>01.2026</strong><span>Planowany początek projektu.</span></li>
  <li><strong>—</strong><span>Kamienie milowe badań dopiszemy po uzgodnieniu harmonogramu. Nie podajemy tu wymyślonych dat.</span></li>
  <li><strong>12.2028</strong><span>Planowane zakończenie projektu.</span></li>
</ul>
<p><a href="do-pobrania.html">Biblioteka materiałów</a></p>
'''
    return '''
<p>LIGHT aims to set a pattern for healthy, efficient and inclusive Positive Energy Districts. The results below are planned. They are not published yet.</p>
<h2 id="framework">Transformation framework</h2>
<p>A model other European cities can reuse.</p>
<h2 id="guidelines">LIGHT Guidelines</h2>
<p>Public, practical guidance for integrated urban planning.</p>
<h2 id="toolkit">Decision-support toolkit</h2>
<p>Open software based on CitySim and DALEC. CitySim is to cover indoor daylight and indoor and outdoor thermal comfort. DALEC is to cover shading and daylight in dense neighbourhoods. Investors, planners and local authorities are the users.</p>
<h2 id="time">Timeline</h2>
<ul class="timeline">
  <li><strong>01.2026</strong><span>Planned start.</span></li>
  <li><strong>—</strong><span>Research milestones will be added once the timetable is agreed. No dates are invented here.</span></li>
  <li><strong>12.2028</strong><span>Planned end.</span></li>
</ul>
<p><a href="downloads.html">Download library</a></p>
'''


def files_body(pl):
    if pl:
        rows = [
            ("Karta projektu", "O projekcie", "PL / EN", "PDF"),
            ("Raporty badawcze", "Raporty i publikacje", "PL / EN", "PDF"),
            ("Wytyczne LIGHT", "Wytyczne", "PL / EN", "PDF"),
            ("CitySim i DALEC", "Narzędzia cyfrowe", "EN", "link"),
            ("Prezentacje", "Prezentacje", "PL / EN", "PDF"),
            ("Logo i plansze", "Materiały graficzne", "—", "PNG / SVG"),
        ]
        note = "Biblioteka jest pusta, bo te pliki powstaną w trakcie projektu. Każdy późniejszy plik dostanie tytuł, datę, język, format, rozmiar i — przy narzędziach oraz publikacjach — licencję."
        heads = ("Tytuł", "Kategoria", "Język", "Format", "Status")
        status = "W przygotowaniu"
        filters = [("all", "Wszystkie"), ("projekt", "O projekcie"), ("raporty", "Raporty"), ("wytyczne", "Wytyczne"), ("narzedzia", "Narzędzia"), ("prezentacje", "Prezentacje"), ("grafika", "Grafika")]
        cats = ["projekt", "raporty", "wytyczne", "narzedzia", "prezentacje", "grafika"]
    else:
        rows = [
            ("Project sheet", "About", "PL / EN", "PDF"),
            ("Research reports", "Reports and papers", "PL / EN", "PDF"),
            ("LIGHT Guidelines", "Guidelines", "PL / EN", "PDF"),
            ("CitySim and DALEC", "Digital tools", "EN", "link"),
            ("Presentations", "Slides", "PL / EN", "PDF"),
            ("Logo and boards", "Graphics", "—", "PNG / SVG"),
        ]
        note = "The library is empty because these files will appear during the project. Each file will then have a title, date, language, format, size and, for tools and publications, a licence."
        heads = ("Title", "Category", "Language", "Format", "Status")
        status = "In preparation"
        filters = [("all", "All"), ("projekt", "About"), ("raporty", "Reports"), ("wytyczne", "Guidelines"), ("narzedzia", "Tools"), ("prezentacje", "Slides"), ("grafika", "Graphics")]
        cats = ["projekt", "raporty", "wytyczne", "narzedzia", "prezentacje", "grafika"]
    buttons = "".join(
        f'<button type="button" data-cat="{c}" aria-pressed="{"true" if c == "all" else "false"}">{n}</button>'
        for c, n in filters
    )
    body = "".join(
        f'<tr data-cat="{cat}"><td>{a}</td><td>{b}</td><td>{c}</td><td>{e}</td><td class="status">{status}</td></tr>'
        for (a, b, c, e), cat in zip(rows, cats)
    )
    return f'''<p class="note">{note}</p>
<div class="filters" data-filter="#pliki">{buttons}</div>
<div class="table-wrap"><table id="pliki">
<thead><tr><th>{heads[0]}</th><th>{heads[1]}</th><th>{heads[2]}</th><th>{heads[3]}</th><th>{heads[4]}</th></tr></thead>
<tbody>{body}</tbody></table></div>'''


def partner_src(filename, pl):
    return asset(f"img/partners/{filename}", 0 if pl else 1)


def partners():
    return [
        ("pg", "pg.svg", "https://pg.edu.pl/", True,
         "Politechnika Gdańska", "Gdańsk University of Technology",
         "Polska", "Poland", "Koordynator", "Coordinator",
         "Koordynuje projekt i łączy planowanie przestrzenne, energię oraz zdrowie mieszkańców.",
         "Coordinates the project and joins spatial planning, energy and residents’ health."),
        ("lu", "lu.svg", "https://www.lu.se/", False,
         "Uniwersytet w Lund", "Lund University",
         "Szwecja", "Sweden", "Partner", "Partner",
         "Prowadzi laboratorium w Lund: zagęszczanie, energia i rozwiązania bezemisyjne.",
         "Runs the Lund lab: densification, energy and zero-emission solutions."),
        ("gumed", "gumed.png", "https://gumed.edu.pl/", False,
         "Gdański Uniwersytet Medyczny", "Medical University of Gdańsk",
         "Polska", "Poland", "Partner", "Partner",
         "Uczelnia medyczna w konsorcjum. Wnosi perspektywę zdrowia mieszkańców.",
         "The medical university in the consortium. Brings the residents’ health perspective."),
        ("uibk", "uibk.svg", "https://www.uibk.ac.at/", False,
         "Uniwersytet w Innsbrucku", "Universität Innsbruck",
         "Austria", "Austria", "Partner", "Partner",
         "Prowadzi wirtualne laboratorium: zagęszczanie, hałas, powietrze i światło dzienne.",
         "Runs the virtual lab: densification, noise, air and daylight."),
        ("idiap", "idiap.svg", "https://www.idiap.ch/", False,
         "Idiap Research Institute", "Idiap Research Institute",
         "Szwajcaria", "Switzerland", "Partner", "Partner",
         "Instytut badawczy. Partner naukowy konsorcjum.",
         "A research institute. Scientific partner of the consortium."),
        ("ug", "ug.png", "https://ug.edu.pl/", False,
         "Uniwersytet Gdański", "University of Gdańsk",
         "Polska", "Poland", "Partner", "Partner",
         "Partner akademicki z Gdańska.",
         "Academic partner from Gdańsk."),
        ("gfsi", "gfsi.svg", "https://gfis.pl/", False,
         "Gdańska Fundacja Innowacji Społecznych", "Gdańsk Foundation for Social Innovation",
         "Polska", "Poland", "Partner", "Partner",
         "Organizacja społeczna. Włącza mieszkańców i lokalnych partnerów.",
         "A social organisation. Brings in residents and local partners."),
        ("kartuzy", "kartuzy.png", "https://kartuzy.pl/", False,
         "Gmina Kartuzy", "Municipality of Kartuzy",
         "Polska", "Poland", "Partner", "Partner",
         "Samorząd laboratorium. Renowacja istniejącej zabudowy i błękitno-zielona infrastruktura.",
         "The municipal authority of the lab. Renovation of the existing fabric and blue-green infrastructure."),
        ("foton", "foton.png", "https://foton-oze.pl/", False,
         "Foton-OZE", "Foton-OZE",
         "Polska", "Poland", "Partner stowarzyszony", "Associated partner",
         "Partner stowarzyszony po stronie energii odnawialnej.",
         "Associated partner on the renewable-energy side."),
        ("iig", "iig.png", "https://www.iig.at/", False,
         "Innsbrucker Immobiliengesellschaft", "Innsbrucker Immobiliengesellschaft",
         "Austria", "Austria", "Partner stowarzyszony", "Associated partner",
         "Partner stowarzyszony. Miejska spółka nieruchomości w Innsbrucku.",
         "Associated partner. The municipal property company in Innsbruck."),
        ("lund", "lund.png", "https://www.lund.se/", False,
         "Gmina Lund", "Lund Municipality",
         "Szwecja", "Sweden", "Partner stowarzyszony", "Associated partner",
         "Partner stowarzyszony laboratorium w Lund.",
         "Associated partner of the Lund lab."),
    ]


def partner_cards(pl):
    items = []
    for pid, logo, url, lead, pl_name, en_name, pl_c, en_c, pl_role, en_role, pl_desc, en_desc in partners():
        name = pl_name if pl else en_name
        country = pl_c if pl else en_c
        role = pl_role if pl else en_role
        cls = "role lead" if lead else "role"
        title = f'<a href="{url}">{name}</a>' if url else name
        src = partner_src(logo, pl)
        items.append(
            f'<li class="partner-card" id="{pid}">'
            f'<span class="logo-slot"><img src="{src}" alt=""></span>'
            f'<div><h2>{title}</h2>'
            f'<p class="kicker">{country}</p></div>'
            f'<span class="{cls}">{role}</span></li>'
        )
    intro = "Konsorcjum łączy uczelnie, samorządy, fundację, instytut badawczy i partnerów stowarzyszonych." if pl else "The consortium brings together universities, municipalities, a foundation, a research institute and associated partners."
    return f'<p>{intro}</p><ul class="partner-grid">{"".join(items)}</ul>'


def partner_logos(pl):
    page = "partnerzy.html" if pl else "partners.html"
    bits = []
    for pid, logo, url, lead, pl_name, en_name, *rest in partners():
        name = pl_name if pl else en_name
        src = partner_src(logo, pl)
        bits.append(f'<li><a href="{page}#{pid}"><img src="{src}" alt="{name}"></a></li>')
    return f'<ul class="logo-row">{"".join(bits)}</ul>'


def partners_body(pl):
    return partner_cards(pl)


def team_members():
    return [
        {
            "pl_name": "prof. dr hab. inż. arch. Justyna Martyniuk-Pęczek",
            "en_name": "Prof. Justyna Martyniuk-Pęczek",
            "pl_org": "Politechnika Gdańska",
            "en_org": "Gdańsk University of Technology",
            "pl_role": "kierownik projektu",
            "en_role": "Project leader",
            "lead": True,
            "photo": "img/team/justyna-martyniuk-peczek.jpg",
            "initials": "JM",
            "url": "https://pg.edu.pl/p/justyna-martyniuk-peczek-19369",
        },
        {
            "pl_name": "dr inż. Dubon Rodrigue",
            "en_name": "Dr. Dubon Rodrigue",
            "pl_org": "Idiap Research Institute",
            "en_org": "Idiap Research Institute",
            "pl_role": "Badacz po doktoracie",
            "en_role": "Postdoctoral researcher",
            "photo": "img/team/dubon-rodrigue.jpg",
            "initials": "DR",
            "url": "https://www.idiap.ch/en/people/dubon-rodrigue-2064",
        },
        {
            "pl_name": "prof. dr inż. Marie-Claude Dubois",
            "en_name": "Prof. Marie-Claude Dubois",
            "pl_org": "Uniwersytet w Lund",
            "en_org": "Lund University",
            "pl_role": "Associate professor",
            "en_role": "Associate professor",
            "photo": "img/team/marie-claude-dubois.jpg",
            "initials": "MD",
            "url": "https://portal.research.lu.se/en/persons/marie-claude-dubois/",
        },
        {
            "pl_name": "prof. dr inż. Jérôme Kämpf",
            "en_name": "Prof. Jérôme Kämpf",
            "pl_org": "Idiap Research Institute",
            "en_org": "Idiap Research Institute",
            "pl_role": "Starszy pracownik naukowy",
            "en_role": "Senior research scientist",
            "photo": "img/team/jerome-kampf.jpg",
            "initials": "JK",
            "url": "https://www.idiap.ch/~jkaempf/",
        },
        {
            "pl_name": "dr Olga Martyniuk",
            "en_name": "Dr. Olga Martyniuk",
            "pl_org": "Uniwersytet Gdański",
            "en_org": "University of Gdańsk",
            "pl_role": "Adiunkt",
            "en_role": "Assistant professor",
            "photo": "img/team/olga-martyniuk.jpg",
            "initials": "OM",
            "url": "https://repozytorium.bg.ug.edu.pl/info/author/UOG445c047d26c8486ba9cb9ef938330fe3/",
        },
        {
            "pl_name": "dr inż. Natalia Sokół",
            "en_name": "Dr. Natalia Sokół",
            "pl_org": "Politechnika Gdańska",
            "en_org": "Gdańsk University of Technology",
            "pl_role": "Adiunkt",
            "en_role": "Assistant professor",
            "photo": "img/team/natalia-sokol.jpg",
            "initials": "NS",
            "url": "https://pg.edu.pl/p/natalia-sokol-944955",
        },
        {
            "pl_name": "dr hab. inż. Maciej Tankiewicz",
            "en_name": "Prof. Maciej Tankiewicz",
            "pl_org": "Gdański Uniwersytet Medyczny",
            "en_org": "Medical University of Gdańsk",
            "pl_role": "Kierownik zespołu GUMed",
            "en_role": "GUMed team lead",
            "photo": "img/team/maciej-tankiewicz.jpg",
            "initials": "MT",
            "url": "https://informator.gumed.edu.pl/259",
        },
        {
            "pl_name": "Przemysław Kluz",
            "en_name": "Przemysław Kluz",
            "pl_org": "Gdańska Fundacja Innowacji Społecznych",
            "en_org": "Gdańsk Foundation for Social Innovation",
            "pl_role": "Dyrektor ds. organizacji społeczności lokalnej",
            "en_role": "Director for community organising",
            "photo": "img/team/przemyslaw-kluz.jpg",
            "initials": "PK",
            "url": "https://www.kongresobywatelski.pl/osoby/kluz-przemyslaw/",
        },
        {
            "pl_name": "dr inż. David Geisler-Moroder",
            "en_name": "Dr. David Geisler-Moroder",
            "pl_org": "Uniwersytet w Innsbrucku",
            "en_org": "Universität Innsbruck",
            "pl_role": "Pracownik naukowy",
            "en_role": "Research associate",
            "photo": "img/team/david-geisler-moroder.jpg",
            "initials": "DG",
            "url": "https://www.uibk.ac.at/en/energy-efficient-building/about-us/staff/david-geisler-moroder/",
        },
        {
            "pl_name": "dr inż. Nikodem Derengowski",
            "en_name": "Dr. Nikodem Derengowski",
            "pl_org": "Politechnika Gdańska",
            "en_org": "Gdańsk University of Technology",
            "pl_role": "Pracownik naukowy",
            "en_role": "Researcher",
            "photo": "img/team/nikodem-derengowski.jpg",
            "initials": "ND",
            "url": "https://orcid.org/0009-0001-9071-8010",
        },
        {
            "pl_name": "dr inż. arch. Roman Ruczyński",
            "en_name": "Dr. Roman Ruczyński",
            "pl_org": "Politechnika Gdańska",
            "en_org": "Gdańsk University of Technology",
            "pl_role": "",
            "en_role": "",
            "photo": "img/team/roman-ruczynski.jpg",
            "initials": "RR",
            "url": "https://pg.edu.pl/p/roman-ruczynski-8644",
        },
        {
            "pl_name": "dr hab. inż. arch. Izabela Mironowicz",
            "en_name": "Prof. Izabela Mironowicz",
            "pl_org": "Politechnika Gdańska",
            "en_org": "Gdańsk University of Technology",
            "pl_role": "",
            "en_role": "",
            "photo": "",
            "initials": "IM",
            "url": "https://pg.edu.pl/p/izabela-mironowicz-880097",
        },
        {
            "pl_name": "mgr inż. Anna Zackiewicz",
            "en_name": "Anna Zackiewicz",
            "pl_org": "Politechnika Gdańska",
            "en_org": "Gdańsk University of Technology",
            "pl_role": "",
            "en_role": "",
            "photo": "",
            "initials": "AZ",
            "url": "https://pg.edu.pl/p/anna-zackiewicz-1298558",
        },
        {
            "pl_name": "dr inż. Niko Gentile",
            "en_name": "Prof. Niko Gentile",
            "pl_org": "Uniwersytet w Lund",
            "en_org": "Lund University",
            "pl_role": "",
            "en_role": "",
            "photo": "",
            "initials": "NG",
            "url": "https://portal.research.lu.se/en/persons/niko-gentile/",
        },
        {
            "pl_name": "Natalia Lekner",
            "en_name": "Natalia Lekner",
            "pl_org": "Gmina Kartuzy",
            "en_org": "Municipality of Kartuzy",
            "pl_role": "",
            "en_role": "",
            "photo": "img/team/natalia-lekner.jpg",
            "initials": "NL",
            "url": "https://kartuzy.pl/",
        },
        {
            "pl_name": "dr hab. Anna Wojewnik-Filipkowska",
            "en_name": "Dr. Anna Wojewnik-Filipkowska",
            "pl_org": "Uniwersytet Gdański",
            "en_org": "University of Gdańsk",
            "pl_role": "",
            "en_role": "",
            "photo": "img/team/anna-wojewnik-filipkowska.jpg",
            "initials": "AW",
            "url": "https://sd.ug.edu.pl/node/791",
        },
        {
            "pl_name": "Ewa Patyk",
            "en_name": "Ewa Patyk",
            "pl_org": "Gdańska Fundacja Innowacji Społecznych",
            "en_org": "Gdańsk Foundation for Social Innovation",
            "pl_role": "",
            "en_role": "",
            "photo": "",
            "initials": "EP",
            "url": "https://gfis.pl/",
        },
        {
            "pl_name": "dr inż. Aleksandra Koszarek-Cyra",
            "en_name": "Dr. Aleksandra Koszarek-Cyra",
            "pl_org": "Uniwersytet Gdański",
            "en_org": "University of Gdańsk",
            "pl_role": "",
            "en_role": "",
            "photo": "img/team/aleksandra-koszarek-cyra.jpg",
            "initials": "AK",
            "url": "https://old.wzr.ug.edu.pl/wydzial/index.php?prac=845&str=121",
        },
        {
            "pl_name": "mgr inż. Aleksandra Szewczyk",
            "en_name": "Aleksandra Szewczyk",
            "pl_org": "Foton-OZE",
            "en_org": "Foton-OZE",
            "pl_role": "",
            "en_role": "",
            "photo": "img/team/aleksandra-szewczyk.jpg",
            "initials": "AS",
            "url": "https://foton-oze.pl/zespol/",
        },
        {
            "pl_name": "dr inż. arch. Weronika Maria Mazurkiewicz",
            "en_name": "Dr. Weronika Maria Mazurkiewicz",
            "pl_org": "Politechnika Gdańska",
            "en_org": "Gdańsk University of Technology",
            "pl_role": "",
            "en_role": "",
            "photo": "",
            "initials": "WM",
            "url": "https://pg.edu.pl/p/weronika-mazurkiewicz-163163",
        },
        {
            "pl_name": "dr hab. inż. arch. Karolina Krośnicka",
            "en_name": "Prof. Karolina Krośnicka",
            "pl_org": "Politechnika Gdańska",
            "en_org": "Gdańsk University of Technology",
            "pl_role": "",
            "en_role": "",
            "photo": "",
            "initials": "KK",
            "url": "https://pg.edu.pl/p/karolina-krosnicka-405355",
        },
        {
            "pl_name": "dr inż. arch. Barbara Zgórska",
            "en_name": "Dr. Barbara Zgórska",
            "pl_org": "Politechnika Gdańska",
            "en_org": "Gdańsk University of Technology",
            "pl_role": "",
            "en_role": "",
            "photo": "",
            "initials": "BZ",
            "url": "https://pg.edu.pl/p/barbara-zgorska-480266",
        },
        {
            "pl_name": "dr inż. Agnieszka Fiszka Borzyszkowska",
            "en_name": "Dr. Agnieszka Fiszka Borzyszkowska",
            "pl_org": "Gdański Uniwersytet Medyczny",
            "en_org": "Medical University of Gdańsk",
            "pl_role": "",
            "en_role": "",
            "photo": "img/team/agnieszka-fiszka-borzyszkowska.jpg?v=2",
            "initials": "AB",
            "url": "https://informator.gumed.edu.pl/259e",
        },
        {
            "pl_name": "Karol Niciejewski",
            "en_name": "Karol Niciejewski",
            "pl_org": "Gdański Uniwersytet Medyczny",
            "en_org": "Medical University of Gdańsk",
            "pl_role": "",
            "en_role": "",
            "photo": "img/team/karol-niciejewski.jpg?v=2",
            "initials": "KN",
            "url": "https://gumed.edu.pl/",
        },
        {
            "pl_name": "dr Gracja Topka-Bielecka",
            "en_name": "Dr. Gracja Topka-Bielecka",
            "pl_org": "Gdański Uniwersytet Medyczny",
            "en_org": "Medical University of Gdańsk",
            "pl_role": "",
            "en_role": "",
            "photo": "img/team/gracja-topka-bielecka.jpg?v=2",
            "initials": "GT",
            "url": "https://informator.gumed.edu.pl/259e",
        },
        {
            "pl_name": "dr Aleksandra Dydecka",
            "en_name": "Dr. Aleksandra Dydecka",
            "pl_org": "Gdański Uniwersytet Medyczny",
            "en_org": "Medical University of Gdańsk",
            "pl_role": "",
            "en_role": "",
            "photo": "img/team/aleksandra-dydecka.jpg?v=2",
            "initials": "AD",
            "url": "https://informator.gumed.edu.pl/259e",
        },
        {
            "pl_name": "dr Monika Cieszyńska-Semenowicz",
            "en_name": "Dr. Monika Cieszyńska-Semenowicz",
            "pl_org": "Gdański Uniwersytet Medyczny",
            "en_org": "Medical University of Gdańsk",
            "pl_role": "",
            "en_role": "",
            "photo": "img/team/monika-cieszynska-semenowicz.jpg?v=2",
            "initials": "MC",
            "url": "https://informator.gumed.edu.pl/259e",
        },
    ]


def team_rank(person):
    en = person["en_name"]
    if person.get("lead"):
        rank = -1
    elif en.startswith("Prof."):
        rank = 0
    elif en.startswith("Dr."):
        rank = 1
    else:
        rank = 2
    plain = en.removeprefix("Prof. ").removeprefix("Dr. ")
    # Kept together after the professors. Zackiewicz sits directly after Nikodem.
    pin = {
        "David Geisler-Moroder": 0,
        "Natalia Sokół": 1,
        "Roman Ruczyński": 2,
        "Nikodem Derengowski": 3,
        "Anna Zackiewicz": 4,
        "Anna Wojewnik-Filipkowska": 5,
    }
    if plain in pin:
        return (1, 0, pin[plain])
    surname = plain.split()[-1].casefold()
    return (rank, 1, surname)


def team_body(pl):
    items = []
    for person in sorted(team_members(), key=team_rank):
        name = person["pl_name"] if pl else person["en_name"]
        org = person["pl_org"] if pl else person["en_org"]
        role = (person["pl_role"] if pl else person["en_role"]) if person.get("lead") else ""
        role_html = f'<p class="role">{role}</p>' if role else ""
        photo = person.get("photo") or ""
        if photo:
            face = f'<img class="avatar" src="{asset(photo, 0 if pl else 1)}" alt="">'
        else:
            face = f'<span class="avatar" aria-hidden="true">{person["initials"]}</span>'
        title = name
        url = person.get("url") or ""
        if url:
            title = f'<a href="{url}">{name}</a>'
        items.append(
            f'<li class="team-card">{face}<div>'
            f'<h2>{title}</h2>'
            f'{role_html}'
            f'<p class="org">{org}</p></div></li>'
        )
    if pl:
        note = "Lista może się jeszcze powiększyć. Kolejne osoby dopiszemy razem ze zdjęciem i instytucją."
    else:
        note = "The list can still grow. Further people will be added with a photo and an organisation."
    return f'<ul class="team-list">{"".join(items)}</ul><p class="note">{note}</p>'



def contact_body(pl):
    if pl:
        return '''
<div class="contact-grid">
  <div>
    <p>Koordynacja projektu jest na Politechnice Gdańskiej. Zapraszamy do kontaktu samorządy, badaczy i instytucje zainteresowane współpracą.</p>
    <p>Formularza zgłoszeniowego nie ma. Taki formularz wymaga uzgodnienia z uczelnią zasad ochrony danych i obsługi wiadomości.</p>
    <h2>Laboratoria</h2>
    <p><a href="laboratorium-kartuzy.html">Kartuzy</a> · <a href="laboratorium-lund.html">Lund</a> · <a href="laboratorium-innsbruck.html">Innsbruck</a></p>
  </div>
  <aside class="panel">
    <h2>Koordynatorka</h2>
    <p>prof. dr hab. inż. arch. Justyna Martyniuk-Pęczek</p>
    <p>Politechnika Gdańska</p>
    <p><a href="mailto:juspecze@pg.edu.pl">juspecze@pg.edu.pl</a></p>
    <p>ul. Gabriela Narutowicza 11/12<br>80-233 Gdańsk</p>
  </aside>
</div>
'''
    return '''
<div class="contact-grid">
  <div>
    <p>The project is coordinated at Gdańsk University of Technology. Municipalities, researchers and other organisations are welcome to write.</p>
    <p>There is no message form. A form needs the university’s rules on personal data and how messages are handled.</p>
    <h2>Living labs</h2>
    <p><a href="lab-kartuzy.html">Kartuzy</a> · <a href="lab-lund.html">Lund</a> · <a href="lab-innsbruck.html">Innsbruck</a></p>
  </div>
  <aside class="panel">
    <h2>Coordinator</h2>
    <p>Prof. Justyna Martyniuk-Pęczek, PhD, DSc, Eng., Arch.</p>
    <p>Gdańsk University of Technology</p>
    <p><a href="mailto:juspecze@pg.edu.pl">juspecze@pg.edu.pl</a></p>
    <p>ul. Gabriela Narutowicza 11/12<br>80-233 Gdańsk, Poland</p>
  </aside>
</div>
'''


def search_body(pl):
    if pl:
        return '<div data-search-page><p>Wyszukiwanie obejmuje tytuły i skróty podstron oraz aktualności w tej wersji językowej.</p><div data-results></div></div>'
    return '<div data-search-page><p>Search covers titles and short descriptions of pages and news in this language.</p><div data-results></div></div>'


# Fix article image injection after we know depth
ARTICLE_KIND = {
    "spotkania": "spotkania",
    "badania": "badania",
    "warsztaty": "warsztaty",
    "narzedzia": "narzedzia",
}


def build_article(pl, kind, depth):
    html = article(pl, kind)
    img = {"spotkania": TALK, "badania": ILLU, "warsztaty": ILLU, "narzedzia": ILLU}[kind]
    return html.replace("IMGPLACE", media(img, depth))


def source_line(pl, href, title):
    label = "Źródło" if pl else "Source"
    return f'<p class="source">{label}: <a href="{href}" target="_blank" rel="noopener">{title}</a>, Wydział Architektury PG.</p>' if pl else f'<p class="source">{label}: <a href="{href}" target="_blank" rel="noopener">{title}</a>, Faculty of Architecture, Gdańsk Tech.</p>'


def real_article(key, pl, depth):
    if key == "lund":
        shots = []
        for path, cap_pl, cap_en in LUND_PHOTOS:
            cap = cap_pl if pl else cap_en
            shots.append(f'<figure class="figure"><img src="{asset(path, depth)}" alt="{cap}"><figcaption>{cap}</figcaption></figure>')
        gallery = f'<div class="gallery">{"".join(shots)}</div>'
        if pl:
            return f'''
<p class="kicker">27–30.09.2026 · Lund</p>
<p class="lead">27–30 września 2026 r. partnerzy projektu LIGHT spotkali się w Lund.</p>
<p>W programie były sesje robocze. Jedna z nich dotyczyła narzędzi DALEC. Partnerzy wyszli też w teren: odbył się lot dronem, rozmowa na dziedzińcu i spacer po mieście, między innymi przy przystanku Lund C.</p>
{gallery}
'''
        return f'''
<p class="kicker">27–30.09.2026 · Lund</p>
<p class="lead">On 27–30 September 2026 the LIGHT partners met in Lund.</p>
<p>The programme included working sessions. One of them presented the DALEC tools. The partners also went out into the city: there was a drone flight, a conversation in a courtyard and a walk, including the Lund C stop.</p>
{gallery}
'''
    if key == "martigny":
        img = asset("img/news/martigny.jpg", depth)
        if pl:
            return f'''
<p class="kicker">17.08.2026 · Badania</p>
<p class="lead">W ramach międzynarodowego projektu LIGHT, realizowanego w programie Driving Urban Transitions (DUT), Politechnika Gdańska we współpracy ze szwajcarskim Fondation de l’Institut de Recherche IDIAP przeprowadziła kompleksowe skanowanie miasta Martigny z wykorzystaniem dronów i technologii fotogrametrycznej. Zebrany materiał posłuży do stworzenia szczegółowego modelu 3D miasta.</p>
<figure class="figure"><img src="{img}" alt="Widok z nalotu nad Martigny"><figcaption>Nalot fotogrametryczny nad Martigny.</figcaption></figure>
<p>Projekt LIGHT, pod przewodnictwem dr hab. inż. arch. Justyny Martyniuk-Pęczek, prof. PG, koncentruje się na transformacji miast w kierunku pozytywnie energetycznych i zdrowych dzielnic. Prace związane ze skanowaniem Martigny za pomocą dronów przeprowadzili ze strony Politechniki Gdańskiej dr Roman Ruczyński oraz dr Nikodem Derengowski, którzy udali się do Szwajcarii, aby zrealizować misję pomiarową.</p>
<p>Powstały model 3D będzie wykorzystywany przez partnerów projektu do symulacji przepływów ciepła oraz innowacyjnych rozwiązań urbanistyczno-energetycznych w skali miasta, a także do stworzenia cyfrowego bliźniaka Martigny. Na Politechnice Gdańskiej model posłuży również do analiz nasłonecznienia i dostępu do światła dziennego.</p>
<p>Wykorzystanie wspólnego modelu 3D pozwoli partnerom projektu analizować różne aspekty funkcjonowania miasta oraz lepiej oceniać wpływ zmian urbanistycznych na środowisko i jakość życia mieszkańców.</p>
<p>Projekt LIGHT jest realizowany w latach 2026–2028 przez międzynarodowe konsorcjum partnerów z Polski, Szwecji, Austrii i Szwajcarii. Liderem projektu jest Politechnika Gdańska.</p>
<p>Projekt LIGHT – Poszukiwanie zintegrowanych rozwiązań dla zdrowych pozytywnych energetycznie dzielnic, realizowany w ramach Partnerstwa Driving Urban Transitions (DUT), współfinansowany przez Unię Europejską. Projekt uzyskał dofinansowanie od Narodowego Centrum Badań i Rozwoju (NCBR) w ramach konkursu DUT Call 2024.</p>
{source_line(True, SRC_MARTIGNY, "Drony i fotogrametria – cyfrowy model 3D miasta Martigny")}
'''
        return f'''
<p class="kicker">17.08.2026 · Fieldwork</p>
<p class="lead">Within the international LIGHT project, carried out in the Driving Urban Transitions (DUT) programme, Gdańsk Tech together with the Swiss Fondation de l’Institut de Recherche IDIAP scanned the city of Martigny with drones and photogrammetry. The material will be used to build a detailed 3D model of the city.</p>
<figure class="figure"><img src="{img}" alt="A view from the drone survey over Martigny"><figcaption>Photogrammetric flight over Martigny.</figcaption></figure>
<p>LIGHT, led by Justyna Martyniuk-Pęczek, PhD, DSc, Eng., Arch., Professor at Gdańsk Tech, works on the shift of cities towards healthy Positive Energy Districts. On the Gdańsk Tech side the drone survey of Martigny was carried out by Roman Ruczyński, PhD, and Nikodem Derengowski, PhD, who went to Switzerland for the measurement campaign.</p>
<p>Partners will use the 3D model for heat-flow simulations and innovative urban-energy solutions at city scale, and to build a digital twin of Martigny. At Gdańsk Tech the model will also support studies of sunlight and daylight.</p>
<p>A shared 3D model will let the partners examine different aspects of how the city works and judge more clearly how urban changes affect the environment and residents’ quality of life.</p>
<p>LIGHT runs from 2026 to 2028. An international consortium from Poland, Sweden, Austria and Switzerland carries it out, led by Gdańsk Tech.</p>
<p>LIGHT – Seeking integrated solutions for healthy Positive Energy Districts is carried out in the Driving Urban Transitions (DUT) partnership, co-funded by the European Union. The project received funding from the National Centre for Research and Development (NCBR) under DUT Call 2024.</p>
{source_line(False, SRC_MARTIGNY, "Drones and photogrammetry: a 3D model of Martigny")}
'''
    img = asset("img/news/inauguracja.jpg", depth)
    if pl:
        return f'''
<p class="kicker">10.02.2026 · Spotkania</p>
<p class="lead">10 lutego 2026 r. na Wydziale Architektury Politechniki Gdańskiej oficjalnie został zainaugurowany międzynarodowy projekt badawczo-wdrożeniowy LIGHT w ramach Partnerstwa Driving Urban Transitions (DUT), poświęcony transformacji energetycznej współczesnych dzielnic miejskich w kierunku tworzenia pozytywnych energetycznie dzielnic – PED (Positive Energy Districts), ze szczególnym naciskiem na zdrowie oraz jakość życia mieszkańców. Liderem projektu jest Politechnika Gdańska, reprezentowana przez prof. Justynę Martyniuk-Pęczek.</p>
<figure class="figure"><img src="{img}" alt="Inauguracja projektu LIGHT na Wydziale Architektury"><figcaption>Inauguracja projektu LIGHT, 10 lutego 2026 r.</figcaption></figure>
<p>Wydarzenie otworzył krótkim przemówieniem prof. dr hab. inż. Dariusz Mikielewicz – Prorektor ds. Nauki, następnie do gości zwrócił się prof. dr hab. inż. arch. Jakub Szczepański – Dziekan Wydziału Architektury oraz dr hab. inż. arch. Karolina Krośnicka, profesor PG – Prodziekan ds. Nauki oraz dr hab. inż. arch. Justyna Martyniuk-Pęczek, profesor PG.</p>
<p>Projekt LIGHT koncentruje się na kompleksowym podejściu do planowania i modernizacji istniejących oraz nowych obszarów miejskich. Łączy cele energetyczne, środowiskowe, przestrzenne, społeczne i mobilnościowe, traktując zdrowie mieszkańców jako fundament skutecznej transformacji. W ramach badań analizowany będzie m.in. potencjał zielono-niebieskiej infrastruktury w ograniczaniu efektu miejskiej wyspy ciepła, poprawa dostępu do światła dziennego w zagęszczonych obszarach, redukcja hałasu oraz poprawa jakości powietrza.</p>
<p>„Pozytywne energetycznie dzielnice, będące przedmiotem projektu LIGHT, to rozwiązania projektowane z myślą o zabezpieczeniu interesów lokalnych mieszkańców – szczególnie w obliczu wyjątkowych sytuacji, z jakimi mierzymy się dziś, takich jak kryzysy energetyczne czy nasilające się ekstremalne zjawiska klimatyczne. Wprowadzenie tych zmian wymaga jednak przeformułowania sposobu kształtowania struktury urbanistycznej oraz infrastruktury miejskiej, a przede wszystkim – akceptacji społecznej. Projekt LIGHT, poprzez zaproponowane rozwiązania, nie tylko wspiera transformację energetyczną, lecz także dostarcza realnych argumentów na to, że może ona przyczyniać się do poprawy zdrowia i jakości życia mieszkańców, stając się dźwignią koniecznych zmian.”</p>
<p>Jednym z kluczowych elementów projektu będzie stworzenie trzech Urban Living Labs (ULLs), w których testowane i porównywane będą różne ścieżki transformacji energetycznej miast.</p>
<ul>
  <li>Kartuzy staną się laboratorium renowacji energetycznej budynków oraz integracji zielono-niebieskiej infrastruktury,</li>
  <li>Lund (Szwecja) skupi się na zagęszczaniu zabudowy i neutralnym klimatycznie wytwarzaniu energii,</li>
  <li>Innsbruck (Austria) rozwinie wirtualne laboratorium (vULL), wykorzystujące projektowanie parametryczne do analizy scenariuszy urbanistycznych.</li>
</ul>
<p>Efektem projektu będzie zestaw narzędzi, wytycznych i modeli symulacyjnych dla tzw. zdrowych dzielnic PED (Positive Energy Districts), które będzie można wdrażać i powielać w różnych kontekstach miejskich w całej Europie.</p>
<p>W realizację projektu zaangażowane są liczne instytucje naukowe, samorządowe oraz biznesowe. Polskimi partnerami są: Politechnika Gdańska, Gdański Uniwersytet Medyczny, Uniwersytet Gdański, Gdańska Fundacja Innowacji Społecznej oraz Gmina Kartuzy – Urząd Miejski w Kartuzach. Międzynarodowe konsorcjum tworzą również partnerzy ze Szwecji, Austrii i Szwajcarii, w tym m.in. Universität Innsbruck, Lunds Universitet, Lunds Kommun oraz Fondation de l’Institut de Recherche IDIAP, a także renomowana na świecie firma architektoniczno-urbanistyczna White Arkitekter.</p>
<p>Projekt LIGHT realizowany będzie w latach 2026–2028. Już podczas spotkania inauguracyjnego zaplanowano pierwszą rundę dyskusji z udziałem partnerów, a kolejne spotkania – również w formule online – posłużą wypracowaniu wspólnych rozwiązań, identyfikacji wyzwań i dalszemu doprecyzowaniu kierunków badań.</p>
<p>Inicjatywa stanowi ważny krok w umacnianiu międzynarodowej współpracy Politechniki Gdańskiej oraz rozwoju innowacyjnych „żywych laboratoriów miejskich”, które mają realnie wspierać zrównoważoną transformację europejskich miast w kierunku tworzenia pozytywnie energetycznych dzielnic.</p>
<p>Projekt realizowany w ramach Partnerstwa Driving Urban Transitions (DUT) współfinansowanego przez Unię Europejską. Projekt uzyskał dofinansowanie od Narodowego Centrum Badań i Rozwoju (NCBR) w ramach konkursu DUT Call 2024.</p>
<p>Wartość projektu (całkowita): 5&nbsp;399&nbsp;394,98&nbsp;PLN / 1&nbsp;263&nbsp;016,37&nbsp;EUR. Wartość dofinansowania z NCBR: 2&nbsp;029&nbsp;556,22&nbsp;PLN, decyzja nr DWM/DUT/8/2026. Okres realizacji: 01.01.2026 r. – 31.12.2028 r.</p>
{source_line(True, SRC_LIGHT, "PG inauguruje międzynarodowy projekt LIGHT")}
'''
    return f'''
<p class="kicker">10.02.2026 · Meetings</p>
<p class="lead">On 10 February 2026 the Faculty of Architecture at Gdańsk Tech officially launched the international research and implementation project LIGHT, within the Driving Urban Transitions (DUT) partnership. It works on the energy transition of urban districts towards Positive Energy Districts (PEDs), with a particular emphasis on residents’ health and quality of life. Gdańsk Tech leads the project, represented by Prof. Justyna Martyniuk-Pęczek.</p>
<figure class="figure"><img src="{img}" alt="The LIGHT project launch at the Faculty of Architecture"><figcaption>Launch of the LIGHT project, 10 February 2026.</figcaption></figure>
<p>Prof. Dariusz Mikielewicz, PhD, DSc, Eng., Vice-Rector for Research, opened the event with a short address. The guests were then addressed by Prof. Jakub Szczepański, PhD, DSc, Eng., Arch., Dean of the Faculty of Architecture, by Karolina Krośnicka, PhD, DSc, Eng., Arch., Professor at Gdańsk Tech and Vice-Dean for Research, and by Justyna Martyniuk-Pęczek, PhD, DSc, Eng., Arch., Professor at Gdańsk Tech.</p>
<p>LIGHT takes a comprehensive approach to planning and upgrading existing and new urban areas. It joins energy, environmental, spatial, social and mobility goals, and treats residents’ health as the basis of an effective transition. The research will examine, among other things, the potential of blue-green infrastructure to limit the urban heat island, better access to daylight in denser areas, noise reduction and air quality.</p>
<p>“Positive Energy Districts, the subject of LIGHT, are solutions designed to protect the interests of local residents — especially in the exceptional situations we face today, such as energy crises and increasingly extreme weather. Introducing these changes does, however, require a different way of shaping urban structure and infrastructure, and above all public acceptance. Through the solutions it proposes, LIGHT not only supports the energy transition. It also offers concrete arguments that the transition can improve residents’ health and quality of life, and so become a lever for the changes that are needed.”</p>
<p>A central part of the project will be three Urban Living Labs (ULLs), where different paths of urban energy transition will be tested and compared.</p>
<ul>
  <li>Kartuzy will become a lab for energy renovation of buildings and the integration of blue-green infrastructure,</li>
  <li>Lund, Sweden, will focus on densification and climate-neutral energy generation,</li>
  <li>Innsbruck, Austria, will develop a virtual lab (vULL), using parametric design to study urban scenarios.</li>
</ul>
<p>The project will leave a set of tools, guidelines and simulation models for healthy Positive Energy Districts, which can be applied and repeated in different urban contexts across Europe.</p>
<p>Research institutions, local authorities and businesses are taking part. The Polish partners are Gdańsk Tech, the Medical University of Gdańsk, the University of Gdańsk, the Gdańsk Foundation for Social Innovation and the Municipality of Kartuzy. The international consortium also includes partners from Sweden, Austria and Switzerland, among them Universität Innsbruck, Lund University, Lund Municipality and the Fondation de l’Institut de Recherche IDIAP, as well as the architecture and urban design practice White Arkitekter.</p>
<p>LIGHT will run from 2026 to 2028. The launch meeting already set a first round of discussion with the partners. Further meetings, including online, will be used to work out shared solutions, identify challenges and sharpen the research directions.</p>
<p>The initiative is a step in strengthening Gdańsk Tech’s international cooperation and in developing urban living labs that can support a sustainable transition of European cities towards Positive Energy Districts.</p>
<p>The project is carried out within the Driving Urban Transitions (DUT) partnership, co-funded by the European Union. It received funding from the National Centre for Research and Development (NCBR) under DUT Call 2024.</p>
<p>Total project value: PLN 5,399,394.98 / EUR 1,263,016.37. NCBR funding: PLN 2,029,556.22, decision no. DWM/DUT/8/2026. Duration: 1 January 2026 – 31 December 2028.</p>
{source_line(False, SRC_LIGHT, "Gdańsk Tech launches the international LIGHT project")}
'''


# labs_body for EN uses relative lab-*.html because those pages live in en/
# Polish labs_body uses paths from prototyp root. When called, links are not passed through link()
# Polish page depth 0 so "laboratorium-kartuzy.html" works.
# English page is en/living-labs.html depth 1, and lab pages are en/lab-kartuzy.html.
# labs_body EN links "lab-kartuzy.html" which is correct relative to en/.
# lab pages EN related news "news/fieldwork.html" is correct relative to en/.
# Polish lab related "aktualnosci/badania.html" correct at depth 0.
# results EN link "downloads.html" correct in en/.
# files don't need cross links.
# news list uses link(url, d) with full site paths. Good.
# article pages don't include cross-folder mistakes except we build images with depth.

SIDE_PL_ABOUT = [
    ("Wyzwania", "o-projekcie.html#wyzwania", "w"),
    ("Rozwiązanie", "o-projekcie.html#rozwiazanie", "r"),
    ("Dane projektu", "o-projekcie.html#dane", "d"),
    ("Zasady", "o-projekcie.html#zasady", "z"),
]
SIDE_EN_ABOUT = [
    ("Challenges", "en/about.html#challenges", "w"),
    ("Solution", "en/about.html#solution", "r"),
    ("Project data", "en/about.html#facts", "d"),
    ("Principles", "en/about.html#principles", "z"),
]
SIDE_PL_LABS = [
    ("Wszystkie", "laboratoria.html", "all"),
    ("Kartuzy", "laboratorium-kartuzy.html", "k"),
    ("Lund", "laboratorium-lund.html", "l"),
    ("Innsbruck", "laboratorium-innsbruck.html", "i"),
]
SIDE_EN_LABS = [
    ("All labs", "en/living-labs.html", "all"),
    ("Kartuzy", "en/lab-kartuzy.html", "k"),
    ("Lund", "en/lab-lund.html", "l"),
    ("Innsbruck", "en/lab-innsbruck.html", "i"),
]
SIDE_PL_RES = [
    ("Rezultaty", "rezultaty.html", "r"),
    ("Do pobrania", "do-pobrania.html", "f"),
]
SIDE_EN_RES = [
    ("Results", "en/results.html", "r"),
    ("Downloads", "en/downloads.html", "f"),
]


def page(**kwargs):
    add(kwargs)


# Register pages
page(id="home-pl", file="index.html", depth=0, lang="pl", nav="", home=True,
     title="LIGHT | Politechnika Gdańska", h1="LIGHT",
     desc="LIGHT – zdrowe dzielnice dodatnie energetycznie. Projekt Politechniki Gdańskiej w programie Driving Urban Transitions.",
     pl="index.html", alt="en/index.html", body=home_pl())

page(id="about-pl", file="o-projekcie.html", depth=0, lang="pl", nav="about",
     title="O projekcie | LIGHT", h1="O projekcie",
     desc="Cele, wyzwania i dane projektu LIGHT.",
     pl="o-projekcie.html", alt="en/about.html",
     crumbs=[("O projekcie", "")],
     side=SIDE_PL_ABOUT, side_title="O projekcie", side_current="",
     body=about_body(True, 0))

page(id="labs-pl", file="laboratoria.html", depth=0, lang="pl", nav="labs",
     title="Laboratoria miejskie | LIGHT", h1="Laboratoria miejskie",
     desc="Kartuzy, Lund i wirtualne laboratorium w Innsbrucku.",
     pl="laboratoria.html", alt="en/living-labs.html",
     crumbs=[("Laboratoria", "")],
     side=SIDE_PL_LABS, side_title="Laboratoria", side_current="all",
     body=labs_body(True, 0))

for pid, file, h1, key, body, alt in [
    ("k-pl", "laboratorium-kartuzy.html", "Kartuzy", "k", lab_kartuzy(True, 0), "en/lab-kartuzy.html"),
    ("l-pl", "laboratorium-lund.html", "Lund", "l", lab_lund(True, 0), "en/lab-lund.html"),
    ("i-pl", "laboratorium-innsbruck.html", "Innsbruck", "i", lab_inns(True, 0), "en/lab-innsbruck.html"),
]:
    page(id=pid, file=file, depth=0, lang="pl", nav="labs",
         title=f"{h1} | LIGHT", h1=h1,
         desc=f"Laboratorium miejskie LIGHT: {h1}.",
         pl=file, alt=alt,
         crumbs=[("Laboratoria", "laboratoria.html"), (h1, "")],
         side=SIDE_PL_LABS, side_title="Laboratoria", side_current=key,
         body=body)

page(id="news-pl", file="aktualnosci.html", depth=0, lang="pl", nav="news",
     title="Aktualności | LIGHT", h1="Aktualności",
     desc="Relacje z życia projektu LIGHT.",
     pl="aktualnosci.html", alt="en/news.html",
     crumbs=[("Aktualności", "")],
     body=news_list(True, 0))

articles_pl = [
    ("a1", "aktualnosci/spotkania.html", "Relacje ze spotkań konsorcjum", "spotkania", "en/news/meetings.html"),
    ("a2", "aktualnosci/badania.html", "Badania w terenie i wizyty studyjne", "badania", "en/news/fieldwork.html"),
    ("a3", "aktualnosci/warsztaty.html", "Warsztaty i udział mieszkańców", "warsztaty", "en/news/workshops.html"),
    ("a4", "aktualnosci/narzedzia.html", "Postępy prac nad narzędziami cyfrowymi", "narzedzia", "en/news/tools.html"),
]
for pid, file, h1, kind, alt in articles_pl:
    page(id=pid, file=file, depth=1, lang="pl", nav="news",
         title=f"{h1} | LIGHT", h1=h1,
         desc=h1,
         pl=file, alt=alt,
         crumbs=[("Aktualności", "aktualnosci.html"), (h1, "")],
         body=build_article(True, kind, 1))

for item in REAL_NEWS:
    s, e = item["pl"], item["en"]
    page(id=item["id"] + "-pl", file=s["file"], depth=1, lang="pl", nav="news",
         title=f'{s["title"]} | LIGHT', h1=s["title"],
         desc=s["lead"],
         pl=s["file"], alt=e["file"],
         crumbs=[("Aktualności", "aktualnosci.html"), (s["title"], "")],
         body=real_article(item["id"], True, 1))

page(id="res-pl", file="rezultaty.html", depth=0, lang="pl", nav="results",
     title="Rezultaty | LIGHT", h1="Rezultaty i narzędzia",
     desc="Planowane rezultaty projektu LIGHT.",
     pl="rezultaty.html", alt="en/results.html",
     crumbs=[("Rezultaty", "")],
     side=SIDE_PL_RES, side_title="Rezultaty", side_current="r",
     body=results_body(True))

page(id="files-pl", file="do-pobrania.html", depth=0, lang="pl", nav="files",
     title="Do pobrania | LIGHT", h1="Do pobrania",
     desc="Biblioteka materiałów projektu LIGHT.",
     pl="do-pobrania.html", alt="en/downloads.html",
     crumbs=[("Do pobrania", "")],
     side=SIDE_PL_RES, side_title="Rezultaty", side_current="f",
     body=files_body(True))

page(id="par-pl", file="partnerzy.html", depth=0, lang="pl", nav="partners",
     title="Partnerzy | LIGHT", h1="Partnerzy",
     desc="Konsorcjum projektu LIGHT.",
     pl="partnerzy.html", alt="en/partners.html",
     crumbs=[("Partnerzy", "")],
     body=partners_body(True))

page(id="team-pl", file="zespol.html", depth=0, lang="pl", nav="team",
     title="Zespół | LIGHT", h1="Zespół",
     desc="Osoby w projekcie LIGHT: rola i instytucja.",
     pl="zespol.html", alt="en/team.html",
     crumbs=[("Zespół", "")],
     body=team_body(True))

page(id="con-pl", file="kontakt.html", depth=0, lang="pl", nav="contact",
     title="Kontakt | LIGHT", h1="Kontakt",
     desc="Kontakt do koordynacji projektu LIGHT na Politechnice Gdańskiej.",
     pl="kontakt.html", alt="en/contact.html",
     crumbs=[("Kontakt", "")],
     body=contact_body(True))

page(id="search-pl", file="szukaj.html", depth=0, lang="pl", nav="",
     title="Szukaj | LIGHT", h1="Szukaj",
     desc="Wyszukiwarka prototypu LIGHT.",
     pl="szukaj.html", alt="en/search.html",
     crumbs=[("Szukaj", "")],
     body=search_body(True))


def home_en():
    d = 1
    graphic = media(PATHWAY, d)
    return f'''
<section class="hero">
  <div class="hero-media"><img src="{graphic}" alt="Main Transition Pathway: Positive Energy Districts, with sun, buildings, turbines and greenery"></div>
  <div class="wrap hero-copy" id="tresc">
    <p class="eyebrow">Driving Urban Transitions · Positive Energy Districts</p>
    <h1>LIGHT</h1>
    <p class="subtitle">Looking for Integrated Solutions for Healthy PEDs</p>
    <p class="lead">Healthy, energy-efficient districts that work for the people who live there. The project joins the energy transition with daylight, comfort and health.</p>
    <p><a class="more" href="about.html">About the project</a></p>
  </div>
</section>
<section class="section">
  <div class="wrap prose">
    <h2>Why healthy energy districts?</h2>
    <p>Denser cities often lose daylight and quality of life. LIGHT treats residents’ health as part of planning Positive Energy Districts, together with energy, blue-green infrastructure and mobility.</p>
    <p><a href="about.html">Challenges and the proposal</a></p>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="section-head"><h2>Three living labs</h2><a href="living-labs.html">More</a></div>
    {europe_map([
        ("lab-lund.html", "Lund", 365.9, 265.5, 380, 252),
        ("lab-kartuzy.html", "Kartuzy", 432.7, 285.8, 446, 278),
        ("lab-innsbruck.html", "Innsbruck", 341.8, 390.4, 356, 378),
    ], "Map of Europe with the three LIGHT living labs", "Choose a dot: Lund, Kartuzy or Innsbruck.")}
    {lab_cards(False, d)}
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="section-head"><h2>News</h2><a href="news.html">More</a></div>
    {home_news(False, d)}
  </div>
</section>
<section class="section soft">
  <div class="wrap">
    <div class="section-head"><h2>What will be produced</h2><a href="results.html">Results</a></div>
    <div class="cards">
      <a class="card" href="results.html"><h3>LIGHT Guidelines</h3><p>Practical advice for integrated urban planning.</p></a>
      <a class="card" href="results.html"><h3>CitySim and DALEC</h3><p>Open extensions for energy, daylight and comfort.</p></a>
      <a class="card" href="downloads.html"><h3>Downloads</h3><p>Reports, slides and documentation as they are published.</p></a>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Partners</h2><a href="partners.html">The consortium</a></div>
    <p>11 organisations in Poland, Austria, Sweden and Switzerland. Coordinated by Gdańsk University of Technology.</p>
    {partner_logos(False)}
  </div>
</section>
'''

page(id="home-en", file="en/index.html", depth=1, lang="en", nav="", home=True,
     title="LIGHT | Gdańsk University of Technology", h1="LIGHT",
     desc="LIGHT – healthy Positive Energy Districts. A Gdańsk Tech project in Driving Urban Transitions.",
     pl="index.html", alt="en/index.html", body=home_en())

page(id="about-en", file="en/about.html", depth=1, lang="en", nav="about",
     title="About | LIGHT", h1="About the project",
     desc="Aims, challenges and facts for LIGHT.",
     pl="o-projekcie.html", alt="en/about.html",
     crumbs=[("About", "")],
     side=SIDE_EN_ABOUT, side_title="About", side_current="",
     body=about_body(False, 1))

page(id="labs-en", file="en/living-labs.html", depth=1, lang="en", nav="labs",
     title="Living labs | LIGHT", h1="Living labs",
     desc="Kartuzy, Lund and the virtual lab in Innsbruck.",
     pl="laboratoria.html", alt="en/living-labs.html",
     crumbs=[("Living labs", "")],
     side=SIDE_EN_LABS, side_title="Living labs", side_current="all",
     body=labs_body(False, 1))

for pid, file, h1, key, body, plink in [
    ("k-en", "en/lab-kartuzy.html", "Kartuzy", "k", lab_kartuzy(False, 1), "laboratorium-kartuzy.html"),
    ("l-en", "en/lab-lund.html", "Lund", "l", lab_lund(False, 1), "laboratorium-lund.html"),
    ("i-en", "en/lab-innsbruck.html", "Innsbruck", "i", lab_inns(False, 1), "laboratorium-innsbruck.html"),
]:
    page(id=pid, file=file, depth=1, lang="en", nav="labs",
         title=f"{h1} | LIGHT", h1=h1,
         desc=f"LIGHT living lab: {h1}.",
         pl=plink, alt=file,
         crumbs=[("Living labs", "en/living-labs.html"), (h1, "")],
         side=SIDE_EN_LABS, side_title="Living labs", side_current=key,
         body=body)

page(id="news-en", file="en/news.html", depth=1, lang="en", nav="news",
     title="News | LIGHT", h1="News",
     desc="News from the LIGHT project.",
     pl="aktualnosci.html", alt="en/news.html",
     crumbs=[("News", "")],
     body=news_list(False, 1))

articles_en = [
    ("b1", "en/news/meetings.html", "Consortium meetings", "spotkania", "aktualnosci/spotkania.html"),
    ("b2", "en/news/fieldwork.html", "Fieldwork and study visits", "badania", "aktualnosci/badania.html"),
    ("b3", "en/news/workshops.html", "Workshops and residents", "warsztaty", "aktualnosci/warsztaty.html"),
    ("b4", "en/news/tools.html", "Progress on the digital tools", "narzedzia", "aktualnosci/narzedzia.html"),
]
for pid, file, h1, kind, plink in articles_en:
    page(id=pid, file=file, depth=2, lang="en", nav="news",
         title=f"{h1} | LIGHT", h1=h1,
         desc=h1,
         pl=plink, alt=file,
         crumbs=[("News", "en/news.html"), (h1, "")],
         body=build_article(False, kind, 2))

for item in REAL_NEWS:
    s, e = item["pl"], item["en"]
    page(id=item["id"] + "-en", file=e["file"], depth=2, lang="en", nav="news",
         title=f'{e["title"]} | LIGHT', h1=e["title"],
         desc=e["lead"],
         pl=s["file"], alt=e["file"],
         crumbs=[("News", "en/news.html"), (e["title"], "")],
         body=real_article(item["id"], False, 2))

page(id="res-en", file="en/results.html", depth=1, lang="en", nav="results",
     title="Results | LIGHT", h1="Results and tools",
     desc="Planned results of LIGHT.",
     pl="rezultaty.html", alt="en/results.html",
     crumbs=[("Results", "")],
     side=SIDE_EN_RES, side_title="Results", side_current="r",
     body=results_body(False))

page(id="files-en", file="en/downloads.html", depth=1, lang="en", nav="files",
     title="Downloads | LIGHT", h1="Downloads",
     desc="LIGHT materials library.",
     pl="do-pobrania.html", alt="en/downloads.html",
     crumbs=[("Downloads", "")],
     side=SIDE_EN_RES, side_title="Results", side_current="f",
     body=files_body(False))

page(id="par-en", file="en/partners.html", depth=1, lang="en", nav="partners",
     title="Partners | LIGHT", h1="Partners",
     desc="The LIGHT consortium.",
     pl="partnerzy.html", alt="en/partners.html",
     crumbs=[("Partners", "")],
     body=partners_body(False))

page(id="team-en", file="en/team.html", depth=1, lang="en", nav="team",
     title="Team | LIGHT", h1="Team",
     desc="People in the LIGHT project: role and organisation.",
     pl="zespol.html", alt="en/team.html",
     crumbs=[("Team", "")],
     body=team_body(False))

page(id="con-en", file="en/contact.html", depth=1, lang="en", nav="contact",
     title="Contact | LIGHT", h1="Contact",
     desc="Contact the LIGHT coordination at Gdańsk University of Technology.",
     pl="kontakt.html", alt="en/contact.html",
     crumbs=[("Contact", "")],
     body=contact_body(False))

page(id="search-en", file="en/search.html", depth=1, lang="en", nav="",
     title="Search | LIGHT", h1="Search",
     desc="Search this LIGHT prototype.",
     pl="szukaj.html", alt="en/search.html",
     crumbs=[("Search", "")],
     body=search_body(False))


INDEX = [
    ("pl", "LIGHT", "Strona główna projektu", "index.html"),
    ("pl", "O projekcie", "Wyzwania, rozwiązanie, dane, budżet, czas trwania", "o-projekcie.html"),
    ("pl", "Laboratoria miejskie", "Kartuzy Lund Innsbruck", "laboratoria.html"),
    ("pl", "Kartuzy", "Renowacja energetyczna błękitno-zielona infrastruktura", "laboratorium-kartuzy.html"),
    ("pl", "Lund", "Zagęszczanie energia rozwiązania bezemisyjne", "laboratorium-lund.html"),
    ("pl", "Innsbruck", "Wirtualne laboratorium światło dzienne hałas powietrze", "laboratorium-innsbruck.html"),
    ("pl", "Aktualności", "Spotkania badania warsztaty rezultaty Lund Martigny inauguracja", "aktualnosci.html"),
    ("pl", "Spotkanie konsorcjum w Lund", "27–30 września 2026 DALEC Lund", "aktualnosci/lund.html"),
    ("pl", "Drony i model 3D Martigny", "fotogrametria IDIAP Roman Ruczyński Nikodem Derengowski", "aktualnosci/martigny.html"),
    ("pl", "PG inauguruje projekt LIGHT", "10 lutego 2026 inauguracja Wydział Architektury Mikielewicz Szczepański Krośnicka NCBR DUT", "aktualnosci/inauguracja.html"),
    ("pl", "Relacje ze spotkań konsorcjum", "Przykładowy wpis spotkania partnerzy", "aktualnosci/spotkania.html"),
    ("pl", "Badania w terenie i wizyty studyjne", "Przykładowy wpis Kartuzy Lund", "aktualnosci/badania.html"),
    ("pl", "Warsztaty i udział mieszkańców", "Przykładowy wpis samorząd społeczność", "aktualnosci/warsztaty.html"),
    ("pl", "Postępy prac nad narzędziami cyfrowymi", "CitySim DALEC światło komfort", "aktualnosci/narzedzia.html"),
    ("pl", "Rezultaty i narzędzia", "Wytyczne CitySim DALEC oś czasu", "rezultaty.html"),
    ("pl", "Do pobrania", "Raporty wytyczne prezentacje materiały", "do-pobrania.html"),
    ("pl", "Partnerzy", "Konsorcjum Politechnika Gdańska Idiap Lund Innsbruck", "partnerzy.html"),
    ("pl", "Zespół", "Justyna Martyniuk-Pęczek Dubon Rodrigue Marie-Claude Dubois Jérôme Kämpf Olga Martyniuk Natalia Sokół Maciej Tankiewicz Przemysław Kluz David Geisler-Moroder Nikodem Derengowski Roman Ruczyński Izabela Mironowicz Anna Zackiewicz Niko Gentile Natalia Lekner Anna Wojewnik-Filipkowska Ewa Patyk Aleksandra Koszarek-Cyra Aleksandra Szewczyk Weronika Maria Mazurkiewicz Karolina Krośnicka Barbara Zgórska Agnieszka Fiszka Borzyszkowska Karol Niciejewski Gracja Topka-Bielecka Aleksandra Dydecka Monika Cieszyńska-Semenowicz", "zespol.html"),
    ("pl", "Kontakt", "Justyna Martyniuk-Pęczek juspecze@pg.edu.pl", "kontakt.html"),
    ("en", "LIGHT", "Project home", "en/index.html"),
    ("en", "About the project", "Challenges solution facts budget duration", "en/about.html"),
    ("en", "Living labs", "Kartuzy Lund Innsbruck", "en/living-labs.html"),
    ("en", "Kartuzy", "Energy renovation blue-green infrastructure", "en/lab-kartuzy.html"),
    ("en", "Lund", "Densification energy zero-emission", "en/lab-lund.html"),
    ("en", "Innsbruck", "Virtual living lab daylight noise air", "en/lab-innsbruck.html"),
    ("en", "News", "Meetings fieldwork workshops results Lund Martigny launch", "en/news.html"),
    ("en", "Consortium meeting in Lund", "27–30 September 2026 DALEC Lund", "en/news/lund.html"),
    ("en", "Drones and a 3D model of Martigny", "photogrammetry Idiap Roman Ruczyński Nikodem Derengowski", "en/news/martigny.html"),
    ("en", "Gdańsk Tech launches LIGHT", "10 February 2026 inauguration Faculty of Architecture Mikielewicz Szczepański Krośnicka NCBR DUT", "en/news/inauguration.html"),
    ("en", "Consortium meetings", "Sample story partners", "en/news/meetings.html"),
    ("en", "Fieldwork and study visits", "Sample story Kartuzy Lund", "en/news/fieldwork.html"),
    ("en", "Workshops and residents", "Sample story community", "en/news/workshops.html"),
    ("en", "Progress on the digital tools", "CitySim DALEC daylight comfort", "en/news/tools.html"),
    ("en", "Results and tools", "Guidelines CitySim DALEC timeline", "en/results.html"),
    ("en", "Downloads", "Reports guidelines slides graphics", "en/downloads.html"),
    ("en", "Partners", "Consortium Gdańsk Tech Idiap Lund Innsbruck", "en/partners.html"),
    ("en", "Team", "Justyna Martyniuk-Pęczek Dubon Rodrigue Marie-Claude Dubois Jérôme Kämpf Olga Martyniuk Natalia Sokół Maciej Tankiewicz Przemysław Kluz David Geisler-Moroder Nikodem Derengowski Roman Ruczyński Izabela Mironowicz Anna Zackiewicz Niko Gentile Natalia Lekner Anna Wojewnik-Filipkowska Ewa Patyk Aleksandra Koszarek-Cyra Aleksandra Szewczyk Weronika Maria Mazurkiewicz Karolina Krośnicka Barbara Zgórska Agnieszka Fiszka Borzyszkowska Karol Niciejewski Gracja Topka-Bielecka Aleksandra Dydecka Monika Cieszyńska-Semenowicz", "en/team.html"),
    ("en", "Contact", "Justyna Martyniuk-Pęczek juspecze@pg.edu.pl", "en/contact.html"),
]


def main():
    # screen reader helper
    css_extra = (ROOT / "css" / "style.css").read_text()
    if ".sr{" not in css_extra and ".sr {" not in css_extra:
        css_extra += "\n.sr{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);border:0;}\n"
        (ROOT / "css" / "style.css").write_text(css_extra)
    for p in PAGES:
        html = chrome(p)
        path = ROOT / p["file"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html, encoding="utf-8")
        print(p["file"])
    data = [{"lang": a, "title": b, "text": c, "url": d} for a, b, c, d in INDEX]
    (ROOT / "js" / "search-index.js").write_text(
        "window.LIGHT_INDEX = " + json.dumps(data, ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )
    print(len(PAGES), "pages")


if __name__ == "__main__":
    main()
