// External page init script. Observe real calls; preserve receiver/arguments/result/errors.
export function installCompressedUploadTrace() {
  const ids = new WeakMap(), contexts = new WeakMap();
  let nextId = 1, phase = 'boot', stackCount = 0;
  const events = [], censuses = [], notes = [], wrappedMethods = [];
  const limit = 24000;
  let dropped = 0, droppedNotes = 0;
  const id = (object) => {
    if (!object || (typeof object !== 'object' && typeof object !== 'function')) return null;
    if (!ids.has(object)) ids.set(object, nextId++);
    return ids.get(object);
  };
  const context = (gl) => {
    if (!contexts.has(gl)) contexts.set(gl, { id: id(gl), unit: 0x84c0, bindings: new Map() });
    return contexts.get(gl);
  };
  const record = (value) => {
    if (events.length < limit) events.push({ phase, ms: performance.now(), ...value });
    else dropped++;
  };
  const blockSize = (format) => {
    if ([0x83f0, 0x83f1, 0x8c4c, 0x8c4d, 0x8dbb, 0x8dbc, 0x9270, 0x9271,
      0x9274, 0x9275, 0x9276, 0x9277, 0x8d64].includes(format)) return [4, 4, 8];
    if ([0x83f2, 0x83f3, 0x8c4e, 0x8c4f, 0x8dbd, 0x8dbe, 0x8e8c, 0x8e8d,
      0x9272, 0x9273, 0x9278, 0x9279].includes(format)) return [4, 4, 16];
    const astc = [[4,4],[5,4],[5,5],[6,5],[6,6],[8,5],[8,6],[8,8],[10,5],[10,6],
      [10,8],[10,10],[12,10],[12,12]];
    const index = format >= 0x93d0 ? format - 0x93d0 : format - 0x93b0;
    return index >= 0 && index < astc.length ? [...astc[index], 16] : null;
  };
  const wrap = (proto, name, observe) => {
    const descriptor = Object.getOwnPropertyDescriptor(proto, name);
    if (!descriptor || typeof descriptor.value !== 'function') return;
    wrappedMethods.push({ prototype: proto.constructor.name, method: name });
    const original = descriptor.value;
    Object.defineProperty(proto, name, { ...descriptor, value: function (...args) {
      // Diagnostic bookkeeping may never prevent or replace a real WebGL call.
      try { observe(this, args); } catch (error) {
        if (notes.length < 32) notes.push({ phase, name, error: String(error) });
        else droppedNotes++;
      }
      return Reflect.apply(original, this, args);
    } });
  };
  for (const proto of [globalThis.WebGLRenderingContext?.prototype,
    globalThis.WebGL2RenderingContext?.prototype].filter(Boolean)) {
    wrap(proto, 'activeTexture', (gl, args) => { context(gl).unit = args[0]; });
    wrap(proto, 'bindTexture', (gl, args) => {
      const c = context(gl), target = args[0];
      c.bindings.set(`${c.unit}:${target}`, id(args[1]));
    });
    wrap(proto, 'deleteTexture', (gl, args) => record({ call: 'deleteTexture', context: context(gl).id,
      gpu_texture: id(args[0]) }));
    wrap(proto, 'texStorage2D', (gl, args) => {
      const c = context(gl);
      record({ call: 'texStorage2D', context: c.id, unit: c.unit, target: args[0],
        gpu_texture: c.bindings.get(`${c.unit}:${args[0]}`) ?? null,
        levels: args[1], internal_format: args[2], width: args[3], height: args[4] });
    });
    for (const name of ['compressedTexImage2D', 'compressedTexSubImage2D']) {
      wrap(proto, name, (gl, args) => {
        const sub = name === 'compressedTexSubImage2D', c = context(gl), target = args[0];
        const format = args[sub ? 6 : 2], width = args[sub ? 4 : 3], height = args[sub ? 5 : 4];
        const dataIndex = sub ? 7 : 6, data = args[dataIndex], view = ArrayBuffer.isView(data);
        const offset = view && args.length > dataIndex + 1 ? args[dataIndex + 1] : 0;
        const length = view && args.length > dataIndex + 2 ? args[dataIndex + 2] : null;
        const available = view ? Math.max(0, data.byteLength - offset * data.BYTES_PER_ELEMENT) : null;
        const effective = view ? (length ? length * data.BYTES_PER_ELEMENT : available) : null;
        const block = blockSize(format);
        const expected = block ? Math.ceil(width / block[0]) * Math.ceil(height / block[1]) * block[2] : null;
        const mismatch = effective !== null && expected !== null && effective !== expected;
        const normalizedTarget = target >= 0x8515 && target <= 0x851a ? 0x8513 : target;
        record({ call: name, context: c.id, unit: c.unit, target, level: args[1],
          gpu_texture: c.bindings.get(`${c.unit}:${normalizedTarget}`) ?? null,
          xoffset: sub ? args[2] : 0, yoffset: sub ? args[3] : 0, width, height, format,
          argument_count: args.length, data_kind: view ? data.constructor.name : typeof data,
          data_id: id(data), buffer_id: view ? id(data.buffer) : null,
          data_byte_offset: view ? data.byteOffset : null, data_byte_length: view ? data.byteLength : null,
          source_offset_elements: offset, source_length_override_elements: length,
          effective_data_bytes: effective, expected_block_bytes: expected, arithmetic_mismatch: mismatch,
          pbo_image_size_argument: typeof data === 'number' ? data : null,
          stack: mismatch && stackCount++ < 64 ? new Error('compressed upload call site').stack : null });
      });
    }
  }
  function textureMeta(texture, owner) {
    const api = globalThis.__chicago4d;
    const properties = api?.renderer?.properties;
    const gpu = properties?.has(texture) ? properties.get(texture) : null;
    const sourceProperties = properties?.has(texture.source) ? properties.get(texture.source) : null;
    return { owner, texture_id: id(texture), texture_uuid: texture.uuid, texture_name: texture.name,
      source_id: id(texture.source), source_uuid: texture.source?.uuid,
      version: texture.version, source_version: texture.source?.version,
      cached_source_version: sourceProperties?.__version ?? null, source_data_ready: texture.source?.dataReady,
      gpu_texture: id(gpu?.__webglTexture), uploaded_texture_version: gpu?.__version ?? null,
      compressed: !!texture.isCompressedTexture, format: texture.format, type: texture.type,
      internal_format: texture.internalFormat, color_space: texture.colorSpace,
      image_width: texture.image?.width, image_height: texture.image?.height,
      wrapS: texture.wrapS, wrapT: texture.wrapT, minFilter: texture.minFilter, magFilter: texture.magFilter,
      mipmaps: (texture.mipmaps || []).map((m, level) => ({ level, width: m.width, height: m.height,
        descriptor_id: id(m), data_id: id(m.data), bytes: m.data?.byteLength ?? null,
        buffer_id: id(m.data?.buffer), byte_offset: m.data?.byteOffset ?? null })) };
  }
  function census(label) {
    const api = globalThis.__chicago4d, textures = new Map();
    function add(texture, owner) {
      const key = id(texture);
      if (!textures.has(key)) textures.set(key, { ...textureMeta(texture, null), owners: new Set() });
      textures.get(key).owners.add(owner);
    }
    function material(mat, owner) {
      if (!mat) return;
      for (const [key, value] of Object.entries(mat)) if (value?.isTexture) {
        add(value, `${owner}/${mat.name || mat.type}/${key}`);
      }
      for (const [key, uniform] of Object.entries(mat.uniforms || {})) {
        for (const [index, value] of [].concat(uniform?.value ?? []).entries()) if (value?.isTexture) {
          add(value, `${owner}/uniform:${key}:${index}`);
        }
      }
    }
    function scan(root, owner) {
      root?.traverse?.((node) => {
        const nodeOwner = `${owner}/${node.name || node.type}#${id(node)}`;
        for (const [i, mat] of [].concat(node.material || []).entries()) material(mat, `${nodeOwner}:${i}`);
        material(node.customDepthMaterial, `${nodeOwner}/customDepthMaterial`);
        material(node.customDistanceMaterial, `${nodeOwner}/customDistanceMaterial`);
      });
    }
    scan(api?.scene3d, 'visible-scene');
    for (const [key, value] of api?.registry || []) scan(value.gltf?.scene, `source-registry:${key}`);
    censuses.push({ label, phase, ms: performance.now(), event_index: events.length,
      textures: [...textures.values()].map((value) => ({ ...value, owners: [...value.owners] })) });
    return { phase, events: events.length, dropped, textures: textures.size };
  }
  globalThis.__t3173UploadTrace = {
    mark(label) { phase = label; return census(label); },
    snapshot() { return { scope: 'Actual compressed upload arguments and weak identity associations only',
      phase, event_limit: limit, dropped_events: dropped, dropped_notes: droppedNotes,
      wrapped_methods: wrappedMethods, notes, events, censuses }; },
  };
}
