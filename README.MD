# tool-timspm0-sysconfig

TI SysConfig CLI packaged for the [timspm0 PlatformIO platform](https://github.com/Berkays/platform-ti-mspm0).

Contents:

- `bin/dist` — the SysConfig 1.25.0 CLI (JavaScript) distribution from TI
- `bin/sysconfig_cli.sh` / `bin/sysconfig_cli.bat` — convenience launchers
- `scripts/download_nodejs.py` — post-install script that downloads an
  official Node.js 22 binary for the host OS into `bin/nodejs/` (the
  PlatformIO build invokes `bin/dist/cli.js` through this Node.js directly,
  so no shell wrapper is required and Windows/macOS/Linux all work)

The SysConfig tool is licensed by Texas Instruments (see `LICENSE.MD`);
this packaging is for the timspm0 PlatformIO platform.

## Updating to a newer SysConfig release

1. Download the standalone SysConfig CLI archive from
   <https://www.ti.com/tool/SYSCONFIG> and replace `bin/dist`.
2. Update the `minToolVersion` check: the MSPM0 SDK's
   `.metadata/product.json` declares the minimum compatible SysConfig
   version.
3. Bump `version` in `package.json` and publish with `pio pkg publish`.
