# Prairie Avenue people — review evidence

Seventeen identified photographs and the current reconstructed figures. Captions, scan hashes and crop coordinates are in [manifest.json](manifest.json). The primary code branch carries full landmark records and fitted values.

The model images use the resident’s age in 1904. Picture dates may differ or be unknown. Colour, stature, clothing and unseen facial form are reconstructed. A numerical fit and this comparison do not constitute owner approval or a claim of photographic realism. Unpictured residents receive clearly labelled reconstructions.

- [Portrait comparisons 1](portrait-comparisons-1.jpg)
- [Portrait comparisons 2](portrait-comparisons-2.jpg)
- [Portrait comparisons 3](portrait-comparisons-3.jpg)
- [Portrait comparisons 4](portrait-comparisons-4.jpg)

Clothing references show other American children in 1904. They do not identify Prairie Avenue children. The five new role prototypes have canonical exports and desktop/phone comparisons in [the child review packet](child-prototypes/README.md). The owner subsequently approved all five prototypes: “Approve these five prototypes.” The original review packet is preserved as captured before that answer. The approved roles now underpin 35 younger residents, with five infants in household care, in the pushed integration linked below. This approval does not assert exact photographic likeness.

Desktop native-resolution verification: [street and Interact](prairie-menu-1280.png), [portrait card](prairie-card-1280.png), [behavior and budget log](probe-desktop-1x.log). Default desktop supersampling exceeded the software-renderer startup timeout; that limitation remains in the code PR validation record.

[Family genealogy p. 61](buckingham-genealogy-p61.jpg): Ebenezer Buckingham, *Solomon Sturges and His Descendants* (1907), public domain. This records Kate’s 1858-08-03 and Lucy Maud’s 1870-09-09 birth dates, correcting the inherited census transcription while retaining the conflict. Archive access n114, scan leaf 115.

Corrected phone verification: [Harriet Pullman and Interact](prairie-menu-390.png), [card drawer](prairie-card-390.png), [complete behavior/asset/budget log](probe-phone-pullman-idle.log). The intended female asset and scene age 62 are asserted; a paired conversation with Miss Robinson returns both indoors, with no page errors. The portrait comparison sheets above show the complete images beyond the scrollable drawer.

Additional clothing comparison: [Pach Brothers’ Roosevelt family photograph (1903)](roosevelt-family-1903.jpg), [catalogue, rights and checksum](roosevelt-family-1903-source.json). This is a review reference for the girls’ period clothing, not an identification or likeness of a Prairie Avenue resident. The current garment geometry was constructed before this additional comparison was found.

[Tribune society page, 3 March 1907](tribune-society-women-1907.jpg): the original captions identify Grace Murray Meeker and Albertine Huck Field. MSU Libraries item 9696, Part 7, p. 4. The period print is public domain; the exposure dates are unknown. Other faces on this page were not reused.

[Complete 445-entry roster index](roster-review.csv), [counts and checksum](roster-review.json), generated from code revision `bf9db83f8fa6359268058ece9c123c6da70c0b78`. The index separates scene casting age from sourced birth evidence, includes each household and canonical card link, and records the bounded search coverage. Search hits are leads, not verified portraits. The current roster contains 397 additional callable figures (362 adults and 35 children/teens), eight existing Glessner figures, five infants in household care, 23 absent former residents, nine aliases and three collective listings.

[Earlier adult checkpoint validation](final-revision/README.md): Grace Meeker phone and Albertine Field desktop checks and the complete earlier adult-only renderer results, retained as baseline evidence.

[Combined integration validation](integrated-revision/README.md): all five younger roles and five infant door cards on desktop and phone, inspected final views, unchanged-source commit binding, four passing local gate parts, and the final remote test inventory. All required CI and the complete renderer suite (stages 1–15 on desktop and phone) pass on pushed commit bf9db83f8. Exact run heads and conclusions were rechecked before merge.
