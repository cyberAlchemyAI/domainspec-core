import { join } from 'path';
import { readFile } from 'fs/promises';

const root = process.cwd();
const activeStitchDirName = "stitch_tilth_os_institutional_shell 3";
const stitchNavRoutes = { scout: "scout_mission_control_functional_openclaw_interface" };

async function test() {
  const p = join(root, activeStitchDirName, stitchNavRoutes["scout"], "code.html");
  console.log("Path:", p);
  try {
    const data = await readFile(p, 'utf8');
    console.log("Read success, length:", data.length);
  } catch(e) {
    console.error("Read failed:", e);
  }
}
test();
