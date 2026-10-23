# Stubbs anatomy plate retrieval follow-up

2026-10-18. New official catalog evidence was read, but no anatomical plate was acquired. This file is the only repository file changed by this pass. Earlier acquisition report remains unchanged; its normalized “1815 reissue” description should be read with the catalog uncertainty below.

## New source text actually retrieved

`https://archive.org/download/b33544049/b33544049_dc.xml` returned HTTP 200 and exposed the item's Dublin Core catalog record. Transcribed fields:

- Title: *The anatomy of the horse ... /*
- Creator: Stubbs, George, 1724–1806.
- Publisher: London: Printed by J. Purser, for the author.
- **Date: `1766 [i.e. 1815?]`.** Preserve this uncertainty. The IA JSON metadata normalizes the date to 1815, but this source catalog explicitly questions the inferred reissue year.
- Physical description: 4 unnumbered pages, 47 pages, 24 leaves of plates (oblong folio).
- Description: “Original text sheets re-issued with plates reprinted on wove paper watermarked 1815/1.”
- Subjects: Horses—Anatomy; Anatomy, Artistic.

`https://archive.org/download/b33544049/b33544049_metasource.xml` returned HTTP 200. It identifies source handle `wellcome`, field `local`, term `b33544049`, and text ID `b33544049`. This substantiates the local Wellcome identifier; it does not reveal an eight-character modern Wellcome works ID or an IIIF canvas/image locator.

`https://archive.org/metadata/b33544049` was reread. External identifiers are only `urn:oclc:record:1565429087`, IA ARK `ark:/13960/s2swnr54dbd`, and the archive.org access identifier. The explicit Public Domain Mark recorded in the previous report remains present. The questionable reissue date does not move this eighteenth/early-nineteenth-century work into modern copyright; it matters for accurate catalog attribution.

The IA details page returned 200, but yielded no external Wellcome work link in a targeted link extraction. No OCLC catalog was read, so no modern holder UUID is inferred from that number.

## Official endpoints tested and observed results

All requests used inherited HTTPS proxy and TLS verification; no direct-network route, proxy unsetting, host substitution or access-control bypass was attempted.

| Requested official endpoint | Actual result |
|---|---|
| `https://api.wellcomecollection.org/catalogue/v2/works?query=b33544049` | Proxy tunnel 403 Forbidden; no catalog response read |
| `https://wellcomecollection.org/works?query=b33544049` | Proxy tunnel 403 Forbidden |
| `https://wellcomelibrary.org/item/b33544049` | Proxy tunnel 403 Forbidden; no redirect target or work record read |
| `https://iiif.wellcomecollection.org/presentation/b33544049` | Proxy tunnel 403 Forbidden; endpoint is a candidate tested against local ID, not a verified existing manifest |
| `https://archive.org/download/b33544049/b33544049_scandata.xml` | HTTP 500 on this pass; prior pass observed redirect to `dn720707.ca.archive.org` then tunnel403 |
| `https://archive.org/download/b33544049/b33544049_marc.xml` | Redirect follow blocked by proxy tunnel403; MARC contents not read |
| `https://archive.org/download/b33544049/b33544049_dc.xml` | HTTP200; catalog fields read above |
| `https://archive.org/download/b33544049/b33544049_metasource.xml` | HTTP200; source-local identifier read above |

An unavailable guessed manifest URL is not evidence of a missing collection object. Actual holder resolution needs the permitted Wellcome catalog response or source MARC record first. Do not fabricate canvas IDs, plate numbers or direct image URLs from the item identifier.

## Result and next concrete step

No photograph/plate was viewed and no new anatomy shape measurements were made. The useful new result is the primary catalog's uncertain edition date plus confirmed Wellcome local identifier. The source remains a promising explicitly public-domain-marked anatomical basis, with OCR-only structural evidence already recorded; visual plate comparison remains unpassed.

A supported allowlist update for `api.wellcomecollection.org`, `wellcomecollection.org`, `wellcomelibrary.org`, `iiif.wellcomecollection.org` and/or the exact IA image/storage hosts reported earlier would unblock catalog/manifest resolution and plate retrieval. Preserve existing rules rather than replacing an unknown allowlist. Retry the appropriate endpoint after an actual policy change, resolve the returned work/manifest identifier, inspect the skeleton and muscular plates themselves, then save exact leaf/canvas and source-image locators before any claimed model comparison. No secret or paid permission is required by the evidence gathered here.
