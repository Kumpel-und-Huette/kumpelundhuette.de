# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Two primary audiences, equally:

- Seniors with Pflegegrad 2 or higher (exceptions by arrangement) who want a shared home instead of living alone or moving into a nursing home, including people who need everyday support and people who feel lonely or isolated. They need to manage the day independently or with light support.
- Relatives and family carers looking for a warm alternative, deciding whether someone can move in, and who stay involved after the move.

Job applicants are a secondary audience. The site has a careers page; hiring is not a primary job of the site.

## Product Purpose

Kumpel und Hütte Service runs shared homes (Wohngemeinschaften) where older people live with privacy, company, everyday help, and nursing care. Success is a real home: self-determined, affordable, and not a Pflegeheim, hotel, or anonymous WG.

The published address is Im Heidewinkel 30, 44267 Dortmund. The pilot shared home is published as the WG „Glück auf“ in Lütgendortmund: 3 people on 100 m². “Lütgendortmund” is allowed for that WG and for the event name “Seniorenbüro Lütgendortmund”. Copy may speak of more than one WG, because support and barrier-free fittings depend on the WG, and the price sits on each accommodation’s page. Address, phone and coordinates live in `data/business.yaml`.

## Positioning

Kumpel und Hütte provides the home. Everyday support and nursing care are optional. The WG holds the Hausrecht: residents decide who provides care and help, how much, how often and for how long, and who moves in. The team provides household help, accompaniment and support itself or with service partners. Nursing care is provided by cooperation partners, in agreement with the resident and with Kumpel und Hütte. Activities are offered, not required.

The only mandatory published amount is the rent of 570 € all-in (electricity, gas, cold utilities, internet, GEZ if applicable). Housekeeping and Betreuung are an optional service contract, priced by need, with hourly billing possible, following state guidelines. Further detail is at https://www.heykumpel.com. With a care grade, those services can be billed through the Pflegekasse. Do not publish a 970 € package or fixed 200 € lines for housekeeping and support.

## Operating Context

- Legal entity: Kumpel und Hütte Service UG (haftungsbeschränkt), Amtsgericht Dortmund, HRB 37362. Geschäftsführer: Robin Grunwald. Robin und Julianne Grunwald are named as founders on the team page.
- Contact: info@kumpelundhuette.de, +49 160 90889269. Public site: https://kumpelundhuette.de/
- Move-in path: contact, viewing, application form plus documents (Pflegegradbescheid when one exists, insurance card and medication list, optional powers of attorney, family or guardian contacts). No Wohnfähigkeitsbescheinigung. Then a cost check with Pflegekasse or Sozialamt, and a welcome week. Residents decide on new housemates and pets.
- Published price: rent 570 € all-in is the only mandatory amount. Optional housekeeping and support follow state guidelines and are not a fixed monthly package. From care grade 2 the Pflegekasse benefits named on the move-in page can apply, including the Wohngruppenzuschlag from 3 people, the Entlastungsbetrag, conversion of 40% of Pflegesachleistungen, and Verhinderungspflege of 3,539 €. The rent is within Dortmund Grundsicherung.
- Office hours are unresolved: the site and the structured data say Mon–Fri 10:00–17:00; the unused `data/de/openinghours.yaml` says 9:00–17:00.

## Capabilities and Constraints

- German is the authoritative language. English pages are a translation, not a separate market.
- Admission target is Pflegegrad 2–5, with exceptions by arrangement, plus willingness to live in a WG.
- Homes are not always fully barrier-free; it depends on the WG. Published adaptations include a floor-level shower, handrails, and considered lighting. Rooms may be furnished by the resident or, by agreement, by the house.
- Support on offer includes household help, accompaniment, Betreuung, activities, and care coordination. Nursing care comes from cooperation partners. Housekeeping and Betreuung can also be provided by the team or by partners.
- Placeholder facts that must not be treated as real: Umsatzsteuer-ID DE123456789 in the Impressum. Generic social profile URLs are not published. The founding news post contains lorem ipsum tab copy.
- The site is a bilingual Hugo site (theme `hugobricks`), default language German, deployed from the `main` branch.

## Brand Commitments

Name: Kumpel und Hütte / Kumpel & Hütte Service. Lines already used as the offer: “Gemeinsam statt einsam” and “Nicht Heim. Nicht allein. Einfach Zuhause!”

Stated values: Vertrauen, Herzlichkeit, Gemeinschaft, Würde, Erschwinglichkeit. The organization describes itself as Kumpel and support, not as a Dienstleister.

## Evidence on Hand

- Homepage offer and values: `content/de/_index.md`
- Admission, price table, and move-in steps: `content/de/einziehen-bei-uns.md`
- Legal identity: `content/de/impressum.md`
- Lütgendortmund house: `content/de/posts/LüDo.md`
- Founders and team: `data/de/people.yaml` (the Betreuerin is published as “Guilia”)
- Motivation and concept essays: `content/de/motivation.md`, `content/de/unser-konzept.md`

No confirmed resident testimonial, review, or press quote is on the site. The concept-page line “Hier fühle ich mich wieder wie zu Hause – aber nie allein.” is labeled “So soll es sein.” The reviews block on the homepage is unused. Do not invent testimonials, reviews, case studies, or press.

## Product Principles

- Seniors and relatives are equal audiences. A surface that only informs one of them is incomplete.
- The product is a home, not a nursing-home institution. Care is optional and decided by the WG. Kumpel und Hütte may coordinate it and provide everyday support; cooperation partners may provide the nursing care.
- Admission rules and the published prices stay exact. Affordability is a claim with numbers attached.
- German copy is the source of truth. English follows it.
- Placeholders and unused proof blocks are not facts.

## Accessibility & Inclusion

Residents are older people, often with a care grade, who can manage the daytime alone or with light support. The homes are not always fully barrier-free; safety comes from everyday adaptations and people being there, not from a claimed barrier-free standard. No formal accessibility standard was set for the website.
