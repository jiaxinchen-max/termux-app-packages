# Termux App Packages

Versioned runtime components for [Termux App](https://github.com/jiaxinchen-max/termux-app).
This repository was renamed from `termux-box-packages`; existing releases and assets retain their names and contents.

- `catalog-v1.json`: current component catalog, synchronized with the App's bundled index.
- `repository/index-v1.json`: published catalog with explicit download URLs, sizes, and SHA-256 values.
- `repository/gnome-usb-20261030-r1.json`: pinned GNOME, Mutter, USB bridge, and GIO asset manifest.
- `legacy-termux-app-*` releases: historical runtime components copied from App releases. These are archival assets and are not automatically selected by the current catalog.

KWin, Xserver, and third-party upstream releases continue to use their dedicated repositories.
The App repository publishes APKs; runtime assets are maintained here.

The manually dispatched **Verify and publish package catalog** workflow downloads every declared payload, verifies its size and SHA-256, and publishes the catalog without synthesizing or substituting URLs.

To copy historical runtime assets from another release repository, use explicit source and target arguments:

```sh
python3 tools/migrate-app-release-assets.py \
  --source jiaxinchen-max/termux-app \
  --target jiaxinchen-max/termux-app-packages \
  --work-dir /tmp/termux-package-migration
```

The migration tool verifies all uploaded SHA-256 values and retains source assets.

## Source-built Hangover 11.16

`rootfs_hangover_11.16-v2` publishes IDAP's source-built Wine
`11.16~trixie+idap.pdb2` with unchanged pinned FEX/Box64/DXVK inputs.
The 100,485,120-byte runtime tar replaces the 293,099,520-byte v1 input;
v1 assets remain available. PE PDBs and ELF dbgsym are separate developer
artifacts and are not downloaded by the App.

Build inputs and symbol identities are recorded in
`repository/hangover/11.16-pdb2/candidate-manifest.json`; subsequent device
results and remaining limitations are in `runtime-validation.json` beside it.
The original build-time status is retained unchanged. App initialization,
Winfile rendering, 32/64-bit smoke tests and safe exit passed. Full ABI,
physical controllers, the integrated APK fresh-download path and full
backup/restore acceptance remain pending. Build recipes and validators live
in the App repository under `distribution/termux-app-packages/`.
