// SPDX-License-Identifier: GPL-3.0-or-later
// Modern asset credit is separate from historically graded animal claims.
export function standingHorseCard(row, spec) {
  const citations = [...new Set([...row.source_ids, spec.source.id])].map(source_id => {
    const source = spec.citation_records?.[source_id] ?? row.citation_records?.[source_id];
    if (!source?.citation || !source.url) throw Error('Standing horse citation does not resolve: ' + source_id);
    return { ...source, source_id };
  });
  const yard1835 = row.scene_id !== '1904';
  const context = yard1835 ? 'the 1835 Western Hotel yard' : row.location;
  const year = yard1835 ? '1835' : '1904';
  return { id: row.id, sidecar: {
    name: row.name, phase: null,
    change_note: `A reconstructed, unidentified horse in ${context}. Modern model credit (published ${spec.source.publication_date.slice(0, 4)}): ${spec.source.credit} This modern asset credit is not evidence of a particular ${year} horse, breed or owner.`,
    placement: { symbolic_location: row.location, position_confidence: 'reconstructed',
      position_sources: row.source_ids, position_note: row.note },
    attributes: {
      animal: { value: 'Standing horse; individual unidentified', confidence: 'reconstructed',
        sources: row.source_ids, note: yard1835
          ? 'Yard context supports horsekeeping; this individual is a reconstruction.'
          : 'Neighborhood stable context supports horsekeeping; neither this individual nor its exact street stand is attested.' },
      breed_owner: { value: 'Unidentified', confidence: 'reconstructed', sources: [],
        note: 'No historical breed, owner, measured stature, coat or grooming is attested for this model.' },
      state: { value: 'Standing, unhitched, untied and unmounted', confidence: 'reconstructed', sources: [],
        note: row.animation?.enabled
          ? 'Gentle body weight shifts are reconstructed; hooves stay planted. This horse is unhitched and unmounted; walking and riding are not available.'
          : 'Idle activation awaits qualification; no halter, tie rope, harness, rider, driver, boarding, route or physical coupling is enabled.' },
    },
    citations,
    research_note: `${row.note} Modern model credit (${spec.source.publication_date.slice(0, 4)}): ${spec.source.credit} Model adaptations: canonical metre-space derivative at unit scale,
      declared whole-root support rotation, ${yard1835 ? 'yard' : 'carriageway'} placement and reconstructed planted body shifts. Original head/tail and walking clips are not composed. ${spec.material_variants[row.material_variant].change_notice}`,
  } };
}
