// Observation only: mirror the committed GLSL linear Red/UnsignedByte cut sampler.
// All arguments come from actual compiled material uniforms and its DataTexture.
export function sampleGroundCut({ data, width, height, box, on, flipY = false }, e, n) {
  if (!Number.isInteger(width) || !Number.isInteger(height) || width < 1 || height < 1
      || data.length !== width * height || box.length !== 4
      || ![...box, on, e, n].every(Number.isFinite)) throw Error('Incomplete actual ground-cut input');
  const u = (e - box[0]) * box[2], v = (-n - box[1]) * box[3];
  const inside = u > 0 && v > 0 && u < 1 && v < 1;
  const x = u * width - 0.5, y = (flipY ? 1 - v : v) * height - 0.5;
  const x0 = Math.floor(x), y0 = Math.floor(y), fx = x - x0, fy = y - y0;
  const at = (ix, iy) => data[Math.max(0, Math.min(height - 1, iy)) * width
    + Math.max(0, Math.min(width - 1, ix))] / 255;
  const texels = [at(x0, y0), at(x0 + 1, y0), at(x0, y0 + 1), at(x0 + 1, y0 + 1)];
  const red = (texels[0] * (1 - fx) + texels[1] * fx) * (1 - fy)
    + (texels[2] * (1 - fx) + texels[3] * fx) * fy;
  return { u, v, inside, red, texels, discarded: on > 0.5 && inside && red > 0.5 };
}
