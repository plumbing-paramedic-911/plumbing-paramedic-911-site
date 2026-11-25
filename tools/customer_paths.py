"""Build the no-water landing page and link it from existing well pages."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = "/no-water-from-well/"
TITLE = "No Water From Your Well? | Plumbing Paramedic 911"
DESCRIPTION = (
    "No water from your private well in Upstate South Carolina? Use our free checklist "
    "and request well pump service in Abbeville, McCormick, Iva and Lake Secession."
)
WELL_PAGES = (
    "services/well-pump-repair/index.html",
    "well-pump-repair-mccormick-sc/index.html",
    "well-pump-repair-iva-lake-secession-sc/index.html",
)


def render(build):
    crumbs = [("Home", "/"), ("No Water From Your Well", PATH)]
    page = {
        "@type": "WebPage",
        "@id": build.BASE_URL + PATH + "#webpage",
        "url": build.BASE_URL + PATH,
        "name": TITLE,
        "description": DESCRIPTION,
        "inLanguage": "en-US",
        "isPartOf": {"@id": build.WEBSITE_ID},
        "publisher": {"@id": build.LOCALBUSINESS_ID},
    }
    return (
        build.head(TITLE, DESCRIPTION, PATH, extra_jsonld=[
            *build.business_ld(), page, build.breadcrumb_ld(crumbs),
        ], body_page="well-no-water").replace(
            "</head>", "<noscript><style>#wellNoWaterForm{display:none}</style></noscript>\n</head>",
        )
        + build.nav()
        + f'''<main id="well-help">
  <section class="service-hero">
    <div class="container">
      <nav class="breadcrumb" aria-label="Breadcrumb">{build.breadcrumb_html(crumbs)}</nav>
      <h1 class="speakable-headline">No water from your well?</h1>
      <p class="speakable-summary">Get your next step for a private well that has lost pressure or stopped delivering water. We serve Abbeville, McCormick, Iva, Lake Secession, and nearby Upstate South Carolina communities.</p>
      <a class="btn btn-green btn-lg" href="#request-well-service" data-customer-path="well_request_start">Request well pump service</a>
    </div>
  </section>
  <section class="section-sm">
    <div class="container grid-2 well-help-grid">
      <article class="card" id="well-checklist" aria-labelledby="well-checklist-title">
        <h2 id="well-checklist-title">Free no-water checklist</h2>
        <ol>
          <li><strong>Check another cold-water faucet.</strong> Note whether one fixture or the whole house has lost water.</li>
          <li><strong>Write down when it started.</strong> Tell us whether the water stopped suddenly, faded to a trickle, or came back and cut off again.</li>
          <li><strong>Note what happened beforehand.</strong> An outage, storm, or heavy water use can give the technician a starting point.</li>
          <li><strong>Tell us what you know about your well.</strong> A previous invoice or well record may list the pump type, depth, or age.</li>
        </ol>
        <p>Use observations from a dry, accessible spot. Leave electrical covers and well equipment closed.</p>
        <button id="print-well-checklist" class="btn btn-blue btn-sm" type="button" hidden>Print checklist</button>
        <p class="well-checklist-link"><a href="/guides/well-pump-owners-manual-upstate-sc/" data-customer-path="well_owners_manual">Read about the Well Pump Owner’s Manual</a></p>
      </article>
      <article class="card" id="request-well-service" aria-labelledby="well-request-title">
        <h2 id="well-request-title">Request well pump service</h2>
        <p>A technician can check the pump, pressure tank, controls, and water line to find where the problem starts. If you need immediate help, call <a href="tel:+18644468911">(864) 446-8911</a>.</p>
        <p>Service calls are $79 Monday–Friday, 9 AM–5 PM, $99 after hours and on weekends, and $158 after midnight or on holidays. We quote repairs separately for approval before work begins.</p>
        <form class="lead-form" id="wellNoWaterForm" method="post" action="#request-well-service">
          <div class="form-success" role="status">Request received. The office will contact you to confirm availability.</div>
          <input type="hidden" name="service" value="Well Pump Service">
          <div class="form-field"><label for="well-name">Name</label><input id="well-name" name="name" autocomplete="name" maxlength="120" required></div>
          <div class="form-field"><label for="well-phone">Phone</label><input id="well-phone" name="phone" type="tel" autocomplete="tel" maxlength="32" required></div>
          <div class="form-field"><label for="well-city">Service city</label><input id="well-city" name="city" autocomplete="address-level2" maxlength="120" required></div>
          <div class="form-field"><label for="well-address">Service street address (optional)</label><input id="well-address" name="address" autocomplete="street-address" maxlength="200"></div>
          <div class="form-field"><label for="well-message">What is the water doing?</label><textarea id="well-message" name="message" maxlength="2000" placeholder="Example: All faucets stopped after the storm." required></textarea></div>
          <button class="btn btn-green" type="submit">Send well service request</button>
        </form>
      </article>
    </div>
  </section>
</main>
'''
        + build.FOOTER_HTML
        + '<script src="/js/customer-paths.js" defer></script>\n</body>\n</html>\n'
    )


def generate(build):
    build.write(f"{PATH.strip('/')}/index.html", render(build))
    for relative_path in WELL_PAGES:
        page = ROOT / relative_path
        markup = page.read_text(encoding="utf-8")
        link = (
            f'<div class="container"><p class="well-checklist-link"><a href="{PATH}">'
            'No water from your well? Use the free checklist and request service.</a></p></div>'
        )
        if f'href="{PATH}"' not in markup:
            before, end, after = markup.partition("</section>")
            if not end:
                raise ValueError(f"Missing first section in {relative_path}")
            page.write_text(f"{before}{end}\n{link}\n{after}", encoding="utf-8")
