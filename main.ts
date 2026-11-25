// Tuesday 24 November 2026 world-news broadsheet entry (Node 22, standard library only).
// Validates ./entry.png (PNG signature, IHDR dimensions <= 1024x1024, size <= 1 MiB),
// copies it to ${MAKEFUN_OUTPUT_DIR || '/output'}/entry.png, and verifies SHA-256 integrity.

import { createHash } from 'node:crypto';
import { copyFileSync, existsSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const MAX_BYTES = 1_048_576;
const MAX_DIMENSION = 1024;
const PNG_MAGIC: ReadonlyArray<number> = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];

interface ValidatedPng {
  bytes: number;
  width: number;
  height: number;
  sha256: string;
}

function sha256Hex(data: Buffer): string {
  return createHash('sha256').update(data).digest('hex');
}

function validateSourcePng(sourceUrl: URL): ValidatedPng {
  if (!existsSync(sourceUrl)) {
    throw new Error('Missing source image: ./entry.png does not exist');
  }

  const data: Buffer = readFileSync(sourceUrl);
  if (data.length === 0 || data.length > MAX_BYTES) {
    throw new Error(`Invalid ./entry.png size: ${data.length} bytes (must be 1..${MAX_BYTES})`);
  }
  if (data.length < 24) {
    throw new Error(`Truncated PNG file: ${data.length} bytes`);
  }

  for (let i = 0; i < PNG_MAGIC.length; i += 1) {
    if (data[i] !== PNG_MAGIC[i]) {
      throw new Error('Invalid PNG signature in ./entry.png');
    }
  }

  const chunkType: string = data.subarray(12, 16).toString('ascii');
  if (chunkType !== 'IHDR') {
    throw new Error(`Expected IHDR chunk at byte 12, found "${chunkType}"`);
  }

  const width: number = data.readUInt32BE(16);
  const height: number = data.readUInt32BE(20);
  if (width < 1 || width > MAX_DIMENSION || height < 1 || height > MAX_DIMENSION) {
    throw new Error(`Invalid PNG dimensions: ${width}x${height} (must be 1..${MAX_DIMENSION})`);
  }

  return {
    bytes: data.length,
    width,
    height,
    sha256: sha256Hex(data),
  };
}

const sourceUrl = new URL('./entry.png', import.meta.url);
const validated: ValidatedPng = validateSourcePng(sourceUrl);

const outputDir: string = process.env.MAKEFUN_OUTPUT_DIR || '/output';
mkdirSync(outputDir, { recursive: true });

const destPath: string = join(outputDir, 'entry.png');
copyFileSync(sourceUrl, destPath);

const copiedData: Buffer = readFileSync(destPath);
const copiedSha256: string = sha256Hex(copiedData);
if (copiedData.length !== validated.bytes || copiedSha256 !== validated.sha256) {
  throw new Error(
    `Output verification mismatch at ${destPath}: ` +
      `expected ${validated.bytes} bytes (${validated.sha256}), ` +
      `got ${copiedData.length} bytes (${copiedSha256})`,
  );
}

console.log(
  `OK entry.png -> ${destPath} | ${validated.width}x${validated.height} | ${validated.bytes} bytes | sha256=${copiedSha256}`,
);
